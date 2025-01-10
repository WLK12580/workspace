import config
from window_class import class_window as window
from data_api import nc_data as data
from data_class import class_ncplc as ncplc


class NcPlcDataWindow(window.WindowTable):
    def __init__(self):
        super().__init__()

    def init_table(self):
        # self.add_item(self.add_item(data.x_velocity))
        print("NcPlcDataWindow init_table")