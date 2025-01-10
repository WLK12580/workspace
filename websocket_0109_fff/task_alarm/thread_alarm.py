import config as config
import hal
import time
import threading
from task_alarm import class_alarm_items as alarm_items
from task_alarm import net_watchdog as net_watchdog
from task_alarm import extract_error as extract_error
from task_process_timer import thread_process_timer as processing_timer
from data_class import nc_module as module
from data_class import class_alarm as class_alarm
from task_mdi import target_position as target_position
import re


"""
刷新报警线程
"""


class AlarmThread:
    _freq = 0.015
    def getAlarmInfos(self):
        print("fresh alarm chanel thread started")
        # 读取配置文件检测频率
        self.load_freq()
        err = module.error
        while True:
            # 复位
            if hal.get_value(config.halpin_reset):
                # 定位清除
                target_position.PositionStateMachine.stop()
				# 定位模式退出
                hal.set_p(config.halpin_position_flag, "0")
                hal.set_p(config.halpin_alarm, "0")
                time.sleep(0.1)
                processing_timer.process_task.reset_program()
                module.AlarmItem.hard_reset_alarm()
                self.write_alarm_to_file()
                hal.set_p(config.halpin_server_reset, "1")
                time.sleep(0.1)
            else:
                hal.set_p(config.halpin_server_reset, "0")
                # 错误通道读取NC报警
                error = err.poll()
                if error:
                    print(error)
                    info = extract_error.extract_error(str(error))
                    if info:
                        err_code = info[0]      # 报警等级错误码 11或者13
                        err_content = info[1]   # 报警文本
                        if "关节" in err_content:
                            err_content = err_content.replace("关节", "轴")

                        # MSG清除指令
                        if err_code == "13" and err_content == "":
                            self.write_msg_to_file()
                        elif err_code == "13" and err_content != "":
                            alarm_items.CustomMessage(err_content).trigger_msg()
                            print("custom msg:" + err_content)
                        elif err_code == "11":
                            err_level = "alarm"
                            module.AlarmItem("NC", err_content, err_level).trigger_alarm()
                            hal.set_p(config.halpin_alarm, "1")
                            print("error text:" + err_content)
                    else:
                        # 报未知错误
                        err_content = "未知错误"
                        print("未知错误:" + err_content)
                        module.AlarmItem("NC", err_content, "alarm").trigger_alarm()
                        hal.set_p(config.halpin_alarm, "1")

                    error_kind, error_text = error
                    if error_kind in (module.NML_ERROR, module.OPERATOR_ERROR):
                        error_type = "Error :: "
                    else:
                        error_type = "Info :: "
            time.sleep(AlarmThread._freq)

    def write_alarm_to_file(self):
        thread = threading.Thread(target=self.write_history_alarms)
        thread.start()

    def write_msg_to_file(self):
        thread = threading.Thread(target=self.write_custom_msg)
        thread.start()

    # 把报警写入历史报警文件
    def write_history_alarms(self):
        module.AlarmItem.export_hardreset_history_alarms(config.history_alarm_path)

    # 把用户自定义信息写入历史报警文件
    def write_custom_msg(self):
        alarm_items.CustomMessage.end_custom_msg(config.history_alarm_path)

    def load_freq(self):
        # 读取配置文件检测频率
        try:
            AlarmThread._freq = float(config.freq_alarm_monitor)
        except ValueError:
            AlarmThread._freq = 0.015
        print("monitor freq:" + str(AlarmThread._freq))
