from PySide2.QtCore import QTimer
from datetime import datetime

from .config import *
from .hold_dialog import HoldDialog
from .settings_dialog import SettingsDialog
from .sounds import Sound
from .system_tray_icon import SystemTrayIcon
from .user_activity import UserActivity
from .volume_control import VolumeControl


class AwakeGurdian:
    def __init__(self, app):
        self.cfg = Config()
        self.hold_timer = QTimer()
        self.main_timer = QTimer()
        self.main_timer.setInterval(1000)
        self.main_timer.timeout.connect(self.loop)
        self.main_timer.start()

        self.app = app
        self.last_state = 0

        self.dialog_settings = SettingsDialog(self)
        self.dialog_hold = HoldDialog(self)

        self.tray_icon = SystemTrayIcon(self)
        self.tray_icon.show()

    def timer_toggle(self):
        if self.main_timer.isActive():
            self.hold()
        else:
            self.resume()

    def resume(self, text=PAUSE):
        self.hold_timer.stop()
        self.tray_icon.setIcon(ICON_EYES)
        self.main_timer.start()
        self.tray_icon.systray_menu_main.setText(text)
        self.tray_icon.systray_menu_main.setIcon(ICON_INACTIVE)

    def hold(self, text=RESUME):
        self.dialog_hold.show()
        self.tray_icon.setIcon(ICON_INACTIVE)
        self.main_timer.stop()
        self.tray_icon.systray_menu_main.setText(text)
        self.tray_icon.systray_menu_main.setIcon(ICON_EYES)

    def loop(self):
        if self.cfg.t_range_a:
            t = datetime.now().time()
            tf = self.cfg.t_range_f.toPython()
            tt = self.cfg.t_range_t.toPython()
            if tf > t > tt:
                self.last_state = -1
                self.tray_icon.setIcon(ICON_CLOCK)
                return

        idle_secs = UserActivity.check_idle()
        if idle_secs >= self.cfg.t_to_nag_m * 60 + self.cfg.t_to_nag_s:
            self.nag()
            if self.cfg.inc_volume_nag:
                VolumeControl.raise_volume()
            self.last_state = 2
        elif idle_secs >= self.cfg.t_to_remind_m * 60 + self.cfg.t_to_remind_s:
            self.remind()
            self.last_state = 1
        else:
            self.tray_icon.setIcon(ICON_EYES)
            if self.last_state == 2:
                VolumeControl.restore_volume()
            self.last_state = 0

    def remind(self):
        self.tray_icon.setIcon(ICON_BEEP)
        self.main_timer.setInterval(1000)
        Sound.remind()

    def nag(self):
        self.tray_icon.setIcon(ICON_SHOUT)
        self.main_timer.setInterval(2000)
        Sound.nag()
