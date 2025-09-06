# 临时密码模块的桥梁组件
import lzytools.common
from PySide6.QtCore import QObject, Signal

from components.dialog_temp_password.temp_password_model import TempPasswordModel
from components.dialog_temp_password.temp_password_viewer import TempPasswordViewer


class TempPasswordPresenter(QObject):
    """临时密码模块的桥梁组件"""
    TempPassword = Signal(list, name="临时密码清单")
    WriteTODB = Signal(list, name="将临时密码写入密码本")

    def __init__(self, viewer: TempPasswordViewer, model: TempPasswordModel):
        super().__init__()
        self.viewer = viewer
        self.model = model

        # 初始化
        self._bind_signal()

    def exec(self):
        self.viewer.exec()

    def get_passwords(self):
        """获取临时密码"""
        pws = self.viewer.get_passwords()
        pws = lzytools.common.dedup_list(pws)
        return pws

    def _bind_signal(self):
        """绑定Viewer信号"""
        self.viewer.WriteToDB.connect(self.write_to_db)
        self.viewer.ReadClipboard.connect(self._read_clipboard)
        self.viewer.DropFiles.connect(self._drop_files)

    def _read_clipboard(self):
        self.viewer.append_pw(self.model.read_clipboard())

    def _drop_files(self, files):
        pws_drop = self.model.drop_files(files)
        print('拖入文件中包含的密码', pws_drop)
        if pws_drop:
            self.viewer.append_pw('\n'.join(pws_drop))

    def write_to_db(self):
        """将临时密码写入密码库"""
        temp_pws = self.viewer.get_passwords()
        self.WriteTODB.emit(temp_pws)
