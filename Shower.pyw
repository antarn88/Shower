from sys import argv

from PySide2.QtCore import Qt
from PySide2.QtGui import QGuiApplication, QIcon, QPixmap
from PySide2.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QWidget, QTabWidget, QStyle, QMessageBox

from tabs.DecryptFileTab import DecryptFileTab
from tabs.EncryptFileTab import EncryptFileTab
from utilities.DecryptFileWorker import DecryptFileWorker
from utilities.EncryptFileWorker import EncryptFileWorker
from utilities.GetImages import app_icon


class Shower(QMainWindow):
    def __init__(self):
        super(Shower, self).__init__()

        # App attributes
        self.encrypt_file_worker = None
        self.decrypt_file_worker = None

        # The size of the starting window
        self.setFixedSize(500, 400)

        # Set window center of screen
        self.setGeometry(
            QStyle.alignedRect(
                Qt.LeftToRight,
                Qt.AlignCenter,
                self.size(),
                QGuiApplication.primaryScreen().availableGeometry(),
            ),
        )

        # The title of the program
        self.setWindowTitle("Shower v0.52")

        # Set app icon
        self.setWindowIcon(QIcon(QPixmap(app_icon())))

        # Before using the main layout, need to create a central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        self.enc_file_tab = EncryptFileTab(self)
        self.dec_file_tab = DecryptFileTab(self)

        self.tabwidget = QTabWidget()
        self.tabwidget.addTab(self.enc_file_tab, "Encrypt file")
        self.tabwidget.addTab(self.dec_file_tab, "Decrypt file")
        main_layout.addWidget(self.tabwidget)

        self.enc_file_tab.input_field.setFocus()

    def enc_action(self, child):
        input_filename = child.input_filename
        output_filename = child.output_filename
        self.encrypt_file_worker = EncryptFileWorker(input_filename, output_filename)
        self.encrypt_file_worker.setTerminationEnabled(True)
        self.encrypt_file_worker.file_encryption_completed.connect(self.enc_file_tab.file_encryption_completed)
        self.encrypt_file_worker.written_file_size.connect(self.enc_file_tab.set_output_filename_label)
        self.encrypt_file_worker.written_bytes_raw_divided.connect(self.enc_file_tab.set_progressbar_value)
        self.encrypt_file_worker.start()

    def dec_action(self, child):
        input_filename = child.input_filename
        output_filename = child.output_filename
        key_string = child.key_string
        self.decrypt_file_worker = DecryptFileWorker(input_filename, output_filename, key_string)
        self.decrypt_file_worker.setTerminationEnabled(True)
        self.decrypt_file_worker.file_decryption_completed.connect(self.dec_file_tab.file_decryption_completed)
        self.decrypt_file_worker.written_file_size.connect(self.dec_file_tab.set_output_filename_label)
        self.decrypt_file_worker.written_bytes_raw_divided.connect(self.dec_file_tab.set_progressbar_value)
        self.decrypt_file_worker.start()

    def terminate_box(self, text):
        msgbox = QMessageBox(self)
        msgbox.setWindowTitle("Shower")
        msgbox.setIcon(QMessageBox.Warning)
        msgbox.setText(text)
        msgbox.addButton("OK", QMessageBox.AcceptRole)
        cancel_btn = msgbox.addButton("Cancel", QMessageBox.RejectRole)
        msgbox.setDefaultButton(cancel_btn)
        return msgbox.exec_()

    def terminate_process(self):
        text = "Are you sure you want to abort the process?\nTHE OUTPUT FILE WILL BE CORRUPTED!"
        if self.encrypt_file_worker and self.encrypt_file_worker.isRunning() and self.terminate_box(text) == QMessageBox.AcceptRole:
            self.encrypt_file_worker.terminate()
            self.encrypt_file_worker.wait()
            self.encrypt_file_worker = None
            self.enc_file_tab.encrypt_new_file_action(True)
        elif self.decrypt_file_worker and self.decrypt_file_worker.isRunning() and self.terminate_box(text) == QMessageBox.AcceptRole:
            self.decrypt_file_worker.terminate()
            self.decrypt_file_worker.wait()
            self.decrypt_file_worker = None
            self.dec_file_tab.decrypt_new_file_action(True)

    def closeEvent(self, event):
        text = "Are you sure you want to abort the process and exit?\nTHE OUTPUT FILE WILL BE CORRUPTED!"
        if self.encrypt_file_worker and self.encrypt_file_worker.isRunning():
            if self.terminate_box(text) == QMessageBox.AcceptRole:
                self.encrypt_file_worker.terminate()
                self.encrypt_file_worker.wait()
                event.accept()
            else:
                event.ignore()
        elif self.decrypt_file_worker and self.decrypt_file_worker.isRunning():
            if self.terminate_box(text) == QMessageBox.AcceptRole:
                self.decrypt_file_worker.terminate()
                self.decrypt_file_worker.wait()
                event.accept()
            else:
                event.ignore()


if __name__ == '__main__':
    app = QApplication(argv)
    win = Shower()
    win.show()
    app.exec_()
