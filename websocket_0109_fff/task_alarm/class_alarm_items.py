import config
import hal
from data_class import nc_module as module
import time
import copy


# 软限位
class SoftLimit(module.AlarmItem):
    def __init__(self, index: int, name: str, direction: str):
        """
        :param index: 轴序号（用于替换×的数字）
        :param name: 轴名称（用于显示报警信息）
        :param direction: [pos]:正限位
                          [neg]:负限位
        """
        self._index = index  # 序号
        self._axis = name  # 轴名字
        self._direction = direction  # 方向（正或负）

        if direction == "pos":
            self._halPin = config.halpin_pos_softlimit.replace("*", str(index))
            self._content = self._axis + "轴到达正向软限位"
        elif direction == "neg":
            self._halPin = config.halpin_neg_softlimit.replace("*", str(index))
            self._content = self._axis + "轴到达负向软限位"

        super().__init__("NC", self._content, "alarm")

    def end_alarm_override(self):
        self.struct.end_time = time.strftime("%Y-%m-%d,%H:%M:%S", time.localtime())
        struct = copy.copy(self.struct)
        module.AlarmItem._history_hardreset_alarms.append(struct)
        module.AlarmItem._current_hardreset_alarms.remove(self)

    def update(self):
        if hal.get_value(self._halPin):
            hal.set_p(config.halpin_alarm, "1")
            if self.flag:
                self.trigger_alarm()
                self.flag = False
        else:
            if not self.flag:
                self.end_alarm_override()
                # 如果当前没有报警
                if not self.is_alarm():
                    hal.set_p(config.halpin_alarm, "0")
            self.flag = True


# 硬限位
class HardLimit(module.AlarmItem):
    def __init__(self, index: int, name: str, direction: str):
        """
        :param index: 轴序号（用于替换×的数字）
        :param name: 轴名称（用于显示报警信息）
        :param direction: [pos]:正限位
                          [neg]:负限位
        """
        self._index = index  # 序号
        self._axis = name  # 轴名字
        self._direction = direction  # 方向（正或负）

        if direction == "pos":
            self._halPin = config.halpin_pos_hardlimit.replace("*", str(index))
            self._content = self._axis + "轴到达正向硬件限位开关"
        elif direction == "neg":
            self._halPin = config.halpin_neg_hardlimit.replace("*", str(index))
            self._content = self._axis + "轴到达负向硬件限位开关"
        super().__init__("NC", self._content, "alarm")

    def update(self):
        # 负限位
        if hal.get_value(self._halPin):
            hal.set_p(config.halpin_alarm, "1")
            if self.flag:
                self.trigger_alarm()
                self.flag = False
        else:
            self.flag = True


# PLC Custom Alarm
class CustomAlarm(module.AlarmItem):
    def __init__(self, addr, content, level: str):
        """
        用户自定义报警
        :param addr:plc地址，引脚名
        :param content: 用户自定义的报警内容
        :param level: 用户自定义的报警等级
        """
        self._halPin = str(addr)
        self._content = content  # 报警内容
        super().__init__("PLC", self._content, level)

    def update(self):
        if self._halPin == "":
            return
        try:
            val = hal.get_value(self._halPin)
        except:
            print('Do Not Get PLC Addr Value')
            return
        if val:
            if self.flag:  # 第一次报警
                self.trigger_alarm()
                self.flag = False
                print("append")


# 急停报警
class EStopAlarm(module.AlarmItem):
    def __init__(self):
        super().__init__("NC", "急停报警", "alarm")

    def update(self):
        val = hal.get_value("halui.estop.is-activated")
        if val:
            if self.flag:
                self.trigger_alarm()
                self.flag = False


# 驱动报警
class DriveAlarm(module.AlarmItem):
    def __init__(self, index: int, name: str):
        """
        驱动报警
        :param index: 轴序号，用于替换x的数字，如：lcec.0.[index].error-code
        :param name: 轴名字，用于显示报警内容，如：[name]轴驱动器报警，错误码：XXXX
        """
        self._halPin = config.halpin_drive_alarm.replace("*", str(index))
        self._content = name + "轴驱动器故障，错误码："
        super().__init__("DRIVE", self._content, "alarm")

    def update(self):
        error_code = hal.get_value(self._halPin)
        if error_code != 0:
            hal.set_p(config.halpin_alarm, "1")
            if self.flag:
                self.struct.content = self._content + str(error_code)
                self.trigger_alarm()
                self.flag = False


# EtherCAT通讯报警
class ECATAlarm(module.AlarmItem):
    def __init__(self):
        self._halPin = config.halpin_ecat_allop
        super().__init__("NC", "EtherCAT总线通讯故障", "alarm")

    def update(self):
        if not hal.get_value(self._halPin):
            hal.set_p(config.halpin_alarm, "1")
            if self.flag:
                self.trigger_alarm()
                self.flag = False

# 刀具报警
class ToolAlarm(module.AlarmItem):
    def __init__(self):
        self._halPin = config.halpin_tool_alarm
        self._content = "刀具报警"
        super().__init__("NC", self._content, "alarm")

    def update(self):
        error_code = hal.get_value(self._halPin)
        if error_code != 0:
            if self.flag:
                if error_code == 1:
                    self.struct.content = "刀位管理文件打开失败"
                elif error_code == 2:
                    self.struct.content = "左刀库未找到目标刀具"
                elif error_code == 3:
                    self.struct.content = "右刀库未找到目标刀具"
                elif error_code == 4:
                    self.struct.content = "左刀库无空刀位"
                elif error_code == 5:
                    self.struct.content = "右刀库无空刀位"
                elif error_code == 6:
                    self.struct.content = "刀库管理文件格式错误"
                elif error_code == 7:
                    self.struct.content = "刀库管理文件输入错误"
                elif error_code == 8:
                    self.struct.content = "换刀输入轴参数错误（非双主轴以外的参数）"
                elif error_code == 9:
                    self.struct.content = "左刀库关门超时"
                elif error_code == 10:
                    self.struct.content = "右刀库关门超时"
                elif error_code == 11:
                    self.struct.content = "备用报警项"
                elif error_code == 12:
                    self.struct.content = "冷却液关闭异常"
                elif error_code == 13:
                    self.struct.content = "左主轴当前刀号错误（左主轴检测无刀，当前刀号不为0）"
                elif error_code == 14:
                    self.struct.content = "右主轴当前刀号错误（左主轴检测无刀，当前刀号不为0）"
                elif error_code == 15:
                    self.struct.content = "左主轴当前刀号错误（左主轴检测有刀，当前主轴刀号为0）"
                elif error_code == 16:
                    self.struct.content = "右主轴当前刀号错误（左主轴检测有刀，当前主轴刀号为0）"
                elif error_code == 17:
                    self.struct.content = "左主轴松刀异常（未检测松刀完成信号）"
                elif error_code == 18:
                    self.struct.content = "右主轴松刀异常（未检测松刀完成信号）"
                elif error_code == 19:
                    self.struct.content = "左主轴紧刀异常（未检测松刀完成信号）"
                elif error_code == 20:
                    self.struct.content = "右主轴紧刀异常（未检测松刀完成信号）"
                elif error_code == 21:
                    self.struct.content = "左刀库换刀刀套无刀（接近开关检测无刀，刀具表显示有刀）"
                elif error_code == 22:
                    self.struct.content = "右刀库换刀刀套无刀（接近开关检测无刀，刀具表显示有刀）"
                elif error_code == 23:
                    self.struct.content = "左刀库还刀刀套有刀（接近开关检测有刀，刀具表显示无刀）"
                elif error_code == 24:
                    self.struct.content = "右刀库还刀刀套有刀（接近开关检测有刀，刀具表显示无刀）"
                elif error_code == 25:
                    self.struct.content = "左刀库开门超时"
                elif error_code == 26:
                    self.struct.content = "右刀库开门超时"
                elif error_code == 27:
                    self.struct.content = "文件管理操作超时"
                elif error_code == 28:
                    self.struct.content = "左主轴停车超时"
                elif error_code == 29:
                    self.struct.content = "右主轴停车超时"
                elif error_code == 30:
                    self.struct.content = "刀库旋转超时"
                else:
                    self.struct.content = "未知刀具报警，错误码：" + str(error_code)
                self.trigger_alarm()
                self.flag = False


# 循环启动时程序未加载报警
class ProgramNotReadyAlarm(module.AlarmItem):
    def __init__(self):
        self._halPin = config.halpin_program_not_ready
        super().__init__("NC", "未加载NC程序", "alarm")

    def update(self):
        if hal.get_value(self._halPin):
            hal.set_p(config.halpin_alarm, "1")
            if self.flag:
                self.trigger_alarm()
                self.flag = False


class CustomMessage(module.AlarmItem):

    def __init__(self, content: str):
        super().__init__("NC", content, "warn")

    def update(self):
        """
        :return:
        """


# EtherCAT掉从站报警
class EcatLostSlaveAlarm(module.AlarmItem):
    def __init__(self, slave_id: int):
        self.slave_id = slave_id
        self._halPin = config.halpin_ecat_lost_slave.replace("*", str(slave_id))

        content = "EtherCAT总线通讯，从站" + str(slave_id + 1) + "掉线"
        super().__init__("NC", content, "alarm")

    def update(self):
        if hal.get_value(self._halPin):
            # hal.set_p(config.halpin_alarm, "1")
            if self.flag:
                self.trigger_alarm()
                self.flag = False


# 缺少主轴使能
class SpindleNotEnableWarn(module.AlarmItem):
    def __init__(self):
        """
        """
        self._content = "主轴缺少使能"
        self._halPin = config.halpin_spindle_not_enabled_warn
        super().__init__("NC", self._content, "warn")

    def end_alarm_override(self):
        self.struct.end_time = time.strftime("%Y-%m-%d,%H:%M:%S", time.localtime())
        struct = copy.copy(self.struct)
        module.AlarmItem._history_hardreset_alarms.append(struct)
        module.AlarmItem._current_hardreset_alarms.remove(self)

    def update(self):
        if hal.get_value(self._halPin):
            if self.flag:
                self.trigger_alarm()
                self.flag = False
        else:
            if not self.flag:
                self.end_alarm_override()
            self.flag = True


# 缺少进给使能
class FeedNotEnableWarn(module.AlarmItem):
    def __init__(self):
        """
        """
        self._content = "进给缺少使能"
        self._halPin = config.halpin_feed_not_enabled_warn
        super().__init__("NC", self._content, "warn")

    def end_alarm_override(self):
        self.struct.end_time = time.strftime("%Y-%m-%d,%H:%M:%S", time.localtime())
        struct = copy.copy(self.struct)
        module.AlarmItem._history_hardreset_alarms.append(struct)
        module.AlarmItem._current_hardreset_alarms.remove(self)

    def update(self):
        if hal.get_value(self._halPin):
            if self.flag:
                self.trigger_alarm()
                self.flag = False
        else:
            if not self.flag:
                self.end_alarm_override()
            self.flag = True
