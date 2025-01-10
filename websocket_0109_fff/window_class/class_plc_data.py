from window_class import class_window as window
from data_api import nc_data as data
from data_class import nc_module as module
import config

class CurrentPLCData(window.WindowTable):
    def __init__(self):  # 初始化
        super().__init__()
    def init_table(self):
        # plc 数字量输入
        for item in data.plc_digital_input:
            self.add_item(item)
        # plc 数字量输出
        for item in data.plc_digital_output:
            self.add_item(item)
        # plc 模拟量输入
        for item in data.plc_analog_input:
            self.add_item(item)
        # plc 模拟量输出
        for item in data.plc_analog_output:
            self.add_item(item)
        # plc 中间变量 iw
        for item in data.plc_middle_input_data_list:
            self.add_item(item)
        # plc 中间变量 qw
        for item in data.plc_middle_output_data_list:
            self.add_item(item)