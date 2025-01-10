import json
import os.path
import string
import sys
import hal
import time
import linuxcnc
import copy
from abc import ABC
from abc import abstractmethod

import configparser
from collections import defaultdict

from configparser import ConfigParser
import threading

import config

from data_func import scope_config as scope_conf


NCKPath = "/home/" + config.username + "/linuxcnc/configs/" + config.folder_name + "/"
print("NCKPath: " + NCKPath)

ProgramPath = "/home/" + config.username + "/NcProgram/file.ngc"
print("ProgramPath: " + ProgramPath)

MdiPath = "/home/" + config.username + "/share/temp/mdi.ngc"
print("MdiPath: " + MdiPath)

MicroProgramPath = config.micro_program_path
print("MicroProgramPath: " + MicroProgramPath)

scope = scope_conf.ParseScopeFile(config.scope_config_path)
scope.load()
if os.path.exists(config.scope_data_path):
    os.remove(config.scope_data_path)

ConfigParser.optionxform = str

config = ConfigParser(strict=False)  # 允许ini文件中存在重复定义的section和option
halList = {}  # custom alarm list
program_load_percentage = -1  # 程序文件加载百分比
ipc_program_path = None  # ipc程序文件路径
position_is_exec = 0  # 定位功能是否开始执行


axis = {"x": 0, "y": 1, "z": 2,
        "a": 3, "b": 4, "c": 5,
        "u": 6, "v": 7, "w": 8}

try:
    command = linuxcnc.command()
    stat = linuxcnc.stat()
    error = linuxcnc.error_channel()

    NML_ERROR = linuxcnc.NML_ERROR
    OPERATOR_ERROR = linuxcnc.OPERATOR_ERROR

    mdi = linuxcnc.MODE_MDI
    auto = linuxcnc.MODE_AUTO
    auto_run = linuxcnc.AUTO_RUN
    jog = linuxcnc.MODE_MANUAL

    config.read(stat.ini_filename, encoding='utf-8')
    # ini文件读取接口
    stat.poll()
    inifile = linuxcnc.ini(stat.ini_filename)
    axis_list = inifile.find("TRAJ", "COORDINATES").split(" ")
    axis_count = len(axis_list)
    spindle_count = int(inifile.find("TRAJ", "SPINDLES"))
    print("axis list:" + str(axis_list))
    print("axis count:" + str(axis_count))
    print("spindle count:" + str(spindle_count))

except:
    print("system initialization exception exited.")
    sys.exit(1)
else:
    print("system starts up normally. ")


# 获取轴对应的id
def get_axis_id(joint_id: int):
    """
    :param joint_id: 关节号
    :return:轴名，轴编号（用于获取xyzabcuvw固定顺序的接口数据）
    """
    axis_name = axis_list[joint_id]  # 关节对应的轴名
    axis_id = axis[axis_name.lower()]  # 轴名对应的编号 xyzabcuvw
    return axis_name, axis_id


# 获取轴对应的id
def get_axis_id_by_name(axis_name: str):
    """
    :param axis_name: 轴名
    :return:轴编号（用于获取xyzabcuvw固定顺序的接口数据）
    """
    axis_id = axis[axis_name.lower()]  # 轴名对应的编号 xyzabcuvw
    return axis_id


def update() -> bool:
    try:
        linuxcnc.error_channel().poll()
        linuxcnc.stat().poll()
        stat.poll()
        error.poll()

    except:
        print("update error")
        return False
    else:
        return True


# 接受ipc数据后自动执行设置参数
class IpcPostHandler:
    _callback_list = {}
    _object_list = {}

    @staticmethod
    def set_value(index: string, value: string):
        if IpcPostHandler._callback_list.get(index) is None:
            print("no such param")
        else:
            IpcPostHandler._callback_list.get(index)(value)

    @staticmethod
    def add_callback(index: string, func):
        IpcPostHandler._callback_list[index] = func

    @staticmethod
    def add_object(index: string, obj):
        IpcPostHandler._object_list[index] = obj

    @staticmethod
    def get_obj(index: string):
        if IpcPostHandler._object_list.get(index) is None:
            return None
        else:
            return IpcPostHandler._object_list.get(index)


class AlarmStruct:
    def __init__(self):
        self.start_time = ""  # 报警开始时间
        self.end_time = ""  # 报警结束时间
        self.source = ""  # 报警来源
        self.content = ""  # 报警内容
        self.level = ""  # 报警等级


class AlarmItem:
    # 当前报警[按键复位]信息的列表
    _current_hardreset_alarms = []
    # 当前报警[软件复位]信息的列表
    _current_softreset_alarms = []
    # 历史报警[按键复位]信息的列表
    _history_hardreset_alarms = []
    # 历史报警[软件复位]信息的列表
    _history_softreset_alarms = []

    # 存储用户自定义报警（PLC)的列表
    _plc_alarms = []
    # 存储NC报警的列表
    _nc_alarms = []
    # 存储软复位报警的列表
    _softreset_alarms = []

    # （MSG，message）
    _msg_info = []

    def __init__(self, source: str, content: str, level: str):
        """
        :param source: 报警来源
        :param content: 报警内容
        """
        self.struct = AlarmStruct()
        self.struct.source = source
        self.struct.content = content
        self.struct.level = level
        self.flag = True  # 第一次触发（上升沿触发） True:等待触发 False:已经触发
        self.is_softreset = False  # 复位类型 是否为软件复位  True:软件复位 False：按键复位

    def data(self):
        data = {
            "start": self.struct.start_time,
            "end": self.struct.end_time,
            "source": self.struct.source,
            "content": self.struct.content,
            "level": self.struct.level,
        }
        return data

    @staticmethod
    def is_alarm() -> bool:
        """
        :return: 是否正在报警
        """
        if len(AlarmItem._current_hardreset_alarms) and len(AlarmItem._current_softreset_alarms):
            return True
        else:
            return False

    def add_to_loop(self, alarm_type: str = " "):
        """
        添加到检测报警的循环中
        :param alarm_type:  [SOFT_RESET] 软件复位
                            [其他] 硬件复位
        :return:
        """
        if alarm_type == "SOFT_RESET":
            AlarmItem._nc_alarms.append(self)
            self.is_softreset = True
            print("softreset append:" + self.struct.content)
        else:
            if self.struct.source == "PLC":
                AlarmItem._plc_alarms.append(self)
                self.is_softreset = False
                print("plc append:" + self.struct.content)
            else:
                AlarmItem._nc_alarms.append(self)
                self.is_softreset = False
                print("nc append:" + self.struct.content)

    # 触发报警
    def trigger_alarm(self):
        self.struct.start_time = time.strftime("%Y-%m-%d,%H:%M:%S", time.localtime())
        if self.is_softreset:
            AlarmItem._current_softreset_alarms.append(self)
        else:
            AlarmItem._current_hardreset_alarms.append(self)
        # print("开始 " + self.struct.start_time + self.struct.content)

    # 触发信息
    def trigger_msg(self):
        self.struct.start_time = time.strftime("%Y-%m-%d,%H:%M:%S", time.localtime())
        AlarmItem._msg_info.append(self)

    # 结束报警
    def end_alarm(self):
        self.struct.end_time = time.strftime("%Y-%m-%d,%H:%M:%S", time.localtime())
        struct = copy.copy(self.struct)
        if self.is_softreset:
            AlarmItem._history_softreset_alarms.append(struct)
        else:
            AlarmItem._history_hardreset_alarms.append(struct)
        # print("结束" + self.struct.end_time + self.struct.content)

    @staticmethod
    def end_custom_msg(path: str):
        if len(AlarmItem._msg_info) == 0:
            return
        end_time = time.strftime("%Y-%m-%d,%H:%M:%S", time.localtime())
        with open(path, "a") as file:
            for item in AlarmItem._msg_info:
                content = item.struct.start_time + "  " + end_time + "  " + item.struct.source + "  " + item.struct.content
                file.write(content + "\n")
            file.close()
        AlarmItem._msg_info = []

    # 清空自定义报警
    @staticmethod
    def clear_custom_alarm_items():
        AlarmItem._plc_alarms = []

    # 检查是否有该报警文本的报警并返回
    @staticmethod
    def check_alarm_item(context: str):
        """
        检查是否有该报警文本的报警并返回该报警
        :param context: 报警文本
        :return:
        """
        for item in AlarmItem._current_hardreset_alarms:
            if item.struct.content == context:
                return item
        return None

    @staticmethod
    def remove_single_item(context: str):
        """
        查找是否有报警内容为context的报警项目，并停止报警
        :param context: 报警文本
        :return: 如果有，执行并返回True，否则返回False
        """
        item = AlarmItem.check_alarm_item(context)
        if item:
            item.end_alarm()
            AlarmItem._current_hardreset_alarms.remove(item)
            return True
        return False

    @staticmethod
    def remove_alarm_item(context: str, path: str):
        """
        查找是否有报警内容为context的报警项目，并停止报警
        :param context: 报警文本
        :return: 如果有，执行并返回True，否则返回False
        """
        item = AlarmItem.check_alarm_item(context)
        if item:
            item.end_alarm()
            AlarmItem._current_hardreset_alarms.remove(item)

            for i in AlarmItem._history_hardreset_alarms:
                if i.start_time == item.struct.start_time and i.end_time == item.struct.end_time and i.content == item.struct.content:
                    AlarmItem._history_hardreset_alarms.remove(i)
                    break
            t = threading.Thread(target=AlarmItem.export_single_history_alarms(path, item))
            t.start()
            return True
        return False

    @staticmethod
    def export_single_history_alarms(path: str, item):
        with open(path, "a") as file:
            content = item.struct.start_time + "  " + item.struct.end_time + "  " + item.struct.source + "  " + item.struct.content
            file.write(content + "\n")
            file.close()

    # 导出历史报警到文件
    @staticmethod
    def export_hardreset_history_alarms(path: str):
        if len(AlarmItem._history_hardreset_alarms) == 0:
            return
        with open(path, "a") as file:
            for item in AlarmItem._history_hardreset_alarms:
                content = item.start_time + "  " + item.end_time + "  " + item.source + "  " + item.content
                file.write(content + "\n")
            file.close()
        AlarmItem._history_hardreset_alarms = []

    # 导出历史报警到文件
    @staticmethod
    def export_softreset_history_alarms(path: str):
        if len(AlarmItem._history_softreset_alarms) == 0:
            return
        with open(path, "a") as file:
            for item in AlarmItem._history_softreset_alarms:
                content = item.start_time + "  " + item.end_time + "  " + item.source + "  " + item.content
                file.write(content + "\n")
            file.close()
        AlarmItem._history_softreset_alarms = []

    # 刷新检测报警
    @staticmethod
    def update_alarm():
        # 1.nc
        for item in AlarmItem._nc_alarms:
            item.update()
        # 2.plc
        for item in AlarmItem._plc_alarms:
            item.update()
        # 3.soft_reset
        for item in AlarmItem._softreset_alarms:
            item.update()

    # 按键复位
    @staticmethod
    def hard_reset_alarm():
        for item in AlarmItem._current_hardreset_alarms:
            item.end_alarm()
            item.flag = True
        AlarmItem._current_hardreset_alarms = []

    # 软件复位
    @staticmethod
    def soft_reset_alarm():
        for item in AlarmItem._current_softreset_alarms:
            item.end_alarm()
            item.flag = True
        AlarmItem._current_softreset_alarms = []

    # 当前报警信息
    @staticmethod
    def current_alarm():
        alarms = []
        for item in AlarmItem._current_hardreset_alarms:
            alarms.append(item.data())
        for item in AlarmItem._current_softreset_alarms:
            alarms.append(item.data())
        for item in AlarmItem._msg_info:
            alarms.append(item.data())
        return alarms

    # 历史报警信息
    @staticmethod
    def hardreset_history_alarm():
        alarms = []  # 当前报警信息
        for item in AlarmItem._history_hardreset_alarms:
            alarms.append(item.data())
        return alarms

    # 历史报警信息
    @staticmethod
    def softreset_history_alarm():
        alarms = []  # 当前报警信息
        for item in AlarmItem._history_softreset_alarms:
            alarms.append(item.data())
        return alarms

    # 更新报警
    @abstractmethod
    def update(self):
        """
        在该函数中编写报警检测条件
        当报警触发时，手动调用 "trigger_alarm()"
        :return:
        """


# 数据对象
class DataNode(ABC):
    def __init__(self, index: string, name, type, description=None):
        self._index = index
        self._name = name
        self._type = type
        self._description = description
        self.source = None
        self.units = None
        self.setable = None
        self._data = None
        self.update()
        IpcPostHandler.add_callback(self._index, self.set_value)
        IpcPostHandler.add_object(self._index, self)

    @abstractmethod
    def value(self):
        """
        数据获取
        """

    def set_value(self, value):
        print(str(self._index) + " doesn't have set_value method")

    def data(self):
        self.update()
        return self._data

    def update(self):
        data = {
            "id": self._index,
            "name": self._name,
            # "type": self._type,
            # "description": self._description,
            "value": self.value(),
            # "source": self.source,
            # "units": self.units,
            # "setable": self.setable,
        }
        self._data = data

    def print(self):
        print("[" + self._index + "] " + self._name + " : " + self.value())


# 设备对象
class DeviceNode:
    def __init__(self, id, name, type, description=None):
        self._id = id
        self._name = name
        self._type = type
        self._description = description
        self._data_items = []
        self._alarms = []
        self._data = None

    def update(self):
        data_item_info = []
        for item in self._data_items:
            data_item_info.append(item.data())
        data = {
            "id": self._id,
            "name": self._name,
            "type": self._type,
            "description": self._description,
            "dataItems": data_item_info,
            "alarms": AlarmItem.current_alarm()
        }
        self._data = data

    def data(self):
        self.update()
        return self._data

    def add_data_item(self, item: DataNode):
        self._data_items.append(item)

    def clear(self):
        self._data_items = []


class DataRoot:
    def __init__(self, id, name, type, description=None):
        self._id = id
        self._name = name
        self._type = type
        self._description = description
        self._devices = []
        self._data = None
        self.update()

    def update(self):
        device_info = []

        for item in self._devices:
            device_info.append(item.data())
        data = {
            # "id": self._id,
            "name": self._name,
            # "type": self._type,
            "description": self._description,
            "devices": device_info
        }
        self._data = data

    def data(self):
        self.update()
        return self._data

    def add_device(self, item: DeviceNode):
        self._devices.append(item)

    def clear(self):
        self._devices = []


# 设置ini文件的参数
def setIniValue(file, section, option, value, is_effect="1"):
    """
    设置ini文件的参数
    :param file: 指定的ini文件路径
    :param section: ini文件的段名，如 [JOINT_8]
    :param option: ini文件参数名，如 BACKLASH
    :param value: 设置的参数值
    :param is_effect: 参数是否生效，true表示参数生效;false表示参数未生效，即 ini文件注释该参数
    :return:
    """
    with open(file, "r+", encoding="utf-8") as f:
        all_content = f.readlines()
        op_id = []
        for i, line in enumerate(all_content):
            if "[" + section + "]" in line:
                section_id = i

            if option in line and line[0] != "[":
                index = line.index("=")
                orig_option = line[:index].strip()
                if option == orig_option or "#" + option == orig_option:
                    op_id.append(i)

        result = next((k for k, value in enumerate(op_id)
                       if value > section_id), "none")
        if result == "none":  # ini文件未搜索到option
            print("not found option!")
            if is_effect == "1":
                all_content.insert(section_id + 1, option + " = " + value + "\n")
            elif is_effect == "0":
                print("set effective false!")
                all_content.insert(section_id + 1, "#" + option + " = " + value + "\n")
            else:
                print("参数输入错误！")
        else:  # 文件内包含option
            if is_effect == "1":
                all_content[op_id[result]] = option + " = " + value + "\n"
            elif is_effect == "0":
                all_content[op_id[result]] = "#" + option + " = " + value + "\n"
            else:
                print("参数输入错误！")

        f.seek(0)
        f.truncate()
        f.writelines(all_content)
    f.close()


class MultiValueConfigParser(configparser.ConfigParser):
    def __init__(self, *args, **kwargs):
        self._duplicates = defaultdict(list)
        self._path = 'test.ini'
        super().__init__(*args, **kwargs)

    def read(self, filenames, encoding=None):
        self._duplicates.clear()
        self._path = filenames
        super().read(filenames, encoding)

    def _read(self, fp, fpname):
        """
        重写read方法，读取含重复option的ini文件，保存至_duplicates
        """
        elements = []
        cursect = None  # section指针
        optname = None  # option
        value_list = []  # (value, isEffect)

        for lineno, line in enumerate(fp, start=1):
            # 跳过文件空行
            comment_end = line.find("\n")
            if comment_end != -1:
                line = line[:comment_end].strip()
            if not line:
                continue

            # section解析
            if line.startswith("[") and line.endswith("]"):
                sectname = line[1:-1].strip()
                cursect = self._dict()
                self._sections[sectname] = cursect
                continue

            # option解析
            if "=" in line:
                optname, optval = map(str.strip, line.split("=", 1))
                if optname[0] == '#':
                    value_list = (optval, "0")
                else:
                    value_list = (optval, "1")

                # 重复option
                self._duplicates.setdefault((sectname, optname), []).append(value_list)

    def isExist(self, section, option, content):
        value_list = self._duplicates.get((section, option), [])
        value_list_ = self._duplicates.get((section, "#" + option), [])
        result = value_list + value_list_

        if result:
            for item in result:
                if content in item[0]:
                    return item[0].split(" ")[2]
            return False

    def getValue(self, section, option):
        """
        :param section: ini段名
        :param option: ini节点名
        :return: 返回指定(section, option) 对应的value
        """
        value_list = self._duplicates.get((section, option), [])
        value_list_ = self._duplicates.get((section, "#" + option), [])
        result = value_list + value_list_

        if result:
            return result
        else:
            return "not found"

    def setValue(self, section, option, value, content = None, isEffect="1"):
        """
        设置参数值， 未找到的option自动添加
        :param section: ini段名
        :param option: ini节点名
        :param value: 设置的值
        :param isEffect: 参数设置是否生效，默认为1
        :return:
        """
        if content is None:
            value_list = self._duplicates.get((section, option), [])
            value_list_ = self._duplicates.get((section, "#" + option), [])
            result = value_list + value_list_
            if not result:
                # 新增option
                self._duplicates.setdefault((section, option), []).append(value)
            else:
                self._duplicates.setdefault((section, option)).clear()
                # 设置value
                self._duplicates.setdefault((section, option), []).append(value)
        else:
            # 重复option 设置参数
            value_list = self._duplicates.get((section, option), [])
            value_list_ = self._duplicates.get((section, "#" + option), [])
            isExist = 0
            tuple = (value, isEffect)

            for index, item in enumerate(value_list):
                if content in item[0]:
                    # print("find target")
                    # print(item)
                    isExist = 1
                    # print(self._duplicates.get((section,option), []))
                    self._duplicates.setdefault((section, option), []).remove(item)
                    self._duplicates.setdefault((section, option), []).append(tuple)
                    # print(self._duplicates.get((section, option), []))
                    break

            for index, item in enumerate(value_list_):
                if content in item[0]:
                    # print("find target")
                    # print(item)
                    isExist = 1
                    # print(self._duplicates.get((section, "#" + option), []))
                    self._duplicates.setdefault((section, "#" + option), []).remove(item)
                    self._duplicates.setdefault((section, "#" + option), []).append(tuple)
                    # print(self._duplicates.get((section, "#" + option), []))
                    break

            if isExist == 0:
                # 新增optioin
                print("new option value")
                self._duplicates.setdefault((section, option), []).append(tuple)

    def updateToFile(self):
        """
        将保存的ini参数刷新到文件中
        """
        with open(self._path, 'w') as configfile:
            section_list = []
            for (section, option), values in sorted(self._duplicates.items(), key=lambda d: d[0]):
                # print((section, option))
                if section not in section_list:
                    configfile.write("\n")
                    configfile.write(f"[{section}]\n")
                    section_list.append(section)

                for value in values:
                    curr = option
                    if value[1] == "1":
                        # 生效
                        if option[:1] == '#':
                            # print("valid and '#'")
                            curr = option[1:]
                    else:
                        # 注释
                        if option[:1] != '#':
                            # print("invalid and no '#'")
                            curr = "#" + option
                    configfile.write(f"{curr} = {value[0]}\n")