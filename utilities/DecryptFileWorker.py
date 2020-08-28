from Crypto.Cipher import AES
from PySide2.QtCore import QThread, Signal

from utilities.CommonResources import get_file_size_formatted, get_file_size


class DecryptFileWorker(QThread):
    written_bytes_raw_divided = Signal(int)
    written_file_size = Signal(str)
    file_decryption_completed = Signal()

    def __init__(self, input_filename, output_filename, key_string):
        super().__init__()
        self.input_filename = input_filename
        self.output_filename = output_filename
        self.key_string = key_string
        self.key_byte = bytes(self.key_string, encoding="utf8")
        self.buffer_size = 65536  # 64 KB
        self.denominator = 100000

    def run(self):
        self.decrypt()
        self.file_decryption_completed.emit()

    def decrypt(self):
        # Open the input and output files
        input_file = open(self.input_filename, "rb")
        output_file = open(self.output_filename, "wb")

        # Read in the iv
        iv = input_file.read(16)

        # Create the cipher object and encrypt the data
        cipher_encrypt = AES.new(self.key_byte, AES.MODE_CFB, iv=iv)

        # Keep reading the file into the buffer, decrypting then writing to the new file
        buffer = input_file.read(self.buffer_size)
        while len(buffer) > 0:
            decrypted_bytes = cipher_encrypt.decrypt(buffer)
            output_file.write(decrypted_bytes)
            buffer = input_file.read(self.buffer_size)
            self.written_bytes_raw_divided.emit(get_file_size(self.output_filename) / self.denominator)
            self.written_file_size.emit(get_file_size_formatted(self.output_filename))

        # Close the input and output files
        input_file.close()
        output_file.close()
