# -*- coding:utf-8 -*-

import tornado.web
import tornado.websocket
import json
import hal
import threading

from handler import ipc_handler
from handler import nc_handler
import config
from data_class import nc_module as module
from data_class import nc_action as action
from task_alarm import thread_alarm as thread_alarm
from task_alarm import thread_detect_alarm as thread_detect_alarm
from task_process_timer import thread_process_timer as process_timer
from task_mdi import thread_detect_mdi as thread_detect_mdi

if __name__ == "__main__":
    # 清空mdi文件
    action.clear_mdi_file()
    # 开启获取报警通道线程
    task_alarm_chanel = thread_alarm.AlarmThread()
    thread_task_alarm_chanel = threading.Thread(target=task_alarm_chanel.getAlarmInfos)
    thread_task_alarm_chanel.start()
    # 开启刷新报警线程
    task_detect_alarm = thread_detect_alarm.DetectAlarms()
    thread_task_detect_alarm = threading.Thread(target=task_detect_alarm.loop_task)
    thread_task_detect_alarm.start()
    # 网络心跳检测
    process_timer.process_task.start_task()
    # MDI检测线程
    model = thread_detect_mdi.MdiThread()
    mdi = threading.Thread(target=model.get_mdi_signal)
    mdi.start()
    # 定位模式检测线程
    position = threading.Thread(target=model.detect_position_finished)
    position.start()
    # 重启清空文件和标志引脚
    action.server_reset_interpreter()
    hal.set_p(config.halpin_program_is_ok, "0")
    print("server started")
    app = tornado.web.Application([
        (r"/GetNckData", nc_handler.APIHandler),
        (r"/GetSystemData", nc_handler.SystemWindowHandler),
        (r"/GetAxisData", nc_handler.AxisWindowHandler),
        (r"/GetToolData", nc_handler.ToolWindowHandler),
        (r"/GetMicroData", nc_handler.MicroWindowHandler),
        (r"/GetInitConfig", nc_handler.InitConfigHandler),
        (r"/GetAlarmData", nc_handler.AlarmWindowHandler),
        (r"/GetOffsetData", nc_handler.OffsetWindowHandler),
        (r"/GetNcPlcData", nc_handler.NcPlcHandler),
        (r"/GetDiagnosisData", nc_handler.DiagnosisWindowHandler),
        (r"/GetMicroProgramData", nc_handler.MicroProgramData),
        (r"/GetChannelData", nc_handler.ChannelData),
        (r"/PLC_Params",nc_handler.PLCParams),

        (r"/SoftReset", ipc_handler.SoftReset),
        (r"/CustomAlarm", ipc_handler.CustomAlarm),
        (r"/GetConfigFile", ipc_handler.DownloadHandler),
        (r"/NcProgram", ipc_handler.ChunkFileHandler),
        (r"/Parameter", ipc_handler.DataPostHandler),
        (r"/DownloadCompFile", ipc_handler.DownloadHandler),
        (r"/MdiCmd", ipc_handler.MdiCmdHandler),
        (r"/MdiClear", ipc_handler.MdiClear),
        (r"/Position", ipc_handler.Position),   # 定位
        (r"/JumpSegment", ipc_handler.JumpSegment),  # 跳段
        (r"/UploadFile", ipc_handler.UploadFileHandler),
        (r"/ManageNCK", ipc_handler.ManageNCKHandler),
        (r"/NcPlc", ipc_handler.NcPlcPostHandler),
        (r"/ResetG92", ipc_handler.ResetG92Handler),
        (r"/SetAxisOrigin", ipc_handler.SetAxisOrigin),
        (r"/SetScopeChannel", ipc_handler.SetScopeChannel),
        (r"/StartCapture", ipc_handler.StartCaptureHandler),
    ],
        debug=True,
    )

    address = config.ip
    port = config.port
    server = tornado.httpserver.HTTPServer(app)
    server.listen(port, address)
    tornado.ioloop.IOLoop.instance().start()

