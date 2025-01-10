import time


class ProcessingTimer:
    def __init__(self):
        self.start_time = None  # 记录开始时间
        self.total_paused_time = 0  # 记录总共暂停的时间
        self.pause_start_time = None  # 记录暂停开始时间
        self.is_running = False  # 记录计时器是否正在运行
        self.total_time = 0  # 记录加工时间

    def start(self):
        """开始计时"""
        self.start_time = time.time()
        self.total_paused_time = 0
        self.pause_start_time = None
        self.is_running = True
        self.total_time = 0
        print("Processing started.")

    def pause(self):
        """暂停计时"""
        if self.is_running:
            self.pause_start_time = time.time()
            self.is_running = False
            print("Processing paused.")

    def resume(self):
        """恢复计时"""
        if not self.is_running:
            if self.pause_start_time:
                # 如果之前暂停过，则将暂停的时间加入总暂停时间中
                paused_duration = time.time() - self.pause_start_time
                self.total_paused_time += paused_duration
                self.pause_start_time = None
            self.is_running = True
            print("Processing resumed.")

    def stop(self):
        """停止计时并输出总时间"""
        if self.is_running:
            self.pause()
            # 计算总时间，减去总暂停时间
            self.total_time = time.time() - self.start_time - self.total_paused_time
        else:
            self.total_time = self.pause_start_time - self.start_time - self.total_paused_time
        self.is_running = False
        # 转换为时分秒格式
        hours, remainder = divmod(self.total_time, 3600)
        minutes, seconds = divmod(remainder, 60)
        print(f"Processing stopped. Total time: {int(hours)} hours, {int(minutes)} minutes, {int(seconds)} seconds.")

    def get_total_time(self):
        if self.is_running:
            self.total_time = time.time() - self.start_time - self.total_paused_time
            return self.total_time
        else:
            return self.total_time
