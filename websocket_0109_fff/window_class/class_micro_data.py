import config
from window_class import class_window as window
from data_api import nc_data as data
from data_class import class_param as class_param


class MicroDataWindow(window.WindowTable):
    def __init__(self):
        super().__init__()

    def init_table(self):
        self.add_item(data.task_mode)
        self.add_item(data.current_coordinate)
        # [3001] Öá»Ø²Î¿¼µã
        for item in data.axis_homed:
            self.add_item(item)

        for i in range(0, int(config.micro_num)):
            self.add_item(data.microy[i])

    @staticmethod
    def update_micro():
        class_param.MicroData.update_all()
