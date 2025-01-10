from data_class import nc_module as module


# 关节-死区
class JointNumDeadband(module.DataNode):
    def __init__(self, num):
        self.joint_id = num
        index = str(400000 + self.joint_id)
        joint_name = "joint_" + str(num)  + "_deadband"
        super().__init__(index, joint_name, "VARIABLE")

    def value(self):
        return str(module.inifile.find("JOINT_" + str(self.joint_id), "DEADBAND"))

    def set_value(self, value):
        module.setIniValue(module.stat.ini_filename, "JOINT_" + str(self.joint_id), "DEADBAND",
                           value)

# 关节-伺服偏移
class JointNumBias(module.DataNode):
    def __init__(self, num):
        self.joint_id = num
        index = str(400010 + self.joint_id)
        joint_name = "joint_" + str(num)  + "_bias"
        super().__init__(index, joint_name, "VARIABLE")

    def value(self):
        return str(module.inifile.find("JOINT_" + str(self.joint_id), "BIAS"))

    def set_value(self, value):
        module.setIniValue(module.stat.ini_filename, "JOINT_" + str(self.joint_id), "BIAS",
                           value)


# 关节-伺服的比例增益
class JointNumP(module.DataNode):
    def __init__(self, num):
        self.joint_id = num
        index = str(400020 + self.joint_id)
        joint_name = "joint_" + str(num)  + "_P"
        super().__init__(index, joint_name, "VARIABLE")

    def value(self):
        return str(module.inifile.find("JOINT_" + str(self.joint_id), "P"))

    def set_value(self, value):
        module.setIniValue(module.stat.ini_filename, "JOINT_" + str(self.joint_id), "P",
                           value)


# 关节-伺服的积分增益
class JointNumI(module.DataNode):
    def __init__(self, num):
        self.joint_id = num
        index = str(400030 + self.joint_id)
        joint_name = "joint_" + str(num)  + "_I"
        super().__init__(index, joint_name, "VARIABLE")

    def value(self):
        return str(module.inifile.find("JOINT_" + str(self.joint_id), "I"))

    def set_value(self, value):
        module.setIniValue(module.stat.ini_filename, "JOINT_" + str(self.joint_id), "I",
                           value)


# 关节-伺服的微分增益
class JointNumD(module.DataNode):
    def __init__(self, num):
        self.joint_id = num
        index = str(400040 + self.joint_id)
        joint_name = "joint_" + str(num)  + "_D"
        super().__init__(index, joint_name, "VARIABLE")

    def value(self):
        return str(module.inifile.find("JOINT_" + str(self.joint_id), "D"))

    def set_value(self, value):
        module.setIniValue(module.stat.ini_filename, "JOINT_" + str(self.joint_id), "D",
                           value)


# 关节-0阶前馈增益
class JointNumFF0(module.DataNode):
    def __init__(self, num):
        self.joint_id = num
        index = str(400050 + self.joint_id)
        joint_name = "joint_" + str(num)  + "_FF0"
        super().__init__(index, joint_name, "VARIABLE")

    def value(self):
        return str(module.inifile.find("JOINT_" + str(self.joint_id), "FF0"))

    def set_value(self, value):
        module.setIniValue(module.stat.ini_filename, "JOINT_" + str(self.joint_id), "FF0",
                           value)


# 关节-1阶前馈增益
class JointNumFF1(module.DataNode):
    def __init__(self, num):
        self.joint_id = num
        index = str(400060 + self.joint_id)
        joint_name = "joint_" + str(num)  + "_FF1"
        super().__init__(index, joint_name, "VARIABLE")

    def value(self):
        return str(module.inifile.find("JOINT_" + str(self.joint_id), "FF1"))

    def set_value(self, value):
        module.setIniValue(module.stat.ini_filename, "JOINT_" + str(self.joint_id), "FF1",
                           value)


# 关节-2阶前馈增益
class JointNumFF2(module.DataNode):
    def __init__(self, num):
        self.joint_id = num
        index = str(400070 + self.joint_id)
        joint_name = "joint_" + str(num)  + "_FF2"
        super().__init__(index, joint_name, "VARIABLE")

    def value(self):
        return str(module.inifile.find("JOINT_" + str(self.joint_id), "FF2"))

    def set_value(self, value):
        module.setIniValue(module.stat.ini_filename, "JOINT_" + str(self.joint_id), "FF2",
                           value)


# 关节-输出到电机放大器的比例系数
class JointNumOutputScale(module.DataNode):
    def __init__(self, num):
        self.joint_id = num
        index = str(400080 + self.joint_id)
        joint_name = "joint_" + str(num)  + "_output_scale"
        super().__init__(index, joint_name, "VARIABLE")

    def value(self):
        return str(module.inifile.find("JOINT_" + str(self.joint_id), "OUTPUT_SCALE"))

    def set_value(self, value):
        module.setIniValue(module.stat.ini_filename, "JOINT_" + str(self.joint_id), "OUTPUT_SCALE",
                           value)


# 关节-输出到电机放大器的补偿系数
class JointNumOutputOffset(module.DataNode):
    def __init__(self, num):
        self.joint_id = num
        index = str(400090 + self.joint_id)
        joint_name = "joint_" + str(num)  + "_output_offset"
        super().__init__(index, joint_name, "VARIABLE")

    def value(self):
        return str(module.inifile.find("JOINT_" + str(self.joint_id), "OUTPUT_OFFSET"))

    def set_value(self, value):
        module.setIniValue(module.stat.ini_filename, "JOINT_" + str(self.joint_id), "OUTPUT_OFFSET",
                           value)


# 关节-PID补偿输出的最大值
class JointNumMaxOutput(module.DataNode):
    def __init__(self, num):
        self.joint_id = num
        index = str(400100 + self.joint_id)
        joint_name = "joint_" + str(num)  + "_max_output"
        super().__init__(index, joint_name, "VARIABLE")

    def value(self):
        return str(module.inifile.find("JOINT_" + str(self.joint_id), "MAX_OUTPUT"))

    def set_value(self, value):
        module.setIniValue(module.stat.ini_filename, "JOINT_" + str(self.joint_id), "MAX_OUTPUT",
                           value)


# 关节-移动每个机床单位的编码器反馈脉冲数
class JointNumEncoderScale(module.DataNode):
    def __init__(self, num):
        self.joint_id = num
        index = str(400110 + self.joint_id)
        joint_name = "joint_" + str(num)  + "_encoder_scale"
        super().__init__(index, joint_name, "VARIABLE")

    def value(self):
        return str(module.inifile.find("JOINT_" + str(self.joint_id), "ENCODER_SCALE"))

    def set_value(self, value):
        module.setIniValue(module.stat.ini_filename, "JOINT_" + str(self.joint_id), "ENCODER_SCALE",
                           value)

