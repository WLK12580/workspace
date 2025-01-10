from data_class import nc_module as module
import linuxcnc


# 当前程序名
class CurrentProgramName(module.DataNode):
    def __init__(self):
        index = "100002"
        name = "current_program_name"
        super().__init__(index, name, "VARIABLE")

    def value(self):
        return module.stat.file


# 当前程序执行行
class CurrentProgramLine(module.DataNode):
    def __init__(self):
        index = "100003"
        name = "current_program_line"
        super().__init__(index, name, "VARIABLE")

    def value(self):
        return str(module.stat.motion_line)


# 当前子程序深度
class CurrentCallLevel(module.DataNode):
    def __init__(self):
        index = "100004"
        name = "current_call_level"
        super().__init__(index, name, "VARIABLE")

    def value(self):
        return module.stat.call_level


# 当前命令执行状态
class CurrentExecutionStatus(module.DataNode):
    def __init__(self):
        index = "100005"
        name = "rcs_state"
        super().__init__(index, name, "VARIABLE")

    def value(self):
        if module.stat.state == linuxcnc.RCS_DONE:
            return "done"
        elif module.stat.state == linuxcnc.RCS_EXEC:
            if module.stat.task_paused == 1:
                return "pause"
            elif module.stat.task_paused == 0:
                return "exec"
        elif module.stat.state == linuxcnc.RCS_ERROR:
            return "error"
        else:
            return "NONE"


# 加载程序进度百分比
class ProgramLoadPercentage(module.DataNode):
    def __init__(self):
        index = "100022"
        name = "program_load_percentage"
        self.counter = 0  # 计数器 加载完成后连续发5次100后清0
        super().__init__(index, name, "VARIABLE")

    def value(self):
        if module.program_load_percentage == 100:
            self.counter += 1
            if self.counter >= 10:

                module.program_load_percentage = 100
                self.counter = 0
        return str(int(module.program_load_percentage))


# 加载程序进度百分比
class IPCProgramPath(module.DataNode):
    def __init__(self):
        index = "100023"
        name = "ipc_program_path"
        super().__init__(index, name, "VARIABLE")

    def value(self):
        if module.ipc_program_path is not None:
            return str(module.ipc_program_path)
        else:
            return "NULL"
