from window_class import class_window as window
from data_api import nc_data as data


class OffsetDataWindow(window.WindowTable):
    def __init__(self):
        super().__init__()

    def init_table(self):
        self.add_item(data.g5x_Index)
        # [500008]-[500016] 当前零偏x-w
        for item in data.g5x_offset:
            self.add_item(item)

        # [52000] G54零偏
        for item in data.g54_offset:
            self.add_item(item)

        # [5201] G55零偏
        for item in data.g55_offset:
            self.add_item(item)

        # [5202] G56零偏
        for item in data.g56_offset:
            self.add_item(item)

        # [5203] G57零偏
        for item in data.g57_offset:
            self.add_item(item)

        # [5204] G58零偏
        for item in data.g58_offset:
            self.add_item(item)

        # [5205] G59零偏
        for item in data.g59_offset:
            self.add_item(item)

        # [5206] G92零偏设定值
        for item in data.g92_target_offset:
            self.add_item(item)

        # [5207] G92零偏实际
        for item in data.g92_current_offset:
            self.add_item(item)

        self.add_item(data.G_Code)
        # [3001] 轴回参考点
        for item in data.axis_homed:
            self.add_item(item)
