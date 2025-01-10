import os

import hal
import linuxcnc

import data_func.scope_config
from task_alarm import class_alarm_items as alarm_item
from data_class import nc_module as module, class_alarm as nc_alarm, class_param as param, class_ncplc as ncplc
from data_class import nc_action as action
from window_class import class_ncplc_data as win_ncplc
from window_api import nc_window as window
from data_api import nc_data
from window_api import nc_window
from task_mdi import thread_detect_mdi as thread_detect_mdi
from task_mdi import target_position as target_position
import tornado.websocket
import json
from urllib import parse
import config

import threading

coordinate_dict = {"0_G54": 1, "1_G55": 2, "2_G56": 3, "3_G57": 4, "4_G58": 5}


# 上传文件
class ProgramPostHandler(tornado.web.RequestHandler):
    def post(self):
        print("post program")
        file_path = module.ProgramPath
        for field_name, files in self.request.files.items():
            for info in files:
                filename, content_type = info["filename"], info["content_type"]
                body = info["body"]
                # logging.info('%s', os.getcwd())
                # f = open("/home/top/NcProgram/file.ngc", 'wb')
                f = open(file_path, 'wb')
                f.write(body)
                f.close()
                # logging.info('POST %s %s %d bytes', filename, content_type, len(body))
                print(filename)
                print("filename:" + filename)
                print("field_name:" + field_name)

        # os.system("axis-remote " + file_path)
        linuxcnc.command().program_open(file_path)
        self.write("upload finished")


# 上传参数
class DataPostHandler(tornado.web.RequestHandler):
    def post(self):
        print("post data")

        raw_data = self.request.body.decode('utf-8')
        json_data = json.loads(raw_data)
        index = str(json_data['id'])
        value = str(json_data['value'])
        print(index)
        print(value)
        module.IpcPostHandler.set_value(index, value)


# 下载文件 NCK->IPC
class DownloadHandler(tornado.web.RequestHandler):
    # 设置允许跨域
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "Content-Type")
        self.set_header("Access-Control-Allow-Methods", "POST,GET,OPTIONS")

    def get(self):
        # 获取参数
        # 读取的内存大小，一般会在保存文件的时候记录下来，最好比源文件大
        buf_size = 8192
        filename = self.get_argument('filename', None)
        if not filename:
            self.write({"error": "文件名称为空"})
            return
        # 设置传输的文件类型，有很多例如png/pdf等等 取决于不同场景，这边我用octet-stream
        self.set_header('Content-Type', 'application/octet-stream')
        path = module.NCKPath + filename
        with open(path, 'rb') as f:
            while True:
                data = f.read(buf_size)
                if not data:
                    break
                self.write(data)
        filename = parse.quote(filename)

        # 设置文件保存名，也就是你下载完成.示的名称，我们对文件名进行url编码，因为header对中文是不支持的
        # 下载时显示的文件名称
        self.set_header('Content-Disposition', 'attachment; filename=' + filename)
        self.finish()


# mdi 指令处理
class MdiCmdHandler(tornado.web.RequestHandler):
    def post(self):
        raw_data = self.request.body.decode('utf-8')
        json_data = json.loads(raw_data)
        mdi_cmd = json_data['mdi_cmd']
        print(mdi_cmd)

        if hal.get_value("halui.mode.is-mdi"):
            print("mdi")
            thread_detect_mdi.MdiThread.add_mdi_cmd(mdi_cmd)


# MDI清空缓存指令
class MdiClear(tornado.web.RequestHandler):
    def post(self):
        data = self.request.body.decode('utf-8')
        print("MdiClear")
        thread_detect_mdi.MdiThread.clear_mdi_cmd()


# 定位
class Position(tornado.web.RequestHandler):
    def post(self):
        # 解析
        data = self.request.body.decode('utf-8')
        print("Position")
        print(data)
        json_data = json.loads(data)

        feed_speed = json_data.get('feed_speed')
        if feed_speed:
            target_position.TargetPosition.set_feed(int(feed_speed))

        joint_index = json_data.get('axis_id')
        pos_type = json_data.get('pos_type')
        distance = json_data.get('distance')
        if joint_index is not None and pos_type and distance is not None:
            # joint_index >= 100 是主轴
            if joint_index >= 100:
                target_position.TargetPosition.add_spindle_position(str(pos_type), float(distance))
            else:
                target_position.TargetPosition.add_position(int(joint_index), str(pos_type), float(distance))

        coordinate = json_data.get('coordinate')
        if coordinate:
            action.set_curr_coordinate(coordinate)


# 跳段
class JumpSegment(tornado.web.RequestHandler):
    def post(self):
        data = self.request.body.decode('utf-8')
        print("JumpSegment")
        print(data)
        json_data = json.loads(data)

        enable = json_data.get('enable')
        if enable is not None:
            thread_detect_mdi.MdiThread.set_jump_segment_enable(enable)

        line = json_data.get('line')
        if line is not None:
            thread_detect_mdi.MdiThread.set_jump_segment_line(line)


class ChunkFileHandler(tornado.web.RequestHandler):
    def post(self):
        file_data = self.request.files.get("file")
        file_info = file_data[0]
        file_name = file_info["filename"]
        file_body = file_info["body"]
        # 第几个包
        file_offset = self.request.headers.get("File-Offset")
        file_size = self.request.headers.get("File-Size")
        file_path = self.request.headers.get("File-Path")
        module.ipc_program_path = file_path
        if file_offset == "0":
            module.program_load_percentage = 0
            hal.set_p(config.halpin_program_is_ok, "0")
            f = open(module.ProgramPath, 'wb')
            f.write(file_body)
            f.close()
        else:
            module.program_load_percentage = int(file_offset) / int(file_size) * 100
            f = open(module.ProgramPath, "ab")
            f.write(file_body)
            f.close()

        size = os.path.getsize(module.ProgramPath)
        if file_size == str(size):
            linuxcnc.command().program_open(module.ProgramPath)
            hal.set_p(config.halpin_program_is_ok, "1")
            module.program_load_percentage = 100
            print("open file")


# 上传文件 IPC->NCK
class UploadFileHandler(tornado.web.RequestHandler):
    def post(self):
        file_data = self.request.files.get("file")
        file_info = file_data[0]
        file_name = file_info["filename"]
        file_body = file_info["body"]
        upload_path = module.NCKPath + file_name

        print(upload_path)
        # 第几个包
        file_offset = self.request.headers.get("File-Offset")
        file_size = self.request.headers.get("File-Size")
        if file_offset == "0":
            f = open(upload_path, 'wb')
            f.write(file_body)
            f.close()
        else:
            f = open(upload_path, "ab")
            f.write(file_body)
            f.close()

        size = os.path.getsize(upload_path)
        if file_size == str(size):
            print("Transmission complete.")


# 重启NCK
class ManageNCKHandler(tornado.web.RequestHandler):
    def get(self):
        print("manage NCK")
        hal.set_p(config.halpin_po_machineOff, "1")
        os.system("gnome-terminal -e 'NCK_manager restart'")


class CustomAlarm(tornado.web.RequestHandler):
    def post(self):
        alram_data = self.request.body.decode('utf-8')
        print(alram_data)
        json_data = json.loads(alram_data)
        count = json_data['count']
        module.AlarmItem.clear_custom_alarm_items()

        for i in range(0, count):
            # plc地址
            addr = json_data['alarm_item_{0}'.format(i)]
            # 报警文本
            content = json_data['alarm_item_content_{0}'.format(i)]
            # 报警等级
            level = json_data['alarm_item_level_{0}'.format(i)]
            alarm_item.CustomAlarm(addr, content, level).add_to_loop("plc")


class SoftReset(tornado.web.RequestHandler):
    def post(self):
        alram_data = self.request.body.decode('utf-8')
        print("soft reset")
        module.AlarmItem.soft_reset_alarm()
        self.write_to_file()

    def write_to_file(self):
        thread = threading.Thread(target=self.write_history_alarms)
        thread.start()

    def write_history_alarms(self):
        module.AlarmItem.export_softreset_history_alarms(config.history_alarm_path)


# nc_plc
class NcPlcPostHandler(tornado.web.RequestHandler):
    def post(self):
        # 解析
        nc_data = self.request.body.decode('utf-8')
        print("ncplc list")
        print(nc_data)
        json_data = json.loads(nc_data)
        count = json_data['count']
        ncplc.NcPlcItem.clear_item()
        # 清空window的list
        window.ncplc_data_window.clear()

        for i in range(0, count):
            # 变量编号
            index = json_data['ncplc_item_{0}'.format(i)]
            ncplc.NcPlcItem.add_item(index)
        # 在window添加item
        for item in ncplc.NcPlcItem._nc_vars:
            window.ncplc_data_window.add_item(item)


# G92一键清零
class ResetG92Handler(tornado.web.RequestHandler):
    def post(self):
        axis = self.request.body.decode('utf-8')
        if axis == "-1":
            param.G92_Offset.reset_all()
        else:
            param.G92_Offset.reset_single(int(axis))


# 设定零偏
class SetAxisOrigin(tornado.web.RequestHandler):
    def post(self):
        # 解析
        data = self.request.body.decode('utf-8')
        print("SetAxisOrigin")
        print(data)
        json_data = json.loads(data)
        coordinate = json_data['coordinate']
        axis_id = json_data['axis_id']
        value = json_data['value']

        action.set_axis_origin(axis_id, value)


# 示波器换轴修改配置文件
class SetScopeChannel(tornado.web.RequestHandler):
    def post(self):
        # 解析
        data = self.request.body.decode('utf-8')
        print("scope_config_axis")
        print(data)
        json_data = json.loads(data)
        axis_id = json_data['currAxis']

        list = module.scope.getChannelList()
        for name in list:
            pin = module.scope.getValue(name, "PIN")
            if pin.startswith("joint"):
                tmp = pin.split(".")
                pin = tmp[0] + "." + str(axis_id) + "." + tmp[2]
            elif pin.startswith("acc"):
                tmp = pin.split("_")
                pin = tmp[0] + "_" + str(axis_id)
            elif pin.startswith("lcec"):
                tmp = name.split(".")
                name = tmp[0] + "." + tmp[1] + "." + str(axis_id) + "." + tmp[3]
            print("set scope pin to: " + pin)
            module.scope.setValue(pin, name, "PIN")
        module.scope.update()
        hal.set_p(config.scope_reload_config, "1")
        print("reload scope config")
        hal.set_p(config.scope_reload_config, "0")


# 示波器开始采集，检测数据是否导出
class StartCaptureHandler(tornado.web.RequestHandler):
    def post(self):
        # 解析
        data = self.request.body.decode('utf-8')
        json_data = json.loads(data)
        currTime = json_data['currTime']
        name = "scopeData_" + currTime + ".csv"
        print("scope_data_name")
        print(name)

        # 置位数据导出信号引脚、置位开始采样引脚
        hal.set_p(config.scope_export_flag, "0")    # 置位导出信号
        # 监控数据导出
        export = data_func.scope_config.ScopeDataThread(config.scope_data_path, name, False)
        thread_task_detect_scope = threading.Thread(target=export.detect_file_exist)
        thread_task_detect_scope.start()

class PLCData(tornado.web.RequestHandler):
    def post(self):
        data = self.request.body.decode('utf-8')
        print("PLC_Data={}".format(data))