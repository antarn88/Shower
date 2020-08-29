from PySide2.QtGui import QFont, Qt
from PySide2.QtWidgets import QWidget, QLabel, QGridLayout, QLineEdit, QPushButton, QProgressBar
from pyperclip import copy

from utilities.CommonResources import input_file_browser_action, output_file_browser_action, get_file_size, get_file_size_formatted
from utilities.PopupWindow import PopupWindow
from utilities.Validator import Validator, is_empty


class EncryptFileTab(QWidget):
    def __init__(self, parent):
        super(EncryptFileTab, self).__init__()

        # App attributes
        self.input_filename = None
        self.output_filename = None
        self.encrypt_file_worker = None
        self.progress_label = None
        self.in_file_label = None
        self.in_filename = None
        self.abort_btn = None
        self.out_file_label = None
        self.out_filename = None
        self.complete_label = None
        self.secret_key_label = None
        self.secret_key_field = None
        self.warning_label = None
        self.encrypt_new_file_btn = None
        self.copy_btn = None
        self.parent = parent

        self.main_layout = QGridLayout()
        self.main_layout.setHorizontalSpacing(15)
        self.setLayout(self.main_layout)

        self.input_filename_label = QLabel("Input filename:")
        self.main_layout.addWidget(self.input_filename_label, 0, 0)

        self.input_field = QLineEdit()
        self.input_field.returnPressed.connect(self.start_encryption_action)
        self.main_layout.addWidget(self.input_field, 0, 1)

        self.input_file_browser_btn = QPushButton("Browse")
        self.input_file_browser_btn.clicked.connect(lambda: input_file_browser_action(self, self.input_field))
        self.main_layout.addWidget(self.input_file_browser_btn, 0, 2)

        self.output_filename_label = QLabel("Output filename:")
        self.main_layout.addWidget(self.output_filename_label, 1, 0)

        self.output_field = QLineEdit()
        self.output_field.returnPressed.connect(self.start_encryption_action)
        self.main_layout.addWidget(self.output_field, 1, 1)

        self.output_file_browser_btn = QPushButton("Browse")
        self.output_file_browser_btn.clicked.connect(lambda: output_file_browser_action(self, self.output_field))
        self.main_layout.addWidget(self.output_file_browser_btn, 1, 2)

        self.start_encryption_btn = QPushButton("Start encryption")
        self.start_encryption_btn.clicked.connect(self.start_encryption_action)

        self.main_layout.addWidget(self.start_encryption_btn, 2, 1)

        self.progressbar = QProgressBar()
        self.progressbar.setAlignment(Qt.AlignCenter)
        self.progressbar.setVisible(False)

        self.denominator = 100000

    def is_valid_input_data(self):
        validator = Validator(self.input_filename, self.output_filename)
        if not is_empty(self.input_filename):
            if not is_empty(self.output_filename):
                if validator.is_readable_input_file():
                    if validator.is_writable_output_file():
                        if not validator.is_same_input_and_output_filename():
                            if validator.has_enough_space():
                                return True
                            else:
                                PopupWindow(self, "Not enough free space on the destination drive! Check!", self.output_field)
                        else:
                            PopupWindow(self, "Input and output file cannot be the same! Check!", self.output_field)
                    else:
                        PopupWindow(self, "Output file is unwritable! Check!", self.output_field)
                else:
                    PopupWindow(self, "Input file does not exist! Check!", self.input_field)
            else:
                PopupWindow(self, "Output filename is empty! Check!", self.output_field)
        else:
            PopupWindow(self, "Input filename is empty! Check!", self.input_field)

    def start_encryption_action(self):
        self.input_filename = self.input_field.text()
        self.output_filename = self.output_field.text()

        if self.is_valid_input_data():
            self.progressbar.setValue(0)
            self.progressbar.setMaximum(get_file_size(self.input_filename) / self.denominator)
            self.parent.enc_action(self)

            # Lock decryption tab
            self.parent.tabwidget.setTabEnabled(1, False)

            # Hide GUI elements
            self.input_filename_label.setVisible(False)
            self.input_field.setVisible(False)
            self.input_file_browser_btn.setVisible(False)
            self.output_filename_label.setVisible(False)
            self.output_field.setVisible(False)
            self.output_file_browser_btn.setVisible(False)
            self.start_encryption_btn.setVisible(False)

            # Generate GUI elements
            self.progress_label = QLabel("The file encryption is in progress...")
            self.progress_label.setStyleSheet("QLabel { font-weight: bold; }")

            self.progress_label.setFont(QFont("SansSerif", 15))
            self.progress_label.setAlignment(Qt.AlignHCenter)
            self.main_layout.addWidget(self.progress_label, 0, 0, 1, 3)

            self.in_file_label = QLabel("Input file:")
            self.in_file_label.setFont(QFont("SansSerif", 12))
            self.in_file_label.setAlignment(Qt.AlignHCenter)
            self.in_file_label.setStyleSheet("QLabel { font-weight: bold; }")
            self.main_layout.addWidget(self.in_file_label, 1, 0, 1, 3)

            self.in_filename = QLabel(f"{self.input_filename} ({get_file_size_formatted(self.input_filename)})")
            self.in_filename.setFont(QFont("SansSerif", 8))
            self.in_filename.setAlignment(Qt.AlignHCenter)
            self.in_filename.setWordWrap(True)
            self.in_filename.setMargin(20)
            self.main_layout.addWidget(self.in_filename, 2, 0, 1, 3)

            self.out_file_label = QLabel("Output file:")
            self.out_file_label.setFont(QFont("SansSerif", 12))
            self.out_file_label.setAlignment(Qt.AlignHCenter)
            self.out_file_label.setStyleSheet("QLabel { font-weight: bold; }")
            self.main_layout.addWidget(self.out_file_label, 3, 0, 1, 3)

            self.out_filename = QLabel()
            self.out_filename.setFont(QFont("SansSerif", 8))
            self.out_filename.setAlignment(Qt.AlignHCenter)
            self.out_filename.setWordWrap(True)
            self.out_filename.setMargin(20)
            self.main_layout.addWidget(self.out_filename, 4, 0, 1, 3)

            self.progressbar.setVisible(True)
            self.main_layout.addWidget(self.progressbar, 5, 0, 1, 3)

            self.abort_btn = QPushButton("Abort")
            self.abort_btn.clicked.connect(self.parent.terminate_process)
            self.main_layout.addWidget(self.abort_btn, 6, 1)

    def set_progressbar_value(self, written_bytes_raw_divided):
        self.progressbar.setValue(written_bytes_raw_divided)

    def set_output_filename_label(self, written_file_size):
        output_file_name_with_size = f"{self.output_filename} ({written_file_size} of {get_file_size_formatted(self.input_filename)})"
        self.out_filename.setText(output_file_name_with_size)

    def file_encryption_completed(self, key):
        # Hide GUI elements
        self.progress_label.setVisible(False)
        self.in_file_label.setVisible(False)
        self.in_filename.setVisible(False)
        self.out_file_label.setVisible(False)
        self.out_filename.setVisible(False)
        self.abort_btn.setVisible(False)
        self.progressbar.setVisible(False)

        # Generate GUI elements
        self.complete_label = QLabel("The encryption of the file has been completed.")
        self.complete_label.setFont(QFont("SansSerif", 15))
        self.complete_label.setAlignment(Qt.AlignHCenter)
        self.complete_label.setStyleSheet("QLabel { font-weight: bold; color: green; }")
        self.main_layout.addWidget(self.complete_label, 0, 0, 1, 3)

        self.secret_key_label = QLabel("Your secret key for restoring the file:")
        self.secret_key_label.setFont(QFont("SansSerif", 12))
        self.secret_key_label.setAlignment(Qt.AlignHCenter)
        self.secret_key_label.setStyleSheet("QLabel { font-weight: bold; }")
        self.main_layout.addWidget(self.secret_key_label, 1, 0, 1, 3)

        self.secret_key_field = QLineEdit()
        self.secret_key_field.setText(key)
        self.secret_key_field.setReadOnly(True)
        self.secret_key_field.setAlignment(Qt.AlignHCenter)

        font = self.secret_key_field.font()
        font.setPointSize(15)
        self.secret_key_field.setFont(font)
        self.main_layout.addWidget(self.secret_key_field, 2, 0, 1, 2)

        self.copy_btn = QPushButton("Copy")
        self.copy_btn.setMaximumWidth(50)
        self.copy_btn.setMinimumHeight(32)
        self.copy_btn.clicked.connect(self.copy_key_action)
        self.main_layout.addWidget(self.copy_btn, 2, 2)

        self.warning_label = QLabel("Keep this secret key in a safe place, because without it you will not be able to restore the file!")
        self.warning_label.setFont(QFont("SansSerif", 12))
        self.warning_label.setAlignment(Qt.AlignHCenter)
        self.warning_label.setStyleSheet("QLabel { font-weight: bold; color: red; }")
        self.warning_label.setWordWrap(True)
        self.main_layout.addWidget(self.warning_label, 3, 0, 1, 3)

        self.encrypt_new_file_btn = QPushButton("Encrypt a new file")
        self.encrypt_new_file_btn.clicked.connect(self.encrypt_new_file_action)
        self.encrypt_new_file_btn.setMinimumWidth(120)
        self.main_layout.addWidget(self.encrypt_new_file_btn, 4, 0, 1, 3, alignment=Qt.AlignHCenter)

        # Unlock decryption tab
        self.parent.tabwidget.setTabEnabled(1, True)

    def copy_key_action(self):
        if self.secret_key_field:
            copy(self.secret_key_field.text())

    def encrypt_new_file_action(self, from_abort=False):
        # Hide GUI elements
        if not from_abort:
            self.complete_label.setVisible(False)
            self.secret_key_label.setVisible(False)
            self.secret_key_field.setVisible(False)
            self.warning_label.setVisible(False)
            self.encrypt_new_file_btn.setVisible(False)
            self.copy_btn.setVisible(False)
        else:
            self.progress_label.setVisible(False)
            self.in_file_label.setVisible(False)
            self.in_filename.setVisible(False)
            self.out_file_label.setVisible(False)
            self.out_filename.setVisible(False)
            self.progressbar.setVisible(False)
            self.abort_btn.setVisible(False)

            # Unlock decryption tab
            self.parent.tabwidget.setTabEnabled(1, True)

        # Show default GUI elements
        self.input_filename_label.setVisible(True)
        self.input_field.setVisible(True)
        self.input_file_browser_btn.setVisible(True)
        self.output_filename_label.setVisible(True)
        self.output_field.setVisible(True)
        self.output_file_browser_btn.setVisible(True)
        self.start_encryption_btn.setVisible(True)

        # Clear input fields
        self.input_field.clear()
        self.output_field.clear()
