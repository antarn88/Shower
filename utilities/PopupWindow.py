from PySide2.QtCore import Qt
from PySide2.QtGui import QGuiApplication
from PySide2.QtWidgets import QMessageBox, QStyle


class PopupWindow(QMessageBox):
    def __init__(self, text, focus):
        super(PopupWindow, self).__init__()

        msgbox = self

        # Set window center of screen
        msgbox.setGeometry(
            QStyle.alignedRect(
                Qt.LeftToRight,
                Qt.AlignCenter,
                self.size(),
                QGuiApplication.primaryScreen().availableGeometry(),
            ),
        )

        title = "Shower"

        msgbox.warning(self, title, text)
        focus.setFocus()
