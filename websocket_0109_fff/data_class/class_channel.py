import hal
import linuxcnc

import config
from data_class import nc_module as module
import math

parser = module.MultiValueConfigParser()


class KinematicsSetting(module.DataNode):
    def __init__(self):
        super().__init__("210000", "KinematicsSetting", "VARIABLE")

    def value(self):
        result = module.inifile.find("KINS", "KINEMATICS")
        if config.kinematics_setting_0 in result:
            return "0"
        else:
            return "1"

    def set_value(self, value):
        parser.read(module.stat.ini_filename, encoding='utf-8')
        if value == "0":
            # 注释所有rtcp参数和cmd命令，激活setting_0
            parser.setValue("KINS", "KINEMATICS", config.kinematics_setting_0,
                               config.kinematics_setting_0, "1")
            parser.setValue("KINS", "KINEMATICS", config.kinematics_setting_1,
                            config.kinematics_setting_1, "0")
        else:
            parser.setValue("KINS", "KINEMATICS",config.kinematics_setting_1,
                               config.kinematics_setting_1, "1")
            parser.setValue("KINS", "KINEMATICS", config.kinematics_setting_0,
                            config.kinematics_setting_0, "0")
        # 激活cmd命令
        parser.setValue("HAL", "HALCMD", "net :" +config.kinematics_setting_1_halcmd_1,
                        config.kinematics_setting_1_halcmd_1, value)
        parser.setValue("HAL", "HALCMD", "net :" + config.kinematics_setting_1_halcmd_2,
                        config.kinematics_setting_1_halcmd_2, value)
        # rtcp参数
        # 刀具基座长度
        result = parser.isExist("HAL", "HALCMD",config.rtcp_tool_base_length)
        parser.setValue("HAL", "HALCMD", "setp " + config.rtcp_tool_base_length + " " + result,
                        config.rtcp_tool_base_length, value)
        # 第一旋转X
        result = parser.isExist("HAL", "HALCMD", config.rtcp_first_rotation_center_coordinates_x)
        parser.setValue("HAL", "HALCMD", "setp " + config.rtcp_first_rotation_center_coordinates_x + " " + result,
                        config.rtcp_first_rotation_center_coordinates_x, value)
        # 第二旋转X
        result = parser.isExist("HAL", "HALCMD", config.rtcp_second_rotation_center_coordinates_x)
        parser.setValue("HAL", "HALCMD", "setp " + config.rtcp_second_rotation_center_coordinates_x + " " + result,
                        config.rtcp_second_rotation_center_coordinates_x, value)
        # 第二旋转Y
        result = parser.isExist("HAL", "HALCMD", config.rtcp_second_rotation_center_coordinates_y)
        parser.setValue("HAL", "HALCMD", "setp " + config.rtcp_second_rotation_center_coordinates_y + " " + result,
                        config.rtcp_second_rotation_center_coordinates_y, value)

        parser.updateToFile()


class ToolBaseLength(module.DataNode):
    def __init__(self):
        super().__init__("210001", "ToolBaseLength", "VARIABLE")

    def value(self):
        parser.read(module.stat.ini_filename, encoding='utf-8')
        return parser.isExist('HAL', 'HALCMD', config.rtcp_tool_base_length)

    def set_value(self, value):
        parser.read(module.stat.ini_filename, encoding='utf-8')
        parser.setValue("HAL", "HALCMD", "setp " + config.rtcp_tool_base_length + " " + value,
                        config.rtcp_tool_base_length, "1")
        parser.updateToFile()


class FirstRotationCenterCoordinatesX(module.DataNode):
    def __init__(self):
        super().__init__("210002", "FirstRotationCenterCoordinatesX", "VARIABLE")

    def value(self):
        parser.read(module.stat.ini_filename, encoding='utf-8')
        return parser.isExist('HAL', 'HALCMD', config.rtcp_first_rotation_center_coordinates_x)

    def set_value(self, value):
        parser.read(module.stat.ini_filename, encoding='utf-8')
        parser.setValue("HAL", "HALCMD", "setp " + config.rtcp_first_rotation_center_coordinates_x + " " + value,
                        config.rtcp_first_rotation_center_coordinates_x, "1")
        parser.updateToFile()


class SecondRotationCenterCoordinatesX(module.DataNode):
    def __init__(self):
        super().__init__("210003", "SecondRotationCenterCoordinatesX", "VARIABLE")

    def value(self):
        parser.read(module.stat.ini_filename, encoding='utf-8')
        return parser.isExist('HAL', 'HALCMD', config.rtcp_second_rotation_center_coordinates_x)

    def set_value(self, value):
        parser.read(module.stat.ini_filename, encoding='utf-8')
        parser.setValue("HAL", "HALCMD", "setp " + config.rtcp_second_rotation_center_coordinates_x + " " + value,
                        config.rtcp_second_rotation_center_coordinates_x, "1")
        parser.updateToFile()


class SecondRotationCenterCoordinatesY(module.DataNode):
    def __init__(self):
        super().__init__("210004", "SecondRotationCenterCoordinatesY", "VARIABLE")

    def value(self):
        parser.read(module.stat.ini_filename, encoding='utf-8')
        return parser.isExist('HAL', 'HALCMD', config.rtcp_second_rotation_center_coordinates_y)

    def set_value(self, value):
        parser.read(module.stat.ini_filename, encoding='utf-8')
        parser.setValue("HAL", "HALCMD", "setp " + config.rtcp_second_rotation_center_coordinates_y + " " + value,
                        config.rtcp_second_rotation_center_coordinates_y, "1")
        parser.updateToFile()


class RtcpStatus(module.DataNode):
    def __init__(self):
        super().__init__("210005", "RtcpStatus", "VARIABLE")

    def value(self):
        if hal.get_value(config.rtcp_status):
            return "1"
        return "0"