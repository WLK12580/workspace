from data_class import nc_module as module
from data_class import nc_action as action
from data_func import micro_program as micro_program
import config
import math
import hal

current_coordinate = "false"
current_g5x_r = ""
microData = {}
for i in range(1, 1001):
    index_ = 1000 + i
    microData.update({str(index_): (i - 1)})

g5X_Offset = {"g5x_x": 0, "g5x_y": 1, "g5x_z": 2,
              "g5x_a": 3, "g5x_b": 4, "g5x_c": 5,
              "g5x_u": 6, "g5x_v": 7, "g5x_w": 8}

g92_Offset = {"g92_x": 0, "g92_y": 1, "g92_z": 2,
              "g92_a": 3, "g92_b": 4, "g92_c": 5,
              "g92_u": 6, "g92_v": 7, "g92_w": 8}


class MicroData(module.DataNode):
    _data_dict = {}  # 宏变量编号和值键值对

    def __init__(self, num):
        self.micro_id = num

        self.name_id = None     # 宏变量编号
        if 0 <= num <= 999:
            self.name_id = self.micro_id + 1001  # [#1001 - #2000]
        elif 1000 <= num <= 1999:
            self.name_id = self.micro_id - 999  # [#1 - #1000]
        elif 2000 <= num < 5500:
            self.name_id = self.micro_id + 1  # [#2001 - #5500]

        index = str(530000 + num)
        micro_name = "micro_" + str(self.name_id) + "_data"
        super().__init__(index, micro_name, "VARIABLE")

    @staticmethod
    def update_all():
        # 更新全部宏变量参数和值到字典中
        with open(config.micPath, 'r', encoding='utf-8') as file:
            content = file.read()
        lines = content.splitlines()
        for line in lines:
            key, value = line.split('\t')
            MicroData._data_dict[int(key)] = str(value)

    def value(self):
        # 读取内存中的宏变量值
        return str(MicroData._data_dict.get(self.name_id))

    def set_value(self, value):
        tline = str(self.name_id)

        ps = -1
        file = open(config.micPath, 'r')
        content = file.readlines()
        for i, line in enumerate(content):
            if (tline in line):
                ps = i
                break

        if (value == ''):
            content[ps] = tline + '	0'
        else:
            content[ps] = tline + '	{0}'.format(value)
        content[ps] += "\n"
        file.close()
        w = open(config.micPath, 'w')
        w.writelines(content)
        w.close()

        action.server_reset_interpreter()
        if module.ProgramPath is not None:
            module.linuxcnc.command().program_open(module.ProgramPath)


# Current_Coordinate_System
class G5X_Index(module.DataNode):
    def __init__(self):
        index = str(500007)
        g5X_Index_name = "g5X_index"
        super().__init__(index, g5X_Index_name, "VARIABLE")

    def value(self):
        cur_G5X_Index = module.stat.g5x_index
        return cur_G5X_Index


# 当前坐标系零偏
class G5X_Offset(module.DataNode):
    def __init__(self, joint_id: int):
        """
        :param joint_id: 关节号
        :return:
        """
        self.joint_id = joint_id
        if joint_id > module.axis_count:
            self.axis_name = "R"
            self.axis_id = module.axis_count
        else:
            self.axis_name, self.axis_id = module.get_axis_id(joint_id)

        index = str(500008 + self.joint_id)
        param_name = self.axis_name + "_g5x_offset"
        super().__init__(index, param_name, "VARIABLE")

    def value(self):
        return str(module.stat.g5x_offset[self.axis_id])


# mdi设置的当前坐标系
class CurrentSetCoordinate(module.DataNode):
    def __init__(self):
        super().__init__("500021", "CurrentSetCoordinate", "VARIABLE")

    def value(self):
        if current_coordinate == "7_G92":
            return str(current_coordinate)
        return str(current_coordinate + "_" + current_g5x_r)


# 宏程序 - 读
class MicroProgramRemap(module.DataNode):
    def __init__(self):
        super().__init__("500024", "MircoProgramRemap", "VARIABLE")

    def value(self):
        return micro_program.get_mirco_program_data()



# 宏程序 - 写
class MicroProgramRemapWrite(module.DataNode):
    def __init__(self):
        super().__init__("500025", "MicroProgramRemapWrite", "VARIABLE")

    def value(self):
        return " "

    def set_value(self, value):
        micro_program.set_mirco_program_data(value)


#
# G54-Offset
g54_Orign_Index = 5220


class G54_Offset(module.DataNode):
    def __init__(self, joint_id: int):
        """
        :param joint_id: 关节号
        :return:
        """
        self.joint_id = joint_id
        if joint_id > 8:
            self.axis_name = "R"
            self.axis_id = 9
        else:
            self.axis_name, self.axis_id = module.get_axis_id(joint_id)
        self.index = 5221 + self.axis_id

        index = str(520000 + self.joint_id)
        param_name = self.axis_name + "_g54_offset"
        super().__init__(index, param_name, "VARIABLE")

    def value(self):
        ps = -1
        file = open(config.offsetPath, 'r')
        content = file.readlines()
        for i, line in enumerate(content):
            if str(self.index) in line:
                ps = i
                break
        line = content[ps]
        file.close()
        st = line[5:].strip('\n')
        return str(st)

    def set_value(self, value):
        print(self._name)
        tline = str(self.index)
        print(tline)

        ps = -1
        file = open(config.offsetPath, 'r')
        content = file.readlines()
        for i, line in enumerate(content):
            if tline in line:
                ps = i
                break

        if value == '':
            content[ps] = tline + '	0'
        else:
            content[ps] = tline + '	{0}'.format(value)
        content[ps] += "\n"
        file.close()
        w = open(config.micPath, 'w')
        w.writelines(content)
        w.close()

        action.server_reset_interpreter()
        # module.command.reset_interpreter()

        if module.ProgramPath is not None:
            module.linuxcnc.command().program_open(module.ProgramPath)


# G55-Offset
g55_Orign_Index = 5240


class G55_Offset(module.DataNode):
    def __init__(self, joint_id: int):
        """
        :param joint_id: 关节号
        :return:
        """
        self.joint_id = joint_id
        if joint_id > 8:
            self.axis_name = "R"
            self.axis_id = 9
        else:
            self.axis_name, self.axis_id = module.get_axis_id(joint_id)
        self.index = 5241 + self.axis_id

        index = str(520100 + self.joint_id)
        param_name = self.axis_name + "_g55_offset"
        super().__init__(index, param_name, "VARIABLE")

    def value(self):
        ps = -1
        file = open(config.offsetPath, 'r')
        content = file.readlines()
        for i, line in enumerate(content):
            if str(self.index) in line:
                ps = i
                break
        line = content[ps]
        file.close()
        st = line[5:].strip('\n')
        return str(st)

    def set_value(self, value):
        print(self._name)
        tline = str(self.index)
        print(tline)

        ps = -1
        file = open(config.offsetPath, 'r')
        content = file.readlines()
        for i, line in enumerate(content):
            if tline in line:
                ps = i
                break

        if value == '':
            content[ps] = tline + '	0'
        else:
            content[ps] = tline + '	{0}'.format(value)
        content[ps] += "\n"
        file.close()
        w = open(config.micPath, 'w')
        w.writelines(content)
        w.close()

        action.server_reset_interpreter()

        if module.ProgramPath is not None:
            module.linuxcnc.command().program_open(module.ProgramPath)


# G56-Offset
g56_Orign_Index = 5260


class G56_Offset(module.DataNode):
    def __init__(self, joint_id: int):
        """
        :param joint_id: 关节号
        :return:
        """
        self.joint_id = joint_id
        if joint_id > 8:
            self.axis_name = "R"
            self.axis_id = 9
        else:
            self.axis_name, self.axis_id = module.get_axis_id(joint_id)
        self.index = 5261 + self.axis_id

        index = str(520200 + self.joint_id)
        param_name = self.axis_name + "_g56_offset"
        super().__init__(index, param_name, "VARIABLE")

    def value(self):
        ps = -1
        file = open(config.offsetPath, 'r')
        content = file.readlines()
        for i, line in enumerate(content):
            if str(self.index) in line:
                ps = i
                break
        line = content[ps]
        file.close()
        st = line[5:].strip('\n')
        return str(st)

    def set_value(self, value):
        print(self._name)
        tline = str(self.index)
        print(tline)

        ps = -1
        file = open(config.offsetPath, 'r')
        content = file.readlines()
        for i, line in enumerate(content):
            if tline in line:
                ps = i
                break

        if value == '':
            content[ps] = tline + '	0'
        else:
            content[ps] = tline + '	{0}'.format(value)
        content[ps] += "\n"
        file.close()
        w = open(config.micPath, 'w')
        w.writelines(content)
        w.close()

        action.server_reset_interpreter()

        if module.ProgramPath is not None:
            module.linuxcnc.command().program_open(module.ProgramPath)


# G57-Offset
g57_Orign_Index = 5280


class G57_Offset(module.DataNode):
    def __init__(self, joint_id: int):
        """
        :param joint_id: 关节号
        :return:
        """
        self.joint_id = joint_id
        if joint_id > 8:
            self.axis_name = "R"
            self.axis_id = 9
        else:
            self.axis_name, self.axis_id = module.get_axis_id(joint_id)
        self.index = 5281 + self.axis_id

        index = str(520300 + self.joint_id)
        param_name = self.axis_name + "_g57_offset"
        super().__init__(index, param_name, "VARIABLE")

    def value(self):
        ps = -1
        file = open(config.offsetPath, 'r')
        content = file.readlines()
        for i, line in enumerate(content):
            if str(self.index) in line:
                ps = i
                break
        line = content[ps]
        file.close()
        st = line[5:].strip('\n')
        return str(st)

    def set_value(self, value):
        print(self._name)
        tline = str(self.index)
        print(tline)

        ps = -1
        file = open(config.offsetPath, 'r')
        content = file.readlines()
        for i, line in enumerate(content):
            if tline in line:
                ps = i
                break

        if value == '':
            content[ps] = tline + '	0'
        else:
            content[ps] = tline + '	{0}'.format(value)
        content[ps] += "\n"
        file.close()
        w = open(config.micPath, 'w')
        w.writelines(content)
        w.close()

        action.server_reset_interpreter()

        if module.ProgramPath is not None:
            module.linuxcnc.command().program_open(module.ProgramPath)


# G58-Offset
g58_Orign_Index = 5300


class G58_Offset(module.DataNode):
    def __init__(self, joint_id: int):
        """
        :param joint_id: 关节号
        :return:
        """
        self.joint_id = joint_id
        if joint_id > 8:
            self.axis_name = "R"
            self.axis_id = 9
        else:
            self.axis_name, self.axis_id = module.get_axis_id(joint_id)
        self.index = 5301 + self.axis_id

        index = str(520400 + self.joint_id)
        param_name = self.axis_name + "_g58_offset"
        super().__init__(index, param_name, "VARIABLE")

    def value(self):
        ps = -1
        file = open(config.offsetPath, 'r')
        content = file.readlines()
        for i, line in enumerate(content):
            if str(self.index) in line:
                ps = i
                break
        line = content[ps]
        file.close()
        st = line[5:].strip('\n')
        return str(st)

    def set_value(self, value):
        print(self._name)
        tline = str(self.index)
        print(tline)

        ps = -1
        file = open(config.offsetPath, 'r')
        content = file.readlines()
        for i, line in enumerate(content):
            if tline in line:
                ps = i
                break

        if value == '':
            content[ps] = tline + '	0'
        else:
            content[ps] = tline + '	{0}'.format(value)
        content[ps] += "\n"
        file.close()
        w = open(config.micPath, 'w')
        w.writelines(content)
        w.close()

        action.server_reset_interpreter()

        if module.ProgramPath is not None:
            module.linuxcnc.command().program_open(module.ProgramPath)


# G59-Offset
g59_Orign_Index = 5320


class G59_Offset(module.DataNode):
    def __init__(self, joint_id: int):
        """
        :param joint_id: 关节号
        :return:
        """
        self.joint_id = joint_id
        if joint_id > 8:
            self.axis_name = "R"
            self.axis_id = 9
        else:
            self.axis_name, self.axis_id = module.get_axis_id(joint_id)
        self.index = 5321 + self.axis_id

        index = str(520500 + self.joint_id)
        param_name = self.axis_name + "_g59_offset"
        super().__init__(index, param_name, "VARIABLE")

    def value(self):
        ps = -1
        file = open(config.offsetPath, 'r')
        content = file.readlines()
        for i, line in enumerate(content):
            if str(self.index) in line:
                ps = i
                break
        line = content[ps]
        file.close()
        st = line[5:].strip('\n')
        return str(st)

    def set_value(self, value):
        print(self._name)
        tline = str(self.index)
        print(tline)

        ps = -1
        file = open(config.offsetPath, 'r')
        content = file.readlines()
        for i, line in enumerate(content):
            if tline in line:
                ps = i
                break

        if value == '':
            content[ps] = tline + '	0'
        else:
            content[ps] = tline + '	{0}'.format(value)
        content[ps] += "\n"
        file.close()
        w = open(config.micPath, 'w')
        w.writelines(content)
        w.close()

        action.server_reset_interpreter()

        if module.ProgramPath is not None:
            module.linuxcnc.command().program_open(module.ProgramPath)


# G92-Offset设定值
class G92_Offset(module.DataNode):
    def __init__(self, joint_id: int):
        """
        :param joint_id: 关节号
        :return:
        """
        self.joint_id = joint_id
        if joint_id > 8:
            self.axis_name = "R"
            self.axis_id = 9
        else:
            self.axis_name, self.axis_id = module.get_axis_id(joint_id)
        self.index = 5211 + self.axis_id

        index = str(520600 + self.joint_id)
        param_name = self.axis_name + "_g92_offset"
        super().__init__(index, param_name, "VARIABLE")

    @staticmethod
    def reset_all():
        file = open(config.offsetPath, 'r')
        content = file.readlines()
        for i, line in enumerate(content):
            if "5210" in line:
                ps = i
                content[ps] = "5210" + ' 0\n'
                continue
            if "5211" in line:
                ps = i
                content[ps] = "5211" + ' 0\n'
                continue
            if "5212" in line:
                ps = i
                content[ps] = "5212" + ' 0\n'
                continue
            if "5213" in line:
                ps = i
                content[ps] = "5213" + ' 0\n'
                continue
            if "5214" in line:
                ps = i
                content[ps] = "5214" + ' 0\n'
                continue
            if "5215" in line:
                ps = i
                content[ps] = "5215" + ' 0\n'
                continue
            if "5216" in line:
                ps = i
                content[ps] = "5216" + ' 0\n'
                continue
            if "5217" in line:
                ps = i
                content[ps] = "5217" + ' 0\n'
                continue
            if "5218" in line:
                ps = i
                content[ps] = "5218" + ' 0\n'
                continue
            if "5219" in line:
                ps = i
                content[ps] = "5219" + ' 0\n'
                continue
        file.close()
        w = open(config.micPath, 'w')
        w.writelines(content)
        w.close()

        action.server_reset_interpreter()

        if module.ProgramPath is not None:
            module.linuxcnc.command().program_open(module.ProgramPath)

    @staticmethod
    def reset_single(joint_id: int):
        if joint_id > 9:
            return
        axis_name, axis_id = module.get_axis_id(joint_id)

        axis_line = 5211 + axis_id
        file = open(config.offsetPath, 'r')
        content = file.readlines()
        for i, line in enumerate(content):
            if "5210" in line:
                ps = i
                content[ps] = "5210" + ' 1\n'
                continue
            if str(axis_line) in line:
                ps = i
                content[ps] = str(axis_line) + ' 0\n'
                break

        file.close()
        w = open(config.micPath, 'w')
        w.writelines(content)
        w.close()

        action.server_reset_interpreter()

        if module.ProgramPath is not None:
            module.linuxcnc.command().program_open(module.ProgramPath)

    def value(self):
        return str("0.000")

    def set_value(self, value):
        # global WCS_position
        # 当前激活坐标系R参数
        Current_R_xy = module.stat.rotation_xy
        MCS_position = module.stat.actual_position[self.axis_id]
        current_offset = module.stat.g5x_offset[self.axis_id]
        G43_offset = module.stat.tool_offset[self.axis_id]
        R_offset = Current_R_xy
        WCS_position = None
        if self.axis_id == 0 or self.axis_id == 1:
            # 坐标系Z轴旋转
            if R_offset != 0:
                x = module.stat.actual_position[0] - module.stat.g5x_offset[0] - module.stat.tool_offset[0]
                y = module.stat.actual_position[1] - module.stat.g5x_offset[1] - module.stat.tool_offset[1]
                xx = x * math.cos(math.radians(R_offset)) + y * math.sin(math.radians(R_offset))
                yy = - x * math.sin(math.radians(R_offset)) + y * math.cos(math.radians(R_offset))
                if self.axis_id == 0:
                    WCS_position = str(xx)
                elif self.axis_id == 1:
                    WCS_position = str(yy)
        WCS_position = MCS_position - current_offset - G43_offset

        actual_value = WCS_position - float(value)
        print(self._name)
        tline = str(self.index)
        print(tline)

        ps = -1
        flag = -1
        file = open(config.offsetPath, 'r')
        content = file.readlines()
        for i, line in enumerate(content):
            if tline in line:
                ps = i
                flag = i - self.axis_id - 1
                print("ps" + str(ps))
                print("flag" + str(flag))
                break

        content[ps] = tline + '	{0}'.format(actual_value)
        content[ps] += "\n"
        content[flag] = str(5210) + ' {0}'.format(1)
        content[flag] += "\n"
        file.close()
        w = open(config.micPath, 'w')
        w.writelines(content)
        w.close()

        action.server_reset_interpreter()

        if module.ProgramPath is not None:
            module.linuxcnc.command().program_open(module.ProgramPath)


# G92_Offset实际值
class G92_Current_Offset(module.DataNode):
    def __init__(self, joint_id: int):
        """
        :param joint_id: 关节号
        :return:
        """
        self.joint_id = joint_id
        if joint_id > 8:
            self.axis_name = "R"
            self.axis_id = 9
        else:
            self.axis_name, self.axis_id = module.get_axis_id(joint_id)
        self.index = 5241 + self.axis_id

        index = str(520700 + self.joint_id)
        param_name = self.axis_name + "_g92_offset"
        super().__init__(index, param_name, "VARIABLE")

    def value(self):
        return str(module.stat.g92_offset[self.axis_id])


# 轴Offset是否使能标志(设置值)
class OffsetEnable(module.DataNode):
    def __init__(self, joint_id: int):
        """
        :param joint_id: 关节号
        :return:
        """
        self.joint_id = joint_id
        if joint_id > module.axis_count:
            self.axis_name = "R"
            self.axis_id = 9
        else:
            self.axis_name, self.axis_id = module.get_axis_id(joint_id)

        index = str(520800 + self.joint_id)
        param_name = self.axis_name + "_offset_enable"
        super().__init__(index, param_name, "VARIABLE")

    def value(self):
        return str(config.offset_enable[self.joint_id])

    def set_value(self, value):
        item = "joint_" + str(self.joint_id) + "_offset_enable"
        config.coordinate_ini.set("COORDINATE", item, value)
        with open(config.coordinate_config_path, "w") as configfile:
            config.coordinate_ini.write(configfile)


# 轴Offset是否使能标志（实际值）
class OffsetActualEnabled(module.DataNode):
    def __init__(self, joint_id: int):
        """
        :param joint_id: 关节号
        :return:
        """
        self.joint_id = joint_id
        if joint_id > module.axis_count:
            self.axis_name = "R"
            self.axis_id = 9
        else:
            self.axis_name, self.axis_id = module.get_axis_id(joint_id)

        index = str(520900 + self.joint_id)
        param_name = self.axis_name + "_offset_enable"
        super().__init__(index, param_name, "VARIABLE")

    def value(self):
        return str(config.offset_enable[self.joint_id])
