from data_class import nc_module as nc_module


# NC/PLC类
class NcPlcItem:
    # 存储NC变量列表
    _nc_vars = []
    _microFlag = False

    def __init__(self):
        """
        """
    # 添加数据
    @staticmethod
    def add_item(index: str):
        item = nc_module.IpcPostHandler.get_obj(index)
        if item is not None:
            if int(index) in range(530000, 535499):
                _microFlag = True
            NcPlcItem._nc_vars.append(item)

    # 清空数据
    @staticmethod
    def clear_item():
        _microFlag = False
        NcPlcItem._nc_vars = []

    @property
    def microFlag(self):
        return self._microFlag
