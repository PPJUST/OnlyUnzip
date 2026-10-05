# ???????????
import lzytools
from PySide6.QtCore import QObject, Signal

from components.dialog_temp_password.temp_password_model import TempPasswordModel
from components.dialog_temp_password.temp_password_viewer import TempPasswordViewer


class TempPasswordPresenter(QObject):
    """???????????"""
    TempPassword = Signal(list, name="??????")
    WriteTODB = Signal(list, name="??????????")

    def __init__(self, viewer: TempPasswordViewer, model: TempPasswordModel):
        super().__init__()
        self.viewer = viewer
        self.model = model

        # ???
        self._bind_signal()

    def exec(self):
        self.viewer.exec()

    def get_passwords(self):
        """??????"""
        pws = self.viewer.get_passwords()
        pws = lzytools.common.dedup_list(pws)
        return pws

    def _bind_signal(self):
        """??Viewer??"""
        self.viewer.WriteToDB.connect(self.write_to_db)
        self.viewer.ReadClipboard.connect(self._read_clipboard)
        self.viewer.DropFiles.connect(self._drop_files)

    def _read_clipboard(self):
        self.viewer.append_pw(self.model.read_clipboard())

    def _drop_files(self, files):
        pws_drop = self.model.drop_files(files)
        print('??????????', pws_drop)
        if pws_drop:
            self.viewer.append_pw('\n'.join(pws_drop))

    def write_to_db(self):
        """??????????"""
        temp_pws = self.viewer.get_passwords()
        self.WriteTODB.emit(temp_pws)
