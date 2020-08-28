from os import path
from random import choice
from string import ascii_letters, digits

from PySide2.QtWidgets import QFileDialog


def input_file_browser_action(parent, input_field):
    filename = QFileDialog.getOpenFileName(parent, "Select the input file")
    if filename[0]:
        input_field.setText(filename[0].replace("/", "\\"))


def output_file_browser_action(parent, output_field):
    filename = QFileDialog.getSaveFileName(parent, "Save the output file")
    if filename[0]:
        output_field.setText(filename[0].replace("/", "\\"))


def get_file_size(filename):
    return path.getsize(filename)


def get_file_size_formatted(filename):
    file_size_in_byte = get_file_size(filename)

    if file_size_in_byte < 1024:
        file_size_num = file_size_in_byte
        return f"{file_size_num} B"
    elif 1024 <= file_size_in_byte < 1048576:
        file_size_num = round(file_size_in_byte / 1024, 2)
        return f"{file_size_num} KB"
    elif 1048576 <= file_size_in_byte < 1073741824:
        file_size_num = round(file_size_in_byte / 1024 / 1024, 2)
        return f"{file_size_num} MB"
    elif 1073741824 <= file_size_in_byte < 1099511627776:
        file_size_num = round(file_size_in_byte / 1024 / 1024 / 1024, 2)
        return f"{file_size_num} GB"
    elif 1099511627776 <= file_size_in_byte < 1125899906842624:
        file_size_num = round(file_size_in_byte / 1024 / 1024 / 1024 / 1024, 2)
        return f"{file_size_num} TB"


def get_random_key():
    letters_and_digits = ascii_letters + digits
    return "".join((choice(letters_and_digits) for i in range(32)))
