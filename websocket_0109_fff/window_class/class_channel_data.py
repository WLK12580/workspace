from window_class import class_window as window
from data_api import nc_data as data


class ChannelDataWindow(window.WindowTable):
    def __init__(self):
        super().__init__()

    def init_table(self):
        self.add_item(data.kinematics_setting)
        self.add_item(data.rtcp_tool_base_length)
        self.add_item(data.rtcp_first_rotation_center_coordinates_x)
        self.add_item(data.rtcp_second_rotation_center_coordinates_x)
        self.add_item(data.rtcp_second_rotation_center_coordinates_y)
        self.add_item(data.rtcp_status)