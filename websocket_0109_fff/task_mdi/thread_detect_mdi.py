import threading

import linuxcnc
import hal
import config
from data_class import nc_module as module
from data_class import nc_action as action
from task_mdi import target_position as target_position
import time


class MdiThread():
    _mdi_cmd = []
    _mdi_current_line = -1  # mdi当前行
    _position = {0: [],
                 1: [],
                 2: [],
                 3: [],
                 4: [],
                 5: [],
                 6: [],
                 7: [],
                 8: []}
    _mdi_flag = False
    _feed_speed = 0
    _position_flag = False
    _position_exec_state = False
    _jump_segment_flag = False
    _jump_segment_line = 0

    @staticmethod
    def add_mdi_cmd(cmd: str):
        MdiThread._mdi_cmd.append(cmd)

    @staticmethod
    def clear_mdi_cmd():
        MdiThread._mdi_cmd.clear()

    @staticmethod
    def set_position_feed(speed: int):
        MdiThread._feed_speed = speed

    @staticmethod
    def add_position(joint_id: int, pos_type: str, distance: float):
        """
        :param joint_id: 关节编号
        :param pos_type: 定位方式 abs:绝对，inc：相对
        :param distance: 路程
        :return:
        """
        item = [joint_id, pos_type, distance]
        MdiThread._position[joint_id] = item
        MdiThread._position_flag = True

    @staticmethod
    def execute_mdi():
        if MdiThread._mdi_flag:
            return
        MdiThread._mdi_flag = True
        task = threading.Thread(target=MdiThread.mdi_task)
        task.start()
        print("execute_mdi")

    @staticmethod
    def mdi_current_line()->int:
        return MdiThread._mdi_current_line

    @staticmethod
    def mdi_task():
        print("mdi task")
        # '/home/top/share/temp/mdi.ngc'
        MdiThread._mdi_current_line = 0
        with open(module.MdiPath, 'r', encoding='utf-8') as file:
            for line in file:
                cmd = line.strip()
                module.command.mdi(cmd)
                MdiThread._mdi_current_line += 1
                time.sleep(0.02)
                while module.stat.motion_type != 0:
                    module.stat.poll()
                    time.sleep(0.01)
                module.command.load_tool_table()
                print(cmd)
                time.sleep(0.1)
            file.close()

        MdiThread._mdi_current_line = -1
        # mdi执行后刷新文件
        module.command.load_tool_table()
        hal.set_p(config.halpin_mdi_reset, "1")
        time.sleep(0.1)
        hal.set_p(config.halpin_mdi_reset, "0")
        MdiThread._mdi_flag = False

    @staticmethod
    def execute_position():
        """
        item[0] = joint_id
        item[1] = pos_type
        item[2] = distance
        :return:
        """
        if not MdiThread._position_flag:
            return
        module.position_is_exec = 1  # 定位功能开始执行标志
        for key in MdiThread._position:
            item = MdiThread._position[key]
            print(item)
            dtg = 0
            if not item:
                continue
            joint_id = item[0]
            axis_name, axis_id = module.get_axis_id(joint_id)
            if item[1] == "inc":
                dtg = item[2]
            elif item[1] == "abs":
                distance = float(item[2])
                pin_name = "halui.axis.*.pos-relative"
                curr_pin = pin_name.replace("*", axis_name.lower())
                curr = float(hal.get_value(curr_pin))
                dtg = distance - curr
            print("dtg:" + str(dtg))
            linuxcnc.command().jog(linuxcnc.JOG_INCREMENT, 0, axis_id, MdiThread._feed_speed, dtg)
        print("定位程序执行")
        MdiThread._position_exec_state = True

        # 坐标复位
        MdiThread._position.clear()
        MdiThread._feed_speed = 0
        MdiThread._coordinate = None
        MdiThread._position_flag = False

        # 关闭循环启动按键信号
        hal.set_p(config.halpin_position_reset, "1")
        time.sleep(0.1)
        hal.set_p(config.halpin_position_reset, "0")

    def run_mdi(self):
        while True:
            if MdiThread._mdi_flag:
                continue
            MdiThread._mdi_flag = True

    # 获取面板循环启动信号
    def get_mdi_signal(self):
        # MDI 或 JOG
        task = threading.Thread(target=MdiThread.mdi_task)
        while True:
            # 执行MDI
            if hal.get_value("halui.mode.is-mdi"):
                if hal.get_value(config.halpin_mdi_excute):
                    """
                    print("mdi:")
                    print(MdiThread._mdi_cmd)
                    for cmd_item in MdiThread._mdi_cmd:
                        module.command.mdi(cmd_item)
                    # mdi执行后刷新文件
                    module.command.load_tool_table()
                    hal.set_p(config.halpin_mdi_reset, "1")
                    time.sleep(0.1)
                    hal.set_p(config.halpin_mdi_reset, "0")
                    """
                    MdiThread.execute_mdi()

            # 执行定位
            if hal.get_value("halui.mode.is-manual"):
                if hal.get_value(config.halpin_position_excute):
                    # 通知plc进入定位模式
                    hal.set_p(config.halpin_position_flag, "1")
                    if hal.get_value("halui.mode.is-teleop"):
                        target_position.PositionStateMachine.start()

            # 执行跳段
            if hal.get_value("halui.mode.is-auto"):
                if hal.get_value(config.halpin_jump_segment_flag):
                    if hal.get_value(config.halpin_jump_segment_excute):
                        # 通知plc进入跳段模式
                        MdiThread.execute_jump_segment()
            time.sleep(0.2)

    # 检测定位执行结束，通知plc退出定位模式
    # mdi监控线程
    @staticmethod
    def detect_position_finished():
        while True:
            # 定位模式下，运动停止时，关闭定位模式
            # hal.get_value(config.halpin_position_flag) and
            if target_position.PositionStateMachine.current_state() == "exec":
                if hal.get_value("motion.jog-is-active") == False :
                    hal.set_p(config.halpin_position_flag, "0")
                    MdiThread._position_exec_state = False
                    target_position.PositionStateMachine.stop()


            time.sleep(0.3)

    # 跳段模式开启或关闭
    @staticmethod
    def set_jump_segment_enable(toggle: bool):
        """
        :param toggle:  True:开启 False：关闭
        :return: 
        """
        if toggle:
            hal.set_p(config.halpin_jump_segment_flag, "1")
        else:
            hal.set_p(config.halpin_jump_segment_flag, "0")

    # 跳段模式行
    @staticmethod
    def set_jump_segment_line(line: int):
        if line >= 0:
            MdiThread._jump_segment_line = line
            MdiThread._jump_segment_flag = True

    # 执行跳段
    @staticmethod
    def execute_jump_segment():
        if not MdiThread._jump_segment_flag:
            return
        linuxcnc.command().auto(linuxcnc.AUTO_RUN, MdiThread._jump_segment_line)

        MdiThread._jump_segment_line = 0
        MdiThread._jump_segment_flag = False
        hal.set_p(config.halpin_jump_segment_flag, "0")

        # 关闭循环启动按键信号
        # hal.set_p(config.halpin_jump_segment_reset, "1")
        # time.sleep(0.1)
        # hal.set_p(config.halpin_jump_segment_reset, "0")
