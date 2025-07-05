# 密码模块的桥梁组件
from components.page_password.password_model import PasswordModel
from components.page_password.password_viewer import PasswordViewer


class PasswordPresenter:
    """密码模块的桥梁组件"""

    def __init__(self, viewer: PasswordViewer, model: PasswordModel):
        self.viewer = viewer
        self.model = model

        # 初始化
        self._show_pw_count()
        self._bind_signal()


    def get_passwords(self):
        """获取密码清单"""
        return self.model.get_passwords()
    def _bind_signal(self):
        """绑定Viewer信号"""
        self.viewer.ReadClipboard.connect(self._read_clipboard)
        self.viewer.OutputPassword.connect(self._output_password)
        self.viewer.OpenPassword.connect(self.model.open_password)
        self.viewer.UpdatePassword.connect(self._update_password)

    def _read_clipboard(self):
        self.viewer.set_pw_text(self.model.read_clipboard())

    def _output_password(self):
        self.model.output_password()
        self.viewer.set_open_button_enable(True)

    def _update_password(self, text: str):
        self.model.update_password(text)
        self.viewer.clear_pw()
        self._show_pw_count()  # 更新密码统计

    def _show_pw_count(self):
        self.viewer.show_pw_count(self.model.count_password())
