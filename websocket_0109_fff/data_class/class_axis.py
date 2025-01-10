import hal
import linuxcnc

import config
from data_class import nc_module as module
from task_mdi import target_position as target_position
import math

diagnosis_axis = {0: "X", 1: "Y", 2: "Z", 3: "B",
                  4: "Spindle", 5: "C", 6: "Tool"}


# 轴-使能
class AxisEnabled(module.DataNode):
    def __init__(self, joint_id: int):
        """
        :param joint_id: 关节号
        """
        self.joint_id = joint_id
        axis_name, axis_id = module.get_axis_id(joint_id)
        self.axis_id = axis_id
        self.axis_name = axis_name

        index = str(300000 + self.joint_id)
        axis_name = self.axis_name + "_enabled"
        super().__init__(index, axis_name, "VARIABLE")

    def value(self):
        if module.stat.joint[self.axis_id]["enabled"] == 0:
            return "1"
        else:
            return "0"


# 轴-回零
class AxisHomed(module.DataNode):
    def __init__(self, joint_id: int):
        """
        :param joint_id: 关节号
        """
        self.joint_id = joint_id
        axis_name, axis_id = module.get_axis_id(joint_id)
        self.axis_id = axis_id
        self.axis_name = axis_name
        self.pin = "joint." + str(joint_id) + ".homed"  # 关节对应的引脚
        # 取360余标志
        module.config.read(module.stat.ini_filename, encoding='utf-8')
        if module.config.has_option("AXIS_" + str(self.axis_name.upper()), "WRAPPED_ROTARY"):
            self.rotary_flag = True
        else:
            self.rotary_flag = False

        index = str(300100 + self.joint_id)
        name = self.axis_name + "_homed"
        super().__init__(index, name, "VARIABLE")

    def value(self):
        value = hal.get_value(self.pin)
        if value:
            return "1"
        else:
            return "0"


# 轴-当前位置-MCS
class AxisActualPosition(module.DataNode):
    def __init__(self, joint_id: int):
        self.joint_id = joint_id  # 关节号
        self.axis_name = module.axis_list[joint_id]  # 关节对应的轴名
        self.pin = "joint." + str(joint_id) + ".pos-fb"  # 关节对应的引脚
        # 取360余标志
        module.config.read(module.stat.ini_filename, encoding='utf-8')
        if module.config.has_option("AXIS_" + str(self.axis_name.upper()), "WRAPPED_ROTARY"):
            self.rotary_flag = True
        else:
            self.rotary_flag = False
        index = str(300200 + self.joint_id)
        axis_name = "axis_" + str(self.joint_id) + "_current_position"
        super().__init__(index, axis_name, "POSITION")

    def value(self):
        actual_position = hal.get_value(self.pin)
        if self.rotary_flag:
            return str(actual_position % 360)
        return str(actual_position)


# 轴-目标位置-MCS
class AxisTargetPosition(module.DataNode):
    position_point = {}

    def __init__(self, joint_id: int):
        """
        :param joint_id: 关节号
        """
        self.joint_id = joint_id
        axis_name, axis_id = module.get_axis_id(joint_id)
        self.pin = "joint." + str(joint_id) + ".pos-cmd"  # 关节对应的引脚
        self.axis_id = axis_id
        self.axis_name = axis_name
        # 取360余标志
        module.config.read(module.stat.ini_filename, encoding='utf-8')
        if module.config.has_option("AXIS_" + str(self.axis_name.upper()), "WRAPPED_ROTARY"):
            self.rotary_flag = True
        else:
            self.rotary_flag = False

        index = str(300300 + self.joint_id)
        name = self.axis_name + "_target_position"
        super().__init__(index, name, "POSITION")

    def value(self):
        target_position = hal.get_value(self.pin)
        if self.rotary_flag:
            return str(target_position % 360)
        return str(target_position)

    def set_value(self, value):
        AxisTargetPosition.position_point[self.axis_id] = float(value)


# 轴-余程-MCS
class AxisRemainingDistance(module.DataNode):
    def __init__(self, joint_id: int):
        """
        :param joint_id: 关节号
        """
        self.joint_id = joint_id
        axis_name, axis_id = module.get_axis_id(joint_id)
        self.axis_id = axis_id
        self.axis_name = axis_name
        # 取360余标志
        module.config.read(module.stat.ini_filename, encoding='utf-8')
        if module.config.has_option("AXIS_" + str(self.axis_name.upper()), "WRAPPED_ROTARY"):
            self.rotary_flag = True
        else:
            self.rotary_flag = False

        index = str(300400 + self.joint_id)
        name = self.axis_name + "_remaining_distance"
        super().__init__(index, name, "DISTANCE")

    def value(self):
        remaining_position = module.stat.dtg[self.axis_id]
        if self.rotary_flag:
            return str(remaining_position % 360)
        return str(remaining_position)


# 轴-当前速度
class AxisVelocity(module.DataNode):
    def __init__(self, name):
        self.axis_id = module.axis[name]
        index = str(300500 + self.axis_id)
        axis_name = name + "_velocity"
        super().__init__(index, axis_name, "Velocity")

    def value(self):
        return str(module.stat.joint[self.axis_id]["velocity"])


# 进给率
class AxisFeedrate(module.DataNode):
    def __init__(self):
        index = "300600"
        name = "feedrate"
        super().__init__(index, name, "Feedrate")

    def value(self):
        # 手动模式根据引脚判断 当前进给/快速进给
        if module.stat.task_mode == 1:
            if hal.get_value(config.halpin_feed_rate):
                feed = "%.2f" % module.stat.rapidrate
                return str(int(float(feed) * 100))
            else:
                feed = "%.2f" % module.stat.feedrate
                return str(int(float(feed) * 100))
        else:
            if module.stat.gcodes[1] == 0:
                feed = "%.2f" % module.stat.rapidrate
                return str(int(float(feed) * 100))
            else:
                feed = "%.2f" % module.stat.feedrate
                return str(int(float(feed) * 100))


# 关节-当前跟随误差
class JointCurrentFerror(module.DataNode):
    def __init__(self, num):
        self.joint_id = num
        index = str(300700 + self.joint_id)
        joint_name = str(num) + "_current_ferror"
        super().__init__(index, joint_name, "VARIABLE")

    def value(self):
        return str(module.stat.joint[self.joint_id]["ferror_current"])


# 主轴-转速
class SpindleSpeed(module.DataNode):
    def __init__(self, num):
        self.spindle_id = num
        index = str(300800 + self.spindle_id)
        spindle_name = "spindle_" + str(num) + "_speed"
        super().__init__(index, spindle_name, "VARIABLE")

    def value(self):
        spindle_speed = str(hal.get_value(config.halpin_spindle_vel))
        if spindle_speed[0] == "-":
            return spindle_speed[1:]
        return spindle_speed

    def set_value(self, value):
        module.command.spindle(linuxcnc.SPINDLE_FORWARD, float(value), self.spindle_id)


# 主轴-使能
class SpindleEnabled(module.DataNode):
    def __init__(self, num):
        self.spindle_id = num
        index = str(300900 + self.spindle_id)
        spindle_name = "spindle_" + str(num) + "_enabled"
        super().__init__(index, spindle_name, "VARIABLE")

    def value(self):
        return str(module.stat.spindle[self.spindle_id]["enabled"])


# 主轴-倍率
class SpindleOverride(module.DataNode):
    def __init__(self, num):
        self.spindle_id = num
        index = str(301000 + self.spindle_id)
        spindle_name = "spindle_" + str(num) + "_rate"
        super().__init__(index, spindle_name, "VARIABLE")

    def value(self):
        return str(module.stat.spindle[self.spindle_id]["override"])

    def set_value(self, value):
        module.command.spindleoverride(float(value), self.spindle_id)


# 当前实际进给速度
class CurrentVelocity(module.DataNode):
    def __init__(self):
        super().__init__("301200", "current_velocity", "VARIABLE")

    def value(self):
        vel = hal.get_value(config.halpin_feed_velocity)
        return str(vel * 60)


# 当前设定进给速度
class FeedVelocity(module.DataNode):
    def __init__(self):
        super().__init__("301300", "feed_velocity", "VARIABLE")

    def value(self):
        # if hal.get_value("halui.mode.is-manual"):
        #     if target_position.PositionStateMachine.current_state() == "exec":
        #         rate = float("%.2f" % module.stat.feedrate)
        #         if rate == 0:
        #             return "0"
        #         rev_value = target_position.TargetPosition.feed()
        #         act_value = float(hal.get_value(config.halpin_feed_velocity))*60/rate
        #         if rev_value*1.2 > act_value:
        #             return str(act_value)
        #         else:
        #             return str(rev_value)
        # else:
        vel = hal.get_value(config.halpin_feed_setting_vel)
        return str(vel * 60)


# 主轴-回零
class SpindleHomed(module.DataNode):
    def __init__(self, num):
        self.spindle_id = num
        index = str(301400 + self.spindle_id)
        spindle_name = "spindle_" + str(num) + "_homed"
        super().__init__(index, spindle_name, "VARIABLE")

    def value(self):
        if hal.get_value(config.halpin_spindle_0_homed):
            return "1"
        return "0"
        # return str(module.stat.spindle[self.spindle_id]["homed"])


# 轴-当前位置-WCS
class AxisActualPositionWCS(module.DataNode):
    def __init__(self, joint_id: int):
        self.joint_id = joint_id  # 关节号
        self.axis_name = module.axis_list[joint_id]  # 关节对应的轴名
        self.axis_id = module.axis[self.axis_name.lower()]  # 轴名对应的编号 xyzabcuvw
        pin_name = "halui.axis.*.pos-relative"
        self.pin = pin_name.replace("*", self.axis_name.lower())  # 关节对应的引脚

        # 取360余标志
        module.config.read(module.stat.ini_filename, encoding='utf-8')
        if module.config.has_option("AXIS_" + str(self.axis_name.upper()), "WRAPPED_ROTARY"):
            self.rotary_flag = True
        else:
            self.rotary_flag = False

        index = str(301500 + self.joint_id)
        axis_name = "axis_" + str(self.joint_id) + "_current_position_WCS"
        super().__init__(index, axis_name, "POSITION")

    def value(self):
        position = hal.get_value(self.pin)
        if self.rotary_flag:
            return str(position % 360)
        return str(position)


# 轴-目标位置-WCS
class AxisActualTargetPositionWCS(module.DataNode):
    def __init__(self, joint_id: int):
        self.joint_id = joint_id
        self.axis_name, self.axis_id = module.get_axis_id(joint_id)
        self.pin_tar_mcs = "joint." + str(joint_id) + ".pos-cmd"  # 目标位置-MCS
        self.pin_cur_mcs = "joint." + str(joint_id) + ".pos-fb"  # 当前位置-MCS
        pin_name = "halui.axis.*.pos-relative"
        self.pin_cur_wcs = pin_name.replace("*", self.axis_name.lower())  # 关节对应的引脚

        # 取360余标志
        module.config.read(module.stat.ini_filename, encoding='utf-8')
        if module.config.has_option("AXIS_" + str(self.axis_name.upper()), "WRAPPED_ROTARY"):
            self.rotary_flag = True
        else:
            self.rotary_flag = False

        index = str(301600 + self.joint_id)
        name = "axis_" + str(self.joint_id) + "_target_position_WCS"
        super().__init__(index, name, "POSITION")

    def value(self):
        tar_mcs = hal.get_value(self.pin_tar_mcs)
        cur_mcs = hal.get_value(self.pin_cur_mcs)
        cur_wcs = hal.get_value(self.pin_cur_wcs)
        tar_wcs = cur_wcs + (tar_mcs - cur_mcs)
        if self.rotary_flag:
            return str(tar_wcs % 360)
        return str(tar_wcs)


# 主轴设定转速
class SpindleSettingSpeed(module.DataNode):
    def __init__(self, num):
        self.spindle_id = num
        index = str(301700 + self.spindle_id)
        spindle_name = "spindle_" + str(num) + "_setting_speed"
        super().__init__(index, spindle_name, "VARIABLE")

    def value(self):
        return str(hal.get_value(config.halpin_spindle_setting_vel))


# 主轴当前位置
class SpindleCurrentPosition(module.DataNode):
    def __init__(self, num):
        self.spindle_id = num
        index = str(301800 + self.spindle_id)
        spindle_name = "spindle_" + str(num) + "_current_position"
        super().__init__(index, spindle_name, "VARIABLE")

    def value(self):
        return str(hal.get_value(config.halpin_spindle_current_position))


# 旋转轴设为1时，轴移动0-359.99度
class AxisLetterWrappedRotary(module.DataNode):
    def __init__(self, name):
        self.axis_id = module.axis[name]
        self.axis_name = name.upper()
        index = str(310700 + self.axis_id)
        axis_name = name + "_rotary_units"
        super().__init__(index, axis_name, "Variable")

    def value(self):
        return str(module.inifile.find("AXIS_" + str(self.axis_id), "WRAPPED_ROTARY"))

    def set_value(self, value):
        module.setIniValue(module.stat.ini_filename, "AXIS_" + str(self.axis_name), "WRAPPED_ROTARY",
                           value)


# 轴-锁定的关节号
class AxisLetterLockingIndexerJoint(module.DataNode):
    def __init__(self, name):
        self.axis_id = module.axis[name]
        self.axis_name = name.upper()
        index = str(311000 + self.axis_id)
        axis_name = name + "_locking_joint"
        super().__init__(index, axis_name, "Variable")

    def value(self):
        return str(module.inifile.find("AXIS_" + str(self.axis_id), "LOCKING_INDEXER_JOINT"))

    def set_value(self, value):
        module.setIniValue(module.stat.ini_filename, "AXIS_" + str(self.axis_name), "LOCKING_INDEXER_JOINT",
                           value)


# 轴-外部轴偏移
class AxisLetterOffsetAvRatio(module.DataNode):
    def __init__(self, name):
        self.axis_id = module.axis[name]
        self.axis_name = name.upper()
        index = str(311100 + self.axis_id)
        axis_name = name + "_offset_ratio"
        super().__init__(index, axis_name, "Variable")

    def value(self):
        return str(module.inifile.find("AXIS_" + str(self.axis_id), "OFFSET_AV_RATIO"))

    def set_value(self, value):
        module.setIniValue(module.stat.ini_filename, "AXIS_" + str(self.axis_name), "OFFSET_AV_RATIO",
                           value)


# 关节-类型==轴类型
class JointNumType(module.DataNode):
    def __init__(self, num):
        self.joint_id = num
        index = str(311200 + self.joint_id)
        joint_name = "joint_" + str(num) + "_type"
        super().__init__(index, joint_name, "Type")

    def value(self):
        if module.stat.joint[self.joint_id]["jointType"] == 1:
            return "Linear"
        elif module.stat.joint[self.joint_id]["jointType"] == 2:
            return "Angular"

    def set_value(self, value):
        module.setIniValue(module.stat.ini_filename, "JOINT_" + str(self.joint_id), "TYPE",
                           value)
        module.setIniValue(module.stat.ini_filename, "AXIS_" + str(module.axis_list[self.joint_id]), "TYPE",
                           value)


# 关节-最大速度==轴-最大速度
class JointNumMaxVelocity(module.DataNode):
    def __init__(self, num):
        self.joint_id = num
        index = str(311300 + self.joint_id)
        joint_name = "joint_" + str(num) + "_max_velocity"
        super().__init__(index, joint_name, "VARIABLE")

    def value(self):
        return str(module.inifile.find("JOINT_" + str(self.joint_id), "MAX_VELOCITY"))

    def set_value(self, value):
        module.setIniValue(module.stat.ini_filename, "JOINT_" + str(self.joint_id), "MAX_VELOCITY",
                           value)
        module.setIniValue(module.stat.ini_filename, "AXIS_" + str(module.axis_list[self.joint_id]), "MAX_VELOCITY",
                           value)


# 关节-最大加速度 == 轴-最大加速度
class JointNumMaxAcceleration(module.DataNode):
    def __init__(self, num):
        self.joint_id = num
        index = str(311400 + self.joint_id)
        joint_name = "joint_" + str(num) + "_max_acceleration"
        super().__init__(index, joint_name, "VARIABLE")

    def value(self):
        return str(module.inifile.find("JOINT_" + str(self.joint_id), "MAX_ACCELERATION"))

    def set_value(self, value):
        module.setIniValue(module.stat.ini_filename, "JOINT_" + str(self.joint_id), "MAX_ACCELERATION",
                           value)
        module.setIniValue(module.stat.ini_filename, "AXIS_" + str(module.axis_list[self.joint_id]), "MAX_ACCELERATION",
                           value)


# 关节-反向间隙
class JointNumBacklash(module.DataNode):
    def __init__(self, num):
        self.joint_id = num
        index = str(311500 + self.joint_id)
        joint_name = "joint_" + str(num) + "_backlash"
        super().__init__(index, joint_name, "VARIABLE")

    def value(self):
        return str(module.stat.joint[self.joint_id]["backlash"])

    def set_value(self, value):
        module.setIniValue(module.stat.ini_filename, "JOINT_" + str(self.joint_id), "BACKLASH",
                           value)


# 关节-负向软限位== 轴-负向软限位
class JointNumMinLimit(module.DataNode):
    def __init__(self, num):
        self.joint_id = num
        index = str(311600 + self.joint_id)
        joint_name = "joint_" + str(num) + "_min_limit"
        super().__init__(index, joint_name, "VARIABLE")

    def value(self):
        return str(module.stat.joint[self.joint_id]["min_position_limit"])

    def set_value(self, value):
        module.setIniValue(module.stat.ini_filename, "JOINT_" + str(self.joint_id), "MIN_LIMIT",
                           value)
        module.setIniValue(module.stat.ini_filename, "AXIS_" + str(module.axis_list[self.joint_id]), "MIN_LIMIT",
                           value)


# 关节-正向软限位==轴-正向软限位
class JointNumMaxLimit(module.DataNode):
    def __init__(self, num):
        self.joint_id = num
        self.axis_name = list(module.axis.keys())[num].upper()
        index = str(311700 + self.joint_id)
        joint_name = "joint_" + str(num) + "_max_limit"
        super().__init__(index, joint_name, "VARIABLE")

    def value(self):
        return str(module.stat.joint[self.joint_id]["max_position_limit"])

    def set_value(self, value):
        module.setIniValue(module.stat.ini_filename, "JOINT_" + str(self.joint_id), "MAX_LIMIT",
                           value)
        module.setIniValue(module.stat.ini_filename, "AXIS_" + str(module.axis_list[self.joint_id]), "MAX_LIMIT",
                           value)


# 关节-最小速度比例跟随误差
class JointNumMinFerror(module.DataNode):
    def __init__(self, num):
        self.joint_id = num
        index = str(311800 + self.joint_id)
        joint_name = "joint_" + str(num) + "_min_ferror"
        super().__init__(index, joint_name, "VARIABLE")

    def value(self):
        return str(module.stat.joint[self.joint_id]["min_ferror"])

    def set_value(self, value):
        module.setIniValue(module.stat.ini_filename, "JOINT_" + str(self.joint_id), "MIN_FERROR",
                           value)


# 关节-最大速度比例跟随误差限制
class JointNumFerror(module.DataNode):
    def __init__(self, num):
        self.joint_id = num
        index = str(311900 + self.joint_id)
        joint_name = "joint_" + str(num) + "_max_ferror"
        super().__init__(index, joint_name, "VARIABLE")

    def value(self):
        return str(module.stat.joint[self.joint_id]["max_ferror"])

    def set_value(self, value):
        module.setIniValue(module.stat.ini_filename, "JOINT_" + str(self.joint_id), "FERROR",
                           value)


# 关节-是否为锁定分度器
class JointNumLockingIndexer(module.DataNode):
    def __init__(self, num):
        self.joint_id = num
        index = str(312000 + self.joint_id)
        joint_name = "joint_" + str(num) + "is_locking"
        super().__init__(index, joint_name, "VARIABLE")

    def value(self):
        if module.inifile.find("JOINT_" + str(self.joint_id), "LOCKING_INDEXER") == 1:
            return "1"
        else:
            return "0"

    def set_value(self, value):
        module.setIniValue(module.stat.ini_filename, "JOINT_" + str(self.joint_id), "LOCKING_INDEXER",
                           value)


# 回参考点后关节要到达的位置
class JointNumHome(module.DataNode):
    def __init__(self, num):
        self.joint_id = num
        index = str(312100 + self.joint_id)
        joint_name = "joint_" + str(num) + "_home_position"
        super().__init__(index, joint_name, "VARIABLE")

    def value(self):
        return str(module.inifile.find("JOINT_" + str(self.joint_id), "HOME"))

    def set_value(self, value):
        module.setIniValue(module.stat.ini_filename, "JOINT_" + str(self.joint_id), "HOME",
                           value)


# 零位开关或标志脉冲的关节位置
class JointNumHomeOffset(module.DataNode):
    def __init__(self, num):
        self.joint_id = num
        index = str(312200 + self.joint_id)
        joint_name = "joint_" + str(num) + "_home_offset"
        super().__init__(index, joint_name, "VARIABLE")

    def value(self):
        return str(module.inifile.find("JOINT_" + str(self.joint_id), "HOME_OFFSET"))

    def set_value(self, value):
        module.setIniValue(module.stat.ini_filename, "JOINT_" + str(self.joint_id), "HOME_OFFSET",
                           value)


# 关节-回参考点的初始速度
class JointNumHomeSearchVel(module.DataNode):
    def __init__(self, num):
        self.joint_id = num
        index = str(312300 + self.joint_id)
        joint_name = "joint_" + str(num) + "_home_search_vel"
        super().__init__(index, joint_name, "VARIABLE")

    def value(self):
        return str(module.inifile.find("JOINT_" + str(self.joint_id), "HOME_SEARCH_VEL"))

    def set_value(self, value):
        module.setIniValue(module.stat.ini_filename, "JOINT_" + str(self.joint_id), "HOME_SEARCH_VEL",
                           value)


# 关节-到零位开关的速度
class JointNumHomeLatchVel(module.DataNode):
    def __init__(self, num):
        self.joint_id = num
        index = str(312400 + self.joint_id)
        joint_name = "joint_" + str(num) + "_home_latch_vel"
        super().__init__(index, joint_name, "VARIABLE")

    def value(self):
        return str(module.inifile.find("JOINT_" + str(self.joint_id), "HOME_LATCH_VEL"))

    def set_value(self, value):
        module.setIniValue(module.stat.ini_filename, "JOINT_" + str(self.joint_id), "HOME_LATCH_VEL",
                           value)


# 关节-从零位开关到零位的速度
class JointNumHomeFinalVel(module.DataNode):
    def __init__(self, num):
        self.joint_id = num
        index = str(312500 + self.joint_id)
        joint_name = "joint_" + str(num) + "_home_final_vel"
        super().__init__(index, joint_name, "VARIABLE")

    def value(self):
        return str(module.inifile.find("JOINT_" + str(self.joint_id), "HOME_FINAL_VEL"))

    def set_value(self, value):
        module.setIniValue(module.stat.ini_filename, "JOINT_" + str(self.joint_id), "HOME_FINAL_VEL",
                           value)


# 关节-编码有零脉冲
class JointNumHomeUseIndex(module.DataNode):
    def __init__(self, num):
        self.joint_id = num
        index = str(312600 + self.joint_id)
        joint_name = "joint_" + str(num) + "_home_use_index_pulse"
        super().__init__(index, joint_name, "VARIABLE")

    def value(self):
        if module.inifile.find("JOINT_" + str(self.joint_id), "HOME_USE_INDEX") == "NO":
            return "0"
        elif module.inifile.find("JOINT_" + str(self.joint_id), "HOME_USE_INDEX") == "YES":
            return "1"

    def set_value(self, value):
        if value == "1":
            module.setIniValue(module.stat.ini_filename, "JOINT_" + str(self.joint_id), "HOME_USE_INDEX",
                               "YES")
        elif value == "0":
            module.setIniValue(module.stat.ini_filename, "JOINT_" + str(self.joint_id), "HOME_USE_INDEX",
                               "NO")


# 关节-编码器复位
class JointNumHomeIndexNoEncoderReset(module.DataNode):
    def __init__(self, num):
        self.joint_id = num
        index = str(312700 + self.joint_id)
        joint_name = "joint_" + str(num) + "_home_encoder_reset"
        super().__init__(index, joint_name, "VARIABLE")

    def value(self):
        if module.inifile.find("JOINT_" + str(self.joint_id), "HOME_INDEX_NO_ENCODER_RESET") == "NO":
            return "0"
        elif module.inifile.find("JOINT_" + str(self.joint_id), "HOME_INDEX_NO_ENCODER_RESET") == "YES":
            return "1"

    def set_value(self, value):
        if value == "1":
            module.setIniValue(module.stat.ini_filename, "JOINT_" + str(self.joint_id), "HOME_INDEX_NO_ENCODER_RESET",
                               "YES")
        elif value == "0":
            module.setIniValue(module.stat.ini_filename, "JOINT_" + str(self.joint_id), "HOME_INDEX_NO_ENCODER_RESET",
                               "NO")


# 关节-使用绝对值编码器
class JointNumHomeAbsoluteEncoder(module.DataNode):
    def __init__(self, num):
        self.joint_id = num
        index = str(312800 + self.joint_id)
        joint_name = "joint_" + str(num) + "_absolute_encoder"
        super().__init__(index, joint_name, "VARIABLE")

    def value(self):
        return str(module.inifile.find("JOINT_" + str(self.joint_id), "HOME_ABSOLUTE_ENCODER"))
        # if module.inifile.find("JOINT_" + str(self.joint_id), "HOME_ABSOLUTE_ENCODER") == 0:
        #     return "false"
        # elif module.inifile.find("JOINT_" + str(self.joint_id), "HOME_ABSOLUTE_ENCODER") == 1:
        #     return "move to home"
        # elif module.inifile.find("JOINT_" + str(self.joint_id), "HOME_ABSOLUTE_ENCODER") == 2:
        #     return "not move"

    def set_value(self, value):
        module.setIniValue(module.stat.ini_filename, "JOINT_" + str(self.joint_id), "HOME_ABSOLUTE_ENCODER", value)


# 关节-回零顺序
class JointNumHomeSequence(module.DataNode):
    def __init__(self, num):
        self.joint_id = num
        index = str(312900 + self.joint_id)
        joint_name = "joint_" + str(num) + "_home_sequence"
        super().__init__(index, joint_name, "VARIABLE")

    def value(self):
        return str(module.inifile.find("JOINT_" + str(self.joint_id), "HOME_SEQUENCE"))

    def set_value(self, value):
        module.setIniValue(module.stat.ini_filename, "JOINT_" + str(self.joint_id), "HOME_SEQUENCE", value)


# 主轴-最大正向转速
class SpindleNumMaxForwardVelocity(module.DataNode):
    def __init__(self, num):
        self.spindle_id = num
        index = str(313000 + self.spindle_id)
        spindle_name = "spindle_" + str(num) + "_max_forward_vel"
        super().__init__(index, spindle_name, "VARIABLE")

    def value(self):
        return str(module.inifile.find("SPINDLE_" + str(self.spindle_id), "MAX_FORWARD_VELOCITY"))

    def set_value(self, value):
        module.setIniValue(module.stat.ini_filename, "SPINDLE_" + str(self.spindle_id), "MAX_FORWARD_VELOCITY", value)


# 主轴-最大反向转速
class SpindleNumMaxReverseVelocity(module.DataNode):
    def __init__(self, num):
        self.spindle_id = num
        index = str(313100 + self.spindle_id)
        spindle_name = "spindle_" + str(num) + "_max_reverse_vel"
        super().__init__(index, spindle_name, "VARIABLE")

    def value(self):
        return str(module.inifile.find("SPINDLE_" + str(self.spindle_id), "MAX_REVERSE_VELOCITY"))

    def set_value(self, value):
        module.setIniValue(module.stat.ini_filename, "SPINDLE_" + str(self.spindle_id), "MAX_REVERSE_VELOCITY", value)


# 主轴-速度递增/递减的步长
class SpindleNumIncrement(module.DataNode):
    def __init__(self, num):
        self.spindle_id = num
        index = str(313200 + self.spindle_id)
        spindle_name = "spindle_" + str(num) + "_increment"
        super().__init__(index, spindle_name, "VARIABLE")

    def value(self):
        return str(module.inifile.find("SPINDLE_" + str(self.spindle_id), "INCREMENT"))

    def set_value(self, value):
        module.setIniValue(module.stat.ini_filename, "SPINDLE_" + str(self.spindle_id), "INCREMENT", value)


# 主轴-回零速度
class SpindleNumHomeSearchVelocity(module.DataNode):
    def __init__(self, num):
        self.spindle_id = num
        index = str(313300 + self.spindle_id)
        spindle_name = "spindle_" + str(num) + "_home_vel"
        super().__init__(index, spindle_name, "VARIABLE")

    def value(self):
        return str(module.inifile.find("SPINDLE_" + str(self.spindle_id), "HOME_SEARCH_VELOCITY"))

    def set_value(self, value):
        module.setIniValue(module.stat.ini_filename, "SPINDLE_" + str(self.spindle_id), "HOME_SEARCH_VELOCITY", value)


# 轴总数量
class AxisNum(module.DataNode):
    def __init__(self):
        super().__init__("313400", "AxisNum", "VARIABLE")

    def value(self):
        return str(module.axis_count)


# 轴反向间隙补偿启动设置
# class JointNumBacklashSetting(module.DataNode):
#     def __init__(self, num):
#         self.joint_id = num
#         index = str(313500 + self.joint_id)
#         joint_name = "joint_" + str(num) + "_backlash_setting"
#         super().__init__(index, joint_name, "VARIABLE")
#
#     def value(self):
#         module.config.read(module.stat.ini_filename, encoding='utf-8')
#         if module.config.has_option("JOINT_" + str(self.joint_id), "BACKLASH"):
#             return "1"
#         else:
#             return "0"
#
#     def set_value(self, value):
#         module.setIniValue(module.stat.ini_filename, "JOINT_" + str(self.joint_id), "BACKLASH", "0.000", value)


# 轴螺距误差补偿启动设置
class JointNumPitchCompSetting(module.DataNode):
    def __init__(self, num):
        self.joint_id = num
        index = str(313600 + self.joint_id)
        joint_name = "joint_" + str(num) + "_pitch_comp_setting"
        super().__init__(index, joint_name, "VARIABLE")

    def value(self):
        module.config.read(module.stat.ini_filename, encoding='utf-8')
        if module.config.has_option("JOINT_" + str(self.joint_id), "COMP_FILE") and module.config.has_option(
                "JOINT_" + str(self.joint_id), "COMP_FILE_TYPE"):
            return "1"
        else:
            return "0"

    def set_value(self, value):
        module.setIniValue(module.stat.ini_filename, "JOINT_" + str(self.joint_id), "COMP_FILE",
                           "axis" + str(self.joint_id + 1) + "_pitch_comp.extension", value)


# 当前指令位置
class CmdPos(module.DataNode):
    def __init__(self, name):
        self.axis_id = module.axis[name]
        self.axis = name
        index = str(313700 + self.axis_id)
        axis_name = name + '_CmdPos'
        super().__init__(index, axis_name, "VARIABLE")

    def value(self):
        findSt = ['x', 'y', 'z', 'f']
        module.stat.poll()
        line = module.CmdLine
        if (str(line) == ''):
            return '0'
        line = line.lower()
        begin = str(line).find(self.axis)
        line = str(line)[begin:]
        if (begin == -1):
            return '0'
        for t in findSt:
            if (str(t) != str(self.axis).lower()):
                ps = str(line).find(t)
                if (ps != -1):
                    end = ps
                    break
        newbegin = str(line).find(self.axis)
        strline = str(line)[newbegin + 1: end]
        return str(strline.rstrip())


# 轴加速度
class AxisAcceleration(module.DataNode):
    def __init__(self, num):
        self.accId = num
        index = str(313800 + self.accId)
        axis_name = '_Acceleration_' + index
        super().__init__(index, axis_name, "VARIABLE")

    def value(self):
        # st = 'acc_{0}'.format(self.accId)
        st = config.halpin_axis_acc.format(self.accId)
        accel = hal.get_value(st)
        accel_val = round(accel, 3)
        return str(accel_val)


# 轴补偿文件类型
class JointNumPitchCompType(module.DataNode):
    def __init__(self, num):
        self.joint_id = num
        index = str(313900 + self.joint_id)
        joint_name = "joint_" + str(num) + "_pitch_comp_type"
        super().__init__(index, joint_name, "VARIABLE")

    def value(self):
        module.config.read(module.stat.ini_filename, encoding='utf-8')
        if module.config.has_option("JOINT_" + str(self.joint_id), "COMP_FILE_TYPE"):
            return "1"
        else:
            return "0"

    def set_value(self, value):
        module.setIniValue(module.stat.ini_filename, "JOINT_" + str(self.joint_id), "COMP_FILE_TYPE", value)


# 轴-手动最大快速速度
class AxisLetterJogSpeedRapidMax(module.DataNode):
    def __init__(self, joint_id: int):
        self.joint_id = joint_id
        axis_name, axis_id = module.get_axis_id(joint_id)
        self.axis_id = axis_id
        self.axis_name = axis_name

        index = str(314000 + self.joint_id)
        axis_name = self.axis_name + "_jog_speed_rapid_max"
        super().__init__(index, axis_name, "VARIABLE")

    def value(self):
        return str(module.inifile.find("AXIS_" + str(self.axis_name).upper(), "JOGSPEED_RAPID_MAX"))

    def set_value(self, value):
        print("AXIS_" + str(self.axis_name).upper())
        module.setIniValue(module.stat.ini_filename, "AXIS_" + str(self.axis_name).upper(), "JOGSPEED_RAPID_MAX", value)


# 轴-手动最大进给速度
class AxisLetterJogSpeedFeedMax(module.DataNode):
    def __init__(self, joint_id: int):
        """
        :param joint_id: 关节号
        """
        self.joint_id = joint_id
        axis_name, axis_id = module.get_axis_id(joint_id)
        self.axis_id = axis_id
        self.axis_name = axis_name

        index = str(314100 + self.joint_id)
        axis_name = self.axis_name + "_jog_speed_feed_max"
        super().__init__(index, axis_name, "VARIABLE")

    def value(self):
        return str(module.inifile.find("AXIS_" + str(self.axis_name).upper(), "JOGSPEED_FEED_MAX"))

    def set_value(self, value):
        print("axis" + str(self.axis_name))
        module.setIniValue(module.stat.ini_filename, "AXIS_" + str(self.axis_name).upper(), "JOGSPEED_FEED_MAX", value)


# 轴诊断-轴信息-扭矩
class AxisInfos_Torque(module.DataNode):
    def __init__(self, num):
        self.num = num
        index = str(315000 + self.num)
        type_index = config.halpin_type_1.split(' ')
        if (num == 99):
            self._halPin = config.halpin_torque.replace("*", str(type_index[len(type_index) - 1]))
        elif (num <= len(type_index) - 1):
            self._halPin = config.halpin_torque.replace("*", str(type_index[self.num]))
        super().__init__(index, '_Torque_' + index, "VARIABLE")

    def value(self):
        try:
            val = hal.get_value(self._halPin)
            stVal = str('{:.3f}'.format(val))
            if (stVal == "-0.000"):
                stVal = '0.000'
        except:
            return str('{:.3f}'.format(0.000))
        return str(stVal)

# 轴诊断-轴信息-轴补偿值(速度)
class AxisInfos_Backlash_Vel(module.DataNode):
    def __init__(self, num):
        self.num = num
        index = str(315100 + self.num)
        type_index = config.halpin_type_2.split(' ')
        if (num == 99):
            self._halPin = config.halpin_backlash_vel.replace("*", str(type_index[len(type_index) - 1]))
        elif (num <= len(type_index) - 1):
            self._halPin = config.halpin_backlash_vel.replace("*", str(type_index[self.num]))
        super().__init__(index, '_Backlash_Vel_' + index, "VARIABLE")

    def value(self):
        try:
            val = hal.get_value(self._halPin)
            stVal = str('{:.3f}'.format(val))
            if (stVal == "-0.000"):
                stVal = '0.000'
        except:
            return str('{:.3f}'.format(0.000))
        return str(stVal)

# 轴诊断-轴信息-轴补偿值(差值)
class AxisInfos_Backlash_Filt(module.DataNode):
    def __init__(self, num):
        self.num = num
        index = str(315200 + self.num)
        type_index = config.halpin_type_2.split(' ')
        if (num == 99):
            self._halPin = config.halpin_backlash_filt.replace("*", str(type_index[len(type_index) - 1]))
        elif (num <= len(type_index) - 1):
            self._halPin = config.halpin_backlash_filt.replace("*", str(type_index[self.num]))
        super().__init__(index, '_Backlash_Filt_' + index, "VARIABLE")

    def value(self):
        try:
            val = hal.get_value(self._halPin)
            stVal = str('{:.3f}'.format(val))
            if (stVal == "-0.000"):
                stVal = '0.000'
        except:
            return str('{:.3f}'.format(0.000))
        return str(stVal)

# 轴诊断-轴信息-轴补偿值(原始值)
class AxisInfos_Backlash_Corr(module.DataNode):
    def __init__(self, num):
        self.num = num
        index = str(315300 + self.num)
        type_index = config.halpin_type_2.split(' ')
        if (num == 99):
            self._halPin = config.halpin_backlash_cor.replace("*", str(type_index[len(type_index) - 1]))
        elif (num <= len(type_index) - 1):
            self._halPin = config.halpin_backlash_cor.replace("*", str(type_index[self.num]))
        super().__init__(index, '_Backlash_Corr_' + index, "VARIABLE")

    def value(self):
        try:
            val = hal.get_value(self._halPin)
            stVal = str('{:.3f}'.format(val))
            if (stVal == "-0.000"):
                stVal = '0.000'
        except:
            return str('{:.3f}'.format(0.000))
        return str(stVal)

# 轴诊断-轴信息-轴跟踪误差(最大值)
class AxisInfos_Err_MaxLimit(module.DataNode):
    def __init__(self, num):
        self.num = num
        index = str(315400 + self.num)
        type_index = config.halpin_type_2.split(' ')
        if (num == 99):
            self._halPin = config.halpin_follow_error.replace("*", str(type_index[len(type_index) - 1]))
        elif (num <= len(type_index) - 1):
            self._halPin = config.halpin_follow_error.replace("*", str(type_index[self.num]))
        super().__init__(index, '_Err_MaxLimit_' + index, "VARIABLE")

    def value(self):
        try:
            val = hal.get_value(self._halPin)
            stVal = str('{:.3f}'.format(val))
            if (stVal == "-0.000"):
                stVal = '0.000'
        except:
            return str('{:.3f}'.format(0.000))
        return str(stVal)

# 轴诊断-轴信息-轴跟踪误差(最小值)
class AxisInfos_Err_MinLimit(module.DataNode):
    def __init__(self, num):
        self.num = num
        index = str(315500 + self.num)
        type_index = config.halpin_type_2.split(' ')
        if (num == 99):
            self._halPin = config.halpin_follow_limit.replace("*", str(type_index[len(type_index) - 1]))
        elif (num <= len(type_index) - 1):
            self._halPin = config.halpin_follow_limit.replace("*", str(type_index[self.num]))
        super().__init__(index, '_Err_MinLimit_' + index, "VARIABLE")

    def value(self):
        try:
            val = hal.get_value(self._halPin)
            stVal = str('{:.3f}'.format(val))
            if (stVal == "-0.000"):
                stVal = '0.000'
        except:
            return str('{:.3f}'.format(0.000))
        return str(stVal)

# 轴诊断-轴信息-目标位置
class AxisInfos_TarPos(module.DataNode):
    def __init__(self, num):
        self.num = num
        index = str(315600 + self.num)
        type_index = config.halpin_type_1.split(' ')
        if (num == 99):
            self._halPin = config.halpin_target_position.replace("*", str(type_index[len(type_index) - 1]))
        elif (num <= len(type_index) - 1):
            self._halPin = config.halpin_target_position.replace("*", str(type_index[self.num]))
        super().__init__(index, '_TarPos_' + index, "VARIABLE")

    def value(self):
        try:
            val = hal.get_value(self._halPin)
            stVal = str('{:.3f}'.format(val))
            if (stVal == "-0.000"):
                stVal = '0.000'
        except:
            return str('{:.3f}'.format(0.000))
        return str(stVal)

# 轴诊断-轴信息-反馈位置
class AxisInfos_ActPos(module.DataNode):
    def __init__(self, num):
        self.num = num
        index = str(315700 + self.num)
        type_index = config.halpin_type_1.split(' ')
        if (num == 99):
            self._halPin = config.halpin_act_position.replace("*", str(type_index[len(type_index) - 1]))
        elif (num <= len(type_index) - 1):
            self._halPin = config.halpin_act_position.replace("*", str(type_index[self.num]))
        super().__init__(index, '_ActPos_' + index, "VARIABLE")

    def value(self):
        try:
            val = hal.get_value(self._halPin)
            stVal = str('{:.3f}'.format(val))
            if (stVal == "-0.000"):
                stVal = '0.000'
        except:
            return str('{:.3f}'.format(0.000))
        return str(stVal)

# 轴诊断-轴信息-目标速度
class AxisInfos_TarVel(module.DataNode):
    def __init__(self, num):
        self.num = num
        index = str(315800 + self.num)
        type_index = config.halpin_type_1.split(' ')
        if (num == 99):
            self._halPin = config.halpin_target_velocity.replace("*", str(type_index[len(type_index) - 1]))
        elif (num <= len(type_index) - 1):
            self._halPin = config.halpin_target_velocity.replace("*", str(type_index[self.num]))
        super().__init__(index, '_TarVel_' + index, "VARIABLE")

    def value(self):
        try:
            val = hal.get_value(self._halPin)
            stVal = str('{:.3f}'.format(val))
            if (stVal == "-0.000"):
                stVal = '0.000'
        except:
            return str('{:.3f}'.format(0.000))
        return str(stVal)

# 轴诊断-轴信息-反馈速度
class AxisInfos_ActVel(module.DataNode):
    def __init__(self, num):
        self.num = num
        index = str(315900 + self.num)
        type_index = config.halpin_type_1.split(' ')
        if (num == 99):
            self._halPin = config.halpin_act_velocity.replace("*", str(type_index[len(type_index) - 1]))
        elif (num <= len(type_index) - 1):
            self._halPin = config.halpin_act_velocity.replace("*", str(type_index[self.num]))
        super().__init__(index, '_ActVel_' + index, "VARIABLE")

    def value(self):
        try:
            val = hal.get_value(self._halPin)
            stVal = str('{:.3f}'.format(val))
            if (stVal == "-0.000"):
                stVal = '0.000'
        except:
            return str('{:.3f}'.format(0.000))
        return str(stVal)

# 主轴-最小正向转速
class SpindleNumMinForwardVelocity(module.DataNode):
    def __init__(self, num):
        self.spindle_id = num
        index = str(316000 + self.spindle_id)
        spindle_name = "spindle_" + str(num) + "_min_forward_vel"
        super().__init__(index, spindle_name, "VARIABLE")

    def value(self):
        return str(module.inifile.find("SPINDLE_" + str(self.spindle_id), "MIN_FORWARD_VELOCITY"))

    def set_value(self, value):
        module.setIniValue(module.stat.ini_filename, "SPINDLE_" + str(self.spindle_id), "MIN_FORWARD_VELOCITY", value)


# 主轴-最小反向转速
class SpindleNumMinReverseVelocity(module.DataNode):
    def __init__(self, num):
        self.spindle_id = num
        index = str(316100 + self.spindle_id)
        spindle_name = "spindle_" + str(num) + "_min_reverse_vel"
        super().__init__(index, spindle_name, "VARIABLE")

    def value(self):
        return str(module.inifile.find("SPINDLE_" + str(self.spindle_id), "MIN_REVERSE_VELOCITY"))

    def set_value(self, value):
        module.setIniValue(module.stat.ini_filename, "SPINDLE_" + str(self.spindle_id), "MIN_REVERSE_VELOCITY", value)


# 主轴-PID-P
class SpindlePID_P(module.DataNode):
    def __init__(self, num):
        self.spindle_id = num

        index = str(316300 + self.spindle_id)
        spindle_name = "spindle_" + str(num) + "_pid_p"
        super().__init__(index, spindle_name, "VARIABLE")

    def value(self):
        return str(module.inifile.find("SP_0_PID", "Pgain"))

    def set_value(self, value):
        module.setIniValue(module.stat.ini_filename, "SP_0_PID", "Pgain", str(value))


# 主轴-PID-I
class SpindlePID_I(module.DataNode):
    def __init__(self, num):
        self.spindle_id = num

        index = str(316400 + self.spindle_id)
        spindle_name = "spindle_" + str(num) + "_pid_i"
        super().__init__(index, spindle_name, "VARIABLE")

    def value(self):
        return str(module.inifile.find("SP_0_PID", "Igain"))

    def set_value(self, value):
        module.setIniValue(module.stat.ini_filename, "SP_0_PID", "Igain", str(value))


# 主轴-PID-D
class SpindlePID_D(module.DataNode):
    def __init__(self, num):
        self.spindle_id = num

        index = str(316500 + self.spindle_id)
        spindle_name = "spindle_" + str(num) + "_pid_d"
        super().__init__(index, spindle_name, "VARIABLE")

    def value(self):
        return str(module.inifile.find("SP_0_PID", "Dgain"))

    def set_value(self, value):
        module.setIniValue(module.stat.ini_filename, "SP_0_PID", "Dgain", str(value))


# 轴编码器每转线数
class AxisEncoderLRP(module.DataNode):
    def __init__(self, joint_id):
        self.joint_id = joint_id
        self.axis_name, self.axis_id = module.get_axis_id(joint_id)
        self.option = "gear_" + self.axis_name

        index = str(316600 + self.joint_id)
        spindle_name = "axis_encoder_lrp_" + str(joint_id)
        super().__init__(index, spindle_name, "VARIABLE")

    def value(self):
        return str(module.inifile.find(self.option, "LPR"))

    def set_value(self, value):
        module.setIniValue(module.stat.ini_filename, self.option, "LPR", str(value))


# 轴电子齿轮比分子
class AxisGearMolecule(module.DataNode):
    def __init__(self, joint_id):
        self.joint_id = joint_id
        self.axis_name, self.axis_id = module.get_axis_id(joint_id)
        self.option = "gear_" + self.axis_name

        index = str(316700 + self.joint_id)
        spindle_name = "axis_gear_molecule_" + str(joint_id)
        super().__init__(index, spindle_name, "VARIABLE")

    def value(self):
        return str(module.inifile.find(self.option, "numerator"))

    def set_value(self, value):
        module.setIniValue(module.stat.ini_filename, self.option, "numerator", str(value))


# 轴电子齿轮比分母
class AxisGeaDeniminator(module.DataNode):
    def __init__(self, joint_id):
        self.joint_id = joint_id
        self.axis_name, self.axis_id = module.get_axis_id(joint_id)
        self.option = "gear_" + self.axis_name

        index = str(316800 + self.joint_id)
        spindle_name = "axis_gear_deniminator_" + str(joint_id)
        super().__init__(index, spindle_name, "VARIABLE")

    def value(self):
        return str(module.inifile.find(self.option, "denominator"))

    def set_value(self, value):
        if value == "0":
            return
        module.setIniValue(module.stat.ini_filename, self.option, "denominator", str(value))


# 轴丝杆螺距
class AxisFlightLead(module.DataNode):
    def __init__(self, joint_id):
        self.joint_id = joint_id
        self.axis_name, self.axis_id = module.get_axis_id(joint_id)
        self.option = "gear_" + self.axis_name

        index = str(316900 + self.joint_id)
        spindle_name = "axis_flight_lead_" + str(joint_id)
        super().__init__(index, spindle_name, "VARIABLE")

    def value(self):
        return str(module.inifile.find(self.option, "flightLead"))

    def set_value(self, value):
        module.setIniValue(module.stat.ini_filename, self.option, "flightLead", str(value))


# 轴诊断—伺服准备好
class AxisReadyToSwitchOn(module.DataNode):
    def __init__(self, id):
        self.id = int(id)
        pin_name = config.axis_ready_to_switch_on
        if id == str(6):  # 刀库轴
            self.pin = pin_name.replace("*", "tool")
        else:
            self.pin = pin_name.replace("*", id)

        index = str(317000 + int(self.id))
        name = "axis_" + str(diagnosis_axis[self.id]) + "_ready_to_switch_on"
        super().__init__(index, name, "VARIABLE")

    def value(self):
        value = hal.get_value(self.pin)
        if value:
            return "1"
        else:
            return "0"


# 轴诊断—可以开启伺服运行
class AxisSwitchOn(module.DataNode):
    def __init__(self, id):
        self.id = int(id)
        pin_name = config.axis_switch_on
        if id == str(6):  # 刀库轴
            self.pin = pin_name.replace("*", "tool")
        else:
            self.pin = pin_name.replace("*", id)

        index = str(317100 + self.id)
        name = "axis_" + str(diagnosis_axis[self.id]) + "_switch_on"
        super().__init__(index, name, "VARIABLE")

    def value(self):
        value = hal.get_value(self.pin)
        if value:
            return "1"
        else:
            return "0"


# 轴诊断—伺服运行
class AxisOperationEnabled(module.DataNode):
    def __init__(self, id):
        self.id = int(id)
        pin_name = config.axis_operation_enabled
        if id == str(6):  # 刀库轴
            self.pin = pin_name.replace("*", "tool")
        else:
            self.pin = pin_name.replace("*", id)

        index = str(317200 + self.id)
        name = "axis_" + str(diagnosis_axis[self.id]) + "_operation_enabled"
        super().__init__(index, name, "VARIABLE")

    def value(self):
        value = hal.get_value(self.pin)
        if value:
            return "1"
        else:
            return "0"


# 轴诊断—故障
class AxisFault(module.DataNode):
    def __init__(self, id):
        self.id = int(id)
        pin_name = config.axis_fault
        if id == str(6):  # 刀库轴
            self.pin = pin_name.replace("*", "tool")
        else:
            self.pin = pin_name.replace("*", id)

        index = str(317300 + self.id)
        name = "axis_" + str(diagnosis_axis[self.id]) + "_fault"
        super().__init__(index, name, "VARIABLE")

    def value(self):
        value = hal.get_value(self.pin)
        if value:
            return "1"
        else:
            return "0"


# 轴诊断—主回路电接通
class AxisVoltageEnabled(module.DataNode):
    def __init__(self, id):
        self.id = int(id)
        pin_name = config.axis_voltage_enabled
        if id == str(6):  # 刀库轴
            self.pin = pin_name.replace("*", "tool")
        else:
            self.pin = pin_name.replace("*", id)

        index = str(317400 + self.id)
        name = "axis_" + str(diagnosis_axis[self.id]) + "_voltage_enabled"
        super().__init__(index, name, "VARIABLE")

    def value(self):
        value = hal.get_value(self.pin)
        if value:
            return "1"
        else:
            return "0"


# 轴诊断—快速停机
class AxisQuickStop(module.DataNode):
    def __init__(self, id):
        self.id = int(id)
        pin_name = config.axis_quick_stop
        if id == str(6):  # 刀库轴
            self.pin = pin_name.replace("*", "tool")
        else:
            self.pin = pin_name.replace("*", id)

        index = str(317500 + self.id)
        name = "axis_" + str(diagnosis_axis[self.id]) + "_quick_stop"
        super().__init__(index, name, "VARIABLE")

    def value(self):
        value = hal.get_value(self.pin)
        if value:
            return "1"
        else:
            return "0"


# 轴诊断—伺服不可运行
class AxisSwitchOnDisabled(module.DataNode):
    def __init__(self, id):
        self.id = int(id)
        pin_name = config.axis_switch_on_disabled
        if id == str(6):  # 刀库轴
            self.pin = pin_name.replace("*", "tool")
        else:
            self.pin = pin_name.replace("*", id)

        index = str(317600 + self.id)
        name = "axis_" + str(diagnosis_axis[self.id]) + "_switch_on_disabled"
        super().__init__(index, name, "VARIABLE")

    def value(self):
        value = hal.get_value(self.pin)
        if value:
            return "1"
        else:
            return "0"


# 轴诊断—警告
class AxisWarning(module.DataNode):
    def __init__(self, id):
        self.id = int(id)
        pin_name = config.axis_warning
        if id == str(6):  # 刀库轴
            self.pin = pin_name.replace("*", "tool")
        else:
            self.pin = pin_name.replace("*", id)

        index = str(317700 + self.id)
        name = "axis_" + str(diagnosis_axis[self.id]) + "_warning"
        super().__init__(index, name, "VARIABLE")

    def value(self):
        value = hal.get_value(self.pin)
        if value:
            return "1"
        else:
            return "0"


# 轴诊断—远程控制
class AxisRemote(module.DataNode):
    def __init__(self, id):
        self.id = int(id)
        pin_name = config.axis_remote
        if id == str(6):  # 刀库轴
            self.pin = pin_name.replace("*", "tool")
        else:
            self.pin = pin_name.replace("*", id)

        index = str(317900 + self.id)
        name = "axis_" + str(diagnosis_axis[self.id]) + "_remote"
        super().__init__(index, name, "VARIABLE")

    def value(self):
        value = hal.get_value(self.pin)
        if value:
            return "1"
        else:
            return "0"


# 轴诊断—目标直达
class AxisTargetReach(module.DataNode):
    def __init__(self, id):
        self.id = int(id)
        pin_name = config.axis_target_reach
        if id == str(6):  # 刀库轴
            self.pin = pin_name.replace("*", "tool")
        else:
            self.pin = pin_name.replace("*", id)

        index = str(318000 + self.id)
        name = "axis_" + str(diagnosis_axis[self.id]) + "_target_reach"
        super().__init__(index, name, "VARIABLE")

    def value(self):
        value = hal.get_value(self.pin)
        if value:
            return "1"
        else:
            return "0"


# 轴诊断—内部位置超限
class AxisInternalLimitActive(module.DataNode):
    def __init__(self, id):
        self.id = int(id)
        pin_name = config.axis_internal_limit_active
        if id == str(6):  # 刀库轴
            self.pin = pin_name.replace("*", "tool")
        else:
            self.pin = pin_name.replace("*", id)

        index = str(318100 + self.id)
        name = "axis_" + str(diagnosis_axis[self.id]) + "_internal_limit_active"
        super().__init__(index, name, "VARIABLE")

    def value(self):
        value = hal.get_value(self.pin)
        if value:
            return "1"
        else:
            return "0"


# 轴诊断—目标位置更新
class AxisSetPointAcknowledge(module.DataNode):
    def __init__(self, id):
        self.id = int(id)
        pin_name = config.axis_set_point_acknowledge
        if id == str(6):  # 刀库轴
            self.pin = pin_name.replace("*", "tool")
        else:
            self.pin = pin_name.replace("*", id)

        index = str(318200 + self.id)
        name = "axis_" + str(diagnosis_axis[self.id]) + "_set_point_acknowledge"
        super().__init__(index, name, "VARIABLE")

    def value(self):
        value = hal.get_value(self.pin)
        if value:
            return "1"
        else:
            return "0"


# 轴诊断—跟随误差
class AxisFollowingError(module.DataNode):
    def __init__(self, id):
        self.id = int(id)
        pin_name = config.axis_following_error
        if id == str(6):  # 刀库轴
            self.pin = pin_name.replace("*", "tool")
        else:
            self.pin = pin_name.replace("*", id)

        index = str(318300 + self.id)
        name = "axis_" + str(diagnosis_axis[self.id]) + "_following_error"
        super().__init__(index, name, "VARIABLE")

    def value(self):
        value = hal.get_value(self.pin)
        if value:
            return "1"
        else:
            return "0"


# 轴诊断—扭矩限制激活
class AxisTorqueLimitActive(module.DataNode):
    def __init__(self, id):
        self.id = int(id)
        pin_name = config.axis_torque_limit_active
        if id == str(6):  # 刀库轴
            self.pin = pin_name.replace("*", "tool")
        else:
            self.pin = pin_name.replace("*", id)

        index = str(318400 + self.id)
        name = "axis_" + str(diagnosis_axis[self.id]) + "_torque_limit_active"
        super().__init__(index, name, "VARIABLE")

    def value(self):
        value = hal.get_value(self.pin)
        if value:
            return "1"
        else:
            return "0"


# 轴诊断—原点已找到
class AxisHomeFind(module.DataNode):
    def __init__(self, id):
        self.id = int(id)
        pin_name = config.axis_home_find
        if id == str(6):   # 刀库轴
            self.pin = pin_name.replace("*", "tool")
        else:
            self.pin = pin_name.replace("*", id)

        index = str(318500 + self.id)
        name = "axis_" + str(diagnosis_axis[self.id]) + "_home_find"
        super().__init__(index, name, "VARIABLE")

    def value(self):
        value = hal.get_value(self.pin)
        if value:
            return "1"
        else:
            return "0"


# 轴运动方向
class AxisMotionDir(module.DataNode):
    def __init__(self, joint_id):
        self.joint_id = joint_id
        self.axis_name, self.axis_id = module.get_axis_id(joint_id)
        self.option = "gear_" + self.axis_name

        index = str(318600 + self.joint_id)
        spindle_name = "axis_motion_dir_" + str(joint_id)
        super().__init__(index, spindle_name, "VARIABLE")

    def value(self):
        return str(module.inifile.find(self.option, "ax-motion-dir"))

    def set_value(self, value):
        module.setIniValue(module.stat.ini_filename, self.option, "ax-motion-dir", str(value))


# 主轴点动进给最大速度
class SpindleJogSpeedFeedMax(module.DataNode):
    def __init__(self, num):
        self.spindle_id = num
        self.section = "SPINDLE_" + str(self.spindle_id)

        index = str(318700 + self.spindle_id)
        spindle_name = "spindle_" + str(self.spindle_id) + "_jogSpeed_feed_max"
        super().__init__(index, spindle_name, "VARIABLE")

    def value(self):
        return str(module.inifile.find(self.section, "JOGSPEED_FEED_MAX"))

    def set_value(self, value):
        module.setIniValue(module.stat.ini_filename, self.section, "JOGSPEED_FEED_MAX", str(value))


# 主轴点动快速最大速度
class SpindleJogSpeedRapidMax(module.DataNode):
    def __init__(self, num):
        self.spindle_id = num
        self.section = "SPINDLE_" + str(self.spindle_id)

        index = str(318800 + self.spindle_id)
        spindle_name = "spindle_" + str(self.spindle_id) + "_jogSpeed_rapid_max"
        super().__init__(index, spindle_name, "VARIABLE")

    def value(self):
        return str(module.inifile.find(self.section, "JOGSPEED_RAPID_MAX"))

    def set_value(self, value):
        module.setIniValue(module.stat.ini_filename, self.section, "JOGSPEED_RAPID_MAX", str(value))


# 刀库轴点动快速最大速度
class ToolJogSpeedRapidMax(module.DataNode):
    def __init__(self):
        super().__init__("318900", "ToolJogSpeedRapidMax", "VARIABLE")

    def value(self):
        return str(module.inifile.find("JOINT_9", "JOGSPEED_RAPID_MAX"))

    def set_value(self, value):
        module.setIniValue(module.stat.ini_filename, "JOINT_9", "JOGSPEED_RAPID_MAX",
                           value)


# 刀库轴点动进给最大速度
class ToolJogSpeedFeedMax(module.DataNode):
    def __init__(self):
        super().__init__("318901", "ToolJogSpeedFeedMax", "VARIABLE")

    def value(self):
        return str(module.inifile.find("JOINT_9", "JOGSPEED_FEED_MAX"))

    def set_value(self, value):
        module.setIniValue(module.stat.ini_filename, "JOINT_9", "JOGSPEED_FEED_MAX",
                           value)


# 手轮加速度比例系数
class JogAccelFraction(module.DataNode):
    def __init__(self, num):
        self.joint_id = num
        self.section = "JOINT_" + str(self.joint_id)

        index = str(319000 + self.joint_id)
        name = "joint_" + str(self.joint_id) + "_jog_accel_fraction"
        super().__init__(index, name, "VARIABLE")

    def value(self):
        return str(module.inifile.find(self.section, "JOG_ACCEL_FRACTION"))

    def set_value(self, value):
        module.setIniValue(module.stat.ini_filename, self.section, "JOG_ACCEL_FRACTION", str(value))


# 主轴的轴机械传动比分母
class SpindleTransmissionDenominator(module.DataNode):
    def __init__(self):
        super().__init__("319100", "SpindleTransmissionDenominator", "VARIABLE")

    def value(self):
        return str(module.inifile.find("gear_U", "denominator"))

    def set_value(self, value):
        module.setIniValue(module.stat.ini_filename, "gear_U", "denominator",
                           value)


# 主轴的丝杆螺距
class SpindleScrewPitch(module.DataNode):
    def __init__(self):
        super().__init__("319101", "SpindleScrewPitch", "VARIABLE")

    def value(self):
        return str(module.inifile.find("gear_U", "flightLead"))

    def set_value(self, value):
        module.setIniValue(module.stat.ini_filename, "gear_U", "flightLead",
                           value)


# 主轴的轴机械传动比分子
class SpindleTransmissionNumerator(module.DataNode):
    def __init__(self):
        super().__init__("319102", "SpindleTransmissionNumerator", "VARIABLE")

    def value(self):
        return str(module.inifile.find("gear_U", "numerator"))

    def set_value(self, value):
        module.setIniValue(module.stat.ini_filename, "gear_U", "numerator",
                           value)


# 主轴的线转数
class SpindleLineRevolutionCounts(module.DataNode):
    def __init__(self):
        super().__init__("319103", "SpindleLineRevolutionCounts", "VARIABLE")

    def value(self):
        return str(module.inifile.find("gear_U", "LPR"))

    def set_value(self, value):
        module.setIniValue(module.stat.ini_filename, "gear_U", "LPR",
                           value)


# 主轴的运动方向
class SpindleMotionOrientation(module.DataNode):
    def __init__(self):
        super().__init__("319104", "SpindleMotionOrientation", "VARIABLE")

    def value(self):
        return str(module.inifile.find("gear_U", "ax-motion-dir"))

    def set_value(self, value):
        module.setIniValue(module.stat.ini_filename, "gear_U", "ax-motion-dir",
                           value)


# 主轴速度模式下齿轮比
class SpindleVelocityModeGearRatio(module.DataNode):
    def __init__(self):
        super().__init__("319105", "SpindleVelocityModeGearRatio", "VARIABLE")

    def value(self):
        return str(module.inifile.find("gear_U", "fScale"))

    def set_value(self, value):
        module.setIniValue(module.stat.ini_filename, "gear_U", "fScale",
                           value)


# 主轴速度模式下运动方向
class SpindleVelocityModeMotionOrientation(module.DataNode):
    def __init__(self):
        super().__init__("319106", "SpindleVelocityModeMotionOrientation", "VARIABLE")

    def value(self):
        return str(module.inifile.find("gear_U", "fdir"))

    def set_value(self, value):
        module.setIniValue(module.stat.ini_filename, "gear_U", "fdir",
                           value)