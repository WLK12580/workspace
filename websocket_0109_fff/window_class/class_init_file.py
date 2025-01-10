from window_class import class_window as window
from data_api import nc_data as data


class InitConfigFile(window.WindowTable):
    def __init__(self):
        super().__init__()

    def init_table(self):
        self.add_item(data.ipcts_coordinate_x)
        self.add_item(data.ipcts_coordinate_y)
        self.add_item(data.ipcts_coordinate_z)
        self.add_item(data.ipcts_coordinate_a)
        self.add_item(data.ipcts_coordinate_b)
        self.add_item(data.ipcts_coordinate_c)
        self.add_item(data.ipcts_coordinate_u)
        self.add_item(data.ipcts_coordinate_v)
        self.add_item(data.ipcts_coordinate_w)
        self.add_item(data.axis_list)

        self.add_item(data.axis_count)
        self.add_item(data.spindle_count)

        self.add_item(data.history_alarm_file_name)

        self.add_item(data.G43_Effect)
        self.add_item(data.G41G42_Effect)
        self.add_item(data.Get_Tool_Table_Info)

        self.add_item(data.joint_0_pitch_comp_type)
        self.add_item(data.joint_1_pitch_comp_type)
        self.add_item(data.joint_2_pitch_comp_type)
        self.add_item(data.joint_3_pitch_comp_type)
        self.add_item(data.joint_4_pitch_comp_type)
        self.add_item(data.joint_5_pitch_comp_type)
        self.add_item(data.joint_6_pitch_comp_type)
        self.add_item(data.joint_7_pitch_comp_type)
        self.add_item(data.joint_8_pitch_comp_type)
        self.add_item(data.joint_0_pitch_comp_setting)
        self.add_item(data.joint_1_pitch_comp_setting)
        self.add_item(data.joint_2_pitch_comp_setting)
        self.add_item(data.joint_3_pitch_comp_setting)
        self.add_item(data.joint_4_pitch_comp_setting)
        self.add_item(data.joint_5_pitch_comp_setting)
        self.add_item(data.joint_6_pitch_comp_setting)
        self.add_item(data.joint_7_pitch_comp_setting)
        self.add_item(data.joint_8_pitch_comp_setting)

        self.add_item(data.ipc_program_path)

        # [5208] 轴Offset是否使能标志（设定值）
        for item in data.offset_enable:
            self.add_item(item)

        # [5209] 轴Offset是否使能标志（实际值）
        for item in data.offset_actual_enable:
            self.add_item(item)

        # [101081] 示波器频率列表
        self.add_item(data.scope_frequency_list)
