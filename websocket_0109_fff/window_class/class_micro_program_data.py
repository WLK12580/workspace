import config
from window_class import class_window as window
from data_api import nc_data as data


class MicroProgramDataWindow(window.WindowTable):
    def __init__(self):
        super().__init__()

    def init_table(self):
        self.add_item(data.micro_program)
