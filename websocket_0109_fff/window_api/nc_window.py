
from window_class import class_alarm_data
from window_class import class_axis_data
from window_class import class_init_file
from window_class import class_micro_data
from window_class import class_offset_data
from window_class import class_process
from window_class import class_system_data
from window_class import class_tool_data
from window_class import class_ncplc_data
from window_class import class_diagnosis_data
from window_class import class_micro_program_data
from window_class import class_channel_data
from window_class import class_plc_data

current_alarm = class_alarm_data.CurrentAlarm()
axis_data_window = class_axis_data.AxisDataWindow()
init_files = class_init_file.InitConfigFile()
micro_data_window = class_micro_data.MicroDataWindow()
offset_data_window = class_offset_data.OffsetDataWindow()
process_window = class_process.ProcessWindow()
system_data_window = class_system_data.SystemDataWindow()
tool_data_window = class_tool_data.ToolDataWindow()
ncplc_data_window = class_ncplc_data.NcPlcDataWindow()
diagnosis_data_window = class_diagnosis_data.DiagnosisDataWindow()
micro_program_data_window = class_micro_program_data.MicroProgramDataWindow()
channel_data_window = class_channel_data.ChannelDataWindow()

plc_params_window=class_plc_data.CurrentPLCData() #获取PLC的参数 用于plc监控

