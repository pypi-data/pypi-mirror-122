from PySide2.QtWidgets import (
    QDialog,
    QLabel,
    QVBoxLayout,
    QDialogButtonBox,
    QSpinBox,
    QHBoxLayout,
    QSpacerItem,
    QSizePolicy,
    QCheckBox,
    QGroupBox,
    QTimeEdit,
)
from PySide2.QtGui import Qt

from .common import create_autostart, remove_autostart, is_autostart
from .config import *


class SettingsDialog(QDialog):
    def __init__(self, aw):
        self.aw = aw
        QDialog.__init__(self)
        self.setWindowFlag(Qt.SubWindow, True)
        self.setWindowFlag(Qt.CustomizeWindowHint, True)
        self.setWindowFlag(Qt.WindowStaysOnTopHint, True)
        self.setWindowFlag(Qt.WindowCloseButtonHint, False)

        self.buttons = QDialogButtonBox.Ok
        self.setWindowTitle(SETTINGS)

        remind_label = QLabel()
        remind_label.setText(TR)
        nag_label = QLabel()
        nag_label.setText(TN)
        self.remind_m_spinbox = QSpinBox(
            value=aw.cfg.t_to_remind_m, maximum=59, suffix=SUFFIX_MINUTES
        )
        self.remind_s_spinbox = QSpinBox(
            value=aw.cfg.t_to_remind_s, maximum=59, suffix=SUFFIX_SECONDS
        )
        self.remind_m_spinbox.valueChanged.connect(
            lambda val: aw.cfg.set_time_to_remind(val, None)
        )
        self.remind_s_spinbox.valueChanged.connect(
            lambda val: aw.cfg.set_time_to_remind(None, val)
        )
        self.nag_m_spinbox = QSpinBox(
            value=aw.cfg.t_to_nag_m, maximum=59, suffix=SUFFIX_MINUTES
        )
        self.nag_s_spinbox = QSpinBox(
            value=aw.cfg.t_to_nag_s, maximum=59, suffix=SUFFIX_SECONDS
        )
        self.nag_m_spinbox.valueChanged.connect(
            lambda val: aw.cfg.set_time_to_nag(val, None)
        )
        self.nag_s_spinbox.valueChanged.connect(
            lambda val: aw.cfg.set_time_to_nag(None, val)
        )

        def spacer():
            return QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)

        layout = QVBoxLayout()
        remind_hbox = QHBoxLayout()
        remind_hbox.addWidget(remind_label)
        remind_hbox.addSpacerItem(spacer())
        remind_hbox.addWidget(self.remind_m_spinbox)
        remind_hbox.addWidget(self.remind_s_spinbox)

        nag_hbox = QHBoxLayout()
        nag_hbox.addWidget(nag_label)
        nag_hbox.addSpacerItem(spacer())
        nag_hbox.addWidget(self.nag_m_spinbox)
        nag_hbox.addWidget(self.nag_s_spinbox)

        inc_volume_nag_checkbox = QCheckBox(ING, checked=aw.cfg.inc_volume_nag)
        inc_volume_nag_checkbox.stateChanged.connect(
            lambda val: aw.cfg.set_inc_volume_nag(val)
        )

        layout.addLayout(remind_hbox)
        layout.addLayout(nag_hbox)
        layout.addWidget(inc_volume_nag_checkbox)

        ok_cancel = QDialogButtonBox(standardButtons=self.buttons)
        ok_cancel.accepted.connect(self.hide_dialog)

        s = system()
        if s == "Windows":
            AUTOSTART = WIN_AUTOSTART
        elif s == "Linux":
            AUTOSTART = LIN_AUTOSTART

        self.autostart_checkbox = QCheckBox(AUTOSTART)
        self.autostart_checkbox.stateChanged.connect(
            lambda val: self.toggle_autostart(val)
        )
        layout.addWidget(self.autostart_checkbox)

        time_range_group_box = QGroupBox(WOITM)
        time_range_group_box.setCheckable(True)
        time_range_group_box.setChecked(aw.cfg.t_range_a)
        time_range_group_box.toggled.connect(
            lambda val: aw.cfg.set_time_range_active(val)
        )
        time_range_from_label = QLabel(TIME_FROM)
        self.time_range_from = QTimeEdit(aw.cfg.t_range_f)
        self.time_range_from.setDisplayFormat("hh:mm:ss")
        self.time_range_from.timeChanged.connect(
            lambda val: self.set_time_range_from(val)
        )
        time_range_to_label = QLabel(TIME_TO)
        self.time_range_to = QTimeEdit(aw.cfg.t_range_t)
        self.time_range_to.setDisplayFormat("hh:mm:ss")
        self.time_range_to.timeChanged.connect(lambda val: self.set_time_range_to(val))
        time_range_layout = QHBoxLayout()
        time_range_layout.addWidget(time_range_from_label)
        time_range_layout.addWidget(self.time_range_from)
        time_range_layout.addWidget(time_range_to_label)
        time_range_layout.addWidget(self.time_range_to)
        time_range_group_box.setLayout(time_range_layout)
        layout.addWidget(time_range_group_box)
        layout.addWidget(ok_cancel)

        self.setLayout(layout)

    def hide_dialog(self):
        self.aw.cfg.save_config()
        self.hide()

    def showEvent(self, event):
        self.autostart_checkbox.setChecked(is_autostart())

    def toggle_autostart(self, value):
        if value:
            create_autostart()
        else:
            remove_autostart()

    def set_time_range_from(self, val):
        self.aw.cfg.set_time_range_from(val)
        self.time_range_to.setMaximumTime(self.time_range_from.time().addSecs(-1))

    def set_time_range_to(self, val):
        self.aw.cfg.set_time_range_to(val)
        self.time_range_from.setMinimumTime(self.time_range_to.time().addSecs(1))
