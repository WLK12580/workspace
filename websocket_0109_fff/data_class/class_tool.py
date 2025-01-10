from numpy.testing.print_coercion_tables import print_coercion_table

import config
from data_class import nc_module as module
import hal

tblPath = config.tool_table_path
newtblPath = config.new_tool_table_path

toolData = {}
for i in range(1, 50):
    toolData.update({str(i): (i - 1)})

halTool_Index = {}
for i in range(10, 61):
    halTool_Index.update({str(i):(i - 10)})

# 当前刀具信息查询列表
tool_table_info = []
def getToolInfo():
    ps = -1
    file = open(config.micPath, 'r')
    content = file.readlines()
    for i, line in enumerate(content):
        if str(1100) in line:  #1999
            ps = i
            break
    line = content[ps]
    file.close()
    # 刀具号
    st = line[5:].strip('\n')
    global tool_table_info
    if int(float(st)) == 0:
        tool_table_info = ['0'] * 14
    else:
        tool_id = [row[0] for row in module.stat.tool_table]
        if int(float(st)) in tool_id:
            index_id = tool_id.index(int(float(st)))
            for item in range(14):
                tool_table_info.append(str(module.stat.tool_table[index_id][item]))
        else:
            tool_table_info.append("0")


def getG41G42ToolID():
    # 刀具号
    try:
        st = hal.get_value("halui.tool.number_active")
    except:
        st = '-1'
    global tool_table_info
    if str(st) == '-1':
        tool_table_info.append('0')
    else:
        tool_id = [row[0] for row in module.stat.tool_table]
        if int(float(st)) in tool_id:
            index_id = tool_id.index(int(float(st)))
            for item in range(14):
                tool_table_info.append(str(module.stat.tool_table[index_id][item]))
        else:
            tool_table_info.append('0')


# 初始化所有刀具信息
getToolInfo()

# 初始化所有刀具信息 （新）
getG41G42ToolID()

# 刀具-刀号
class ToolCount(module.DataNode):
    def __init__(self):
        super().__init__("500000", "ToolCount", "VARIABLE")

    def value(self):
        return str(module.stat.tool_in_spindle)


# 刀具-当前刀具的X方向补偿值
class ToolXOffset(module.DataNode):
    def __init__(self):
        super().__init__("500001", "ToolXOffset", "VARIABLE")

    def value(self):
        auto_offset = str(module.stat.tool_table[0][1])
        return auto_offset


# 刀具-当前刀具的Y方向补偿值
class ToolYOffset(module.DataNode):
    def __init__(self):
        super().__init__("500002", "ToolYOffset", "VARIABLE")

    def value(self):
        auto_offset = str(module.stat.tool_table[0][2])
        return auto_offset


# 刀具-当前刀具的Z方向补偿值
class ToolZOffset(module.DataNode):
    def __init__(self):
        super().__init__("500003", "ToolZOffset", "VARIABLE")

    def value(self):
        auto_offset = str(module.stat.tool_table[0][3])
        return auto_offset


# 刀具-当前刀具的刀库号
class ToolFromTable(module.DataNode):
    def __init__(self):
        super().__init__("500004", "ToolFromTable", "VARIABLE")

    def value(self):
        return str(module.stat.tool_from_pocket)


# 刀具-当前刀具直径
class ToolDiameter(module.DataNode):
    def __init__(self):
        super().__init__("500005", "ToolDiameter", "VARIABLE")

    def value(self):
        return str(module.stat.tool_table[0][10])


#  查询当前刀具表刀具信息
class GetToolTableInfo(module.DataNode):
    def __init__(self):
        super().__init__("500017", "GetToolTableInfo", "VARIABLE")

    def value(self):
        tool_table_info.clear()
        getToolInfo()
        tool_info = ','.join(tool_table_info)
        return str(tool_info)


# 手动换刀X方向补偿
class ManualToolX(module.DataNode):
    def __init__(self):
        super().__init__("500018", "ManualToolX", "VARIABLE")

    def value(self):
        manual_offset = str(module.stat.tool_offset[0])
        return manual_offset


# 手动换刀Y方向补偿
class ManualToolY(module.DataNode):
    def __init__(self):
        super().__init__("500019", "ManualToolY", "VARIABLE")

    def value(self):
        manual_offset = str(module.stat.tool_offset[1])
        return manual_offset


# 手动换刀Z方向补偿
class ManualToolZ(module.DataNode):
    def __init__(self):
        super().__init__("500020", "ManualToolZ", "VARIABLE")

    def value(self):
        manual_offset = str(module.stat.tool_offset[2])
        return manual_offset
        
#  查询当前G41/G42生效刀具信息
class GetG41G42Info(module.DataNode):
    def __init__(self):
        super().__init__("500022", "GetG41G42Info", "VARIABLE")

    def value(self):
        tool_table_info.clear()
        getG41G42ToolID()
        tool_info = ','.join(tool_table_info)
        return str(tool_info)


# 当前生效刀号
class CurrentToolId(module.DataNode):
    def __init__(self):
        super().__init__("500026", "CurrentToolId", "VARIABLE")

    def value(self):
        return str(hal.get_value(config.halpin_current_tool_id))


# toolNewTable
class ToolTable(module.DataNode):
    def __init__(self):
        super().__init__("510510", "ToolTable", "VARIABLE")

    def value(self):
        module.command.load_tool_table() #Reload ToolTable
        findSt= ['T', 'P', 'X', 'Y', 'Z', 'D']
        st = ''
        with open(newtblPath, 'r') as file:
            content = file.readlines()
            if(len(content) == 0):
                return -1           
            for line in content:
                stline = line
                for t in findSt:
                    beg = str(line).find(t)
                    end = str(line).find(' ')
                    if(beg == -1):
                        if(findSt.index(t) == len(findSt) - 1):
                            st += "{:.3f}".format(0.000) + '|'
                        else:
                            st += "{:.3f}".format(0.000) + ','
                    else:
                        if(findSt.index(t) == len(findSt) - 1):
                            ch = line[str(line).find(';') + 1 :]
                            if(end == -1):
                                st += str(line[beg + 1 :]) + ',' + ch + '|'
                            else:
                                st += str(line[beg + 1 : end]) + ',' + ch + '|'
                        else:
                            if(end == -1): # avoid chinese contains two space
                                st += str(line[beg + 1 :]) + ',' # above reflect
                            else:
                                st += str(line[beg + 1 : end]) + ','
                            line = line[end + 1 :].strip()      
                if(content.index(stline) == len(content) - 1):
                    return st.strip('|')
        return st.strip('|')


# toolMagazineTable
class ToolMagazineTable(module.DataNode):
    def __init__(self):
        super().__init__("510511", "ToolMagazineTable", "VARIABLE")

    def value(self):
        # st = ''
        # data = module.stat.tool_table
        # for i in range(len(data)):
        #     if(data[i].id != 0 and data[i].id != -1):
        #         st += str(data[i].id)+ ',' + str(data[i].xoffset) + ',' + str(data[i].yoffset) + ',' + str(data[i].zoffset) + ',' + str(data[i].diameter) + str('|')
        # return st.strip('|')
        module.command.load_tool_table() #Reload ToolTable
        findSt= ['T', 'P', 'X', 'Y', 'Z', 'D']
        st = ''
        with open(tblPath, 'r') as file:
            content = file.readlines()
            if(len(content) == 0):
                return -1           
            for line in content:
                stline = line
                for t in findSt:
                    beg = str(line).find(t)
                    end = str(line).find(' ')
                    if(beg == -1):
                        if(findSt.index(t) == len(findSt) - 1):
                            st += "{:.3f}".format(0.000) + '|'
                        else:
                            st += "{:.3f}".format(0.000) + ','
                    else:
                        if(findSt.index(t) == len(findSt) - 1):
                            ch = line[str(line).find(';') + 1 :]
                            if(end == -1):
                                st += str(line[beg + 1 :]) + ',' + ch + '|'
                            else:
                                st += str(line[beg + 1 : end]) + ',' + ch + '|'
                        else:
                            if(end == -1): # avoid chinese contains two space
                                st += str(line[beg + 1 :]) + ',' # above reflect
                            else:
                                st += str(line[beg + 1 : end]) + ','
                            line = line[end + 1 :].strip()      
                if(content.index(stline) == len(content) - 1):
                    st = st.strip('|')
                    return st
            st = st.strip('|')
        return st


# toolStatus
class ToolStatus(module.DataNode):
    def __init__(self):
        super().__init__("510512", "ToolStatus", "VARIABLE")

    def value(self):
        module.command.load_tool_table() #Reload ToolTable
        findSt= ['T', 'P']
        st = ''
        with open(tblPath, 'r') as file:
            content = file.readlines()
            if(len(content) == 0):
                return -1           
            for line in content:
                stline = line
                for t in findSt:
                    beg = str(line).find(t)
                    end = str(line).find(' ')
                    st += str(line[beg + 1 : end]) + ','
                    line = line[end + 1 :].strip() 
                st = st.strip(',') + '|'       
            st = st.strip('|')
        return st


# toolMagazine_Unload
class ToolMagazine_Unload(module.DataNode):
    def __init__(self):
         super().__init__("510513", "toolMagazine_Unload", "VARIABLE")
    
    def value(self):
        return super().value()
    
    def set_value(self, value):
        ps = -1
        st = 'T' + str(value)
        with open(tblPath, 'r') as file:
            content = file.readlines()
            for i, line in enumerate(content):
                t = line.find(' ')
                line = line[0 : t]
                if(str(st) == line):
                    ps = i
                    break
        del content[ps]
        with open(tblPath, 'w') as file:
            for line in content:
                file.write(line)
        module.command.load_tool_table() #Reload ToolTable


#
class ToolMagazine_Move(module.DataNode):
    def __init__(self):
        super().__init__("510515", "toolMagazine_Move", "VARIABLE")
    
    def value(self):
        return super().value()
    
    def set_value(self, value):
        ps = -1
        val = str(value).split(':')
        st = 'T' + str(val[1])
        with open(tblPath, 'r') as file:
            content = file.readlines()
            for i, line in enumerate(content):
                t = line.find(' ')
                line = line[0 : t]
                if(str(st) == line):
                    ps = i
                    break

        begin = content[ps].index('X')
        line = content[ps][begin :]
        new_line = 'T{0} P{1} '.format(val[1], val[0]) + line
        del content[ps]
        inserted_index = len(content)
        content.insert(inserted_index, new_line)

        with open(tblPath, 'w') as file:
            file.writelines(content)
        with open(tblPath, 'r') as file:
            content = file.readlines()
        module.command.load_tool_table() #Reload ToolTable


# toolID
class ToolID(module.DataNode):
    def __init__(self, num):
        self.tool_id = toolData[num]
        index = str(510000 + self.tool_id)
        tool_name = "tool_" + str(num) + "_data"
        super().__init__(index, tool_name, "VARIABLE")
    
    def value(self):
        return super().value()
       
    def set_value(self, value):
        ps = -1
        value = str(value).split(':')
        if(value[0] == '0'):
            path = newtblPath
        else:
            path = tblPath
        toolID= self._name[5:7].strip('_')
        target = 'T' + toolID
        with open(path, 'r') as file:
            content = file.readlines()
            for i, line in enumerate(content):
                t = line.find(' ')
                line = line[0 : t]
                if(str(target) == line):
                    ps = i
                    print(i + 1)
                    break
        begin = content[ps].find(';')
        bstr = content[ps][: begin]
        content[ps] = bstr + ';{0}'.format(value[1]) + '\n'

        with open(path, 'w') as file:
            file.writelines(content)
        module.command.load_tool_table() #Reload ToolTable


# toolOffset_X
class ToolOffset_X(module.DataNode):
    def __init__(self, num):
        self.tool_id = toolData[num]
        index = str(510100 + self.tool_id)
        tool_name = "tool_" + str(num) + "_data"
        super().__init__(index, tool_name, "VARIABLE")
    
    def value(self):
        return super().value()
       
    def set_value(self, value):
        ps = -1
        value = str(value).split(':')
        if(value[0] == '0'):
            path = newtblPath
        else:
            path = tblPath
        toolID= self._name[5:7].strip('_')
        target = 'T' + toolID
        with open(path, 'r') as file:
            content = file.readlines()
            for i, line in enumerate(content):
                t = line.find(' ')
                line = line[0 : t]
                if(str(target) == line):
                    ps = i
                    print(i + 1)
                    break
        begin = content[ps].find('X')
        bstr = content[ps][: begin]
        end = content[ps].find(' ', begin)
        pstr = content[ps][end : ]
        content[ps] = bstr + 'X{0}'.format(value[1]) + pstr

        with open(path, 'w') as file:
            file.writelines(content)
        module.command.load_tool_table() #Reload ToolTable


# toolOffset_Y
class ToolOffset_Y(module.DataNode):
    def __init__(self, num):
        self.tool_id = toolData[num]
        index = str(510200 + self.tool_id)
        tool_name = "tool_" + str(num) + "_data"
        super().__init__(index, tool_name, "VARIABLE")
    
    def value(self):
        return super().value()

    def set_value(self, value):
        ps = -1
        value = str(value).split(':')
        if(value[0] == '0'):
            path = newtblPath
        else:
            path = tblPath
        toolID= self._name[5:7].strip('_')
        target = 'T' + toolID
        with open(path, 'r') as file:
            content = file.readlines()
            for i, line in enumerate(content):
                t = line.find(' ')
                line = line[0 : t]
                if(str(target) == line):
                    ps = i
                    print(i + 1)
                    break
        begin = content[ps].find('Y')
        bstr = content[ps][: begin]
        end = content[ps].find(' ', begin)
        pstr = content[ps][end : ]
        content[ps] = bstr + 'Y{0}'.format(value[1]) + pstr

        with open(path, 'w') as file:
            file.writelines(content)
        module.command.load_tool_table() #Reload ToolTable


# toolOffset_Z
class ToolOffset_Z(module.DataNode):
    def __init__(self, num):
        self.tool_id = toolData[num]
        index = str(510300 + self.tool_id)
        tool_name = "tool_" + str(num) + "_data"
        super().__init__(index, tool_name, "VARIABLE")
    
    def value(self):
        return super().value()

    def set_value(self, value):
        ps = -1
        value = str(value).split(':')
        if(value[0] == '0'):
            path = newtblPath
        else:
            path = tblPath
        toolID= self._name[5:7].strip('_')
        target = 'T' + toolID
        with open(path, 'r') as file:
            content = file.readlines()
            for i, line in enumerate(content):
                t = line.find(' ')
                line = line[0 : t]
                if(str(target) == line):
                    ps = i
                    print(i + 1)
                    break
        begin = content[ps].find('Z')
        bstr = content[ps][: begin]
        end = content[ps].find(' ', begin)
        pstr = content[ps][end : ]
        content[ps] = bstr + 'Z{0}'.format(value[1]) + pstr

        with open(path, 'w') as file:
            file.writelines(content)
        module.command.load_tool_table() #Reload ToolTable


# tool_Diameter
class Tool_Diameter(module.DataNode):
    def __init__(self, num):
        self.tool_id = toolData[num]
        index = str(510400 + self.tool_id)
        tool_name = "tool_" + str(num) + "_data"
        super().__init__(index, tool_name, "VARIABLE")
    
    def value(self):
        return super().value()

    def set_value(self, value):
        ps = -1
        value = str(value).split(':')
        if(value[0] == '0'):
            path = newtblPath
        else:
            path = tblPath
        toolID= self._name[5:7].strip('_')
        target = 'T' + toolID
        with open(path, 'r') as file:
            content = file.readlines()
            for i, line in enumerate(content):
                t = line.find(' ')
                line = line[0 : t]
                if(str(target) == line):
                    ps = i
                    print(i + 1)
                    break
        begin = content[ps].find('D')
        bstr = content[ps][: begin]
        end = content[ps].find(' ', begin)
        pstr = content[ps][end : ]
        content[ps] = bstr + 'D{0}'.format(value[1]) + pstr

        with open(path, 'w') as file:
            file.writelines(content)
        module.command.load_tool_table() #Reload ToolTable


# tool_New
class Tool_New(module.DataNode):
    def __init__(self):
        super().__init__("510500", "tool_New", "VARIABLE")
    
    def value(self):
        return super().value()
    
    def set_value(self, value):
        with open(newtblPath, 'r') as file:
            line = file.readlines()
        value = str(value).split(':')
        new_line = 'T{0} P{1} X0.000 Y0.000 Z0.000 D0.000 ;{2}'.format(value[0], value[0], value[1])
        inserted_index = len(line)
        line.insert(inserted_index, new_line + '\n')

        with open(newtblPath, 'w') as file:
            file.writelines(line)
        module.command.load_tool_table() #Reload ToolTable


# tool_Cancel
class Tool_Cancel(module.DataNode):
    def __init__(self):
         super().__init__("510501", "tool_Cancel", "VARIABLE")
    
    def value(self):
        return super().value()
    
    def set_value(self, value):
        ps = -1
        st = 'T' + str(value)
        with open(newtblPath, 'r') as file:
            content = file.readlines()
            for i, line in enumerate(content):
                t = line.find(' ')
                line = line[0 : t]
                if(str(st) == line):
                    ps = i
                    break
        if ps == -1:
            return
        del content[ps]
        with open(newtblPath, 'w') as file:
            for line in content:
                file.write(line)
        module.command.load_tool_table() #Reload ToolTable


# ToolMagazine_Load
class ToolMagazine_Load(module.DataNode):
    def __init__(self):
        super().__init__("510514", "toolMagazine_Load", "VARIABLE")
    
    def value(self):
        return 0
    
    def set_value(self, value):
        with open(tblPath, 'r') as file:
            line = file.readlines()
        value = str(value).split(',')
        new_line = 'T{0} P{1} X{2} Y{3} Z{4} D{5}'.format(value[0], value[1], value[2], value[3], value[4], value[5])
        inserted_index = len(line)
        line.insert(inserted_index, new_line + '\n')

        with open(tblPath, 'w') as file:
            file.writelines(line)
        module.command.load_tool_table() #Reload ToolTable 


# tool_change M6
class Tool_Change(module.DataNode):
    def __init__(self):
        index = "510508"
        name = "toolChange"
        super().__init__(index, name, "toolChange")
    
    def value(self):
        value = hal.get_value("classicladder.0.in-113")
        return str(value)

    def set_value(self, value):
        hal.set_p("classicladder.0.in-113", value)


# M6 update toolPoc
class ToolPoc_Update(module.DataNode):
    def __init__(self):
        index = "510509"
        name = "toolPoc_Update"
        super().__init__(index, name, "toolPoc_Update")
    
    def value(self):
        try:
            tool = hal.get_value("motion.analog-out-00")
            poc = hal.get_value("motion.analog-out-01")
            mode = hal.get_value("motion.analog-out-02")
            # tool = hal.get_value("classicladder.0.floatout-01")
            # poc = hal.get_value("classicladder.0.floatout-02")
            # mode = hal.get_value("classicladder.0.floatout-03")
        except:
            print('M6 signal not found')
        return str(tool) + ':' + str(poc) + ":" + str(mode) #21:21:0


# M6完成
class M6Finish(module.DataNode):
    def __init__(self):
        super().__init__("510516", "M6Finish", "toolPoc_Update")

    def value(self):
        val = hal.get_value("classicladder.0.in-182")
        return str(val)

    def set_value(self, value):
        hal.set_p("classicladder.0.in-182", value)


# 入刀位-X1
class ToolChangeInsertionPosX1(module.DataNode):
    def __init__(self):
        super().__init__("510517", "ToolChangeInsertionPosX1", "VARIABLE")

    def value(self):
        return str(module.inifile.find("M6_Para", "ToolChange_InsertionPos_X1"))

    def set_value(self, value):
        module.setIniValue(module.stat.ini_filename, "M6_Para", "ToolChange_InsertionPos_X1",
                           value)


# 入刀位-X2
class ToolChangeInsertionPosX2(module.DataNode):
    def __init__(self):
        super().__init__("510518", "ToolChangeInsertionPosX2", "VARIABLE")

    def value(self):
        return str(module.inifile.find("M6_Para", "ToolChange_InsertionPos_X2"))

    def set_value(self, value):
        module.setIniValue(module.stat.ini_filename, "M6_Para", "ToolChange_InsertionPos_X2",
                           value)


# 入刀位-Y
class ToolChangeInsertionPosY(module.DataNode):
    def __init__(self):
        super().__init__("510519", "ToolChangeInsertionPosY", "VARIABLE")

    def value(self):
        return str(module.inifile.find("M6_Para", "ToolChange_InsertionPos_Y"))

    def set_value(self, value):
        module.setIniValue(module.stat.ini_filename, "M6_Para", "ToolChange_InsertionPos_Y",
                           value)


# 入刀位-Z
class ToolChangeInsertionPosZ(module.DataNode):
    def __init__(self):
        super().__init__("510520", "ToolChangeInsertionPosZ", "VARIABLE")

    def value(self):
        return str(module.inifile.find("M6_Para", "ToolChange_InsertionPos_Z"))

    def set_value(self, value):
        module.setIniValue(module.stat.ini_filename, "M6_Para", "ToolChange_InsertionPos_Z",
                           value)


# 出刀位-X1
class ToolChangeOutPosX1(module.DataNode):
    def __init__(self):
        super().__init__("510521", "ToolChangeOutPosX1", "VARIABLE")

    def value(self):
        return str(module.inifile.find("M6_Para", "ToolChange_OutPos_X1"))

    def set_value(self, value):
        module.setIniValue(module.stat.ini_filename, "M6_Para", "ToolChange_OutPos_X1",
                           value)


# 出刀位-X2
class ToolChangeOutPosX2(module.DataNode):
    def __init__(self):
        super().__init__("510522", "ToolChangeOutPosX2", "VARIABLE")

    def value(self):
        return str(module.inifile.find("M6_Para", "ToolChange_OutPos_X2"))

    def set_value(self, value):
        module.setIniValue(module.stat.ini_filename, "M6_Para", "ToolChange_OutPos_X2",
                           value)


# 出刀位-Y
class ToolChangeOutPosY(module.DataNode):
    def __init__(self):
        super().__init__("510523", "ToolChangeOutPosY", "VARIABLE")

    def value(self):
        return str(module.inifile.find("M6_Para", "ToolChange_OutPos_Y"))

    def set_value(self, value):
        module.setIniValue(module.stat.ini_filename, "M6_Para", "ToolChange_OutPos_Y",
                           value)


# 出刀位-Z
class ToolChangeOutPosZ(module.DataNode):
    def __init__(self):
        super().__init__("510524", "ToolChangeOutPosZ", "VARIABLE")

    def value(self):
        return str(module.inifile.find("M6_Para", "ToolChange_OutPos_Z"))

    def set_value(self, value):
        module.setIniValue(module.stat.ini_filename, "M6_Para", "ToolChange_OutPos_Z",
                           value)


# 安全位-X1
class ToolChangeSafePosX1(module.DataNode):
    def __init__(self):
        super().__init__("510525", "ToolChangeSafePosX1", "VARIABLE")

    def value(self):
        return str(module.inifile.find("M6_Para", "ToolChange_SafePos_X1"))

    def set_value(self, value):
        module.setIniValue(module.stat.ini_filename, "M6_Para", "ToolChange_SafePos_X1",
                           value)


# 安全位-X2
class ToolChangeSafePosX2(module.DataNode):
    def __init__(self):
        super().__init__("510526", "ToolChangeSafePosX2", "VARIABLE")

    def value(self):
        return str(module.inifile.find("M6_Para", "ToolChange_SafePos_X2"))

    def set_value(self, value):
        module.setIniValue(module.stat.ini_filename, "M6_Para", "ToolChange_SafePos_X2",
                           value)


# 安全位-Y
class ToolChangeSafePosY(module.DataNode):
    def __init__(self):
        super().__init__("510527", "ToolChangeSafePosY", "VARIABLE")

    def value(self):
        return str(module.inifile.find("M6_Para", "ToolChange_SafePos_Y"))

    def set_value(self, value):
        module.setIniValue(module.stat.ini_filename, "M6_Para", "ToolChange_SafePos_Y",
                           value)


# 安全位-Z
class ToolChangeSafePosZ(module.DataNode):
    def __init__(self):
        super().__init__("510528", "ToolChangeSafePosZ", "VARIABLE")

    def value(self):
        return str(module.inifile.find("M6_Para", "ToolChange_SafePos_Z"))

    def set_value(self, value):
        module.setIniValue(module.stat.ini_filename, "M6_Para", "ToolChange_SafePos_Z",
                           value)


# 左主轴定向角度
class ToolChangeSpindleAngle1(module.DataNode):
    def __init__(self):
        super().__init__("510529", "ToolChangeSpindleAngle1", "VARIABLE")

    def value(self):
        return str(module.inifile.find("M6_Para", "ToolChange_SpindleAngle1"))

    def set_value(self, value):
        module.setIniValue(module.stat.ini_filename, "M6_Para", "ToolChange_SpindleAngle1",
                           value)


# 右主轴定向角度
class ToolChangeSpindleAngle2(module.DataNode):
    def __init__(self):
        super().__init__("510530", "ToolChangeSpindleAngle2", "VARIABLE")

    def value(self):
        return str(module.inifile.find("M6_Para", "ToolChange_SpindleAngle2"))

    def set_value(self, value):
        module.setIniValue(module.stat.ini_filename, "M6_Para", "ToolChange_SpindleAngle2",
                           value)


# 左主轴最大刀位号
class ToolPocMax1(module.DataNode):
    def __init__(self):
        super().__init__("510531", "ToolPocMax1", "VARIABLE")

    def value(self):
        return str(module.inifile.find("M6_Para", "ToolPocMax1"))

    def set_value(self, value):
        module.setIniValue(module.stat.ini_filename, "M6_Para", "ToolPocMax1",
                           value)


# 右主轴最大刀位号
class ToolPocMax2(module.DataNode):
    def __init__(self):
        super().__init__("510532", "ToolPocMax2", "VARIABLE")

    def value(self):
        return str(module.inifile.find("M6_Para", "ToolPocMax2"))

    def set_value(self, value):
        module.setIniValue(module.stat.ini_filename, "M6_Para", "ToolPocMax2",
                           value)


# XX号刀位位置数据
class ToolPos(module.DataNode):
    def __init__(self, num):
        self.name = "ToolPos" + str(num)
        index = str(510533 + int(num))
        name = "ToolPos_" + str(num)
        super().__init__(index, name, "VARIABLE")

    def value(self):
        return str(module.inifile.find("M6_Para", self.name))

    def set_value(self, value):
        module.setIniValue(module.stat.ini_filename, "M6_Para", self.name,
                           value)


# 等待位x1移动位置
class ToolChangeWaitingPosX1(module.DataNode):
    def __init__(self):
        super().__init__("510557", "ToolChangeWaitingPosX1", "VARIABLE")

    def value(self):
        return str(module.inifile.find("M6_Para", "ToolChange_WaitingPos_X1"))

    def set_value(self, value):
        module.setIniValue(module.stat.ini_filename, "M6_Para", "ToolChange_WaitingPos_X1",
                           value)


# 等待位x2移动位置
class ToolChangeWaitingPosX2(module.DataNode):
    def __init__(self):
        super().__init__("510558", "ToolChangeWaitingPosX2", "VARIABLE")

    def value(self):
        return str(module.inifile.find("M6_Para", "ToolChange_WaitingPos_X2"))

    def set_value(self, value):
        module.setIniValue(module.stat.ini_filename, "M6_Para", "ToolChange_WaitingPos_X2",
                           value)


# 等待位Y移动位置
class ToolChangeWaitingPosY(module.DataNode):
    def __init__(self):
        super().__init__("510559", "ToolChangeWaitingPosY", "VARIABLE")

    def value(self):
        return str(module.inifile.find("M6_Para", "ToolChange_WaitingPos_Y"))

    def set_value(self, value):
        module.setIniValue(module.stat.ini_filename, "M6_Para", "ToolChange_WaitingPos_Y",
                           value)


# 等待位Z移动位置
class ToolChangeWaitingPosZ(module.DataNode):
    def __init__(self):
        super().__init__("510560", "ToolChangeWaitingPosZ", "VARIABLE")

    def value(self):
        return str(module.inifile.find("M6_Para", "ToolChange_WaitingPos_Z"))

    def set_value(self, value):
        module.setIniValue(module.stat.ini_filename, "M6_Para", "ToolChange_WaitingPos_Z",
                           value)


# 512200 HAL
class ToolHal_Update(module.DataNode):
    def __init__(self, num):
        self.toolHal_Index = halTool_Index[num]
        index = str(512200 + self.toolHal_Index)
        name = str(num)
        self.pin = config.halpin_tool_update
        super().__init__(index, name, "toolHal_Update")

    def value(self):
        val = hal.get_value(self.pin.format(self._name))
        return str(val)

    def set_value(self, value):
        st = self.pin.format(self._name)
        hal.set_p(st, value)


# 512300 cutter_meassure_done
class CutterMeassureDone(module.DataNode):
    def __init__(self):
        index = str(512300)
        name = str(index)
        self.pin = config.cutter_meassure_done
        super().__init__(index, name, "CutterMeassureDone")

    # get_value
    def value(self):
        try:
            val = hal.get_value(self.pin.format(self._name))
            if val:
                return str(1)
            else:
                return str(0)
        except Exception as e:
            print("CutterMeassureDone::value::{}".format(e))

    # set_value
    def set_value(self, value):
        try:
            st = self.pin.format(self._name)
            hal.set_p(st, value)
        except Exception as e:
            print("CutterMeassureDone::set_value::{}".format(e))


# 512301 cutter_meassure_reset
class CutterMeassureReset(module.DataNode):
    def __init__(self):
        index = str(512301)
        name = str(index)
        self.pin = config.cutter_meassure_reset
        super().__init__(index, name, "CutterMeassureReset")

    def value(self):
        try:
            val = hal.get_value(self.pin.format(self._name))
            return str(val)
        except Exception as e:
            print("CutterMeassureReset::value::{}".format(e))

    def set_value(self, value):
        try:
            st = self.pin.format(self._name)
            hal.set_p(st, value)
        except Exception as e:
            print("CutterMeassureReset::set_value::{}".format(e))

# 512304 刀盘中指向刀口位置的刀号。
class CutterNumberOfHead(module.DataNode):
    def __init__(self):
        index = str(512304)
        name = str(index)
        self.pin = config.cutter_number_of_head
        super().__init__(index, name, "CutterNumberOfHead")

    def value(self):
        try:
            val = hal.get_value(self.pin.format(self._name))
            return str(val)
        except Exception as e:
            # pass
            print("CutterNumberOfHead::{} error".format(e))
