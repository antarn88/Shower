from Crypto.Cipher import AES
from PySide2.QtCore import QThread, Signal

from utilities.CommonResources import get_file_size, get_file_size_formatted, get_random_key


class EncryptFileWorker(QThread):
    written_bytes_raw_divided = Signal(int)
    written_file_size = Signal(str)
    file_encryption_completed = Signal(str)

    def __init__(self, input_filename, output_filename):
        super().__init__()
        self.input_filename = input_filename
        self.output_filename = output_filename
        self.key_string = get_random_key()
        self.key_byte = bytes(self.key_string, encoding="utf8")
        self.buffer_size = 65536  # 64 KB
        self.denominator = 100000

    def run(self):
        self.encrypt()
        self.file_encryption_completed.emit(self.key_string)

    def encrypt(self):
        # Open the input and output files
        input_file = open(self.input_filename, "rb")
        output_file = open(self.output_filename, "wb")

        # Create the cipher object and encrypt the data
        cipher_encrypt = AES.new(self.key_byte, AES.MODE_CFB)

        # Initially write the iv to the output file
        output_file.write(cipher_encrypt.iv)

        # Keep reading the file into the buffer, encrypting then writing to the new file
        buffer = input_file.read(self.buffer_size)
        while len(buffer) > 0:
            ciphered_bytes = cipher_encrypt.encrypt(buffer)
            output_file.write(ciphered_bytes)
            buffer = input_file.read(self.buffer_size)
            self.written_bytes_raw_divided.emit(get_file_size(self.output_filename) / self.denominator)
            self.written_file_size.emit(get_file_size_formatted(self.output_filename))

        # Close the input and output files
        input_file.close()
        output_file.close()
