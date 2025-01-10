from window_class import class_window as window
from data_api import nc_data as data


class ToolDataWindow(window.WindowTable):
    def __init__(self):
        super().__init__()

    def init_table(self):
        self.add_item(data.task_mode)
        self.add_item(data.current_coordinate)

        self.add_item(data.tool_count)
        self.add_item(data.tool_diameter)
        self.add_item(data.tool_table)  # newAdd
        self.add_item(data.toolMagazine_table)  # newAdd
        self.add_item(data.toolMagazine_Unload)
        self.add_item(data.toolMagazine_Load)
        self.add_item(data.tool_status)
        self.add_item(data.toolMagazine_Move)
        self.add_item(data.tool_Change)
        self.add_item(data.toolPoc_Update)
        self.add_item(data.tool_New)
        self.add_item(data.tool_Cancel)
      #  self.add_item(data.move_Pos)

        

        # nc_data.c_tool.add_data_item(nc_data.tool_offset)  #newAdd
        for i in range(1, 50):
            self.add_item(data.tool_ID[i - 1])
        for i in range(1, 50):
            self.add_item(data.tool_offset_X[i - 1])
        for i in range(1, 50):
            self.add_item(data.tool_offset_Y[i - 1])
        for i in range(1, 50):
            self.add_item(data.tool_offset_Z[i - 1])
        for i in range(1, 50):
            self.add_item(data.tool_diameter_Set[i - 1])

        self.add_item(data.program_name)
