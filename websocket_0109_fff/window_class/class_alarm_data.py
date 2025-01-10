from window_class import class_window as window
from data_api import nc_data as data
from data_class import nc_module as module


class CurrentAlarm(window.WindowTable):
    def __init__(self):
        self._alarm_device = self._device = module.DeviceNode("02",
                                         "HMC-5Axis",
                                         "MACHINE",
                                         "当前报警")
        super().__init__()

    def init_table(self):
        self.add_item(data.tool_Change)
        self.add_item(data.toolPoc_Update)
        self.add_item(data.m6_finish)
        self.add_item(data.ipc_operational_status)
        self.add_item(data.estop_status)
        # self.add_item(data.axis_0_cmdPos)
        # self.add_item(data.axis_1_cmdPos)
        # self.add_item(data.axis_2_cmdPos)
        # self.add_item(data.axis_3_cmdPos)
        # self.add_item(data.axis_4_cmdPos)
        # self.add_item(data.axis_5_cmdPos)
        # self.add_item(data.axis_6_cmdPos)
        # self.add_item(data.axis_7_cmdPos)
        # self.add_item(data.axis_8_cmdPos)
        self.add_item(data.single_block_status)
        self.add_item(data.current_set_Coordinate)

        # [500008]-[500016] 当前零偏x-w
        for item in data.g5x_offset:
            self.add_item(item)

        self.add_item(data.process_time)

        self.add_item(data.cutter_measure_done)
        self.add_item(data.cutter_measure_reset)
        self.add_item(data.cutter_number_of_head)
        # self.add_item(data.x_current_position)
        # self.add_item(data.y_current_position)
        # self.add_item(data.z_current_position)
        # self.add_item(data.a_current_position)
        # self.add_item(data.b_current_position)
        # self.add_item(data.c_current_position)
        # self.add_item(data.u_current_position)
        # self.add_item(data.v_current_position)
        # self.add_item(data.w_current_position)
        for item in data.actual_position:
            self.add_item(item)

        # [5207] G92零偏实际
        for item in data.g92_current_offset:
            self.add_item(item)

        for i in range(1, 51):
            self.add_item(data.tool_hal_Index[i - 1])
        self.add_item(data.program_name)
        self.add_item(data.position_finished_flag)

        self.add_item(data.sp0_mode_status)
        self.add_item(data.sp1_mode_status)
        self.add_item(data.spindle_orientation)
        self.add_item(data.sp1_orient)

        # 圆度测试
        self.add_item(data.current_motion_type)
        for item in data.actual_position_wcs:
            self.add_item(item)

        self.add_item(data.rtcp_status)
        self.add_item(data.scope_export_file_flag)
        self.add_item(data.scope_sample_frequency)
