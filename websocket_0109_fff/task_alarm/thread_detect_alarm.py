import config as config
from task_alarm import net_watchdog as net_watchdog
from task_alarm import class_alarm_items as alarm_items
from data_class import nc_module as module
import time
import threading

"""
创建报警
"""
# 1.急停报警
alarm_items.EStopAlarm().add_to_loop()
# 2.软限位报警
for index, item in enumerate(config.softlimit_axis_list):
    alarm_items.SoftLimit(index, item, "pos").add_to_loop()
    alarm_items.SoftLimit(index, item, "neg").add_to_loop()
    print("soft limit:" + str(index) + item)
# 3.硬限位报警
for index, item in enumerate(config.hardlimit_axis_list):
    alarm_items.HardLimit(index, item, "pos").add_to_loop()
    alarm_items.HardLimit(index, item, "neg").add_to_loop()
    print("hard limit:" + str(index) + item)
# 4. ECAT通讯报警
if config.is_activate_ecat_allop:
    # alarm_items.ECATAlarm().add_to_loop("SOFT_RESET")
    alarm_items.ECATAlarm().add_to_loop()
# 5. 网络故障检测线程
network_alarm = net_watchdog.WatchDog()
# 6. 驱动报警
for index, item in enumerate(config.drive_alarm_axis_list):
    if item != "NONE":
        print("drive:" + str(index) + item)
        alarm_items.DriveAlarm(index, item).add_to_loop()
# 7. 刀具报警
alarm_items.ToolAlarm().add_to_loop()
# 8. 程序未加载报警
if config.halpin_program_not_ready != "":
    alarm_items.ProgramNotReadyAlarm().add_to_loop()
# 9. Ecat从站掉线报警
if config.halpin_ecat_lost_slave != "":
    for i in range(0, module.axis_count):
        alarm_items.EcatLostSlaveAlarm(i).add_to_loop()
# 10. 缺少主轴使能
if config.halpin_spindle_not_enabled_warn != "":
    alarm_items.SpindleNotEnableWarn().add_to_loop()
# 11. 缺少进给使能
if config.halpin_feed_not_enabled_warn != "":
    alarm_items.FeedNotEnableWarn().add_to_loop()


class DetectAlarms:
    #  检测频率
    _freq = 0.02

    def loop_task(self):
        print("detect alarms thread started")
        # 读取配置文件检测频率
        self.load_freq()
        # 创建历史报警文件
        with open(config.history_alarm_path, "a") as file:
            file.close()
        # 开始检测网络状态任务
        network_alarm.start_task()
        while True:
            # 检测报警
            module.AlarmItem.update_alarm()
            time.sleep(DetectAlarms._freq)

    def load_freq(self):
        # 读取配置文件检测频率
        try:
            DetectAlarms._freq = float(config.freq_alarm_detect)
        except ValueError:
            DetectAlarms._freq = 0.02
        print("detect freq:" + str(DetectAlarms._freq))
