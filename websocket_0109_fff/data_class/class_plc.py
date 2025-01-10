from data_class import nc_module as module
import linuxcnc
import hal

# PLC 数字量输入
class PLCDigitalInput(module.DataNode):
    def __init__(self, plc_id: int):
        """
        :param plc_id: 引脚编号，例：classicladder.0.in-00，编号为0
        """
        self.plc_id = plc_id
        index = str(600000 + self.plc_id)
        # id小于10补齐两位
        if self.plc_id < 10:
            plc_name = "plc_digital_input_" + "0" + str(self.plc_id)
            self.pin = "classicladder.0.in-" + "0" + str(self.plc_id)
        else:
            plc_name = "plc_digital_input_" + str(self.plc_id)
            self.pin = "classicladder.0.in-" + str(self.plc_id)
        super().__init__(index, plc_name, "VARIABLE")

    def value(self):
        try:
            if hal.get_value(self.pin):
                return "1"
            return "0"
        except Exception as e:
            print("PLCDigitalInput::value::error={}".format(e))

    def set_value(self, value):
        try:
            hal.set_p(self.pin, value)
        except Exception as e:
            print("PLCDigitalInput::set_value::error={}".format(e))


# PLC 数字量输出起始的索引为：610000：最大分配10000个，现在4096分配个，如今开放：个
class PLCDigitalOutput(module.DataNode):
    def __init__(self, plc_id: int):
        """
        :param plc_id: 引脚编号，例：classicladder.0.out-00，编号为0
        """
        self.plc_id = plc_id

        index = str(610000 + self.plc_id)
        # id小于10补齐两位
        if self.plc_id < 10:
            plc_name = "plc_digital_output_" + "0" + str(self.plc_id)
            self.pin = "classicladder.0.out-" + "0" + str(self.plc_id)
        else:
            plc_name = "plc_digital_output_" + str(self.plc_id)
            self.pin = "classicladder.0.out-" + str(self.plc_id)
        super().__init__(index, plc_name, "VARIABLE")

    def value(self):
        try:
            if hal.get_value(self.pin):
                return "1"
            return "0"
        except Exception as e:
            print("PLCDigitalOutput::value::error={}".format(e))


# PLC 模拟量输入起始的索引为：620000：最大分配10000个，现在分配256个，如今开放：64个
class PLCAnalogInput(module.DataNode):
    def __init__(self, plc_id: int):
        """
        :param plc_id: 引脚编号，例：classicladder.0.floatin-00，编号为0
        """
        self.plc_id = plc_id

        index = str(620000 + self.plc_id)
        # id小于10补齐两位
        if self.plc_id < 10:
            plc_name = "plc_analog_input_" + "0" + str(self.plc_id)
            self.pin = "classicladder.0.floatin-" + "0" + str(self.plc_id)
        else:
            plc_name = "plc_analog_input_" + str(self.plc_id)
            self.pin = "classicladder.0.floatin-" + str(self.plc_id)
        super().__init__(index, plc_name, "VARIABLE")

    def value(self):
        try:
            return str(hal.get_value(self.pin))
        except Exception as e:
            print("PLCAnalogInput::value::error={}".format(e))

    def set_value(self, value):
        try:
            hal.set_p(self.pin, value)
        except Exception as e:
            print("PLCAnalogInput::set_value::error={}".format(e))

# PLC 模拟量输出起始的索引为：630000：最大分配10000个，现在分配256个，如今开放：64个
class PLCAnalogOutput(module.DataNode):
    def __init__(self, plc_id: int):
        """
        :param plc_id: 引脚编号，例：classicladder.0.floatin-00，编号为0
        """
        self.plc_id = plc_id
        index = str(630000 + self.plc_id)
        # id小于10补齐两位
        if self.plc_id < 10:
            plc_name = "plc_analog_output_" + "0" + str(self.plc_id)
            self.pin = "classicladder.0.floatout-" + "0" + str(self.plc_id)
        else:
            plc_name = "plc_analog_output_" + str(self.plc_id)
            self.pin = "classicladder.0.floatout-" + str(self.plc_id)
        super().__init__(index, plc_name, "VARIABLE")

    def value(self):
        try:
            return str(hal.get_value(self.pin))
        except Exception as e:
            print("PLCAnalogOutput::value::error={}".format(e))
#[640000-649999 预留给B：]
class PLCMiddleVarsIW(module.DataNode): #plc中间变量 IW 类型int
    def __init__(self,index_:int):
        self.index=str(650000+index_)
        print("PLCMiddleVarsIW::index={}".format(self.index))
        if index_<10:
            plc_middle_var_name="plc_middel_var_iw_0"+str(index_)
            self.pin="classicladder.0.s32in-0"+str(index_)
        else:
            plc_middle_var_name="plc_middel_var_iw_"+str(index_)
            self.pin="classicladder.0.s32in-"+str(index_) 
        super().__init__(self.index, plc_middle_var_name, "middle_value")

    def value(self):
        try:
            return str(hal.get_value(self.pin))
        except Exception as e:
            print("PLCMiddleVarsIW::value::error={}".format(e))

#PLC 中间输出变量：起始的索引为：660000：最大分配10000个，现在分配2048个，如今开放：512个
class PLCMiddleVarsQW(module.DataNode): #plc中间变量 QW 类型int 预留：10000个，以提供后续加入足够的空间
    def __init__(self,index_:int):
        self.index=str(660000+index_)
        print("PLCMiddleVarsQW::index={}".format(self.index))
        if index_<10:
            plc_middle_var_name="plc_middel_var_qw_0"+str(index_)
            self.pin="classicladder.0.s32out-0"+str(index_)
        else:
            plc_middle_var_name="plc_middel_var_qw_"+str(index_)
            self.pin="classicladder.0.s32out-"+str(index_) 
        super().__init__(self.index, plc_middle_var_name, "middle_valu_qw")

    def value(self):
        try:
            return str(hal.get_value(self.pin))  
        except Exception as e:
            print("PLCMiddleVarsQW::value::error={}".format(e))      


