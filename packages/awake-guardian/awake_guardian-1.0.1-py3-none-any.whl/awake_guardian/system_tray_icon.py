from PySide2.QtWidgets import (
    QMenu,
    QSystemTrayIcon,
)
from .config import *


class SystemTrayIcon(QSystemTrayIcon):
    def __init__(self, aw):
        self.aw = aw
        QSystemTrayIcon.__init__(self, ICON_EYES)
        menu = QMenu()

        self.systray_menu_main = menu.addAction(ICON_INACTIVE, PAUSE)
        menu.addSeparator()
        self.systray_menu_settings = menu.addAction(ICON_SETTINGS, SETTINGS)
        self.systray_menu_exit = menu.addAction(ICON_EXIT, EXIT)
        self.setContextMenu(menu)

        self.systray_menu_main.triggered.connect(aw.timer_toggle)
        self.systray_menu_settings.triggered.connect(aw.dialog_settings.show)
        self.systray_menu_exit.triggered.connect(aw.app.exit)
        self.activated.connect(self.click)
        self.setToolTip(f"{TITLE}\n\n{HINT}")

    def click(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            self.aw.timer_toggle()
