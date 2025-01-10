from data_class import nc_module as module
from abc import ABC
from abc import abstractmethod


class WindowTable(ABC):
    def __init__(self):
        self._root = module.DataRoot("01",
                                     "数控设备模型文件",
                                     "HTTP_TORNADO",
                                     "基于Tornado框架的HTTP协议格式内容")
        self._device = module.DeviceNode("01",
                                         "HMC-5Axis",
                                         "MACHINE",
                                         "五轴数控机床")
        self._root.add_device(self._device)
        self.init_table()

    def add_device(self,item:module.DeviceNode):
        self._root.add_device(item)

    def add_item(self, item: module.DataNode):
        self._device.add_data_item(item)

    @abstractmethod
    def init_table(self):
        """
        填充数据表中的数据
        """

    def data(self):
        module.update()
        return self._root.data()

    def clear(self):
        self._device.clear()
