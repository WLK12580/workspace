from data_class import nc_module as module
from task_mdi import target_position as target_position
import config
import hal
import json
import time

component = config.component
h = hal.component(str(int(time.time()) + 1))


class IpcOperationalStatus(module.DataNode):
    def __init__(self):
        index = "540003"
        name = "operational_status"
        super().__init__(index, name, "VARIABLE")

    def value(self):
        """
        if hal.get_value("halui.machine.is-on") == 0:
            return "not ready"
        else:
            if hal.get_value("halui.program.is-idle") == 1:
                return "idle"
            elif hal.get_value(config.halpin_ipc_alarm) == 1:
                return "alarm"
            elif hal.get_value("halui.program.is-running") == 1:
                return "running"
            elif hal.get_value("halui.program.is-paused") == 1:
                return "pause"
            return "ready"
        """
        if hal.get_value("halui.machine.is-on") == 0:
            return "not ready"
        elif hal.get_value(config.halpin_ipc_alarm) == 1:
            return "alarm"
        else:
            # 自动模式
            if hal.get_value("halui.mode.is-auto") or hal.get_value("halui.mode.is-mdi"):
                if hal.get_value("halui.program.is-idle") == 1:
                    return "idle"
                # 单段模式
                elif hal.get_value(config.halpin_single_block_status):
                    if hal.get_value(config.halpin_single_block_running_mode):
                        return "running"
                    else:
                        return "pause"
                elif hal.get_value("halui.program.is-running") == 1:
                    return "running"
                elif hal.get_value("halui.program.is-paused") == 1:
                    return "pause"
                else:
                    return "ready"
            # 手动模式
            elif hal.get_value("halui.mode.is-manual"):
                if target_position.PositionStateMachine.current_state() == "idle":
                    return "idle"
                elif target_position.PositionStateMachine.current_state() == "exec":
                    return "running"
                elif target_position.PositionStateMachine.current_state() == "pause":
                    return "pause"
                else:
                    return "ready"



class EStopStatus(module.DataNode):
    def __init__(self):
        index = "540004"
        name = "estop_status"
        super().__init__(index, name, "VARIABLE")

    def value(self):
        if module.stat.estop == 1:
            return "1"
        return "0"
