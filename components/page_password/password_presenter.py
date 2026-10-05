# ?????????
from typing import Union

from PySide6.QtCore import QObject, Signal

from components.page_password.password_model import PasswordModel
from components.page_password.password_viewer import PasswordViewer


class PasswordPresenter(QObject):
    """?????????"""
    OpenPasswordManager = Signal(name="???????")

    def __init__(self, viewer: PasswordViewer, model: PasswordModel):
        super().__init__()
        self.viewer = viewer
        self.model = model

        # ???
        self.show_pw_count_info()
        self._bind_signal()

    def reload(self):
        """?????"""
        self.model.reload()

    def update_use_count(self, passwords: Union[str, list]):
        """???????????"""
        self.model.add_use_count_once(passwords)

    def get_passwords(self):
        """??????"""
        return self.model.get_passwords()

    def update_password(self, password: Union[str, list]):
        """???????????"""
        self.model.update_password(password)
        self.viewer.clear_pw()
        self.show_pw_count_info()

    def show_pw_count_info(self):
        self.viewer.show_pw_count_info(self.model.count_password())

    def _bind_signal(self):
        """??Viewer??"""
        self.viewer.OpenPasswordManager.connect(self.OpenPasswordManager.emit)
        self.viewer.ReadClipboard.connect(self._read_clipboard)
        self.viewer.OutputPassword.connect(self._output_password)
        self.viewer.OpenPassword.connect(self.model.open_password)
        self.viewer.UpdatePassword.connect(self.update_password)
        self.viewer.DropFiles.connect(self._drop_files)

    def _read_clipboard(self):
        self.viewer.append_pw(self.model.read_clipboard())

    def _output_password(self):
        self.model.output_password()
        self.viewer.set_open_button_enable(True)

    def _drop_files(self, files):
        pws_drop = self.model.drop_files(files)
        print('??????????', pws_drop)
        if pws_drop:
            self.viewer.append_pw('\n'.join(pws_drop))
