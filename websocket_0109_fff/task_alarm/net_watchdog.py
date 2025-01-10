import threading
import time
from data_class import nc_module as module
import copy

class WatchDog(module.AlarmItem):
    connect_state = False  # 网络状态标志位
    counter = 0  # 计数器
    max_counter = 5  # 计数器溢出的最大值

    def __init__(self):
        """
        """
        super().__init__("HMI", "通讯故障，网络断开","alarm")

    @staticmethod
    def feed():
        WatchDog.connect_state = True

    def reset_flag(self):
        WatchDog.connect_state = False
        WatchDog.counter = 0

    def check_flag(self):
        # 检测标志位
        if WatchDog.connect_state:
            self.reset_flag()
        else:
            WatchDog.counter += 1
        # 检测计数器
        if WatchDog.counter >= WatchDog.max_counter:
            if self.flag:
                self.trigger_alarm()
                self.flag = False
        else:
            if not self.flag:
                self.end_alarm_override()
            self.flag = True

    def run_task(self):
        while True:
            self.check_flag()
            time.sleep(1)

    def start_task(self):
        thread = threading.Thread(target=self.run_task)
        thread.start()

    def end_alarm_override(self):
        self.struct.end_time = time.strftime("%Y-%m-%d,%H:%M:%S", time.localtime())
        struct = copy.copy(self.struct)
        module.AlarmItem._history_hardreset_alarms.append(struct)
        module.AlarmItem._current_hardreset_alarms.remove(self)

    def update(self):
        """
        :return:
        """
