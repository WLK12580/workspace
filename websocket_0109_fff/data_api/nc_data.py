import config
from data_class import (
    nc_module as module,
    class_alarm as nc_alarm,
    class_axis as nc_axis,
    class_param as nc_param,
    class_program as nc_program,
    class_system as nc_system,
    class_tool as nc_tool,
    class_plc as nc_plc,
    class_channel as nc_channel,
)


def update() -> bool:
    return module.update()


"""
数据项
# 1.系统数据
"""
# [100000] 工作模式
task_mode = nc_system.TaskMode()
# [100001] 当前坐标系
current_coordinate = nc_system.CurrentCoordinate()
# [100007] SP0-主轴模式状态
sp0_mode_status = nc_system.SP0ModeStatus()
# [100008] 单段模式
single_block_status = nc_system.SingleBlockStatus()
# [100009] 主轴旋转方向
spindle_orientation = nc_system.SpindleOrientation()
# [100010]
G95x_Code = nc_system.G95_Code()
# [100011]
G_Code = nc_system.GCode_Effect()
# [100012]
G21x_Code = nc_system.G21_Code()
# [100013]
M_Code = nc_system.MCode_Effect()
# [100014]
process_time = nc_system.ProcessTime()
# [100015]
G43_Effect = nc_system.G43Effect()
# [100016]
program_finished = nc_system.ProgramFinished()
# [100017]
G41G42_Effect = nc_system.G41G42Effect()
# [100018]
T_Effect = nc_system.TEffect()
# [100019]
process_task_status = nc_system.ProcessTaskStatus()
# [100020]
G40_Effect = nc_system.G40Effect()
# [100021]
G49_Effect = nc_system.G49Effect()
# [100022]
program_load_percentage = nc_program.ProgramLoadPercentage()
# [100023]
ipc_program_path = nc_program.IPCProgramPath()
# [100024]当前生效的r参数
current_rotation_xy = nc_system.CurrentRotationXY()
# [100025] 主轴使能状态
spindle_enable_status = nc_system.SpindleEnableStatus()
# [100026] 进给使能状态
feed_enable_status = nc_system.FeedEnableStatus()
# [100027] 定位执行结束清空标志
position_finished_flag = nc_system.PositionFinishedFlag()
# [100028] 工件号
workpiece_id = nc_system.WorkpieceId()
# [100029] 加工数量
process_num = nc_system.ProcessNum()
# [100030] 跳段模式是否启动
jump_segment_mode = nc_system.JumpSegmentMode()
# [100031] 主轴切削负载
spindle_load = nc_system.SpindleLoad()
# [100032] 当前插补指令集-F
f_effect = nc_system.FEffect()
# [100033] 当前插补指令集-S
s_effect = nc_system.SEffect()
# [100034] SP1-主轴模式状态
sp1_mode_status = nc_system.SP1ModeStatus()
# [100035] SP1-旋转方向
sp1_orient = nc_system.SpindleOrientation_1()
# [100036] 多行MDI的当前执行行
mdi_current_line = nc_system.MdiCurrentLine()
# [100038] 当前运动类型 feed/arc
current_motion_type = nc_system.CurrentMotionType()
# [101000] 系统中的轴的数量
joints_count = nc_system.KinsJoints()
# [101001 - 101009] 系统控制的轴名
ipcts_coordinate_x = nc_system.IPCTSCoordinates("x")
ipcts_coordinate_y = nc_system.IPCTSCoordinates("y")
ipcts_coordinate_z = nc_system.IPCTSCoordinates("z")
ipcts_coordinate_a = nc_system.IPCTSCoordinates("a")
ipcts_coordinate_b = nc_system.IPCTSCoordinates("b")
ipcts_coordinate_c = nc_system.IPCTSCoordinates("c")
ipcts_coordinate_u = nc_system.IPCTSCoordinates("u")
ipcts_coordinate_v = nc_system.IPCTSCoordinates("v")
ipcts_coordinate_w = nc_system.IPCTSCoordinates("w")
# [101010] 系统中的主轴的数量
spindle_count = nc_system.TrajSpindles()
# [101019] 线性轴的机床单位
linear_unit = nc_system.TrajLinearUnits()
# [101020] 旋转轴的机床单位
angular_unit = nc_system.TrajAngularUnits()
# [101021] 线性轴点动的默认初始速率
default_linear_velocity = nc_system.TrajDefaultLinearVelocity()
# [101022] 线性轴点动的默认加速度
default_linear_acceleration = nc_system.TrajDefaultLinearAcceleration()
# [101023] 任意线性轴的最大速度
max_linear_velocity = nc_system.TrajMaxLinearVelocity()
# [101024] 任意线性轴的最大加速度
max_linear_acceleration = nc_system.TrajMaxLinearAcceleration()
# [101025] 强制用户在任何MDI命令或程序执行前回参考点
no_force_homing = nc_system.TrajNoForceHoming()
# [101026] 允许手动点动时绕过探头跳闸检查
no_probe_jog_error = nc_system.TrajNoProbeJogError()
# [101027] 允许回零过程中绕过探头跳闸检查
no_probe_home_error = nc_system.TrajNoProbeHomeError()
# [101028] 打开新的轨迹规划器
arc_blend_enable = nc_system.TrajArcBlendEnable()
# [101029] 回退到抛物线混合方式
arc_blend_fallback_enable = nc_system.TrajArcBlendFallbackEnable()
# [101030] 提前查看程序段数的深度
arc_blend_optimization_depth = nc_system.TrajArcBlendOptimizationDepth()
# [101031] GAP循环
arc_blend_gap_cycles = nc_system.TrajArcBlendGapCycles()
# [101032] 使用斜坡速度的截至频率
arc_blend_ramp_freq = nc_system.TrajArcBlendRampFreq()
# [101033] 定义零位，不考虑编码器安装方向
rs274_ngc_orient_offset = nc_system.RS274NGCOrientOffset()
# [101035] RS274NGC-inch
rs274_ngc_center_arc_radius_tolerance_inch = (
    nc_system.RS274NGCCenterArcRadiusToleranceInch()
)
# [101036] RS274NGC-mm
rs274_ngc_center_arc_radius_tolerance_mm = (
    nc_system.RS274NGCCenterArcRadiusToleranceMm()
)
# [101037] RS274NGC-卸载最后一个刀具时，G43取消
rs274_ngc_retain_G43 = nc_system.RS274NGCRetainG43()
# [101038] RS274NGC-被调用子程序通过检查参数确定传递的实际位置参数数量
rs274_ngc_oword_nargs = nc_system.RS274NGCOwordNargs()
# [101039] RS274NGC-o程序错误只发出警告
rs274_ngc_oword_warnonly = nc_system.RS274NGCOwordWarnOnly()
# [101040] RS274允许配置启动时自动清除G92
rs274_ngc_disable_G92_persistence = nc_system.RS274NGCDisableG92Persistence()
# [101041] 基本任务周期
emcmot_base_period = nc_system.EmcmotBasePeriod()
# [101042] 伺服任务周期
emcmot_servo_period = nc_system.EmcmotServoPeriod()
# [101043] 轨迹规划器任务周期
traj_period = nc_system.TrajPeriod()
# [101044] 等待MOTION确认从task接受信息的秒数
emcmot_comm_timeout = nc_system.EmcmotCommTimeout()
# [101045] task运行时间
task_cycle_time = nc_system.TaskCycleTime()
# [101046] EMCIO运行时间
emcio_cycle_time = nc_system.EmcioCycleTime()
# [101048] 指定换刀时的位置
emcio_tool_change_position = nc_system.EmcioToolChangePosition()
# [101049] Z轴换刀前移动到机床零点
emcio_tool_change_quill_up = nc_system.EmcioToolChangeQuillUp()
# [101050] 当前运行使用历史报警文件名
history_alarm_file_name = nc_system.HistoryAlarmFileName()
# [101051] 轴名顺序
axis_list = nc_system.AxisList()
# [101052] 龙门同步-比例增益
gantry_syn_p = nc_system.SynCorrelativeP()
# [101053] 龙门同步-积分增益
gantry_syn_i = nc_system.SynCorrelativeI()
# [101054] 龙门同步-微分增益
gantry_syn_d = nc_system.SynCorrelativeD()
# [101055] 龙门同步-0阶前馈增益
gantry_syn_ff0 = nc_system.SynCorrelativeFF0()
# [101056] 龙门同步-1阶前馈增益
gantry_syn_ff1 = nc_system.SynCorrelativeFF1()
# [101057] 龙门同步-2阶前馈增益
gantry_syn_ff2 = nc_system.SynCorrelativeFF2()
# [101058] 龙门同步-偏移
gantry_syn_bias = nc_system.SynCorrelativeBias()
# [101059] 龙门同步-死区
gantry_syn_deadband = nc_system.SynCorrelativeDeadband()
# [101060] 龙门同步-最大输出
gantry_syn_max_output = nc_system.SynCorrelativeMaxOutput()
# [101061] 龙门同步-转动惯量比J1：J2
gantry_syn_p_y1 = nc_system.SynCorrelativePY1()
# [101062] 龙门同步-转动惯量比J2：J1
gantry_syn_p_y2 = nc_system.SynCorrelativePY2()
# [101063] 龙门同步-偏差分段阈值1
gantry_syn_frac_th1 = nc_system.SynCorrelativeFracTh1()
# [101064] 龙门同步-偏差分段阈值2
gantry_syn_frac_th2 = nc_system.SynCorrelativeFracTh2()
# [101075] 示波器采样停止
scope_stop_sampling = nc_system.ScopeStopSampling()
# [101076] 示波器采样开始
scope_start_sampling = nc_system.ScopeStartSampling()
# [101077] 示波器采样点数
scope_sample_points_nums = nc_system.ScopeSamplePointsNums()
# [101078] 示波器采样频率
scope_sample_frequency = nc_system.ScopeSampleFrequency()
# [101079] 示波器采样通道数
scope_sample_channel_nums = nc_system.ScopeSampleChannelNums()
# [101080] 示波器数据导出
scope_export_file_flag = nc_system.ScopeExportFile()
# [101081] 示波器频率列表
scope_frequency_list = nc_system.ScopeFrequencyList()

# [102000] 初始化解释器的NC代码字符串
rs274_ngc_startup_code = nc_system.RS274NGCStartupCode()

"""
数据项
# 2.轴数据
"""
# [3000] 轴使能
axis_enabled = []
for index, item in enumerate(str(module.axis_list).split(" ")):
    enabled = nc_axis.AxisEnabled(index)
    axis_enabled.append(enabled)

# [3001] 轴回参考点
axis_homed = []
for index, item in enumerate(str(module.axis_list).split(" ")):
    obj = nc_axis.AxisHomed(index)
    axis_homed.append(obj)

# [3002] 轴当前位置-MCS machine units
actual_position = []

for index, item in enumerate(str(module.axis_list).split(" ")):
    position = nc_axis.AxisActualPosition(index)
    actual_position.append(position)

# [3003] 轴目标位置-MCS
axis_target_position = []

for index, item in enumerate(str(module.axis_list).split(" ")):
    obj = nc_axis.AxisTargetPosition(index)
    axis_target_position.append(obj)

# [3004] 轴余程-MCS
axis_remaining_distance = []

for index, item in enumerate(str(module.axis_list).split(" ")):
    obj = nc_axis.AxisRemainingDistance(index)
    axis_remaining_distance.append(obj)

# [3005] 轴当前速度
x_velocity = nc_axis.AxisVelocity("x")
y_velocity = nc_axis.AxisVelocity("y")
z_velocity = nc_axis.AxisVelocity("z")
a_velocity = nc_axis.AxisVelocity("a")
b_velocity = nc_axis.AxisVelocity("b")
c_velocity = nc_axis.AxisVelocity("c")
u_velocity = nc_axis.AxisVelocity("u")
v_velocity = nc_axis.AxisVelocity("v")
w_velocity = nc_axis.AxisVelocity("w")
# [3006] 进给倍率
feedrate = nc_axis.AxisFeedrate()
# [3007] 关接当前跟随误差
joint_0_ferror = nc_axis.JointCurrentFerror(0)
joint_1_ferror = nc_axis.JointCurrentFerror(1)
joint_2_ferror = nc_axis.JointCurrentFerror(2)
joint_3_ferror = nc_axis.JointCurrentFerror(3)
joint_4_ferror = nc_axis.JointCurrentFerror(4)
joint_5_ferror = nc_axis.JointCurrentFerror(5)
joint_6_ferror = nc_axis.JointCurrentFerror(6)
joint_7_ferror = nc_axis.JointCurrentFerror(7)
joint_8_ferror = nc_axis.JointCurrentFerror(8)
# [3008] 主轴速度
spindle_0_speed = nc_axis.SpindleSpeed(0)
spindle_1_speed = nc_axis.SpindleSpeed(1)
# [3009] 主轴使能
spindle_0_enable = nc_axis.SpindleEnabled(0)
spindle_1_enable = nc_axis.SpindleEnabled(1)
# [3010] 主轴速率
spindle_0_rate = nc_axis.SpindleOverride(0)
spindle_1_rate = nc_axis.SpindleOverride(1)
# [3012] 当前实际进给速度
current_feed_velocity = nc_axis.CurrentVelocity()
# [3013] 当前设定进给速度
set_feed_velocity = nc_axis.FeedVelocity()
# [3014] 主轴回零
spindle_0_homed = nc_axis.SpindleHomed(0)
# # [3015] 轴当前位置-WCS
# x_current_position_wcs = nc_axis.AxisCurrentPositionWCS("x")
# y_current_position_wcs = nc_axis.AxisCurrentPositionWCS("y")
# z_current_position_wcs = nc_axis.AxisCurrentPositionWCS("z")
# a_current_position_wcs = nc_axis.AxisCurrentPositionWCS("a")
# b_current_position_wcs = nc_axis.AxisCurrentPositionWCS("b")
# c_current_position_wcs = nc_axis.AxisCurrentPositionWCS("c")
# u_current_position_wcs = nc_axis.AxisCurrentPositionWCS("u")
# v_current_position_wcs = nc_axis.AxisCurrentPositionWCS("v")
# w_current_position_wcs = nc_axis.AxisCurrentPositionWCS("w")

# # [3015] 轴当前位置-WCS
actual_position_wcs = []
for index, item in enumerate(str(module.axis_list).split(" ")):
    position = nc_axis.AxisActualPositionWCS(index)
    actual_position_wcs.append(position)

# # [3016] 轴目标位置-WCS
# x_target_position_wcs = nc_axis.AxisTargetPositionWCS("x")
# y_target_position_wcs = nc_axis.AxisTargetPositionWCS("y")
# z_target_position_wcs = nc_axis.AxisTargetPositionWCS("z")
# a_target_position_wcs = nc_axis.AxisTargetPositionWCS("a")
# b_target_position_wcs = nc_axis.AxisTargetPositionWCS("b")
# c_target_position_wcs = nc_axis.AxisTargetPositionWCS("c")
# u_target_position_wcs = nc_axis.AxisTargetPositionWCS("u")
# v_target_position_wcs = nc_axis.AxisTargetPositionWCS("v")
# w_target_position_wcs = nc_axis.AxisTargetPositionWCS("w")

# # [3016] 轴目标位置-WCS
actual_target_position_wcs = []
for index, item in enumerate(str(module.axis_list).split(" ")):
    position = nc_axis.AxisActualTargetPositionWCS(index)
    actual_target_position_wcs.append(position)

# [3017] 主轴设定转速
spindle_0_setting_speed = nc_axis.SpindleSettingSpeed(0)
# [3018] 主轴当前位置
spindle_0_current_position = nc_axis.SpindleCurrentPosition(0)

# [3107] 旋转轴设为1时，轴移动0-359.99度
x_rotary_units = nc_axis.AxisLetterWrappedRotary("x")
y_rotary_units = nc_axis.AxisLetterWrappedRotary("y")
z_rotary_units = nc_axis.AxisLetterWrappedRotary("z")
a_rotary_units = nc_axis.AxisLetterWrappedRotary("a")
b_rotary_units = nc_axis.AxisLetterWrappedRotary("b")
c_rotary_units = nc_axis.AxisLetterWrappedRotary("c")
u_rotary_units = nc_axis.AxisLetterWrappedRotary("u")
v_rotary_units = nc_axis.AxisLetterWrappedRotary("v")
w_rotary_units = nc_axis.AxisLetterWrappedRotary("w")
# [3110] 轴-锁定的关节号
x_locking_joint = nc_axis.AxisLetterLockingIndexerJoint("x")
y_locking_joint = nc_axis.AxisLetterLockingIndexerJoint("y")
z_locking_joint = nc_axis.AxisLetterLockingIndexerJoint("z")
a_locking_joint = nc_axis.AxisLetterLockingIndexerJoint("a")
b_locking_joint = nc_axis.AxisLetterLockingIndexerJoint("b")
c_locking_joint = nc_axis.AxisLetterLockingIndexerJoint("c")
u_locking_joint = nc_axis.AxisLetterLockingIndexerJoint("u")
v_locking_joint = nc_axis.AxisLetterLockingIndexerJoint("v")
w_locking_joint = nc_axis.AxisLetterLockingIndexerJoint("w")
# [3111] 轴-外部轴偏移
x_offset_ratio = nc_axis.AxisLetterOffsetAvRatio("x")
y_offset_ratio = nc_axis.AxisLetterOffsetAvRatio("y")
z_offset_ratio = nc_axis.AxisLetterOffsetAvRatio("z")
a_offset_ratio = nc_axis.AxisLetterOffsetAvRatio("a")
b_offset_ratio = nc_axis.AxisLetterOffsetAvRatio("b")
c_offset_ratio = nc_axis.AxisLetterOffsetAvRatio("c")
u_offset_ratio = nc_axis.AxisLetterOffsetAvRatio("u")
v_offset_ratio = nc_axis.AxisLetterOffsetAvRatio("v")
w_offset_ratio = nc_axis.AxisLetterOffsetAvRatio("w")
# [3112] 关节-类型==轴类型
joint_0_type = nc_axis.JointNumType(0)
joint_1_type = nc_axis.JointNumType(1)
joint_2_type = nc_axis.JointNumType(2)
joint_3_type = nc_axis.JointNumType(3)
joint_4_type = nc_axis.JointNumType(4)
joint_5_type = nc_axis.JointNumType(5)
joint_6_type = nc_axis.JointNumType(6)
joint_7_type = nc_axis.JointNumType(7)
joint_8_type = nc_axis.JointNumType(8)
# [3113] 关节-最大速度
joint_0_max_velocity = nc_axis.JointNumMaxVelocity(0)
joint_1_max_velocity = nc_axis.JointNumMaxVelocity(1)
joint_2_max_velocity = nc_axis.JointNumMaxVelocity(2)
joint_3_max_velocity = nc_axis.JointNumMaxVelocity(3)
joint_4_max_velocity = nc_axis.JointNumMaxVelocity(4)
joint_5_max_velocity = nc_axis.JointNumMaxVelocity(5)
joint_6_max_velocity = nc_axis.JointNumMaxVelocity(6)
joint_7_max_velocity = nc_axis.JointNumMaxVelocity(7)
joint_8_max_velocity = nc_axis.JointNumMaxVelocity(8)
# [3114] 关节-最大加速度
joint_0_max_acceleration = nc_axis.JointNumMaxAcceleration(0)
joint_1_max_acceleration = nc_axis.JointNumMaxAcceleration(1)
joint_2_max_acceleration = nc_axis.JointNumMaxAcceleration(2)
joint_3_max_acceleration = nc_axis.JointNumMaxAcceleration(3)
joint_4_max_acceleration = nc_axis.JointNumMaxAcceleration(4)
joint_5_max_acceleration = nc_axis.JointNumMaxAcceleration(5)
joint_6_max_acceleration = nc_axis.JointNumMaxAcceleration(6)
joint_7_max_acceleration = nc_axis.JointNumMaxAcceleration(7)
joint_8_max_acceleration = nc_axis.JointNumMaxAcceleration(8)
# [3115] 关节-反向间隙
joint_0_backlash = nc_axis.JointNumBacklash(0)
joint_1_backlash = nc_axis.JointNumBacklash(1)
joint_2_backlash = nc_axis.JointNumBacklash(2)
joint_3_backlash = nc_axis.JointNumBacklash(3)
joint_4_backlash = nc_axis.JointNumBacklash(4)
joint_5_backlash = nc_axis.JointNumBacklash(5)
joint_6_backlash = nc_axis.JointNumBacklash(6)
joint_7_backlash = nc_axis.JointNumBacklash(7)
joint_8_backlash = nc_axis.JointNumBacklash(8)
# [3116] 关节-负向软限位
joint_0_min_limit = nc_axis.JointNumMinLimit(0)
joint_1_min_limit = nc_axis.JointNumMinLimit(1)
joint_2_min_limit = nc_axis.JointNumMinLimit(2)
joint_3_min_limit = nc_axis.JointNumMinLimit(3)
joint_4_min_limit = nc_axis.JointNumMinLimit(4)
joint_5_min_limit = nc_axis.JointNumMinLimit(5)
joint_6_min_limit = nc_axis.JointNumMinLimit(6)
joint_7_min_limit = nc_axis.JointNumMinLimit(7)
joint_8_min_limit = nc_axis.JointNumMinLimit(8)
# [3117] 配置
joint_0_max_limit = nc_axis.JointNumMaxLimit(0)
joint_1_max_limit = nc_axis.JointNumMaxLimit(1)
joint_2_max_limit = nc_axis.JointNumMaxLimit(2)
joint_3_max_limit = nc_axis.JointNumMaxLimit(3)
joint_4_max_limit = nc_axis.JointNumMaxLimit(4)
joint_5_max_limit = nc_axis.JointNumMaxLimit(5)
joint_6_max_limit = nc_axis.JointNumMaxLimit(6)
joint_7_max_limit = nc_axis.JointNumMaxLimit(7)
joint_8_max_limit = nc_axis.JointNumMaxLimit(8)
# [3118] 关节-最小速度比例跟随误差
joint_0_min_ferror = nc_axis.JointNumMinFerror(0)
joint_1_min_ferror = nc_axis.JointNumMinFerror(1)
joint_2_min_ferror = nc_axis.JointNumMinFerror(2)
joint_3_min_ferror = nc_axis.JointNumMinFerror(3)
joint_4_min_ferror = nc_axis.JointNumMinFerror(4)
joint_5_min_ferror = nc_axis.JointNumMinFerror(5)
joint_6_min_ferror = nc_axis.JointNumMinFerror(6)
joint_7_min_ferror = nc_axis.JointNumMinFerror(7)
joint_8_min_ferror = nc_axis.JointNumMinFerror(8)
# [3119] 关节-最大速度比例跟随误差限制
joint_0_max_ferror = nc_axis.JointNumFerror(0)
joint_1_max_ferror = nc_axis.JointNumFerror(1)
joint_2_max_ferror = nc_axis.JointNumFerror(2)
joint_3_max_ferror = nc_axis.JointNumFerror(3)
joint_4_max_ferror = nc_axis.JointNumFerror(4)
joint_5_max_ferror = nc_axis.JointNumFerror(5)
joint_6_max_ferror = nc_axis.JointNumFerror(6)
joint_7_max_ferror = nc_axis.JointNumFerror(7)
joint_8_max_ferror = nc_axis.JointNumFerror(8)
# [3120] 关节-是否为锁定分度器
joint_0_is_locking = nc_axis.JointNumLockingIndexer(0)
joint_1_is_locking = nc_axis.JointNumLockingIndexer(1)
joint_2_is_locking = nc_axis.JointNumLockingIndexer(2)
joint_3_is_locking = nc_axis.JointNumLockingIndexer(3)
joint_4_is_locking = nc_axis.JointNumLockingIndexer(4)
joint_5_is_locking = nc_axis.JointNumLockingIndexer(5)
joint_6_is_locking = nc_axis.JointNumLockingIndexer(6)
joint_7_is_locking = nc_axis.JointNumLockingIndexer(7)
joint_8_is_locking = nc_axis.JointNumLockingIndexer(8)
# [3121] 回参考点后关节要到达的位置
joint_0_home_position = nc_axis.JointNumHome(0)
joint_1_home_position = nc_axis.JointNumHome(1)
joint_2_home_position = nc_axis.JointNumHome(2)
joint_3_home_position = nc_axis.JointNumHome(3)
joint_4_home_position = nc_axis.JointNumHome(4)
joint_5_home_position = nc_axis.JointNumHome(5)
joint_6_home_position = nc_axis.JointNumHome(6)
joint_7_home_position = nc_axis.JointNumHome(7)
joint_8_home_position = nc_axis.JointNumHome(8)
# [3122] 零位开关或标志脉冲的关节位置
joint_0_home_offset = nc_axis.JointNumHomeOffset(0)
joint_1_home_offset = nc_axis.JointNumHomeOffset(1)
joint_2_home_offset = nc_axis.JointNumHomeOffset(2)
joint_3_home_offset = nc_axis.JointNumHomeOffset(3)
joint_4_home_offset = nc_axis.JointNumHomeOffset(4)
joint_5_home_offset = nc_axis.JointNumHomeOffset(5)
joint_6_home_offset = nc_axis.JointNumHomeOffset(6)
joint_7_home_offset = nc_axis.JointNumHomeOffset(7)
joint_8_home_offset = nc_axis.JointNumHomeOffset(8)
# [3123] 关节-回参考点的初始速度
joint_0_home_search_vel = nc_axis.JointNumHomeSearchVel(0)
joint_1_home_search_vel = nc_axis.JointNumHomeSearchVel(1)
joint_2_home_search_vel = nc_axis.JointNumHomeSearchVel(2)
joint_3_home_search_vel = nc_axis.JointNumHomeSearchVel(3)
joint_4_home_search_vel = nc_axis.JointNumHomeSearchVel(4)
joint_5_home_search_vel = nc_axis.JointNumHomeSearchVel(5)
joint_6_home_search_vel = nc_axis.JointNumHomeSearchVel(6)
joint_7_home_search_vel = nc_axis.JointNumHomeSearchVel(7)
joint_8_home_search_vel = nc_axis.JointNumHomeSearchVel(8)
# [3124] 关节-到零位开关的速度
joint_0_home_latch_vel = nc_axis.JointNumHomeLatchVel(0)
joint_1_home_latch_vel = nc_axis.JointNumHomeLatchVel(1)
joint_2_home_latch_vel = nc_axis.JointNumHomeLatchVel(2)
joint_3_home_latch_vel = nc_axis.JointNumHomeLatchVel(3)
joint_4_home_latch_vel = nc_axis.JointNumHomeLatchVel(4)
joint_5_home_latch_vel = nc_axis.JointNumHomeLatchVel(5)
joint_6_home_latch_vel = nc_axis.JointNumHomeLatchVel(6)
joint_7_home_latch_vel = nc_axis.JointNumHomeLatchVel(7)
joint_8_home_latch_vel = nc_axis.JointNumHomeLatchVel(8)
# [3125] 关节-从零位开关到零位的速度
joint_0_home_final_vel = nc_axis.JointNumHomeFinalVel(0)
joint_1_home_final_vel = nc_axis.JointNumHomeFinalVel(1)
joint_2_home_final_vel = nc_axis.JointNumHomeFinalVel(2)
joint_3_home_final_vel = nc_axis.JointNumHomeFinalVel(3)
joint_4_home_final_vel = nc_axis.JointNumHomeFinalVel(4)
joint_5_home_final_vel = nc_axis.JointNumHomeFinalVel(5)
joint_6_home_final_vel = nc_axis.JointNumHomeFinalVel(6)
joint_7_home_final_vel = nc_axis.JointNumHomeFinalVel(7)
joint_8_home_final_vel = nc_axis.JointNumHomeFinalVel(8)
# [3126] 关节-编码有零脉冲
joint_0_home_use_index_pulse = nc_axis.JointNumHomeUseIndex(0)
joint_1_home_use_index_pulse = nc_axis.JointNumHomeUseIndex(1)
joint_2_home_use_index_pulse = nc_axis.JointNumHomeUseIndex(2)
joint_3_home_use_index_pulse = nc_axis.JointNumHomeUseIndex(3)
joint_4_home_use_index_pulse = nc_axis.JointNumHomeUseIndex(4)
joint_5_home_use_index_pulse = nc_axis.JointNumHomeUseIndex(5)
joint_6_home_use_index_pulse = nc_axis.JointNumHomeUseIndex(6)
joint_7_home_use_index_pulse = nc_axis.JointNumHomeUseIndex(7)
joint_8_home_use_index_pulse = nc_axis.JointNumHomeUseIndex(8)
# [3127] 关节-编码器复位
joint_0_home_encoder_reset = nc_axis.JointNumHomeIndexNoEncoderReset(0)
joint_1_home_encoder_reset = nc_axis.JointNumHomeIndexNoEncoderReset(1)
joint_2_home_encoder_reset = nc_axis.JointNumHomeIndexNoEncoderReset(2)
joint_3_home_encoder_reset = nc_axis.JointNumHomeIndexNoEncoderReset(3)
joint_4_home_encoder_reset = nc_axis.JointNumHomeIndexNoEncoderReset(4)
joint_5_home_encoder_reset = nc_axis.JointNumHomeIndexNoEncoderReset(5)
joint_6_home_encoder_reset = nc_axis.JointNumHomeIndexNoEncoderReset(6)
joint_7_home_encoder_reset = nc_axis.JointNumHomeIndexNoEncoderReset(7)
joint_8_home_encoder_reset = nc_axis.JointNumHomeIndexNoEncoderReset(8)
# [3128] 关节-使用绝对值编码器
joint_0_absolute_encoder = nc_axis.JointNumHomeAbsoluteEncoder(0)
joint_1_absolute_encoder = nc_axis.JointNumHomeAbsoluteEncoder(1)
joint_2_absolute_encoder = nc_axis.JointNumHomeAbsoluteEncoder(2)
joint_3_absolute_encoder = nc_axis.JointNumHomeAbsoluteEncoder(3)
joint_4_absolute_encoder = nc_axis.JointNumHomeAbsoluteEncoder(4)
joint_5_absolute_encoder = nc_axis.JointNumHomeAbsoluteEncoder(5)
joint_6_absolute_encoder = nc_axis.JointNumHomeAbsoluteEncoder(6)
joint_7_absolute_encoder = nc_axis.JointNumHomeAbsoluteEncoder(7)
joint_8_absolute_encoder = nc_axis.JointNumHomeAbsoluteEncoder(8)
# [3129] 配置
joint_0_home_sequence = nc_axis.JointNumHomeSequence(0)
joint_1_home_sequence = nc_axis.JointNumHomeSequence(1)
joint_2_home_sequence = nc_axis.JointNumHomeSequence(2)
joint_3_home_sequence = nc_axis.JointNumHomeSequence(3)
joint_4_home_sequence = nc_axis.JointNumHomeSequence(4)
joint_5_home_sequence = nc_axis.JointNumHomeSequence(5)
joint_6_home_sequence = nc_axis.JointNumHomeSequence(6)
joint_7_home_sequence = nc_axis.JointNumHomeSequence(7)
joint_8_home_sequence = nc_axis.JointNumHomeSequence(8)
# [3130] 主轴-最大正向转速
# spindle_0_max_forward_vel = nc_axis.SpindleNumMaxForwardVelocity(0)
spindle_max_forward_vel = []
for i in range(0, module.spindle_count):
    item = nc_axis.SpindleNumMaxForwardVelocity(i)
    spindle_max_forward_vel.append(item)
# [3131] 主轴-最大反向转速
# spindle_0_max_reverse_vel = nc_axis.SpindleNumMaxReverseVelocity(0)
spindle_max_reverse_vel = []
for i in range(0, module.spindle_count):
    item = nc_axis.SpindleNumMaxReverseVelocity(i)
    spindle_max_reverse_vel.append(item)
# [3132] 主轴-速度递增/递减的步长
# spindle_0_increment = nc_axis.SpindleNumIncrement(0)
spindle_increment = []
for i in range(0, module.spindle_count):
    item = nc_axis.SpindleNumIncrement(i)
    spindle_increment.append(item)
# [3133] 主轴-回零速度
# spindle_0_home_vel = nc_axis.SpindleNumHomeSearchVelocity(0)
spindle_home_vel = []
for i in range(0, module.spindle_count):
    item = nc_axis.SpindleNumHomeSearchVelocity(i)
    spindle_home_vel.append(item)
# [3134] 轴-数量
axis_count = nc_axis.AxisNum()
# [3135] 轴-是否启用反向间隙补偿
# joint_0_backlash_setting = nc_axis.JointNumBacklashSetting(0)
# joint_1_backlash_setting = nc_axis.JointNumBacklashSetting(1)
# joint_2_backlash_setting = nc_axis.JointNumBacklashSetting(2)
# joint_3_backlash_setting = nc_axis.JointNumBacklashSetting(3)
# joint_4_backlash_setting = nc_axis.JointNumBacklashSetting(4)
# joint_5_backlash_setting = nc_axis.JointNumBacklashSetting(5)
# joint_6_backlash_setting = nc_axis.JointNumBacklashSetting(6)
# joint_7_backlash_setting = nc_axis.JointNumBacklashSetting(7)
# joint_8_backlash_setting = nc_axis.JointNumBacklashSetting(8)
# [3136] 轴-是否启用螺距误差补偿
joint_0_pitch_comp_setting = nc_axis.JointNumPitchCompSetting(0)
joint_1_pitch_comp_setting = nc_axis.JointNumPitchCompSetting(1)
joint_2_pitch_comp_setting = nc_axis.JointNumPitchCompSetting(2)
joint_3_pitch_comp_setting = nc_axis.JointNumPitchCompSetting(3)
joint_4_pitch_comp_setting = nc_axis.JointNumPitchCompSetting(4)
joint_5_pitch_comp_setting = nc_axis.JointNumPitchCompSetting(5)
joint_6_pitch_comp_setting = nc_axis.JointNumPitchCompSetting(6)
joint_7_pitch_comp_setting = nc_axis.JointNumPitchCompSetting(7)
joint_8_pitch_comp_setting = nc_axis.JointNumPitchCompSetting(8)
#
# axis_0_cmdPos = nc_axis.CmdPos('x')
# axis_1_cmdPos = nc_axis.CmdPos('y')
# axis_2_cmdPos = nc_axis.CmdPos('z')
# axis_3_cmdPos = nc_axis.CmdPos('a')
# axis_4_cmdPos = nc_axis.CmdPos('b')
# axis_5_cmdPos = nc_axis.CmdPos('c')
# axis_6_cmdPos = nc_axis.CmdPos('u')
# axis_7_cmdPos = nc_axis.CmdPos('v')
# axis_8_cmdPos = nc_axis.CmdPos('w')
#
# [3138] 轴-加速度
axis_0_accel = nc_axis.AxisAcceleration(0)
axis_1_accel = nc_axis.AxisAcceleration(1)
axis_2_accel = nc_axis.AxisAcceleration(2)
# [3139] 关节-螺距误差补偿类型
joint_0_pitch_comp_type = nc_axis.JointNumPitchCompType(0)
joint_1_pitch_comp_type = nc_axis.JointNumPitchCompType(1)
joint_2_pitch_comp_type = nc_axis.JointNumPitchCompType(2)
joint_3_pitch_comp_type = nc_axis.JointNumPitchCompType(3)
joint_4_pitch_comp_type = nc_axis.JointNumPitchCompType(4)
joint_5_pitch_comp_type = nc_axis.JointNumPitchCompType(5)
joint_6_pitch_comp_type = nc_axis.JointNumPitchCompType(6)
joint_7_pitch_comp_type = nc_axis.JointNumPitchCompType(7)
joint_8_pitch_comp_type = nc_axis.JointNumPitchCompType(8)
# # [3140] 轴-手动快速最大速度
# x_jog_speed_rapid_max = nc_axis.AxisLetterJogSpeedRapidMax("x")
# y_jog_speed_rapid_max = nc_axis.AxisLetterJogSpeedRapidMax("y")
# z_jog_speed_rapid_max = nc_axis.AxisLetterJogSpeedRapidMax("z")
# a_jog_speed_rapid_max = nc_axis.AxisLetterJogSpeedRapidMax("a")
# b_jog_speed_rapid_max = nc_axis.AxisLetterJogSpeedRapidMax("b")
# c_jog_speed_rapid_max = nc_axis.AxisLetterJogSpeedRapidMax("c")
# u_jog_speed_rapid_max = nc_axis.AxisLetterJogSpeedRapidMax("u")
# v_jog_speed_rapid_max = nc_axis.AxisLetterJogSpeedRapidMax("v")
# w_jog_speed_rapid_max = nc_axis.AxisLetterJogSpeedRapidMax("w")

# # [3140] 轴-手动快速最大速度
axis_jog_speed_rapid_max = []
for index, item in enumerate(str(module.axis_list).split(" ")):
    axis_item = nc_axis.AxisLetterJogSpeedRapidMax(index)
    axis_jog_speed_rapid_max.append(axis_item)

# [3141] 轴-手动进给最大速度
axis_jog_speed_feed_max = []
for index, item in enumerate(str(module.axis_list).split(" ")):
    axis_item = nc_axis.AxisLetterJogSpeedFeedMax(index)
    axis_jog_speed_feed_max.append(axis_item)

# [31500] 轴诊断-轴信息-扭矩
axis_0_torque = nc_axis.AxisInfos_Torque(0)
axis_1_torque = nc_axis.AxisInfos_Torque(1)
axis_2_torque = nc_axis.AxisInfos_Torque(2)
axis_3_torque = nc_axis.AxisInfos_Torque(3)
axis_4_torque = nc_axis.AxisInfos_Torque(4)
axis_5_torque = nc_axis.AxisInfos_Torque(5)
axis_6_torque = nc_axis.AxisInfos_Torque(6)
axis_7_torque = nc_axis.AxisInfos_Torque(7)
axis_8_torque = nc_axis.AxisInfos_Torque(8)
axis_99_torque = nc_axis.AxisInfos_Torque(99)
# [31510] 轴诊断-轴信息-轴补偿值(速度)
axis_0_backlash_vel = nc_axis.AxisInfos_Backlash_Vel(0)
axis_1_backlash_vel = nc_axis.AxisInfos_Backlash_Vel(1)
axis_2_backlash_vel = nc_axis.AxisInfos_Backlash_Vel(2)
axis_3_backlash_vel = nc_axis.AxisInfos_Backlash_Vel(3)
axis_4_backlash_vel = nc_axis.AxisInfos_Backlash_Vel(4)
axis_5_backlash_vel = nc_axis.AxisInfos_Backlash_Vel(5)
axis_6_backlash_vel = nc_axis.AxisInfos_Backlash_Vel(6)
axis_7_backlash_vel = nc_axis.AxisInfos_Backlash_Vel(7)
axis_8_backlash_vel = nc_axis.AxisInfos_Backlash_Vel(8)
axis_99_backlash_vel = nc_axis.AxisInfos_Backlash_Vel(99)
# [31520] 轴诊断-轴信息-轴补偿值(差值)
axis_0_backlash_filt = nc_axis.AxisInfos_Backlash_Filt(0)
axis_1_backlash_filt = nc_axis.AxisInfos_Backlash_Filt(1)
axis_2_backlash_filt = nc_axis.AxisInfos_Backlash_Filt(2)
axis_3_backlash_filt = nc_axis.AxisInfos_Backlash_Filt(3)
axis_4_backlash_filt = nc_axis.AxisInfos_Backlash_Filt(4)
axis_5_backlash_filt = nc_axis.AxisInfos_Backlash_Filt(5)
axis_6_backlash_filt = nc_axis.AxisInfos_Backlash_Filt(6)
axis_7_backlash_filt = nc_axis.AxisInfos_Backlash_Filt(7)
axis_8_backlash_filt = nc_axis.AxisInfos_Backlash_Filt(8)
axis_99_backlash_filt = nc_axis.AxisInfos_Backlash_Filt(99)
# [31530] 轴诊断-轴信息-轴补偿值(原始值)
axis_0_backlash_corr = nc_axis.AxisInfos_Backlash_Corr(0)
axis_1_backlash_corr = nc_axis.AxisInfos_Backlash_Corr(1)
axis_2_backlash_corr = nc_axis.AxisInfos_Backlash_Corr(2)
axis_3_backlash_corr = nc_axis.AxisInfos_Backlash_Corr(3)
axis_4_backlash_corr = nc_axis.AxisInfos_Backlash_Corr(4)
axis_5_backlash_corr = nc_axis.AxisInfos_Backlash_Corr(5)
axis_6_backlash_corr = nc_axis.AxisInfos_Backlash_Corr(6)
axis_7_backlash_corr = nc_axis.AxisInfos_Backlash_Corr(7)
axis_8_backlash_corr = nc_axis.AxisInfos_Backlash_Corr(8)
axis_99_backlash_corr = nc_axis.AxisInfos_Backlash_Corr(99)
# [31540] 轴诊断-轴信息-轴跟踪误差(最大值)
axis_0_err_maxLimit = nc_axis.AxisInfos_Err_MaxLimit(0)
axis_1_err_maxLimit = nc_axis.AxisInfos_Err_MaxLimit(1)
axis_2_err_maxLimit = nc_axis.AxisInfos_Err_MaxLimit(2)
axis_3_err_maxLimit = nc_axis.AxisInfos_Err_MaxLimit(3)
axis_4_err_maxLimit = nc_axis.AxisInfos_Err_MaxLimit(4)
axis_5_err_maxLimit = nc_axis.AxisInfos_Err_MaxLimit(5)
axis_6_err_maxLimit = nc_axis.AxisInfos_Err_MaxLimit(6)
axis_7_err_maxLimit = nc_axis.AxisInfos_Err_MaxLimit(7)
axis_8_err_maxLimit = nc_axis.AxisInfos_Err_MaxLimit(8)
axis_99_err_maxLimit = nc_axis.AxisInfos_Err_MaxLimit(99)
# [31550] 轴诊断-轴信息-轴跟踪误差(最小值)
axis_0_err_minLimit = nc_axis.AxisInfos_Err_MinLimit(0)
axis_1_err_minLimit = nc_axis.AxisInfos_Err_MinLimit(1)
axis_2_err_minLimit = nc_axis.AxisInfos_Err_MinLimit(2)
axis_3_err_minLimit = nc_axis.AxisInfos_Err_MinLimit(3)
axis_4_err_minLimit = nc_axis.AxisInfos_Err_MinLimit(4)
axis_5_err_minLimit = nc_axis.AxisInfos_Err_MinLimit(5)
axis_6_err_minLimit = nc_axis.AxisInfos_Err_MinLimit(6)
axis_7_err_minLimit = nc_axis.AxisInfos_Err_MinLimit(7)
axis_8_err_minLimit = nc_axis.AxisInfos_Err_MinLimit(8)
axis_99_err_minLimit = nc_axis.AxisInfos_Err_MinLimit(99)
# [31560] 轴诊断-轴信息-目标位置
axis_0_tarpos = nc_axis.AxisInfos_TarPos(0)
axis_1_tarpos = nc_axis.AxisInfos_TarPos(1)
axis_2_tarpos = nc_axis.AxisInfos_TarPos(2)
axis_3_tarpos = nc_axis.AxisInfos_TarPos(3)
axis_4_tarpos = nc_axis.AxisInfos_TarPos(4)
axis_5_tarpos = nc_axis.AxisInfos_TarPos(5)
axis_6_tarpos = nc_axis.AxisInfos_TarPos(6)
axis_7_tarpos = nc_axis.AxisInfos_TarPos(7)
axis_8_tarpos = nc_axis.AxisInfos_TarPos(8)
axis_99_tarpos = nc_axis.AxisInfos_TarPos(99)
# [31570] 轴诊断-轴信息-反馈位置
axis_0_actpos = nc_axis.AxisInfos_ActPos(0)
axis_1_actpos = nc_axis.AxisInfos_ActPos(1)
axis_2_actpos = nc_axis.AxisInfos_ActPos(2)
axis_3_actpos = nc_axis.AxisInfos_ActPos(3)
axis_4_actpos = nc_axis.AxisInfos_ActPos(4)
axis_5_actpos = nc_axis.AxisInfos_ActPos(5)
axis_6_actpos = nc_axis.AxisInfos_ActPos(6)
axis_7_actpos = nc_axis.AxisInfos_ActPos(7)
axis_8_actpos = nc_axis.AxisInfos_ActPos(8)
axis_99_actpos = nc_axis.AxisInfos_ActPos(99)
# [31580] 轴诊断-轴信息-目标速度
axis_0_tarvel = nc_axis.AxisInfos_TarVel(0)
axis_1_tarvel = nc_axis.AxisInfos_TarVel(1)
axis_2_tarvel = nc_axis.AxisInfos_TarVel(2)
axis_3_tarvel = nc_axis.AxisInfos_TarVel(3)
axis_4_tarvel = nc_axis.AxisInfos_TarVel(4)
axis_5_tarvel = nc_axis.AxisInfos_TarVel(5)
axis_6_tarvel = nc_axis.AxisInfos_TarVel(6)
axis_7_tarvel = nc_axis.AxisInfos_TarVel(7)
axis_8_tarvel = nc_axis.AxisInfos_TarVel(8)
axis_99_tarvel = nc_axis.AxisInfos_TarVel(99)
# [31590] 轴诊断-轴信息-反馈速度
axis_0_actvel = nc_axis.AxisInfos_ActVel(0)
axis_1_actvel = nc_axis.AxisInfos_ActVel(1)
axis_2_actvel = nc_axis.AxisInfos_ActVel(2)
axis_3_actvel = nc_axis.AxisInfos_ActVel(3)
axis_4_actvel = nc_axis.AxisInfos_ActVel(4)
axis_5_actvel = nc_axis.AxisInfos_ActVel(5)
axis_6_actvel = nc_axis.AxisInfos_ActVel(6)
axis_7_actvel = nc_axis.AxisInfos_ActVel(7)
axis_8_actvel = nc_axis.AxisInfos_ActVel(8)
axis_99_actvel = nc_axis.AxisInfos_ActVel(99)

# [3160] 主轴-最小正向转速
# spindle_0_min_forward_vel = nc_axis.SpindleNumMinForwardVelocity(0)
spindle_min_forward_vel = []
for i in range(0, module.spindle_count):
    item = nc_axis.SpindleNumMinForwardVelocity(i)
    spindle_min_forward_vel.append(item)
# [3161] 主轴-最小反向转速
# spindle_0_min_reverse_vel = nc_axis.SpindleNumMinReverseVelocity(0)
spindle_min_reverse_vel = []
for i in range(0, module.spindle_count):
    item = nc_axis.SpindleNumMinReverseVelocity(i)
    spindle_min_reverse_vel.append(item)

# [3163] 主轴-PID-P
# spindle_0_pid_p = nc_axis.SpindlePID_P(0)
spindle_pid_p = []
for i in range(0, module.spindle_count):
    item = nc_axis.SpindlePID_P(i)
    spindle_pid_p.append(item)
# [3164] 主轴-PID_I
# spindle_0_pid_i = nc_axis.SpindlePID_I(0)
spindle_pid_i = []
for i in range(0, module.spindle_count):
    item = nc_axis.SpindlePID_I(i)
    spindle_pid_i.append(item)
# [3165] 主轴-PID-D
# spindle_0_pid_d = nc_axis.SpindlePID_D(0)
spindle_pid_d = []
for i in range(0, module.spindle_count):
    item = nc_axis.SpindlePID_D(i)
    spindle_pid_d.append(item)
# [3166] 轴编码器每转线数
axis_encoder_lrp = []
for index, item in enumerate(str(module.axis_list).split(" ")):
    axis_item = nc_axis.AxisEncoderLRP(index)
    axis_encoder_lrp.append(axis_item)

# [3167] 轴电子齿轮比分子
axis_gear_molecule = []
for index, item in enumerate(str(module.axis_list).split(" ")):
    axis_item = nc_axis.AxisGearMolecule(index)
    axis_gear_molecule.append(axis_item)

# [3168] 轴电子齿轮比分母
axis_gear_deniminator = []
for index, item in enumerate(str(module.axis_list).split(" ")):
    axis_item = nc_axis.AxisGeaDeniminator(index)
    axis_gear_deniminator.append(axis_item)

# [3169] 轴丝杆螺距
axis_flight_lead = []
for index, item in enumerate(str(module.axis_list).split(" ")):
    axis_item = nc_axis.AxisFlightLead(index)
    axis_flight_lead.append(axis_item)
# 轴诊断   X，Y，Z，B，主轴，C，刀库轴
num_diagnosis_axis = len(nc_axis.diagnosis_axis)
# [3170] 轴诊断-伺服准备好
axis_ready_to_switch_on = []
for i in range(0, num_diagnosis_axis):
    st = nc_axis.AxisReadyToSwitchOn(str(i))
    axis_ready_to_switch_on.append(st)
# [3171] 轴诊断-可以开启伺服运行
axis_switch_on = []
for i in range(0, num_diagnosis_axis):
    st = nc_axis.AxisSwitchOn(str(i))
    axis_switch_on.append(st)
# [3172] 轴诊断-伺服运行
axis_operation_enabled = []
for i in range(0, num_diagnosis_axis):
    st = nc_axis.AxisOperationEnabled(str(i))
    axis_operation_enabled.append(st)
# [3173] 轴诊断-故障
axis_fault = []
for i in range(0, num_diagnosis_axis):
    st = nc_axis.AxisFault(str(i))
    axis_fault.append(st)
# [3174] 轴诊断-主回路电接通
axis_voltage_enabled = []
for i in range(0, num_diagnosis_axis):
    st = nc_axis.AxisVoltageEnabled(str(i))
    axis_voltage_enabled.append(st)
# [3175] 轴诊断-快速停机
axis_quick_stop = []
for i in range(0, num_diagnosis_axis):
    st = nc_axis.AxisQuickStop(str(i))
    axis_quick_stop.append(st)
# [3176] 轴诊断-伺服不可运行
axis_switch_on_disabled = []
for i in range(0, num_diagnosis_axis):
    st = nc_axis.AxisSwitchOnDisabled(str(i))
    axis_switch_on_disabled.append(st)
# [3177] 轴诊断-警告
axis_warning = []
for i in range(0, num_diagnosis_axis):
    st = nc_axis.AxisWarning(str(i))
    axis_warning.append(st)
# [3179] 轴诊断-远程控制
axis_remote = []
for i in range(0, num_diagnosis_axis):
    st = nc_axis.AxisRemote(str(i))
    axis_remote.append(st)
# [3180] 轴诊断-目标直达
axis_target_reach = []
for i in range(0, num_diagnosis_axis):
    st = nc_axis.AxisTargetReach(str(i))
    axis_target_reach.append(st)
# [3181] 轴诊断-内部位置超限
axis_internal_limit_active = []
for i in range(0, num_diagnosis_axis):
    st = nc_axis.AxisInternalLimitActive(str(i))
    axis_internal_limit_active.append(st)
# [3182] 轴诊断-目标位置更新
axis_set_point_acknowledge = []
for i in range(0, num_diagnosis_axis):
    st = nc_axis.AxisSetPointAcknowledge(str(i))
    axis_set_point_acknowledge.append(st)
# [3183] 轴诊断-跟随误差
axis_following_error = []
for i in range(0, num_diagnosis_axis):
    st = nc_axis.AxisFollowingError(str(i))
    axis_following_error.append(st)
# [3184] 轴诊断-扭矩限制激活
axis_torque_limit_active = []
for i in range(0, num_diagnosis_axis):
    st = nc_axis.AxisTorqueLimitActive(str(i))
    axis_torque_limit_active.append(st)
# [3185] 轴诊断—原点已找到
axis_home_find = []
for i in range(0, num_diagnosis_axis):
    st = nc_axis.AxisHomeFind(str(i))
    axis_home_find.append(st)

# [3186] 轴运动方向
axis_motion_dir = []
for index, item in enumerate(str(module.axis_list).split(" ")):
    axis_item = nc_axis.AxisMotionDir(index)
    axis_motion_dir.append(axis_item)

# [3187] 主轴点动进给最大速度
spindle_jogSpeed_feed_max = []
for i in range(0, module.spindle_count):
    item = nc_axis.SpindleJogSpeedFeedMax(i)
    spindle_jogSpeed_feed_max.append(item)

# [3188] 主轴点动快速最大速度
spindle_jogSpeed_rapid_max = []
for i in range(0, module.spindle_count):
    item = nc_axis.SpindleJogSpeedRapidMax(i)
    spindle_jogSpeed_rapid_max.append(item)

# [318900] 刀库轴点动快速最大速度
tool_jogSpeed_rapid_max = nc_axis.ToolJogSpeedRapidMax()

# [318901] 刀库轴点动进给最大速度
tool_jogSpeed_feed_max = nc_axis.ToolJogSpeedFeedMax()

# [3190] 手轮加速度比例系数
jog_accel_fraction = []
for i in range(0, module.axis_count):
    st = nc_axis.JogAccelFraction(i)
    jog_accel_fraction.append(st)

# [319100] 主轴的轴机械传动比分母
spindle_transmission_denominator = nc_axis.SpindleTransmissionDenominator()
# [319101] 主轴的丝杆螺距
spindle_screw_pitch = nc_axis.SpindleScrewPitch()
# [319102] 主轴的轴机械传动比分子
spindle_transmission_numerator = nc_axis.SpindleTransmissionNumerator()
# [319103] 主轴的线转数
spindle_line_revolution_counts = nc_axis.SpindleLineRevolutionCounts()
# [319104] 主轴的运动方向
spindle_motion_orientation = nc_axis.SpindleMotionOrientation()
# [319105] 主轴速度模式下齿轮比
spindle_velocity_mode_gear_ratio = nc_axis.SpindleVelocityModeGearRatio()
# [319106] 主轴速度模式下运动方向
spindle_velocity_mode_motion_orientation = (
    nc_axis.SpindleVelocityModeMotionOrientation()
)

"""
数据项
# 3.刀具
"""
# [500000] 当前刀具号
tool_count = nc_tool.ToolCount()
# [500001] 当前刀具X方向补偿
tool_length_x = nc_tool.ToolXOffset()
# [500002] 当前刀具Y方向补偿
tool_length_y = nc_tool.ToolYOffset()
# [500003] 当前刀具Z方向补偿
tool_length_z = nc_tool.ToolZOffset()
# [500005] 当前刀具直径
tool_diameter = nc_tool.ToolDiameter()

# [500017] 获取当前刀具表信息
Get_Tool_Table_Info = nc_tool.GetToolTableInfo()
# [500018] 手动换刀X补偿
Manual_Tool_X = nc_tool.ManualToolX()
# [500019] 手动换刀Y补偿
Manual_Tool_Y = nc_tool.ManualToolY()
# [500020] 手动换刀X补偿7
Manual_Tool_Z = nc_tool.ManualToolZ()
# [500022] 查询当前G41/G42生效刀具信息
G41G42_Info = nc_tool.GetG41G42Info()
# [500026] 当前生效刀号
current_tool_id = nc_tool.CurrentToolId()

# [510508]
tool_Change = nc_tool.Tool_Change()
# [510509]
toolPoc_Update = nc_tool.ToolPoc_Update()
# [510510]
tool_table = nc_tool.ToolTable()
# [510511]
toolMagazine_table = nc_tool.ToolMagazineTable()
# [510512]
tool_status = nc_tool.ToolStatus()
# [510513]
toolMagazine_Unload = nc_tool.ToolMagazine_Unload()
# [510514]
toolMagazine_Load = nc_tool.ToolMagazine_Load()
# [510515]
toolMagazine_Move = nc_tool.ToolMagazine_Move()
# [510516]
m6_finish = nc_tool.M6Finish()

# tool_offset = nc_tool.ToolOffset()
tool_ID = []
tool_offset_X = []
tool_offset_Y = []
tool_offset_Z = []
tool_diameter_Set = []
tool_hal_Index = []
# 刀位位置数据
tool_pos_index = []

# [512200]
for i in range(10, 61):
    st = nc_tool.ToolHal_Update(str(i))
    tool_hal_Index.append(st)
# [510000]
for i in range(1, 50):
    st = nc_tool.ToolID(str(i))
    tool_ID.append(st)
# [510100]
for i in range(1, 50):
    st = nc_tool.ToolOffset_X(str(i))
    tool_offset_X.append(st)
# [510200]
for i in range(1, 50):
    st = nc_tool.ToolOffset_Y(str(i))
    tool_offset_Y.append(st)
# [510300]
for i in range(1, 50):
    st = nc_tool.ToolOffset_Z(str(i))
    tool_offset_Z.append(st)
# [510400]
for i in range(1, 50):
    st = nc_tool.Tool_Diameter(str(i))
    tool_diameter_Set.append(st)
# [510500]
tool_New = nc_tool.Tool_New()
# [510501]
tool_Cancel = nc_tool.Tool_Cancel()
# move_Pos = nc_tool.MovePos()
# [512300]
cutter_measure_done = nc_tool.CutterMeassureDone()
# [312301] cutter_reset
cutter_measure_reset = nc_tool.CutterMeassureReset()
# [512302] cutter number of cutter head
cutter_number_of_head = nc_tool.CutterNumberOfHead()

# [510517] 入刀位-X1
toolChange_insertionPos_x1 = nc_tool.ToolChangeInsertionPosX1()
# [510518] 入刀位-X2
toolChange_insertionPos_x2 = nc_tool.ToolChangeInsertionPosX2()
# [510519] 入刀位-Y
toolChange_insertionPos_y = nc_tool.ToolChangeInsertionPosY()
# [510520] 入刀位-Z
toolChange_insertionPos_z = nc_tool.ToolChangeInsertionPosZ()
# [510521] 出刀位-X1
toolChange_outPos_x1 = nc_tool.ToolChangeOutPosX1()
# [510522] 出刀位-X2
toolChange_outPos_x2 = nc_tool.ToolChangeOutPosX2()
# [510523] 出刀位-Y
toolChange_outPos_y = nc_tool.ToolChangeOutPosY()
# [510524] 出刀位-Z
toolChange_outPos_z = nc_tool.ToolChangeOutPosZ()
# [510525] 安全位-X1
toolChange_safePos_x1 = nc_tool.ToolChangeSafePosX1()
# [510526] 安全位-X2
toolChange_safePos_x2 = nc_tool.ToolChangeSafePosX2()
# [510527] 安全位-Y
toolChange_safePos_y = nc_tool.ToolChangeSafePosY()
# [510528] 安全位-Z
toolChange_safePos_z = nc_tool.ToolChangeSafePosZ()
# [510529] 左主轴定向角度
toolChange_spindleAngle_1 = nc_tool.ToolChangeSpindleAngle1()
# [510530] 右主轴定向角度
toolChange_spindleAngle_2 = nc_tool.ToolChangeSpindleAngle2()
# [510531] 左主轴最大刀位号
tool_pocMax_1 = nc_tool.ToolPocMax1()
# [510532] 右主轴最大刀位号
tool_pocMax_2 = nc_tool.ToolPocMax2()
# [510533]
for i in range(1, 24):
    st = nc_tool.ToolPos(str(i))
    tool_pos_index.append(st)
# [510557] 等待位x1移动位置
toolChange_waitingPos_X1 = nc_tool.ToolChangeWaitingPosX1()
# [510558] 等待位x2移动位置
toolChange_waitingPos_X2 = nc_tool.ToolChangeWaitingPosX2()
# [510559] 等待位Y移动位置
toolChange_waitingPos_Y = nc_tool.ToolChangeWaitingPosY()
# [510560] 等待位Z移动位置
toolChange_waitingPos_Z = nc_tool.ToolChangeWaitingPosZ()

"""
数据项
# 4.程序
"""
# 当前加工文件名
program_name = nc_program.CurrentProgramName()
# 当前加工程序行
program_line = nc_program.CurrentProgramLine()
# [100004] 当前子程序深度
program_call_level = nc_program.CurrentCallLevel()
# [100005] 当前命令执行状态
rcs_state = nc_program.CurrentExecutionStatus()

"""
数据项
# 5.报警
"""

# [540003] 当前IPC运行状态
ipc_operational_status = nc_alarm.IpcOperationalStatus()
# [540004] 当前急停状态
estop_status = nc_alarm.EStopStatus()

"""
数据项
# 6.宏变量 & 零偏
"""
# [500007] 当前坐标系
g5x_Index = nc_param.G5X_Index()

# [500008]-[500016] 当前零偏x-w
g5x_offset = []
for index, item in enumerate(str(module.axis_list).split(" ")):
    joint_item = nc_param.G5X_Offset(index)
    g5x_offset.append(joint_item)
g5x_offset_r = nc_param.G5X_Offset(9)  # r参数
g5x_offset.append(g5x_offset_r)

# [500021] mdi设置的当前坐标系
current_set_Coordinate = nc_param.CurrentSetCoordinate()

# [500024] mdi设置的当前坐标系(读)
micro_program = nc_param.MicroProgramRemap()
# [500025] mdi设置的当前坐标系（写）
micro_program_write = nc_param.MicroProgramRemapWrite()

# [52000] G54零偏
g54_offset = []
for index, item in enumerate(str(module.axis_list).split(" ")):
    joint_item = nc_param.G54_Offset(index)
    g54_offset.append(joint_item)
g54_offset_r = nc_param.G54_Offset(9)  # r参数
g54_offset.append(g54_offset_r)

# [5201] G55零偏
g55_offset = []
for index, item in enumerate(str(module.axis_list).split(" ")):
    joint_item = nc_param.G55_Offset(index)
    g55_offset.append(joint_item)
g55_offset_r = nc_param.G55_Offset(9)  # r参数
g55_offset.append(g55_offset_r)

# [5202] G56零偏
g56_offset = []
for index, item in enumerate(str(module.axis_list).split(" ")):
    joint_item = nc_param.G56_Offset(index)
    g56_offset.append(joint_item)
g56_offset_r = nc_param.G56_Offset(9)  # r参数
g56_offset.append(g56_offset_r)

# [5203] G57零偏
g57_offset = []
for index, item in enumerate(str(module.axis_list).split(" ")):
    joint_item = nc_param.G57_Offset(index)
    g57_offset.append(joint_item)
g57_offset_r = nc_param.G57_Offset(9)  # r参数
g57_offset.append(g57_offset_r)

# [5204] G58零偏
g58_offset = []
for index, item in enumerate(str(module.axis_list).split(" ")):
    joint_item = nc_param.G58_Offset(index)
    g58_offset.append(joint_item)
g58_offset_r = nc_param.G58_Offset(9)  # r参数
g58_offset.append(g58_offset_r)

# [5205] G59零偏
g59_offset = []
for index, item in enumerate(str(module.axis_list).split(" ")):
    joint_item = nc_param.G59_Offset(index)
    g59_offset.append(joint_item)
g59_offset_r = nc_param.G59_Offset(9)  # r参数
g59_offset.append(g59_offset_r)

# [5206] G92零偏设定值
g92_target_offset = []
for index, item in enumerate(str(module.axis_list).split(" ")):
    joint_item = nc_param.G92_Offset(index)
    g92_target_offset.append(joint_item)

# [5207] G92零偏实际
g92_current_offset = []
for index, item in enumerate(str(module.axis_list).split(" ")):
    joint_item = nc_param.G92_Current_Offset(index)
    g92_current_offset.append(joint_item)

# [5208] 轴Offset是否使能标志(设定值)
offset_enable = []
for index, item in enumerate(str(module.axis_list).split(" ")):
    joint_item = nc_param.OffsetEnable(index)
    offset_enable.append(joint_item)

# [5209] 轴Offset是否使能标志（实际值）
offset_actual_enable = []
for index, item in enumerate(str(module.axis_list).split(" ")):
    joint_item = nc_param.OffsetActualEnabled(index)
    offset_actual_enable.append(joint_item)

# 宏变量


microy = []
for i in range(0, int(config.micro_num)):
    st = nc_param.MicroData(i)
    microy.append(st)

"""
数据项
# 7. plc变量
"""
# [60 0000 - 609999] PLC 数字量输入:最大数量10000个：最大可以申请的数量：2100个:实际申请的数量有注册时决定
plc_digital_input = []
for i in range(0, int(config.plc_digital_input_num)):
    st = nc_plc.PLCDigitalInput(i)
    plc_digital_input.append(st)

# [60 2100 - 60 4199] PLC 数字量输出
plc_digital_output = []
for i in range(0, int(config.plc_digital_output_num)):
    st = nc_plc.PLCDigitalOutput(i)
    plc_digital_output.append(st)

# [60 4200 - 60 4229] PLC 模拟量输入
plc_analog_input = []
for i in range(0, int(config.plc_analog_input_num)):
    st = nc_plc.PLCAnalogInput(i)
    plc_analog_input.append(st)

# [60 4230 - 60 4259] PLC 模拟量输出
plc_analog_output = []
for i in range(0, int(config.plc_analog_output_num)):
    st = nc_plc.PLCAnalogOutput(i)
    plc_analog_output.append(st)

plc_middle_input_data_list = []
for i in range(int(config.plc_middle_input_data_num_iw_int)):
    params = nc_plc.PLCMiddleVarsIW(i)
    plc_middle_input_data_list.append(params)

plc_middle_output_data_list = []
for i in range(int(config.plc_middle_output_data_num_qw_int)):
    params = nc_plc.PLCMiddleVarsQW(i)
    plc_middle_output_data_list.append(params)

"""
数据项
# 8. 通道变量
"""
kinematics_setting = nc_channel.KinematicsSetting()
rtcp_tool_base_length = nc_channel.ToolBaseLength()
rtcp_first_rotation_center_coordinates_x = nc_channel.FirstRotationCenterCoordinatesX()
rtcp_second_rotation_center_coordinates_x = (
    nc_channel.SecondRotationCenterCoordinatesX()
)
rtcp_second_rotation_center_coordinates_y = (
    nc_channel.SecondRotationCenterCoordinatesY()
)
rtcp_status = nc_channel.RtcpStatus()
