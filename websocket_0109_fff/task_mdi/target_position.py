import linuxcnc
import hal
from data_class import nc_module as module
import time
import threading
import config


class TargetPosition:
    """
    _target_pos:目标位置，最终位置
    _feed:初始进给速度
    _rate:进给倍率
    """
    _position = {}
    _feed = None
    _rate = None
    _spindle = config.position_spindle_list[0]

    @staticmethod
    def feed():
        return TargetPosition._feed*float(60000)

    @staticmethod
    def set_feed(feed: int):
        """
        设置定位进给速度
        :param feed: 进给速度 mm/min => m/s
        :return:
        """
        TargetPosition._feed = float(feed)/float(60000)

    @staticmethod
    def set_rate(rate: float):
        """
        设置进给倍率
        item = [joint_id, pos_type, distance, tar_pos]
        item[0]:joint_id:关节号
        item[1]:pos_type:定位方式，[abs:绝对,inc：相对]
        item[2]:distance:距离，[abs:目标位置,inc：增量]
        item[3]:tar_pos:目标位置
        :param rate: 进给倍率
        :return:
        """
        lists = TargetPosition._position
        for key in lists:
            item = lists[key]
            joint_id = item[0]
            axis_id, act_pos = TargetPosition.get_curr_wcs_pos(joint_id)
            linuxcnc.command().jog(linuxcnc.JOG_INCREMENT, 0, axis_id, rate * TargetPosition._feed, 0)

    @staticmethod
    def add_position(joint_id: int, pos_type: str, distance: float):
        """
        添加定位指令
        :param joint_id: 关节编号
        :param pos_type: 定位方式 abs:绝对，inc：相对
        :param distance: 路程
        :return:
        """
        axis_name, axis_id = module.get_axis_id(joint_id)
        pin_name = "halui.axis.*.pos-relative"
        # 工件坐标引脚
        pos_pin = pin_name.replace("*", axis_name.lower())
        # 关节的工件坐标值
        act_pos = float(hal.get_value(pos_pin))
        tar_pos = None
        # 计算关节的目标位置
        if pos_type == "inc":
            tar_pos = distance + act_pos
        elif pos_type == "abs":
            tar_pos = distance
        item = [axis_id, pos_type, distance, tar_pos]
        TargetPosition._position[joint_id] = item

    @staticmethod
    def add_spindle_position(pos_type: str, distance: float):
        """
        添加定位指令
        :param pos_type: 定位方式 abs:绝对，inc：相对
        :param distance: 路程
        :return:
        """
        axis_id = module.get_axis_id_by_name(TargetPosition._spindle)
        pin_name = "halui.axis.*.pos-relative"
        # 工件坐标引脚
        pos_pin = pin_name.replace("*", TargetPosition._spindle.lower())
        # 关节的工件坐标值
        act_pos = float(hal.get_value(pos_pin))
        tar_pos = None
        # 计算关节的目标位置
        if pos_type == "inc":
            tar_pos = distance + act_pos
        elif pos_type == "abs":
            tar_pos = distance
        item = [axis_id, pos_type, distance, tar_pos]
        TargetPosition._position["spindle"] = item

    @staticmethod
    def clear_position():
        """
        清空定位指令
        :return:
        """
        TargetPosition._position.clear()
        TargetPosition._feed = 0

    @staticmethod
    def position():
        """
        执行定位
        item = [joint_id, pos_type, distance, tar_pos]
        item[0]:joint_id:关节号
        item[1]:pos_type:定位方式，[abs:绝对,inc：相对]
        item[2]:distance:距离，[abs:目标位置,inc：增量]
        item[3]:tar_pos:目标位置
        :return:
        """
        for key in TargetPosition._position:
            item = TargetPosition._position[key]
            print(item)
            joint_id = item[0]
            tar_pos = item[3]
            axis_id, act_pos = TargetPosition.get_curr_wcs_pos(joint_id)
            dtg = tar_pos - act_pos
            print("dtg:" + str(dtg))
            linuxcnc.command().jog(linuxcnc.JOG_INCREMENT, 0, axis_id, TargetPosition._feed, dtg)

        # 关闭循环启动按键信号
        hal.set_p(config.halpin_position_reset, "1")
        time.sleep(0.1)
        hal.set_p(config.halpin_position_reset, "0")

    @staticmethod
    def pause_position():
        hal.set_p("halui.abort", "1")
        time.sleep(0.1)
        hal.set_p("halui.abort", "0")

    @staticmethod
    def get_curr_wcs_pos(joint_id: int):
        axis_name, axis_id = module.get_axis_id(joint_id)
        pin_name = "halui.axis.*.pos-relative"
        curr_pin = pin_name.replace("*", axis_name.lower())
        curr = float(hal.get_value(curr_pin))
        return axis_id, curr


class PositionStateMachine:
    """
    idle = 0
    exec = 1
    pause = 2
    """
    _current_state = "idle"
    _pin_pause = config.halpin_position_pause
    _pin_resume = config.halpin_position_resume
    _pin_state = config.halpin_position_state
    _thread = None  # threading.Thread(target=PositionStateMachine.task_loop)

    @staticmethod
    def current_state():
        return PositionStateMachine._current_state

    @staticmethod
    def start():
        if PositionStateMachine._current_state == "exec":
            return
        print("start position")
        PositionStateMachine._current_state = "exec"
        module.position_is_exec = 1  # 定位功能开始执行标志
        TargetPosition.position()
        PositionStateMachine.run()
        hal.set_p(PositionStateMachine._pin_state, "1")

    @staticmethod
    def pause():
        if PositionStateMachine._current_state == "pause":
            return
        PositionStateMachine._current_state = "pause"
        # TargetPosition.pause_position()
        hal.set_p(PositionStateMachine._pin_state, "2")

    @staticmethod
    def resume():
        PositionStateMachine.start()

    @staticmethod
    def stop():
        PositionStateMachine._current_state = "idle"
        hal.set_p(PositionStateMachine._pin_state, "0")

    @staticmethod
    def state_machine():
        match PositionStateMachine._current_state:
            case "exec":
                # 有暂停信号
                if hal.get_value(PositionStateMachine._pin_pause):
                    print("pause")
                    PositionStateMachine.pause()
                # 无暂停信号 调整倍率
                else:
                    rate = float("%.2f" % module.stat.feedrate)
                    TargetPosition.set_rate(rate)
                return True
            case "pause":
                # 有恢复信号
                if hal.get_value(PositionStateMachine._pin_resume):
                    PositionStateMachine.resume()
                return True
            case "idle":
                TargetPosition.clear_position()
                print("position finished")
                return False

    @staticmethod
    def task_loop():
        ret = True
        while ret:
            ret = PositionStateMachine.state_machine()
            time.sleep(0.1)

    @staticmethod
    def run():
        if PositionStateMachine._thread is None or not PositionStateMachine._thread.is_alive():
            PositionStateMachine._thread = threading.Thread(target=PositionStateMachine.task_loop)
            PositionStateMachine._thread.start()
