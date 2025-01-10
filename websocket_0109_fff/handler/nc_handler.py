import asyncio

import tornado.websocket
import tornado.web
import tornado.gen
import tornado.ioloop
import json
from window_api import nc_window
from task_alarm import net_watchdog as net_watchdog
from data_class import class_ncplc as class_ncplc

class APIHandler(tornado.web.RequestHandler):
    def get(self):
        # print("process")
        self.write(json.dumps(nc_window.process_window.data()))


class SystemWindowHandler(tornado.web.RequestHandler):
    def get(self):
        self.write(json.dumps(nc_window.system_data_window.data()))
        # nc_api.print_data()


class AxisWindowHandler(tornado.web.RequestHandler):
    def get(self):
        self.write(json.dumps(nc_window.axis_data_window.data()))


class ToolWindowHandler(tornado.web.RequestHandler):
    def get(self):
        self.write(json.dumps(nc_window.tool_data_window.data()))


class MicroWindowHandler(tornado.web.RequestHandler):
    def get(self):
        nc_window.micro_data_window.update_micro()
        self.write(json.dumps(nc_window.micro_data_window.data()))


class OffsetWindowHandler(tornado.web.RequestHandler):
    def get(self):
        self.write(json.dumps(nc_window.offset_data_window.data()))


class InitConfigHandler(tornado.web.RequestHandler):
    def get(self):
        self.write(json.dumps(nc_window.init_files.data()))


class AlarmWindowHandler(tornado.web.RequestHandler):
    def get(self):
        net_watchdog.WatchDog.feed()
        self.write(json.dumps(nc_window.current_alarm.data()))


class HistoryAlarmHandler(tornado.web.RequestHandler):
    def get(self):
        self.write(json.dumps(nc_window.offset_data_window.data()))


class NcPlcHandler(tornado.web.RequestHandler):
    def get(self):
        if class_ncplc.NcPlcItem.microFlag:
            nc_window.micro_data_window.update_micro()
        self.write(json.dumps(nc_window.ncplc_data_window.data()))


class DiagnosisWindowHandler(tornado.web.RequestHandler):
    def get(self):
        self.write(json.dumps(nc_window.diagnosis_data_window.data()))


class MicroProgramData(tornado.web.RequestHandler):
    def get(self):
        self.write(json.dumps(nc_window.micro_program_data_window.data()))


class ChannelData(tornado.web.RequestHandler):
    def get(self):
        self.write(json.dumps(nc_window.channel_data_window.data()))
        
class PLCParams(tornado.web.RequestHandler): #plc≤Œ ˝¿‡
    def get(self):
        self.write(json.dumps(nc_window.plc_params_window.data()))
