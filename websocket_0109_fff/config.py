import configparser
import time
from datetime import datetime
import os

# ini_path = "/usr/local/bin/main/conf.ini"
ini_path = "conf.ini"
ini = configparser.ConfigParser()
ini.read(ini_path)

# 网络
ip = ini.get("NETWORK", "IP")
port = ini.get("NETWORK", "PORT")
username = ini.get("NETWORK", "USERNAME")
folder_name = ini.get("NETWORK", "FOLDER_NAME")
nc_ini_name = ini.get("NETWORK", "NC_INI_NAME")
# hal组件名称
component = str(int(time.time()))
# 刀具
tblPath = ini.get("TOOL", "PATH")
newtblPath = ini.get("TOOL", "NEWPATH")
# 宏变量
path = ini.get("PARAM", "PATH")
microPath = ini.get("PARAM", "MICPATH")

# 定位
position_spindle = ini.get("TARGET_POSITION", "SPINDLE_AXIS")
position_spindle_list = position_spindle.split()
# 限位
# 软限位轴名
softlimit_axis = ini.get("LIMIT","SOFTLIMIT")
softlimit_axis_list = softlimit_axis.split()
# 硬限位轴名
hardlimit_axis = ini.get("LIMIT","HARDLIMIT")
hardlimit_axis_list = hardlimit_axis.split()

# 驱动器报警
# 驱动器报警轴名
drive_alarm_axis = ini.get("DRIVE_ALARM","DRIVE_ALARM_AXIS")
drive_alarm_axis_list = drive_alarm_axis.split()

# hal引脚
# 复位
halpin_reset = ini.get("HAL","RESET")
# 服务器复位
halpin_server_reset = ini.get("HAL","SERVER_RESET")
# nc报警
halpin_alarm = ini.get("HAL","NC_ALARM")

# 软限位报警
halpin_neg_softlimit = ini.get("HAL","NEG_SOFTLIMIT")
halpin_pos_softlimit = ini.get("HAL","POS_SOFTLIMIT")
# 硬限位报警
halpin_neg_hardlimit = ini.get("HAL","NEG_HARDLIMIT")
halpin_pos_hardlimit = ini.get("HAL","POS_HARDLIMIT")
# 驱动报警
halpin_drive_alarm = ini.get("HAL","DRIVE_ALARM_PIN")



# ipc_handler
# 执行mdi
halpin_mdi_excute = ini.get("HAL", "MDI_EXCUTE")
# 复位mdi
halpin_mdi_reset = ini.get("HAL", "MDI_RESET")
# 执行定位
halpin_position_excute = ini.get("HAL", "POSITION_EXCUTE")
# 复位定位
halpin_position_reset = ini.get("HAL", "POSITION_RESET")
# 定位模式标志
halpin_position_flag = ini.get("HAL", "POSITION_FLAG")
# 定位暂停
halpin_position_pause = ini.get("HAL", "POSITION_PAUSE")
# 定位恢复
halpin_position_resume = ini.get("HAL", "POSITION_RESUME")
# 定位状态
halpin_position_state = ini.get("HAL", "POSITION_STATE")
# 执行跳段
halpin_jump_segment_excute = ini.get("HAL", "JUMP_SEGMENT_EXECUTE")
# 复位跳段
# halpin_jump_segment_reset = ini.get("HAL", "JUMP_SEGMENT_RESET")
# 跳段模式标志
halpin_jump_segment_flag = ini.get("HAL", "JUMP_SEGMENT_FLAG")


# ipc状态-报警
halpin_ipc_alarm = ini.get("HAL", "IPC_ALARM")

# 主轴回零
halpin_spindle_0_homed: str = ini.get("HAL", "SPINDLE_0_HOEMD")

# ECAT状态检测
halpin_ecat_allop = ini.get("HAL", "ECAT_ALLOP")

# 执行PO下使能
halpin_po_machineOff = ini.get("HAL","PO_MACHINE_OFF")

# 进给速率
halpin_feed_velocity = ini.get("HAL","FEED_VELOCITY")
# 设定速度
halpin_feed_setting_vel = ini.get("HAL", "FEED_SETTING_VEL")

# 手动模式下进给倍率
halpin_feed_rate = ini.get("HAL", "JOG_FEEDRATE")

# 程序是否下发完成
halpin_program_is_ok = ini.get("HAL", "PROGRAM_IS_OK")

# 刀具报警引脚
halpin_tool_alarm = ini.get("HAL", "TOOL_ALARM_PIN")

# 轴加速度
halpin_axis_acc = ini.get("HAL", "AXIS_ACC")
# 刀具初始化
halpin_tool_update = ini.get("HAL", "TOOL_UPDATE")
# 程序未加载报警
halpin_program_not_ready = ini.get("HAL", "PROGRAM_NOT_READY")

# 刀具和工件测量完成信号
cutter_meassure_done=ini.get("HAL","cutter_meassure_done")
cutter_meassure_reset=ini.get("HAL","cutter_meassure_reset")
#到盘中指向取刀口的刀号
cutter_number_of_head=ini.get("HAL","cutter_number_of_head")
# 主轴使能
halpin_spindle_enable = ini.get('HAL', 'SPINDLE_ENABLE')
# 主轴掉使能
halpin_spindle_disable = ini.get('HAL', 'SPINDLE_DISABLE')
# 进给掉使能
halpin_feed_disable = ini.get('HAL', 'FEED_DISABLE')
# 进给使能
halpin_feed_enable = ini.get('HAL', 'FEED_ENABLE')

# EtherCAT检测从站掉线报警
halpin_ecat_lost_slave = ini.get('HAL', 'ECAT_LOST_SLAVE_ALARM')
# 主轴缺少使能提示
halpin_spindle_not_enabled_warn = ini.get('HAL', 'SPINDLE_NOT_ENABLED_WARN')
# 进给缺少使能提示
halpin_feed_not_enabled_warn = ini.get('HAL', 'FEED_NOT_ENABLED_WARN')
# 轴全部回零信号
halpin_axis_all_homed = ini.get('HAL', 'AXIS_ALL_HOMED')
# 轴诊断—轴信息
halpin_torque = ini.get("AXISINFOS", "TORQUE_HAL")
halpin_backlash_vel = ini.get("AXISINFOS", "BACKLASH_VEL_HAL")
halpin_backlash_filt = ini.get("AXISINFOS", "BACKLASH_FILT_HAL")
halpin_backlash_cor = ini.get("AXISINFOS", "BACKLASH_COR_HAL")
halpin_follow_error = ini.get("AXISINFOS", "FOLLOW_ERROR_HAL")
halpin_follow_limit = ini.get("AXISINFOS", "FOLLOW_ERROR_LIMIT_HAL")
halpin_target_position = ini.get("AXISINFOS", "TARGET_POSITION_HAL")
halpin_act_position = ini.get("AXISINFOS", "ACT_POSITION_HAL")
halpin_target_velocity = ini.get("AXISINFOS", "TARGET_VELOCITY_HAL")
halpin_act_velocity = ini.get("AXISINFOS", "ACT_VELOCITY_HAL")
halpin_type_1 = ini.get("AXISINFOS", "INDEX_DEF_1")
halpin_type_2 = ini.get("AXISINFOS", "INDEX_DEF_2")

# 工件号
halpin_workpiece_id = ini.get("HAL", "WORKPIECE_ID")
# 加工数量
halpin_process_num = ini.get("HAL", "PROCESS_NUM")
# 主轴切削负载
halpin_spindle_load = ini.get("HAL", "SPINDLE_LOAD")
# 主轴当前位置
halpin_spindle_current_position = ini.get("HAL", "SPINDLE_CURRENT_POSITION")

# 主轴实际速度
halpin_spindle_vel = ini.get("HAL", "SPINDLE_VEL")
# 主轴指令速度
halpin_spindle_setting_vel = ini.get("HAL", "SPINDLE_SETTING_VEL")

# 单段状态
halpin_single_block_status = ini.get("HAL", "SINGLE_BLOCK_STATUS")
# 单段运行模式
halpin_single_block_running_mode = ini.get("HAL", "SINGLE_BLOCK_RUNNING_MODE")
# 主轴0-模式状态
halpin_sp0_mode_status = ini.get("HAL", "SP0_MODE_STATUS")
# 主轴1-模式状态
halpin_sp1_mode_status = ini.get("HAL", "SP1_MODE_STATUS")

# 当前刀号
halpin_current_tool_id = ini.get("HAL", "CURRENT_TOOL_ID")

##########
# 报警是否生效
##########
is_activate_ecat_allop = ini.get("ALARMS", "ECAT")
##########
# PLC开放的数据个数

plc_digital_input_num = ini.get("PLC", "DIGITAL_INPUT_NUM")# 数字量输入：bool
plc_digital_output_num = ini.get("PLC", "DIGITAL_OUTPUT_NUM") # 数字量输出：bool
plc_analog_input_num = ini.get("PLC", "ANALOG_INPUT_NUM") #模拟量输入：float
plc_analog_output_num = ini.get("PLC", "ANALOG_OUTPUT_NUM") #模拟量输出 ：float
# plc_middle_var_num_bool=ini.get("PLC","middle_var_num") #PLC的中间变量，类型为bool plc那边暂未开发出来，
plc_middle_input_data_num_iw_int=ini.get("PLC","middle_input_num") #PLC中间变量：int类型
plc_middle_output_data_num_qw_int=ini.get("PLC","middle_output_num") #PLC中间变量：int类型

##########
# 宏变量开放的数据个数
micro_num = ini.get("MICRO", "MICRO_NUM")
micro_program_path = ini.get("MICRO", "SUBROUTINES")
# 监控通道频率
freq_alarm_monitor = ini.get("ALARMS","MONITOR_FREQ")
# 检测报警频率
freq_alarm_detect = ini.get("ALARMS","DETECT_FREQ")

##########
# 示波器
##########
scope_config_name = ini.get("SCOPE", "CONF_PATH")
scope_data_name = ini.get("SCOPE", "DATA_PATH")
scope_bind_channel_counts = ini.get("SCOPE", "BIND_CHANNEL_COUNTS")
scope_reload_config = ini.get("SCOPE", "RELOAD_CONFIG")
scope_start_sample = ini.get("SCOPE", "SCOPE_START_SAMPLE")
scope_stop_sample = ini.get("SCOPE", "SCOPE_STOP_SAMPLE")
scope_export_flag = ini.get("SCOPE", "EXPORT_FLAG")
scope_frequency_list = ini.get("SCOPE", "SCOPE_SAMPLE_FREQUENCY")

##########
# 路径
##########
# 历史报警存放路径
current_datetime = datetime.now().strftime("%Y%m%d%H%M%S")
history_alarm_file = "history_" + current_datetime + ".txt"
history_alarm_path = "/home/"+username+"/share/history/"+history_alarm_file
# 宏变量
micPath = "/home/" + username + "/linuxcnc/configs/" + folder_name + "/" + microPath
# 零偏
offsetPath = "/home/" + username + "/linuxcnc/configs/" + folder_name + "/" + path
# 刀具
tool_table_path = "/home/" + username + "/linuxcnc/configs/" + folder_name + "/" + tblPath
new_tool_table_path = "/home/" + username + "/linuxcnc/configs/" + folder_name + "/" + newtblPath
# 示波器
scope_config_path = "/home/" + username + "/linuxcnc/configs/" + folder_name + "/" + scope_config_name
scope_data_path = "/home/" + username + "/linuxcnc/configs/" + folder_name + "/" + scope_data_name

##########
# 零偏是否使能
##########
coordinate_config_path = ini.get("COORDINATE", "CONFIG")
coordinate_ini = configparser.ConfigParser()
coordinate_ini.read(coordinate_config_path)
offset_enable = [coordinate_ini.get("COORDINATE", "JOINT_0_OFFSET_ENABLE"),
                 coordinate_ini.get("COORDINATE", "JOINT_1_OFFSET_ENABLE"),
                 coordinate_ini.get("COORDINATE", "JOINT_2_OFFSET_ENABLE"),
                 coordinate_ini.get("COORDINATE", "JOINT_3_OFFSET_ENABLE"),
                 coordinate_ini.get("COORDINATE", "JOINT_4_OFFSET_ENABLE"),
                 coordinate_ini.get("COORDINATE", "JOINT_5_OFFSET_ENABLE"),
                 coordinate_ini.get("COORDINATE", "JOINT_6_OFFSET_ENABLE"),
                 coordinate_ini.get("COORDINATE", "JOINT_7_OFFSET_ENABLE"),
                 coordinate_ini.get("COORDINATE", "JOINT_8_OFFSET_ENABLE")]
##########
# 轴诊断
##########
axis_ready_to_switch_on = ini.get("AXIS_DIAGNOSIS","READY_TO_SWITCH_ON")
axis_switch_on = ini.get("AXIS_DIAGNOSIS","SWITCH_ON")
axis_operation_enabled = ini.get("AXIS_DIAGNOSIS","OPERATION_ENABLED")
axis_fault = ini.get("AXIS_DIAGNOSIS","FAULT")
axis_voltage_enabled = ini.get("AXIS_DIAGNOSIS","VOLTAGE_ENABLED")
axis_quick_stop = ini.get("AXIS_DIAGNOSIS","QUICK_STOP")
axis_switch_on_disabled = ini.get("AXIS_DIAGNOSIS","SWITCH_ON_DISABLED")
axis_warning = ini.get("AXIS_DIAGNOSIS","WARNING")

axis_remote = ini.get("AXIS_DIAGNOSIS","REMOTE")
axis_target_reach = ini.get("AXIS_DIAGNOSIS","TARGET_REACH")
axis_internal_limit_active = ini.get("AXIS_DIAGNOSIS","INTERNAL_LIMIT_ACTIVE")
axis_set_point_acknowledge = ini.get("AXIS_DIAGNOSIS","SET_POINT_ACKNOWLEDGE")
axis_following_error = ini.get("AXIS_DIAGNOSIS","FOLLOWING_ERROR")
axis_torque_limit_active = ini.get("AXIS_DIAGNOSIS","TORQUE_LIMIT_ACTIVE")
axis_home_find = ini.get("AXIS_DIAGNOSIS", "HOME_FIND")

##########
# RTCP
##########
kinematics_setting_0 = ini.get("RTCP", "KINEMATICS_SETTING_0")
kinematics_setting_1 = ini.get("RTCP", "KINEMATICS_SETTING_1")
kinematics_setting_1_halcmd_1 = ini.get("RTCP", "KINEMATICS_SETTING_1_HALCMD1")
kinematics_setting_1_halcmd_2 = ini.get("RTCP", "KINEMATICS_SETTING_1_HALCMD2")

rtcp_tool_base_length = ini.get("RTCP", "RTCP_TOOL_BASE_LENGTH")
rtcp_first_rotation_center_coordinates_x = ini.get("RTCP", "RTCP_FIRST_ROTATION_CENTER_COORDINATES_X")
rtcp_second_rotation_center_coordinates_x = ini.get("RTCP", "RTCP_SECOND_ROTATION_CENTER_COORDINATES_X")
rtcp_second_rotation_center_coordinates_y = ini.get("RTCP", "RTCP_SECOND_ROTATION_CENTER_COORDINATES_Y")

rtcp_status = ini.get("RTCP", "RTCP_STATUS")

print(ip)
print(port)
print(username)
print(component)

print("halpin_reset: " + halpin_reset)
print("cutter_meassure_done= "+cutter_meassure_done)
print("cutter_meassure_reset= "+cutter_meassure_reset)

print("halpin_alarm: " + halpin_alarm)
print("halpin_mdi_excute: " + halpin_mdi_excute)
print("halpin_mdi_reset: " + halpin_mdi_reset)
print("halpin_position_excute: " + halpin_position_excute)
print("halpin_position_reset: " + halpin_position_reset)
print("halpin_position_flag: " + halpin_position_flag)
print("halpin_ipc_alarm: " + halpin_ipc_alarm)
print("halpin_spindle_0_homed" + halpin_spindle_0_homed)
print("halpin_program_is_ok" + halpin_program_is_ok)
print("halpin_tool_alarm" + halpin_tool_alarm)
print("********************************************")
print("soft limit axis count:" + str(len(softlimit_axis_list)))
print("hard limit axis count:" + str(len(hardlimit_axis_list)))
print("PATH********************************************")
print("history alarm path:"+history_alarm_path)
print("micPath: " + micPath)
print("offsetPath: " + offsetPath)
print("tool_table_path: " + tool_table_path)
print("new_tool_table_path: " + new_tool_table_path)
print("scope_config_path: " + scope_config_path)
print("scope_data_path: " + scope_data_path)
# print("halpin_jog_spindle_vel" + halpin_jog_spindle_vel)