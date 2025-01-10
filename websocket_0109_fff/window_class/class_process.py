from window_class import class_window as window
from data_api import nc_data as data


class ProcessWindow(window.WindowTable):
    def __init__(self):
        super().__init__()

    def init_table(self):
        self.add_item(data.task_mode)
        self.add_item(data.current_coordinate)
        self.add_item(data.ipcts_coordinate_x)
        self.add_item(data.ipcts_coordinate_y)
        self.add_item(data.ipcts_coordinate_z)
        self.add_item(data.ipcts_coordinate_a)
        self.add_item(data.ipcts_coordinate_b)
        self.add_item(data.ipcts_coordinate_c)
        self.add_item(data.ipcts_coordinate_u)
        self.add_item(data.ipcts_coordinate_v)
        self.add_item(data.ipcts_coordinate_w)

        self.add_item(data.feedrate)
        self.add_item(data.current_feed_velocity)
        self.add_item(data.set_feed_velocity)
        self.add_item(data.spindle_0_rate)
        self.add_item(data.spindle_0_speed)
        self.add_item(data.spindle_0_homed)
        self.add_item(data.spindle_0_setting_speed)
        self.add_item(data.spindle_0_current_position)

        for item in data.axis_enabled:
            self.add_item(item)

        for item in data.actual_position:
            self.add_item(item)

        # [3003] 轴目标位置-MCS
        for item in data.axis_target_position:
            self.add_item(item)

        self.add_item(data.x_velocity)
        self.add_item(data.y_velocity)
        self.add_item(data.z_velocity)
        self.add_item(data.a_velocity)
        self.add_item(data.b_velocity)
        self.add_item(data.c_velocity)
        self.add_item(data.u_velocity)
        self.add_item(data.v_velocity)
        self.add_item(data.w_velocity)
        # [3001] 轴回参考点
        for item in data.axis_homed:
            self.add_item(item)

        # [3004] 轴余程-MCS
        for item in data.axis_remaining_distance:
            self.add_item(item)

        for item in data.actual_position_wcs:
            self.add_item(item)

        for item in data.actual_target_position_wcs:
            self.add_item(item)
        self.add_item(data.G95x_Code)
        self.add_item(data.G_Code)
        self.add_item(data.G21x_Code)
        self.add_item(data.M_Code)

        self.add_item(data.Get_Tool_Table_Info)
        self.add_item(data.G41G42_Info)
        self.add_item(data.Manual_Tool_X)
        self.add_item(data.Manual_Tool_Y)
        self.add_item(data.Manual_Tool_Z)
        self.add_item(data.G43_Effect)
        self.add_item(data.G41G42_Effect)
        self.add_item(data.T_Effect)
        self.add_item(data.tool_count)
        self.add_item(data.tool_diameter)
        self.add_item(data.tool_length_x)
        self.add_item(data.tool_length_y)
        self.add_item(data.tool_length_z)
        self.add_item(data.G40_Effect)
        self.add_item(data.G49_Effect)
        self.add_item(data.axis_0_accel)
        self.add_item(data.axis_1_accel)
        self.add_item(data.axis_2_accel)

        self.add_item(data.program_name)
        self.add_item(data.program_line)
        self.add_item(data.rcs_state)

        self.add_item(data.ipc_operational_status)
        self.add_item(data.process_time)
        self.add_item(data.process_task_status)
        self.add_item(data.program_finished)
        self.add_item(data.program_load_percentage)

        self.add_item(data.current_rotation_xy)

        self.add_item(data.spindle_enable_status)
        self.add_item(data.feed_enable_status)

        # [5207] G92零偏实际
        for item in data.g92_current_offset:
            self.add_item(item)

        self.add_item(data.process_num)
        self.add_item(data.workpiece_id)
        self.add_item(data.spindle_load)
        self.add_item(data.jump_segment_mode)

        self.add_item(data.f_effect)
        self.add_item(data.s_effect)

        self.add_item(data.mdi_current_line)

        self.add_item(data.current_tool_id)
