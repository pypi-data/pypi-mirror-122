from appdirs import AppDirs
from configparser import ConfigParser
from os import mkdir
from os.path import dirname, isdir
from platform import system
from PySide2.QtCore import QTime
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QApplication

from .lang import *

app = QApplication()
path = dirname(__file__)

ICON_BEEP = QIcon(f"{path}/images/beep.png")
ICON_CLOCK = QIcon(f"{path}/images/clock.png")
ICON_EXIT = QIcon(f"{path}/images/exit.png")
ICON_EYES = QIcon(f"{path}/images/eyes.png")
ICON_INACTIVE = QIcon(f"{path}/images/inactive.png")
ICON_SETTINGS = QIcon(f"{path}/images/settings.png")
ICON_SHOUT = QIcon(f"{path}/images/shout.png")

AUDIO_COIN = f"{path}/audio/coin.wav"
AUDIO_WILHELM = f"{path}/audio/wilhelm.wav"

CONFIG_FILE = "AwakeGuardian"
CONFIG_FILE_EXT = ".conf"

D = "DEFAULT"
TTRM = "time_to_remind_m"
TTRS = "time_to_remind_s"
TTNM = "time_to_nag_m"
TTNS = "time_to_nag_s"
IVG = "increase_volume_nag"
LHT = "last_hold_time"
TRA = "time_range_active"
TRF = "time_range_from"
TRT = "time_range_to"


class Config:
    def __init__(self):
        self.config_file = self.setup_config_file()
        self.config_parser = ConfigParser()
        self.config_parser.read(self.config_file)

        self.last_hold_time = int(self.config_parser[D].get(LHT, 15))
        self.t_to_remind_m = int(self.config_parser[D].get(TTRM, 10))
        self.t_to_remind_s = int(self.config_parser[D].get(TTRS, 0))
        self.t_to_nag_m = int(self.config_parser[D].get(TTNM, 15))
        self.t_to_nag_s = int(self.config_parser[D].get(TTNS, 0))

        self.inc_volume_nag = int(self.config_parser[D].get(IVG, 1))
        self.volume = None

        self.t_range_a = int(self.config_parser[D].get(TRA, 1))
        self.t_range_f = QTime.fromString(self.config_parser[D].get(TRF, "20:00:00"))
        self.t_range_t = QTime.fromString(self.config_parser[D].get(TRT, "08:00:00"))

    def setup_config_file(self):
        dirs = AppDirs(CONFIG_FILE)
        config_dir = dirname(dirs.user_config_dir)
        if not isdir(config_dir):
            try:
                mkdir(config_dir)
            except Exception as e:
                raise e
        return f"{dirs.user_config_dir}{CONFIG_FILE_EXT}"

    def set_hold_time(self, minutes):
        self.last_hold_time = minutes
        self.save_config()

    def set_time_to_remind(self, minutes, seconds):
        if minutes is not None:
            self.t_to_remind_m = minutes
        if seconds is not None:
            self.t_to_remind_s = seconds
        self.save_config()

    def set_time_to_nag(self, minutes, seconds):
        if minutes is not None:
            self.t_to_nag_m = minutes
        if seconds is not None:
            self.t_to_nag_s = seconds
        self.save_config()

    def set_inc_volume_nag(self, value):
        self.inc_volume_nag = value
        self.save_config()

    def set_time_range_active(self, value):
        self.t_range_a = int(value)
        self.save_config()

    def set_time_range_from(self, time):
        self.t_range_f = time
        self.save_config()

    def set_time_range_to(self, time):
        self.t_range_t = time
        self.save_config()

    def save_config(self):
        settings = {
            TTRM: self.t_to_remind_m,
            TTRS: self.t_to_remind_s,
            TTNM: self.t_to_nag_m,
            TTNS: self.t_to_nag_s,
            IVG: self.inc_volume_nag,
            LHT: self.last_hold_time,
            TRA: self.t_range_a,
            TRF: self.t_range_f.toString(),
            TRT: self.t_range_t.toString(),
        }
        self.config_parser[D] = settings
        with open(self.config_file, "w") as cf:
            self.config_parser.write(cf)
