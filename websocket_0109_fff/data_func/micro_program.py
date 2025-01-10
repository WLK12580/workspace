import os
from data_class import nc_module as module
import config


# 读取配置文件并返回结果
def read_conf():
    return module.NCKPath + config.nc_ini_name, module.MicroProgramPath


# 读取LinuxCNC配置文件并尝试修改目标部分重新写入
def get_ini_content():
    ini_path, nc_filedir_path = read_conf()
    print(ini_path)
    print(nc_filedir_path)
    try:
        fini = open(ini_path, 'r')

        try:
            ini_content = fini.read()
            fini.close()
        except:
            print("getIniContent():read <" + ini_path + "> final!")
            fini.close()
            return [""]

    except:
        print("getIniContent():open <" + ini_path + "> final!")
        return [""]

    index = ini_content.find("#remap start")
    if index == -1:
        print("getIniContent():ini file no exists valid content")
        return [""]

    inilist = ini_content.split('\n')
    return inilist


# 修改配置文件
def update_ini(num, old, new):
    ini_list = get_ini_content()
    ini_path, nc_filedir_path = read_conf()
    listlen = len(ini_list)

    if listlen == 0:
        print(listlen)
        return False

    try:
        index = ini_list.index("#remap start")
    except:
        print("nc ini there is no valid marking!")
        return False

    index += 1

    # num=0->m
    # num=1->m代号
    # num=2->m组
    # num=3->g
    # num=4->g代号
    # num=5->g组

    if num == '0':
        oldprefix = 'M'
    elif num == '1' or num == '2':
        oldprefix = 'm'
    elif num == '3':
        oldprefix = 'G'
    elif num == '4' or num == '5':
        oldprefix = 'g'
    else:
        return False

    pos = -1
    for i in range(index, listlen):
        if ini_list[i].find("#remap end") != -1:
            break
        if len(ini_list[i]) == 0 or ini_list[i][0] == '#':
            continue
        if ini_list[i].find(oldprefix + old) != -1:
            pos = i
            break

    if pos == -1:
        return False

    # 开始修改
    nctmp = ini_list[pos]

    # 0 3 修改 nclist[0]
    # 1 4 修改 nclist[2]
    if num == '0' or num == '3':
        nctmp = nctmp.replace(oldprefix + old, oldprefix + new)
        if nctmp == ini_list[pos]: return False
    elif num == '1' or num == '4':
        nctmp = nctmp.replace(oldprefix + old, oldprefix + new)
        if nctmp == ini_list[pos]: return False
        ok = update_nc_file(oldprefix, old, new)
        if ok == False:
            return False
    elif num == '2' or num == '5':
        nctmplen = len(nctmp)
        ipos = nctmp.find('modalgroup')
        if ipos == -1:
            return False
        ipos = nctmp.find('=', ipos)
        if ipos == -1:
            return False
        ipos += 1
        while ipos < nctmplen and nctmp[ipos] == ' ': ipos += 1
        startpos = ipos
        while ipos < nctmplen and nctmp[ipos] != ' ':  ipos += 1
        nctmp = nctmp[0:startpos] + new + nctmp[ipos:nctmplen]

    # 修改到表中
    ini_list[pos] = nctmp

    # 整合成一个字符串 直接写入文件
    filestr = ""
    for i in range(0, listlen):
        filestr += ini_list[i]
        if i + 1 < listlen:
            filestr += '\n'

    # 持久化到配置文件
    with open(file=ini_path, mode='w', encoding='utf-8') as inifile:
        inifile.write(filestr)

    return True


# 修改nc文件和文件名
def update_nc_file(prefix, old, new):
    ini_path, nc_filedir_path = read_conf()
    dirfilelist = os.listdir(nc_filedir_path)
    suffix = ".ngc"

    try:
        pos = dirfilelist.index(prefix + old + suffix)
    except:
        print(f"updateNCFile(prefix,old,new):dir <{nc_filedir_path}> no {prefix + old} nc file!")
        return False

    ncfilepath = nc_filedir_path + dirfilelist[pos]

    try:
        fnc = open(ncfilepath)
        try:
            ncfile_content = fnc.read()
            fnc.close()
        except:
            print("updateNCFile(prefix,old,new):read <" + ncfilepath + "> final!")
            fnc.close()
            return False

    except:
        print("updateNCFile(prefix,old,new):open <" + ncfilepath + "> final!")
        return False

    ncfile_content_list = ncfile_content.split("<" + prefix + old + ">")

    filestr = ""
    ncfile_content_list_len = len(ncfile_content_list)
    for i in range(0, ncfile_content_list_len):
        filestr += ncfile_content_list[i]
        if i + 1 < ncfile_content_list_len:
            filestr += ("<" + prefix + new + ">")

    oldfilename = prefix + old + suffix
    newfilename = prefix + new + suffix

    with open(ncfilepath, 'w') as wncfile:
        wncfile.write(filestr)

    os.rename(nc_filedir_path + oldfilename, nc_filedir_path + newfilename)

    return True


def interceptestr(sstr, finds):
    tmps = ""
    sstrlen = len(sstr)
    ipos = sstr.find(finds)
    if ipos == -1:
        return ""
    ipos = sstr.find('=', ipos)
    if ipos == -1:
        return ""
    ipos += 1
    while ipos < sstrlen and sstr[ipos] == ' ': ipos += 1
    startpos = ipos
    while ipos < sstrlen and sstr[ipos] != ' ':
        tmps += sstr[ipos]
        ipos += 1

    return tmps


# 获取配置文件信息上传到宏程序界面
def get_file_table():
    ini_content = get_ini_content()

    try:
        index = ini_content.index("#remap start")
    except:
        print("nc ini there is no valid marking!")
        return ""

    index += 1
    listlen = len(ini_content)

    ini_conf_list = []

    for i in range(index, listlen):
        if ini_content[i].find("#remap end") != -1:
            break
        if len(ini_content[i]) == 0 or ini_content[i][0] == '#':
            continue

        ini_conf_list.append(ini_content[i])

    tablelist = []
    ini_conf_list_len = len(ini_conf_list)
    for i in range(0, ini_conf_list_len):
        # 取出字母和数字
        tablelist.append(interceptestr(ini_conf_list[i], 'REMAP') + '|' + interceptestr(ini_conf_list[i],
                                                                                        'ngc') + '|' + interceptestr(
            ini_conf_list[i], 'modalgroup'))

    tablelistlen = len(tablelist)
    initstr = ""
    # M代号|m程序|M组
    # G代号|g程序|G组
    for i in range(0, tablelistlen):
        initstr += tablelist[i]
        if i + 1 < tablelistlen: initstr += '\n'

    return initstr


# 接收和执行程序
def receive(msg):  # msg类型是str
    datalist = msg.split("|")
    if datalist[1] == datalist[2]:
        return
    elif datalist[0] == "init":
        tablestr = "init\n" + get_file_table()
        send_message(tablestr)
    elif str(datalist[0]).isdigit():
        numstr = str(datalist[0])
        ok = update_ini(datalist[0], datalist[1], datalist[2])
        if ok == False:
            send_message("UPDATE FINAL")  # 向对端返回失败结果

    return


# 获取宏程序信息
def get_mirco_program_data():
    table_str = "init\n" + get_file_table()
    return table_str


# 修改宏程序值
def set_mirco_program_data(data):
    data_list = data.split("|")
    if data_list[1] == data_list[2]:
        return
    ok = update_ini(data_list[0], data_list[1], data_list[2])
    if not ok:
        print("UPDATE FINAL")  # 设置失败


def send_message(msg):
    # utf-8转码
    # 网络发送
    return

# ---------------------------------------------------------------------------------------
# 收到消息后调用    receive(接收的字符串 必须decode('utf-8'))
