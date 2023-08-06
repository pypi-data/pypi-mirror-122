from datetime import datetime, timedelta

from PySide2.QtWidgets import (
    QDialog,
    QLabel,
    QVBoxLayout,
    QDialogButtonBox,
    QSpinBox,
    QHBoxLayout,
    QSpacerItem,
    QSizePolicy,
)
from PySide2.QtGui import Qt

from .config import *


class HoldDialog(QDialog):
    def __init__(self, aw):
        self.aw = aw
        QDialog.__init__(self)
        self.setWindowFlag(Qt.SubWindow, True)
        self.setWindowFlag(Qt.CustomizeWindowHint, True)
        self.setWindowFlag(Qt.WindowStaysOnTopHint, True)
        self.setWindowFlag(Qt.WindowCloseButtonHint, False)

        self.buttons = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        self.setWindowTitle(PAUSE)

        hold_label = QLabel()
        hold_label.setText(PAUSE_LABEL)
        self.hold_m_spinbox = QSpinBox(
            value=aw.cfg.last_hold_time, maximum=1440, suffix=SUFFIX_MINUTES
        )
        self.hold_m_spinbox.valueChanged.connect(lambda val: aw.cfg.set_hold_time(val))

        spacer1 = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)

        layout = QVBoxLayout()
        hold_hbox = QHBoxLayout()
        hold_hbox.addWidget(hold_label)
        hold_hbox.addSpacerItem(spacer1)
        hold_hbox.addWidget(self.hold_m_spinbox)

        layout.addLayout(hold_hbox)

        ok_cancel = QDialogButtonBox(standardButtons=self.buttons)
        ok_cancel.accepted.connect(self.ok)
        ok_cancel.rejected.connect(self.cancel)

        layout.addWidget(ok_cancel)
        self.setLayout(layout)

    def ok(self):
        lht = self.aw.cfg.last_hold_time * 60
        t = datetime.now() + timedelta(0, lht)
        self.aw.hold(f'{RESUME} ({STR_AUTO}: {t.strftime("%H:%M:%S")})')
        self.aw.hold_timer.singleShot(lht * 1000, self.aw.resume)
        self.aw.cfg.save_config()
        self.close()

    def cancel(self):
        self.aw.resume()
        self.close()
