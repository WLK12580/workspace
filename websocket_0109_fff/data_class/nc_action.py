import hal
import config
from data_class import nc_module as module

from qtvcp.core import Status

STATUS = Status()

coordinate_info = ["G54", "G55", "G56", "G57", "G58", "G59"]


def ensure_mode(*modes):
    truth, premode = STATUS.check_for_modes(modes)
    if truth is False:
        module.command.mode(modes[0])
        module.command.wait_complete()
        return True, premode
    else:
        return truth, premode


# 当前坐标系设定工件坐标目标值
def set_axis_origin(axis: str, value: str):
    """
    :param axis:
    :param value:
    :return:
    """
    param_axis = module.axis_list[int(axis)]
    m = "G10 L20 P0 %s%s" % (param_axis, value)
    print(m)
    fail, premode = ensure_mode(module.linuxcnc.MODE_MDI)
    module.command.mdi(m)
    module.command.wait_complete()
    ensure_mode(premode)
    STATUS.emit('reload-display')


# 当前坐标系设定工件坐标目标值
def set_curr_coordinate(coordinate: str):
    """
    :param coordinate: 坐标系 G54～G59
    :return:
    """
    if coordinate == "G54" or coordinate == "G55" or coordinate == "G56" or coordinate == "G57" or coordinate == "G58" or coordinate == "G59":
        print(coordinate)
        fail, premode = ensure_mode(module.linuxcnc.MODE_MDI)
        module.command.mdi(coordinate)
        module.command.wait_complete()
        ensure_mode(premode)
        STATUS.emit('reload-display')


# 服务器重置解析器
def server_reset_interpreter():
    module.update()
    if hal.get_value(config.halpin_axis_all_homed):
        print("server_reset_interpreter")
        module.command.reset_interpreter()
        module.command.wait_complete()
        fail, premode = ensure_mode(module.linuxcnc.MODE_MDI)
        module.command.mdi("G49")
        module.command.wait_complete()
        ensure_mode(premode)
        STATUS.emit('reload-display')
        # module.command.reset_interpreter()


# 设置宏变量
def set_macro(index: int, value: str):
    m = "#%s = %s" % (str(index), value)
    print(m)
    fail, premode = ensure_mode(module.linuxcnc.MODE_MDI)
    module.command.mdi(m)
    module.command.wait_complete()
    ensure_mode(premode)
    STATUS.emit('reload-display')


# 清空mdi文件
def clear_mdi_file():
    with open(module.MdiPath, "w") as file:
        pass
