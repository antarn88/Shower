from os import path, access, W_OK, getcwd
from shutil import disk_usage

from utilities.CommonResources import get_file_size


class Validator:
    def __init__(self, input_filename, output_filename, key=None):
        self.input_filename = input_filename
        self.output_filename = output_filename
        self.key = key

    def is_readable_input_file(self):
        if path.exists(self.input_filename):
            return True
        return False

    def is_writable_output_file(self):
        dirname = path.dirname(self.output_filename)
        if dirname == "":
            dirname = getcwd()
        if access(path.dirname(dirname), W_OK):
            return True
        return False

    def is_same_input_and_output_filename(self):
        if self.input_filename == self.output_filename:
            return True
        return False

    def get_free_space_on_destination_disk(self):
        dirname = path.dirname(self.output_filename)
        if dirname == "":
            dirname = getcwd()
        drive = path.splitdrive(dirname)[0]
        return disk_usage(drive)[2]

    def has_enough_space(self):
        if self.get_free_space_on_destination_disk() > get_file_size(self.input_filename):
            return True
        return False

    def is_valid_key(self):
        if len(self.key) == 32:
            lowercase = False
            uppercase = False
            digit = False
            for i in self.key:
                if str(i).islower():
                    lowercase = True
                elif str(i).isupper():
                    uppercase = True
                elif str(i).isdigit():
                    digit = True
                if lowercase and uppercase and digit:
                    return True
        return False


def is_empty(text):
    if text == "":
        return True
    return False
