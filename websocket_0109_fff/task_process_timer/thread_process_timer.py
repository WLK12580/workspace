import time

from task_process_timer import processing_timer as processing_timer
from data_class import nc_module as module
import threading
import linuxcnc
import hal

process_done = 0
process_pause = 1
process_exec = 2
process_error = 3


class ProcessStateMachine:
    def __init__(self):
        self.current_state = process_done  # 当前NC执行状态
        self.isFinished = False  # 程序是否完成
        self.isReset = False  # 程序是否复位
        self.timer = processing_timer.ProcessingTimer()

    # 开始检测运行状态
    def start_task(self):
        t = threading.Thread(target=self.task_loop)
        t.start()

    # 获取程序执行时间
    def get_total_time(self):
        return self.timer.get_total_time()

    # 状态机循环任务
    def task_loop(self):
        while True:
            self.state_machine()
            time.sleep(0.05)

    # 获取当前程序执行状态
    def get_current_state(self):
        # 空闲
        if hal.get_value("halui.program.is-idle"):
            return process_done
        # 运行
        elif hal.get_value("halui.program.is-running"):
            return process_exec
        # 暂停
        elif hal.get_value("halui.program.is-paused"):
            return process_pause
        else:
            return process_error

    # 程序运行中点击复位按钮
    def reset_program(self):
        self.isReset = True

    def state_machine(self):
        """状态切换"""
        module.update()
        # if not (module.stat.task_mode == linuxcnc.MODE_AUTO or self.current_state == process_exec):
        #     return

        if self.current_state == process_done:
            # done -> exec
            if self.get_current_state() == process_exec:
                self.timer.start()
                self.current_state = process_exec
                self.isFinished = False
                self.isReset = False

        elif self.current_state == process_exec:
            # exec -> pause
            if self.get_current_state() == process_pause:
                self.timer.pause()
                self.current_state = process_pause
            # exec -> done
            elif self.get_current_state() == process_done:
                self.timer.stop()
                self.current_state = process_done
                # 检测M30作为程序结束
                m30 = 30
                if m30 in module.stat.mcodes and not self.isReset:
                    self.isFinished = True
            # exec -> error
            elif self.get_current_state() == process_error:
                self.timer.pause()
                self.current_state = process_error

        elif self.current_state == process_pause:
            # pause -> exec
            if self.get_current_state() == process_exec:
                self.timer.resume()
                self.current_state = process_exec
            # pause -> done
            elif self.get_current_state() == process_done:
                self.timer.stop()
                self.current_state = process_done

        elif self.current_state == process_error:
            # error -> exec
            if self.get_current_state() == process_exec:
                self.timer.resume()
                self.current_state = process_exec
            # error -> done
            elif self.get_current_state() == process_done:
                self.timer.stop()
                self.current_state = process_done


process_task = ProcessStateMachine()
