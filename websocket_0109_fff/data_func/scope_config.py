import os.path
import time

import hal

import config
import shutil

scopePath = "/home/" + config.username + "/share/scope/"
print("scopePath: " + scopePath)


# 示波器数据文件检测
class ScopeDataThread:
    def __init__(self, path, name, flag):
        self._path = path
        self._name = name
        self._export_flag = flag

    def detect_file_exist(self):
        while not self._export_flag:
            if os.path.exists(self._path):
                print("示波器数据已导出")
                # 复制文件到share，并删除源文件
                if os.path.exists(config.scope_data_path):
                    print(config.scope_data_path)
                    print(scopePath + self._name)
                    shutil.copyfile(str(config.scope_data_path), str(scopePath + self._name))
                os.remove(config.scope_data_path)
                # 发送导出信号
                hal.set_p(config.scope_export_flag, "1")
                hal.set_p(config.scope_start_sample, "0")
                self._export_flag = True
            else:
                print("示波器数据未导出")

            time.sleep(0.5)


# 示波器配置文件解析
class ParseScopeFile:
    def __init__(self, path):
        self._path = path
        self._content = {}
        self._channelCounts = 0
        self._channelNameList = []

    def load(self):
        print("load scope file")
        with open(self._path, "r", encoding="utf-8") as f:
            all_content = f.readlines()
            for lineNo, line in enumerate(all_content):
                line = line.replace("\n", "")

                # channel id
                if line.startswith("CHAN"):
                    self._channelCounts = self._channelCounts + 1
                    chanId = line.replace(" ", "")
                    self._channelNameList.append(chanId)

                    # channel item
                    for i in range(4):
                        tmp = all_content[lineNo + i + 1].replace("\n", "")
                        name = tmp.split(" ")[0]
                        val = tmp.split(" ")[1]
                        self._content.setdefault(chanId, {}).setdefault(name, val)
                    continue

                if line.startswith("PIN") or line.startswith("VSCALE") or line.startswith("VPOS") or line.startswith("VOFF"):
                    continue
                name = line.split(" ")[0]
                val = line.split(" ")[1]
                self._content.setdefault(name, val)
        f.close()

    def getValue(self, name, sub_name = None):
        '''
        读取配置文件参数
        :param name: 通道名：CHAN1、CHAN2 或 非通道所属参数名：THREAD、HMULT等
        :param sub_name: 通道所属参数名：PIN、VSCALE等，非通道所属参数使用默认参数 None
        :return: 返回参数值，未找到返回字符串“scope param is not found”
        '''
        value = "scope param is not found"
        if name in self._content:
            if sub_name is None:
                value = self._content[name]
            else:
                if sub_name in self._content[name]:
                    value = self._content[name][sub_name]
        return value

    # 设置参数
    def setValue(self, value, name, sub_name = None):
        '''
        设置配置文件参数
        :param value: 设置参数值
        :param name: 通道名 或 非通道参数名
        :param sub_name: 通道所属参数名
        :return:
        '''
        # print("set scope value")
        if name in self._content:
            if sub_name is None:
                self._content[name] = value
            else:
                if sub_name in self._content[name]:
                    self._content[name][sub_name] = value

    # 刷新文件
    def update(self):
        with open(self._path, "w", encoding="utf-8") as f:
            for key, value in self._content.items():
                if type(value) is dict:
                    f.write(key[:4] + " " + key[4:] + "\n")
                    for subkey in self._content[key]:
                        f.write(subkey + " " + self._content[key][subkey] + "\n")
                else:
                    f.write(key + " " + value + "\n")
        f.close()

    # 获取通道个数
    def getChannelCounts(self):
        return self._channelCounts

    # 获取通道列表
    def getChannelList(self):
        return self._channelNameList
