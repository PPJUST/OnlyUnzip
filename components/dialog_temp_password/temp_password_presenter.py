# 临时密码模块的桥梁组件
from PySide6.QtCore import QObject, Signal

from components.dialog_temp_password.temp_password_model import TempPasswordModel
from components.dialog_temp_password.temp_password_viewer import TempPasswordViewer


class TempPasswordPresenter(QObject):
    """临时密码模块的桥梁组件"""

    WriteToDB = Signal(list, name="将临时密码写入密码本")

    def __init__(self, viewer: TempPasswordViewer, model: TempPasswordModel):
        super().__init__()
        self.viewer = viewer
        self.model = model

        self._bind_signal()

    def exec(self):
        """显示临时密码对话框"""
        self.viewer.exec()

    def get_passwords(self) -> list:
        """获取去重后的临时密码"""
        passwords = self.viewer.get_passwords()
        return self.model.dedup_passwords(passwords)

    def _bind_signal(self):
        """绑定界面组件的信号"""
        self.viewer.WriteToDB.connect(self._write_to_db)
        self.viewer.ReadClipboard.connect(self._read_clipboard)
        self.viewer.DropFiles.connect(self._drop_files)

    def _read_clipboard(self):
        """把剪贴板内容添加到密码框"""
        self.viewer.append_pw(self.model.read_clipboard())

    def _drop_files(self, files):
        """把拖入文件中的密码添加到密码框"""
        passwords = self.model.read_passwords_from_files(files)
        if passwords:
            self.viewer.append_pw('\n'.join(passwords))

    def _write_to_db(self, passwords: list):
        """发出写入密码本的信号"""
        unique_passwords = self.model.dedup_passwords(passwords)
        self.WriteToDB.emit(unique_passwords)
