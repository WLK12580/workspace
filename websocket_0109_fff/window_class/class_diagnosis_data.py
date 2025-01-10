from window_class import class_window as window
from data_api import nc_data as data

class DiagnosisDataWindow(window.WindowTable):
    def __init__(self):
        super().__init__()

    def init_table(self):
        # [3170] 轴诊断-伺服准备好
        for item in data.axis_ready_to_switch_on:
            self.add_item(item)

        # [3171] 轴诊断-可以开启伺服运行
        for item in data.axis_switch_on:
            self.add_item(item)

        # [3172] 轴诊断-伺服运行
        for item in data.axis_operation_enabled:
            self.add_item(item)

        # [3173] 轴诊断-故障
        for item in data.axis_fault:
            self.add_item(item)

        # [3174] 轴诊断-主回路电接通
        for item in data.axis_voltage_enabled:
            self.add_item(item)

        # [3175] 轴诊断-快速停机
        for item in data.axis_quick_stop:
            self.add_item(item)

        # [3176] 轴诊断-伺服不可运行
        for item in data.axis_switch_on_disabled:
            self.add_item(item)

        # [3177] 轴诊断-警告
        for item in data.axis_warning:
            self.add_item(item)

        # [3179] 轴诊断-远程控制
        for item in data.axis_remote:
            self.add_item(item)

        # [3180] 轴诊断-目标直达
        for item in data.axis_target_reach:
            self.add_item(item)

        # [3181] 轴诊断-内部位置超限
        for item in data.axis_internal_limit_active:
            self.add_item(item)

        # [3182] 轴诊断-目标位置更新
        for item in data.axis_set_point_acknowledge:
            self.add_item(item)

        # [3183] 轴诊断-跟随误差
        for item in data.axis_following_error:
            self.add_item(item)

        # [3184] 轴诊断-扭矩限制激活
        for item in data.axis_torque_limit_active:
            self.add_item(item)

        # [3185] 轴诊断—原点已找到
        for item in data.axis_home_find:
            self.add_item(item)