# 密码模块的桥梁组件
from typing import Union

from PySide6.QtCore import QObject, Signal

from components.page_password.password_model import PasswordModel
from components.page_password.password_viewer import PasswordViewer


class PasswordPresenter(QObject):
    """密码模块的桥梁组件"""
    OpenPasswordManager = Signal(name="打开密码管理器")

    def __init__(self, viewer: PasswordViewer, model: PasswordModel):
        super().__init__()
        self.viewer = viewer
        self.model = model

        # 初始化
        self.show_pw_count_info()
        self._bind_signal()

    def update_use_count(self, passwords: Union[str, list]):
        """增加一次密码的使用次数"""
        self.model.add_use_count_once(passwords)

    def get_passwords(self):
        """获取密码清单"""
        return self.model.get_passwords()

    def show_pw_count_info(self):
        self.viewer.show_pw_count_info(self.model.count_password())

    def _bind_signal(self):
        """绑定Viewer信号"""
        self.viewer.OpenPasswordManager.connect(self.OpenPasswordManager.emit)
        self.viewer.ReadClipboard.connect(self._read_clipboard)
        self.viewer.OutputPassword.connect(self._output_password)
        self.viewer.OpenPassword.connect(self.model.open_password)
        self.viewer.UpdatePassword.connect(self._update_password)
        self.viewer.DropFiles.connect(self._drop_files)

    def _read_clipboard(self):
        self.viewer.append_pw(self.model.read_clipboard())

    def _output_password(self):
        self.model.output_password()
        self.viewer.set_open_button_enable(True)

    def _update_password(self, text: str):
        self.model.update_password(text)
        self.viewer.clear_pw()
        self.show_pw_count_info()  # 更新密码统计

    def _drop_files(self, files):
        pws_drop = self.model.drop_files(files)
        print('拖入文件中包含的密码', pws_drop)
        if pws_drop:
            self.viewer.append_pw('\n'.join(pws_drop))
