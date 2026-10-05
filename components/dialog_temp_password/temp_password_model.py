# ???????????

from PySide6.QtWidgets import QApplication

from common import function_password
from common.function_password import DBPassword  # ????DBPassword, Password?


class TempPasswordModel:
    """?????????"""

    def __init__(self):
        self.password_db: DBPassword = function_password.read_db()

    @staticmethod
    def read_clipboard():
        """?????,????????"""
        clipboard = QApplication.clipboard()
        return clipboard.text()

    def drop_files(self, files):
        """???????"""
        passwords_in_files = function_password.read_passwords_from_files(files)
        return passwords_in_files
