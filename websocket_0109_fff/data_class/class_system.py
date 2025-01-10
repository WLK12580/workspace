import time

from data_class import nc_module as module
import hal
import config
from task_process_timer import thread_process_timer as process_timer
from task_mdi import thread_detect_mdi as thread_detect_mdi

component = config.component
h = hal.component(component)


axis = {"x": 0, "y": 1, "z": 2,
        "a": 3, "b": 4, "c": 5,
        "u": 6, "v": 7, "w": 8}




# 系统运行模式
class TaskMode(module.DataNode):
    def __init__(self):
        super().__init__("100000", "TaskMode", "VARIABLE")

    def value(self):
        # if hal.get_value("classicladder.0.out-135"):
        #     return "Jog"
        if module.stat.task_mode == 1:
            return "Jog"
        elif module.stat.task_mode == 2:
            return "Auto"
        elif module.stat.task_mode == 3:
            return "Mdi"

    def set_value(self, value):
        print("set task mode" + value)


# 当前坐标系
class CurrentCoordinate(module.DataNode):
    def __init__(self):
        super().__init__("100001", "CurrentCoordinate", "VARIABLE")

    def value(self):
        index = 53 + module.stat.g5x_index
        return "G" + str(index)


# 主轴0-模式状态  （主轴1：100034）
class SP0ModeStatus(module.DataNode):
    def __init__(self):
        super().__init__("100007", "SP0ModeStatus", "VARIABLE")

    def value(self):
        status = hal.get_value(config.halpin_sp0_mode_status)
        if status == 1:
            return "position"
        elif status == 2:
            return "velocity"
        elif status == 3:
            return "homing"
        else:
            return "none"


# 单段模式
class SingleBlockStatus(module.DataNode):
    def __init__(self):
        super().__init__("100008", "SingleBlockStatus", "VARIABLE")

    def value(self):
        if hal.get_value(config.halpin_single_block_status):
            return "1"
        return "0"


# 主轴旋转方向
class SpindleOrientation(module.DataNode):
    def __init__(self):
        super().__init__("100009", "SpindleOrientation", "VARIABLE")

    def value(self):
        if hal.get_value("spindle.0.on") == 0:
            return "brake"
        if hal.get_value("spindle.0.reverse"):
            return "backward"
        if hal.get_value("spindle.0.forward"):
            return "forward"


# G95
class G95_Code(module.DataNode):
    def __init__(self):
        super().__init__("100010", "G95_Code", "VARIABLE")

    def value(self):
        for g_Code in module.stat.gcodes:
            if(str(g_Code)[:2]  == "95"):
                return "1"
        return "0"


# GCode_Effect
class GCode_Effect(module.DataNode):
    def __init__(self):
        super().__init__("100011", "GCode_Effect", "VARIABLE")

    def value(self):
        G_Code = []
        for g_Code in module.stat.gcodes:
            if g_Code != -1 and list(module.stat.gcodes).index(g_Code) != 0:
                if(len(str(g_Code)) > 2):
                    if(str(g_Code)[2] == '0'):
                        G_Code.append(str('G') + str(g_Code)[:2])
                        continue
                    else:
                        G_Code.append(str('G') + str(g_Code)[:2] + "." + str(g_Code)[2])
                        continue
                else:
                    if(len(str(g_Code)) == 1):
                        G_Code.append(str('G') + str(g_Code)[:1])
                        continue
                    if(str(g_Code)[1] == '0'):
                        G_Code.append(str('G') + str(g_Code)[:1])
                        continue
                    else:
                        G_Code.append(str('G') + str(g_Code)[:2])
                        continue
        return str(' '.join(G_Code))


# G21
class G21_Code(module.DataNode):
    def __init__(self):
        super().__init__("100012", "G21_Code", "VARIABLE")

    def value(self):
        for g_Code in module.stat.gcodes:
            if(str(g_Code)[:2]  == "21"):
                return "1"
        return "0"


# M代码生效
class MCode_Effect(module.DataNode):
    def __init__(self):
        super().__init__("100013", "MCode_Effect", "VARIABLE")

    def value(self):
        M_Code = []
        for m_Code in module.stat.mcodes:
            if m_Code != -1 and list(module.stat.mcodes).index(m_Code) != 0:
                M_Code.append(str('M') + str(m_Code)[:2])
        return str(' '.join(M_Code))


# 加工时间
class ProcessTime(module.DataNode):
    def __init__(self):
        super().__init__("100014", "ProcessTotalTime", "VARIABLE")

    def value(self):
        return str(int(process_timer.process_task.get_total_time()))


# G43生效
class G43Effect(module.DataNode):
    def __init__(self):
        super().__init__("100015", "G43Effect", "VARIABLE")

    def value(self):
        for g_Code in module.stat.gcodes:
            if str(g_Code)[:2] == "43" and list(module.stat.gcodes).index(g_Code) != 0:
                return "1"
        return "0"


#  程序执行完成
class ProgramFinished(module.DataNode):
    def __init__(self):
        super().__init__("100016", "ProgramFinished", "VARIABLE")

    def value(self):
        if process_timer.process_task.isFinished:
            return "1"
        else:
            return "0"


# G41生效
class G41G42Effect(module.DataNode):
    def __init__(self):
        super().__init__("100017", "G41G42Effect", "VARIABLE")

    def value(self):
        for g_Code in module.stat.gcodes:
            if str(g_Code)[:2] == "41" and list(module.stat.gcodes).index(g_Code) != 0:
                return "left"
            elif str(g_Code)[:2] == "42" and list(module.stat.gcodes).index(g_Code) != 0:
                return "right"
        return "false"


# T生效
class TEffect(module.DataNode):
    def __init__(self):
        super().__init__("100018", "TEffect", "VARIABLE")

    def value(self):
        return str(hal.get_value("iocontrol.0.tool-prep-number"))


#  程序运行状态
class ProcessTaskStatus(module.DataNode):

    def __init__(self):
        super().__init__("100019", "ProcessTaskStatus", "VARIABLE")

    def value(self):
        if process_timer.process_task.get_current_state() == process_timer.process_exec:
            return str("running")
        elif process_timer.process_task.get_current_state() == process_timer.process_pause:
            return str("pause")
        elif process_timer.process_task.get_current_state() == process_timer.process_done:
            return str("idle")
        else:
            return str("error")


# G40生效
class G40Effect(module.DataNode):
    def __init__(self):
        super().__init__("100020", "G40Effect", "VARIABLE")

    def value(self):
        for g_Code in module.stat.gcodes:
            if str(g_Code)[:2] == "40" and list(module.stat.gcodes).index(g_Code) != 0:
                return "1"
        return "0"


# G49生效
class G49Effect(module.DataNode):
    def __init__(self):
        super().__init__("100021", "G49Effect", "VARIABLE")

    def value(self):
        for g_Code in module.stat.gcodes:
            if str(g_Code)[:2] == "49" and list(module.stat.gcodes).index(g_Code) != 0:
                return "1"
        return "0"


# 当前生效的r参数
class CurrentRotationXY(module.DataNode):
    def __init__(self):
        super().__init__("100024", "CurrentRotationXY", "VARIABLE")

    def value(self):
        return str(module.stat.rotation_xy)


# 主轴使能状态
class SpindleEnableStatus(module.DataNode):
    def __init__(self):
        super().__init__("100025", "SpindleEnableStatus", "VARIABLE")

    def value(self):
        if hal.get_value(config.halpin_spindle_enable):
            return "1"
        elif config.halpin_spindle_disable:
            return "0"
        else:
            return "0"


# 进给使能状态
class FeedEnableStatus(module.DataNode):
    def __init__(self):
        super().__init__("100026", "FeedEnableStatus", "VARIABLE")

    def value(self):
        if hal.get_value(config.halpin_feed_disable):
            return "0"
        elif hal.get_value(config.halpin_feed_enable):
            return "1"
        else:
            return "0"


# 定位执行结束清空标志
class PositionFinishedFlag(module.DataNode):
    def __init__(self):
        self.counter = 0  # 计数器 加载完成后连续发5次100后清0
        super().__init__("100027", "FeedEnableStatus", "VARIABLE")

    def value(self):
        if module.position_is_exec == 1:
            self.counter += 1
            if self.counter >= 5:
                module.position_is_exec = 0
                self.counter = 0
        return str(int(module.position_is_exec))


# 工件号
class WorkpieceId(module.DataNode):
    def __init__(self):
        super().__init__("100028", "WorkpieceId", "VARIABLE")

    def value(self):
        return str(hal.get_value(config.halpin_workpiece_id))


# 加工数量
class ProcessNum(module.DataNode):
    def __init__(self):
        super().__init__("100029", "ProcessNum", "VARIABLE")

    def value(self):
        return str(hal.get_value(config.halpin_process_num))


# 跳段模式是否启动
class JumpSegmentMode(module.DataNode):
    def __init__(self):
        super().__init__("100030", "JumpSegmentMode", "VARIABLE")

    def value(self):
        if hal.get_value(config.halpin_jump_segment_flag):
            return "1"
        else:
            return "0"


# 主轴切削负载
class SpindleLoad(module.DataNode):
    def __init__(self):
        super().__init__("100031", "SpindleLoad", "VARIABLE")

    def value(self):
        return str(hal.get_value(config.halpin_spindle_load))


# 当前插补指令集-F
class FEffect(module.DataNode):
    def __init__(self):
        super().__init__("100032", "FEffect", "VARIABLE")

    def value(self):
        return str(module.stat.settings[1])


# 当前插补指令集-S
class SEffect(module.DataNode):
    def __init__(self):
        super().__init__("100033", "SEffect", "VARIABLE")

    def value(self):
        return str(module.stat.settings[2])


# 主轴1-模式状态  （主轴0：100007）
class SP1ModeStatus(module.DataNode):
    def __init__(self):
        super().__init__("100034", "SP1ModeStatus", "VARIABLE")

    def value(self):
        status = hal.get_value(config.halpin_sp1_mode_status)
        if status == 1:
            return "position"
        elif status == 2:
            return "velocity"
        elif status == 3:
            return "homing"
        else:
            return "none"


# 主轴1旋转方向
class SpindleOrientation_1(module.DataNode):
    def __init__(self):
        super().__init__("100035", "SpindleOrientation_1", "VARIABLE")

    def value(self):
        if module.stat.spindles < 2:
            return "brake"
        if hal.get_value("spindle.1.on") == 0:
            return "brake"
        if hal.get_value("spindle.1.reverse"):
            return "backward"
        if hal.get_value("spindle.1.forward"):
            return "forward"


# 多行MDI的当前执行行
class MdiCurrentLine(module.DataNode):
    def __init__(self):
        super().__init__("100036", "MdiCurrentLine", "VARIABLE")

    def value(self):
        return str(thread_detect_mdi.MdiThread.mdi_current_line())


# 当前运动类型 feed/arc
class CurrentMotionType(module.DataNode):
    def __init__(self):
        super().__init__("100038", "CurrentMotionType", "VARIABLE")

    def value(self):
        type = module.stat.motion_type
        if type == 0:
            return "stop"
        elif type == 2:
            return "feed"
        elif type == 3:
            return "arc"


# 系统中的关节数量
class KinsJoints(module.DataNode):
    def __init__(self):
        super().__init__("101000", "KinsJoints", "VARIABLE")

    def value(self):
        return str(module.stat.joints)


# 系统控制的轴名
class IPCTSCoordinates(module.DataNode):
    def __init__(self, name):
        self.axis_name = name
        self.axis_id = axis[name]
        index = str(101001 + self.axis_id)
        super().__init__(index, "IPCTSCoordinates", "NAME")

    def value(self):
        name_str = module.inifile.find("TRAJ", "COORDINATES")
        if self.axis_name.upper() in name_str:
            return "1"
        else:
            return "0"


# 系统中的主轴数量
class TrajSpindles(module.DataNode):
    def __init__(self):
        super().__init__("101010", "TrajSpindles", "VARIABLE")

    def value(self):
        return str(module.stat.spindles)

    def set_value(self, value):
        module.setIniValue(module.stat.ini_filename, "TRAJ", "SPINDLES",
                           value)


# 线性轴的机床单位
class TrajLinearUnits(module.DataNode):
    def __init__(self):
        super().__init__("101019", "TrajLinearUnits", "VARIABLE")

    def value(self):
        if module.inifile.find("TRAJ", "LINEAR_UNITS") == "mm":
            return "mm"
        elif module.inifile.find("TRAJ", "LINEAR_UNITS") == "inch":
            return "inch"

    def set_value(self, value):
        module.setIniValue(module.stat.ini_filename, "TRAJ", "LINEAR_UNITS",
                           value)


# 旋转轴的机床单位
class TrajAngularUnits(module.DataNode):
    def __init__(self):
        super().__init__("101020", "TrajAngularUnits", "VARIABLE")

    def value(self):
        if module.inifile.find("TRAJ", "ANGULAR_UNITS") == "deg":
            return "deg"
        elif module.inifile.find("TRAJ", "ANGULAR_UNITS") == "degree":
            return "degree"
        elif module.inifile.find("TRAJ", "ANGULAR_UNITS") == "rad":
            return "rad"
        elif module.inifile.find("TRAJ", "ANGULAR_UNITS") == "radian":
            return "radian"
        elif module.inifile.find("TRAJ", "ANGULAR_UNITS") == "grad":
            return "grad"
        elif module.inifile.find("TRAJ", "ANGULAR_UNITS") == "gon":
            return "gon"

    def set_value(self, value):
        module.setIniValue(module.stat.ini_filename, "TRAJ", "ANGULAR_UNITS",
                           value)


# 点动的默认初速率
class TrajDefaultLinearVelocity(module.DataNode):
    def __init__(self):
        super().__init__("101021", "TrajDefaultLinearVelocity", "VARIABLE")

    def value(self):
        return str(module.inifile.find("TRAJ", "DEFAULT_LINEAR_VELOCITY"))

    def set_value(self, value):
        module.setIniValue(module.stat.ini_filename, "TRAJ", "DEFAULT_LINEAR_VELOCITY",
                           value)


# 点动的默认加速度
class TrajDefaultLinearAcceleration(module.DataNode):
    def __init__(self):
        super().__init__("101022", "TrajDefaultLinearAcceleration", "VARIABLE")

    def value(self):
        return str(module.stat.acceleration)

    def set_value(self, value):
        module.setIniValue(module.stat.ini_filename, "TRAJ", "DEFAULT_LINEAR_ACCELERATION",
                           value)


# 任意轴的最大速度
class TrajMaxLinearVelocity(module.DataNode):
    def __init__(self):
        super().__init__("101023", "TrajMaxLinearVelocity", "VARIABLE")

    def value(self):
        return str(module.inifile.find("TRAJ", "MAX_LINEAR_VELOCITY"))

    def set_value(self, value):
        module.setIniValue(module.stat.ini_filename, "TRAJ", "MAX_LINEAR_VELOCITY",
                           value)


# 任意轴的最大加速度
class TrajMaxLinearAcceleration(module.DataNode):
    def __init__(self):
        super().__init__("101024", "TrajMaxLinearAcceleration", "VARIABLE")

    def value(self):
        return str(module.inifile.find("TRAJ", "MAX_LINEAR_ACCELERATION"))

    def set_value(self, value):
        module.setIniValue(module.stat.ini_filename, "TRAJ", "MAX_LINEAR_ACCELERATION",
                           value)


# 强制回参考点
class TrajNoForceHoming(module.DataNode):
    def __init__(self):
        super().__init__("101025", "TrajNoForceHoming", "VARIABLE")

    def value(self):
        return str(module.inifile.find("TRAJ", "NO_FORCE_HOMING"))

    def set_value(self, value):
        module.setIniValue(module.stat.ini_filename, "TRAJ", "NO_FORCE_HOMING",
                           value)


# 允许手动点动时绕过探头跳闸检查
class TrajNoProbeJogError(module.DataNode):
    def __init__(self):
        super().__init__("101026", "TrajNoProbeJogError", "VARIABLE")

    def value(self):
        return str(module.inifile.find("TRAJ", "NO_PROBE_JOG_ERROR"))

    def set_value(self, value):
        module.setIniValue(module.stat.ini_filename, "TRAJ", "NO_PROBE_JOG_ERROR",
                           value)


# 允许回零过程中绕过探头跳闸检查
class TrajNoProbeHomeError(module.DataNode):
    def __init__(self):
        super().__init__("101027", "TrajNoProbeHomeError", "VARIABLE")

    def value(self):
        return str(module.inifile.find("TRAJ", "NO_PROBE_HOME_ERROR"))

    def set_value(self, value):
        module.setIniValue(module.stat.ini_filename, "TRAJ", "NO_PROBE_HOME_ERROR",
                           value)


# 打开新的轨迹规划器
class TrajArcBlendEnable(module.DataNode):
    def __init__(self):
        super().__init__("101028", "TrajArcBlendEnable", "VARIABLE")

    def value(self):
        return str(module.inifile.find("TRAJ", "ARC_BLEND_ENABLE"))

    def set_value(self, value):
        module.setIniValue(module.stat.ini_filename, "TRAJ", "ARC_BLEND_ENABLE",
                           value)


# 回退到抛物线混合方式
class TrajArcBlendFallbackEnable(module.DataNode):
    def __init__(self):
        super().__init__("101029", "TrajArcBlendFallbackEnable", "VARIABLE")

    def value(self):
        return str(module.inifile.find("TRAJ", "ARC_BLEND_FALLBACK_ENABLE"))

    def set_value(self, value):
        module.setIniValue(module.stat.ini_filename, "TRAJ", "ARC_BLEND_FALLBACK_ENABLE",
                           value)


# 提前查看程序段数的深度
class TrajArcBlendOptimizationDepth(module.DataNode):
    def __init__(self):
        super().__init__("101030", "TrajArcBlendOptimizationDepth", "VARIABLE")

    def value(self):
        return str(module.inifile.find("TRAJ", "ARC_BLEND_OPTIMIZATION_DEPTH"))

    def set_value(self, value):
        module.setIniValue(module.stat.ini_filename, "TRAJ", "ARC_BLEND_OPTIMIZATION_DEPTH",
                           value)


# GAP循环
class TrajArcBlendGapCycles(module.DataNode):
    def __init__(self):
        super().__init__("101031", "TrajArcBlendGapCycles", "VARIABLE")

    def value(self):
        return str(module.inifile.find("TRAJ", "ARC_BLEND_GAP_CYCLES"))

    def set_value(self, value):
        module.setIniValue(module.stat.ini_filename, "TRAJ", "ARC_BLEND_GAP_CYCLES",
                           value)


# 使用斜坡速度的截至频率
class TrajArcBlendRampFreq(module.DataNode):
    def __init__(self):
        super().__init__("101032", "TrajArcBlendRampFreq", "VARIABLE")

    def value(self):
        return str(module.inifile.find("TRAJ", "ARC_BLEND_RAMP_FREQ"))

    def set_value(self, value):
        module.setIniValue(module.stat.ini_filename, "TRAJ", "ARC_BLEND_RAMP_FREQ",
                           value)


# 定义零位，不考虑编码器安装方向
class RS274NGCOrientOffset(module.DataNode):
    def __init__(self):
        super().__init__("101033", "RS274NGCOrientOffset", "VARIABLE")

    def value(self):
        return str(module.inifile.find("RS274NGC", "ORIENT_OFFSET"))

    def set_value(self, value):
        module.setIniValue(module.stat.ini_filename, "RS274NGC", "ORIENT_OFFSET",
                           value)


# RS274NGC-inch
class RS274NGCCenterArcRadiusToleranceInch(module.DataNode):
    def __init__(self):
        super().__init__("101035", "RS274NGCCenterArcRadiusToleranceInch", "VARIABLE")

    def value(self):
        return str(module.inifile.find("RS274NGC", "CENTER_ARC_RADIUS_TOLERANCE_INCH"))

    def set_value(self, value):
        module.setIniValue(module.stat.ini_filename, "RS274NGC", "CENTER_ARC_RADIUS_TOLERANCE_INCH",
                           value)


# RS274NGC-mm
class RS274NGCCenterArcRadiusToleranceMm(module.DataNode):
    def __init__(self):
        super().__init__("101036", "RS274NGCCenterArcRadiusToleranceMm", "VARIABLE")

    def value(self):
        return str(module.inifile.find("RS274NGC", "CENTER_ARC_RADIUS_TOLERANCE_MM"))

    def set_value(self, value):
        module.setIniValue(module.stat.ini_filename, "RS274NGC", "CENTER_ARC_RADIUS_TOLERANCE_MM",
                           value)


# RS274NGC-卸载最后一个刀具时，G43取消
class RS274NGCRetainG43(module.DataNode):
    def __init__(self):
        super().__init__("101037", "RS274NGCRetainG43", "VARIABLE")

    def value(self):
        return str(module.inifile.find("RS274NGC", "RETAIN_G43"))

    def set_value(self, value):
        module.setIniValue(module.stat.ini_filename, "RS274NGC", "RETAIN_G43",
                           value)


# RS274NGC-被调用子程序通过检查参数确定传递的实际位置参数数量
class RS274NGCOwordNargs(module.DataNode):
    def __init__(self):
        super().__init__("101038", "RS274NGCOwordNargs", "VARIABLE")

    def value(self):
        return str(module.inifile.find("RS274NGC", "OWORD_NARGS"))

    def set_value(self, value):
        module.setIniValue(module.stat.ini_filename, "RS274NGC", "OWORD_NARGS",
                           value)


# RS274NGC-o程序错误只发出警告
class RS274NGCOwordWarnOnly(module.DataNode):
    def __init__(self):
        super().__init__("101039", "RS274NGCOwordWarnOnly", "VARIABLE")

    def value(self):
        return str(module.inifile.find("RS274NGC", "OWORD_WARNONLY"))

    def set_value(self, value):
        module.setIniValue(module.stat.ini_filename, "RS274NGC", "OWORD_WARNONLY",
                           value)


# RS274允许配置启动时自动清除G92
class RS274NGCDisableG92Persistence(module.DataNode):
    def __init__(self):
        super().__init__("101040", "RS274NGCDisableG92Persistence", "VARIABLE")

    def value(self):
        return str(module.inifile.find("RS274NGC", "DISABLE_G92_PERSISTENCE"))

    def set_value(self, value):
        module.setIniValue(module.stat.ini_filename, "RS274NGC", "DISABLE_G92_PERSISTENCE",
                           value)


# 基本任务周期
class EmcmotBasePeriod(module.DataNode):
    def __init__(self):
        super().__init__("101041", "EmcmotBasePeriod", "VARIABLE")

    def value(self):
        return str(module.inifile.find("EMCMOT", "BASE_PERIOD"))

    def set_value(self, value):
        module.setIniValue(module.stat.ini_filename, "EMCMOT", "BASE_PERIOD",
                           value)


# 伺服任务周期
class EmcmotServoPeriod(module.DataNode):
    def __init__(self):
        super().__init__("101042", "EmcmotServoPeriod", "VARIABLE")

    def value(self):
        return str(module.inifile.find("EMCMOT", "SERVO_PERIOD"))

    def set_value(self, value):
        module.setIniValue(module.stat.ini_filename, "EMCMOT", "SERVO_PERIOD",
                           value)


# 轨迹规划器任务周期
class TrajPeriod(module.DataNode):
    def __init__(self):
        super().__init__("101043", "TrajPeriod", "VARIABLE")

    def value(self):
        return str(module.inifile.find("EMCMOT", "TRAJ_PERIOD"))

    def set_value(self, value):
        module.setIniValue(module.stat.ini_filename, "EMCMOT", "TRAJ_PERIOD",
                           value)


# 等待MOTION确认从task接受信息的秒数
class EmcmotCommTimeout(module.DataNode):
    def __init__(self):
        super().__init__("101044", "EmcmotCommTimeout", "VARIABLE")

    def value(self):
        return str(module.inifile.find("EMCMOT", "COMM_TIMEOUT"))

    def set_value(self, value):
        module.setIniValue(module.stat.ini_filename, "EMCMOT", "COMM_TIMEOUT",
                           value)


# task运行时间
class TaskCycleTime(module.DataNode):
    def __init__(self):
        super().__init__("101045", "TaskCycleTime", "VARIABLE")

    def value(self):
        return str(module.inifile.find("TASK", "CYCLE_TIME"))

    def set_value(self, value):
        module.setIniValue(module.stat.ini_filename, "TASK", "CYCLE_TIME",
                           value)


# EMCIO运行时间
class EmcioCycleTime(module.DataNode):
    def __init__(self):
        super().__init__("101046", "EMCIOCycleTime", "VARIABLE")

    def value(self):
        return str(module.inifile.find("EMCIO", "CYCLE_TIME"))

    def set_value(self, value):
        module.setIniValue(module.stat.ini_filename, "EMCIO", "CYCLE_TIME",
                           value)


# 指定换刀时的位置
class EmcioToolChangePosition(module.DataNode):
    def __init__(self):
        super().__init__("101048", "EmcioToolChangePosition", "VARIABLE")

    def value(self):
        return str(module.inifile.find("EMCIO", "TOOL_CHANGE_POSITION"))

    def set_value(self, value):
        module.setIniValue(module.stat.ini_filename, "EMCIO", "TOOL_CHANGE_POSITION",
                           value)


# Z轴换刀前移动到机床零点
class EmcioToolChangeQuillUp(module.DataNode):
    def __init__(self):
        super().__init__("101049", "EmcioToolChangeQuillUp", "VARIABLE")

    def value(self):
        return str(module.inifile.find("EMCIO", "TOOL_CHANGE_QUILL_UP"))

    def set_value(self, value):
        module.setIniValue(module.stat.ini_filename, "EMCIO", "TOOL_CHANGE_QUILL_UP",
                           value)


# 当前运行使用历史报警文件名
class HistoryAlarmFileName(module.DataNode):
    def __init__(self):
        super().__init__("101050", "HistoryAlarmFileName", "VARIABLE")

    def value(self):
        return str(config.history_alarm_file)


# 当前轴名顺序
class AxisList(module.DataNode):
    def __init__(self):
        super().__init__("101051", "AxisList", "VARIABLE")

    def value(self):
        return str(module.inifile.find("TRAJ", "COORDINATES"))


# 龙门同步-比例增益
class SynCorrelativeP(module.DataNode):
    def __init__(self):
        super().__init__("101052", "SynCorrelativeP", "VARIABLE")

    def value(self):
        return str(module.inifile.find("SYN CORRELATIVE", "P"))


# 龙门同步-积分增益
class SynCorrelativeI(module.DataNode):
    def __init__(self):
        super().__init__("101053", "SynCorrelativeI", "VARIABLE")

    def value(self):
        return str(module.inifile.find("SYN CORRELATIVE", "I"))


# 龙门同步-微分增益
class SynCorrelativeD(module.DataNode):
    def __init__(self):
        super().__init__("101054", "SynCorrelativeD", "VARIABLE")

    def value(self):
        return str(module.inifile.find("SYN CORRELATIVE", "D"))


# 龙门同步-0阶前馈增益
class SynCorrelativeFF0(module.DataNode):
    def __init__(self):
        super().__init__("101055", "SynCorrelativeFF0", "VARIABLE")

    def value(self):
        return str(module.inifile.find("SYN CORRELATIVE", "FF0"))


# 龙门同步-1阶前馈增益
class SynCorrelativeFF1(module.DataNode):
    def __init__(self):
        super().__init__("101056", "SynCorrelativeFF1", "VARIABLE")

    def value(self):
        return str(module.inifile.find("SYN CORRELATIVE", "FF1"))


# 龙门同步-2阶前馈增益
class SynCorrelativeFF2(module.DataNode):
    def __init__(self):
        super().__init__("101057", "SynCorrelativeFF2", "VARIABLE")

    def value(self):
        return str(module.inifile.find("SYN CORRELATIVE", "FF2"))


# 龙门同步-偏移
class SynCorrelativeBias(module.DataNode):
    def __init__(self):
        super().__init__("101058", "SynCorrelativeBias", "VARIABLE")

    def value(self):
        return str(module.inifile.find("SYN CORRELATIVE", "BIAS"))


# 龙门同步-死区
class SynCorrelativeDeadband(module.DataNode):
    def __init__(self):
        super().__init__("101059", "SynCorrelativeDeadband", "VARIABLE")

    def value(self):
        return str(module.inifile.find("SYN CORRELATIVE", "DEADBAND"))


# 龙门同步-最大输出
class SynCorrelativeMaxOutput(module.DataNode):
    def __init__(self):
        super().__init__("101060", "SynCorrelativeMaxOutput", "VARIABLE")

    def value(self):
        return str(module.inifile.find("SYN CORRELATIVE", "MAX OUTPUT"))


# 龙门同步-转动惯量比J1：J2
class SynCorrelativePY1(module.DataNode):
    def __init__(self):
        super().__init__("101061", "SynCorrelativePY1", "VARIABLE")

    def value(self):
        return str(module.inifile.find("SYN CORRELATIVE", "P Y1"))


# 龙门同步-转动惯量比J2：J1
class SynCorrelativePY2(module.DataNode):
    def __init__(self):
        super().__init__("101062", "SynCorrelativePY2", "VARIABLE")

    def value(self):
        return str(module.inifile.find("SYN CORRELATIVE", "P Y2"))


# 龙门同步-偏差分段阈值1
class SynCorrelativeFracTh1(module.DataNode):
    def __init__(self):
        super().__init__("101063", "SynCorrelativeFracTh1", "VARIABLE")

    def value(self):
        return str(module.inifile.find("SYN CORRELATIVE", "FRAC TH1"))


# 龙门同步-偏差分段阈值2
class SynCorrelativeFracTh2(module.DataNode):
    def __init__(self):
        super().__init__("101064", "SynCorrelativeFracTh2", "VARIABLE")

    def value(self):
        return str(module.inifile.find("SYN CORRELATIVE", "FRAC TH2"))


# 示波器采样停止
class ScopeStopSampling(module.DataNode):
    def __init__(self):
        super().__init__("101075", "ScopeStopSampling", "VARIABLE")

    def value(self):
        return str(hal.get_value(config.scope_stop_sample))

    def set_value(self, value):
        hal.set_p(config.scope_stop_sample, value)


# 示波器采样开始
class ScopeStartSampling(module.DataNode):
    def __init__(self):
        super().__init__("101076", "ScopeStartSampling", "VARIABLE")

    def value(self):
        return str(hal.get_value(config.scope_start_sample))

    def set_value(self, value):
        hal.set_p(config.scope_start_sample, value)


# 示波器采样点数
class ScopeSamplePointsNums(module.DataNode):
    def __init__(self):
        super().__init__("101077", "ScopeSamplePointsNums", "VARIABLE")

    def value(self):
        all_points = int(module.inifile.find("SCOPE", "SAMPLE_POINTS"))
        return str(int(all_points / 16))

    def set_value(self, value):
        all_points = int(value) * 16
        module.setIniValue(module.stat.ini_filename, "SCOPE", "SAMPLE_POINTS",
                           str(all_points))


# 示波器采样频率
class ScopeSampleFrequency(module.DataNode):
    def __init__(self):
        self.f = config.scope_frequency_list.split(" ")
        self.f_high = self.f[0]
        self.f_medium = self.f[1]
        self.f_low = self.f[2]
        super().__init__("101078", "ScopeSampleFrequency", "VARIABLE")

    def value(self):
        multi = module.scope.getValue("HMULT")
        f = int(1000 / float(multi))
        if f == int(self.f_high):
            return "0"
        elif f == int(self.f_medium):
            return "1"
        elif f == int(self.f_low):
            return "2"

    def set_value(self, value):
        # multi = 1000 / (周期 * 频率) = 1000 / （1 ms * value）
        f = 1000
        if value == "0":
            f = self.f_high
        elif value == "1":
            f = self.f_medium
        elif value == "2":
            f = self.f_low
        tmp = (int)(1000 / int(f))
        multi = str(tmp)
        module.scope.setValue(multi, "HMULT")
        module.scope.update()
        # 加载配置文件
        hal.set_p(config.scope_reload_config, "1")
        print("reload scope config")
        time.sleep(0.2)
        hal.set_p(config.scope_reload_config, "0")


# 示波器采样通道数
class ScopeSampleChannelNums(module.DataNode):
    def __init__(self):
        super().__init__("101079", "ScopeSampleChannelNums", "VARIABLE")

    def value(self):
        return str(module.scope.getChannelCounts() - (int)(config.scope_bind_channel_counts.replace(" ", "")))


# 示波器数据导出
class ScopeExportFile(module.DataNode):
    def __init__(self):
        self.flag_pin = config.scope_export_flag
        super().__init__("101080", "ScopeExportFile", "VARIABLE")

    def value(self):
        flag = hal.get_value(self.flag_pin)
        if flag:
            return "1"
        return "0"

    def set_value(self, value):
        hal.set_p(config.scope_export_flag, value)


# 示波器频率列表
class ScopeFrequencyList(module.DataNode):
    def __init__(self):
        self.list_pin = config.scope_frequency_list
        super().__init__("101081", "ScopeFrequencyList", "VARIABLE")

    def value(self):
        return str(self.list_pin)


# 初始化解释器的NC代码字符串
class RS274NGCStartupCode(module.DataNode):
    def __init__(self):
        super().__init__("102000", "RS274NGCStartupCode", "VARIABLE")

    def value(self):
        return str(module.inifile.find("RS274NGC", "RS274NGC_STARTUP_CODE"))

    def set_value(self, value):
        module.setIniValue(module.stat.ini_filename, "RS274NGC", "RS274NGC_STARTUP_CODE",
                           value)


