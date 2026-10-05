import lzytools_Qt
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QApplication, QToolButton

from common.class_7zip import TYPES_MODEL_ARCHIVE, ModelArchive
from components.page_home.res.icon_base64 import ICON_TEMP_PASSWORD
from components.page_home.res.label_icon import LabelIcon

_BUTTON_HEIGHT = 20
_BUTTON_WIDTH = 20
_HIGHLIGHT_STYLESHEET = "color: blue; font-weight: bold"
_NORMAL_STYLESHEET = "color: black; font-weight: normal"


class LabelIconWithFloatButton(LabelIcon):
    """??????????label,?????button"""
    OpenTempPasswords = Signal(name="??????")
    AskUpdateSetting = Signal(name="????????")
    ChangeSettingArchiveModel = Signal(object, name="??????")
    ChangeSettingTryUnknownFiletype = Signal(bool, name="????????????")
    ChangeSettingRecursiveExtract = Signal(bool, name="????????")
    ChangeSettingDeleteOrigin = Signal(bool, name="?????????")
    ChangeSettingTopWindow = Signal(bool, name="??????")

    def __init__(self, parent=None):
        super().__init__(parent)
        # ????????,???????????
        self.float_button_temp_pws = QToolButton()
        self.float_button_temp_pws.setFixedSize(_BUTTON_WIDTH, _BUTTON_HEIGHT)
        self.float_button_temp_pws.setIcon(lzytools_Qt.convert_base64_image_to_pixmap(ICON_TEMP_PASSWORD))
        self.float_button_temp_pws.setParent(self)
        self.float_button_temp_pws.clicked.connect(self.OpenTempPasswords.emit)
        self.float_button_temp_pws.show()

        # ????????,????????
        # ??????????
        self.float_button_expand = QToolButton()
        self.float_button_expand.setFixedSize(_BUTTON_WIDTH, _BUTTON_HEIGHT)
        self.float_button_expand.setText('>')
        self.float_button_expand.setParent(self)
        self.float_button_expand.clicked.connect(self._expand_buttons)
        # ????/???????
        self.setting_archive_model: TYPES_MODEL_ARCHIVE = ModelArchive.Test()
        self.float_button_et = QToolButton()
        self.float_button_et.setFixedSize(_BUTTON_WIDTH, _BUTTON_HEIGHT)
        self.float_button_et.setText('?')
        self.float_button_et.setParent(self)
        self.float_button_et.clicked.connect(self._click_et_buton)
        self.float_button_et.show()
        # ???????????????
        self.setting_is_enable_try_unknown_filetype: bool = True
        self.float_button_du = QToolButton()
        self.float_button_du.setFixedSize(_BUTTON_WIDTH, _BUTTON_HEIGHT)
        self.float_button_du.setText('?')
        self.float_button_du.setParent(self)
        self.float_button_du.clicked.connect(self._click_du_button)
        self.float_button_du.show()
        # ???????????
        self.setting_is_enable_recursive_extract: bool = True
        self.float_button_rc = QToolButton()
        self.float_button_rc.setFixedSize(_BUTTON_WIDTH, _BUTTON_HEIGHT)
        self.float_button_rc.setText('?')
        self.float_button_rc.setParent(self)
        self.float_button_rc.clicked.connect(self._click_rc_button)
        self.float_button_rc.show()
        # ????????????
        self.setting_is_enable_delete_origin: bool = True
        self.float_button_do = QToolButton()
        self.float_button_do.setFixedSize(_BUTTON_WIDTH, _BUTTON_HEIGHT)
        self.float_button_do.setText('?')
        self.float_button_do.setParent(self)
        self.float_button_do.clicked.connect(self._click_do_button)
        self.float_button_do.show()
        # ???????????
        self.setting_is_enable_top_window: bool = False
        self.float_button_tp = QToolButton()
        self.float_button_tp.setFixedSize(_BUTTON_WIDTH, _BUTTON_HEIGHT)
        self.float_button_tp.setText('?')
        self.float_button_tp.setParent(self)
        self.float_button_tp.clicked.connect(self._click_tp_button)
        self.float_button_tp.show()

        # ???????????????
        self.float_button_expand.setToolTip('??/??????')
        self.float_button_temp_pws.setToolTip('???????')
        self.float_button_et.setToolTip('??????/????')
        self.float_button_du.setToolTip('????????(??????)')
        self.float_button_rc.setToolTip('?????????')
        self.float_button_do.setToolTip('??????????')
        self.float_button_tp.setToolTip('????')

        # ????????
        self._adjust_button_position()

    def update_setting(self, archive_model: TYPES_MODEL_ARCHIVE,
                       try_unknown_filetype: bool,
                       recursive_extract: bool,
                       delete_origin: bool,
                       top_window: bool):
        """??????"""
        self.setting_archive_model = archive_model
        self.setting_is_enable_try_unknown_filetype = try_unknown_filetype
        self.setting_is_enable_recursive_extract = recursive_extract
        self.setting_is_enable_delete_origin = delete_origin
        self.setting_is_enable_top_window = top_window

        self._change_et_button_style()
        self._change_du_button_style()
        self._change_rc_button_style()
        self._change_do_button_style()
        self._change_tp_button_style()

    def set_float_button_enable(self, is_enable: bool):
        """??????????"""
        self.float_button_expand.setEnabled(is_enable)
        if not is_enable:
            self.hide_buttons()

    def _expand_buttons(self):
        """???????"""
        if self.float_button_expand.text() == '<':
            self.float_button_expand.setText('>')
            self._show_buttons()
            self.AskUpdateSetting.emit()
        else:
            self.hide_buttons()

    def hide_buttons(self):
        """?????????"""
        self.float_button_expand.setText('<')
        self.float_button_temp_pws.hide()
        self.float_button_et.hide()
        self.float_button_du.hide()
        self.float_button_rc.hide()
        self.float_button_do.hide()
        self.float_button_tp.hide()

    def _show_buttons(self):
        """????????"""
        self.float_button_temp_pws.show()
        self.float_button_et.show()
        self.float_button_du.show()
        self.float_button_rc.show()
        self.float_button_do.show()
        self.float_button_tp.show()

    def _click_et_buton(self):
        """????/????"""
        # ????
        if isinstance(self.setting_archive_model, ModelArchive.Test):
            self.setting_archive_model = ModelArchive.Extract()
        elif isinstance(self.setting_archive_model, ModelArchive.Extract):
            self.setting_archive_model = ModelArchive.Test()
        # ??????
        self._change_et_button_style()
        # ????????
        self.ChangeSettingArchiveModel.emit(self.setting_archive_model)

    def _change_et_button_style(self):
        """????/???????"""
        if isinstance(self.setting_archive_model, ModelArchive.Extract):
            text = '?'
            self.float_button_et.setToolTip('??:????(?????????)')
        else:
            text = '?'
            self.float_button_et.setToolTip('??:????(?????????)')
        self.float_button_et.setText(text)

    def _click_du_button(self):
        """????????????"""
        # ????
        self.setting_is_enable_try_unknown_filetype = not self.setting_is_enable_try_unknown_filetype
        # ??????
        self._change_du_button_style()
        # ????????
        self.ChangeSettingTryUnknownFiletype.emit(self.setting_is_enable_try_unknown_filetype)

    def _change_du_button_style(self):
        """???????????????"""
        if self.setting_is_enable_try_unknown_filetype:
            stylesheet = _HIGHLIGHT_STYLESHEET
            self.float_button_du.setToolTip('???:????????(????)')
        else:
            stylesheet = _NORMAL_STYLESHEET
            self.float_button_du.setToolTip('???:???????(????)')
        self.float_button_du.setStyleSheet(stylesheet)

    def _click_rc_button(self):
        """????????"""
        # ????
        self.setting_is_enable_recursive_extract = not self.setting_is_enable_recursive_extract
        # ??????
        self._change_rc_button_style()
        # ????????
        self.ChangeSettingRecursiveExtract.emit(self.setting_is_enable_recursive_extract)

    def _change_rc_button_style(self):
        """???????????"""
        if self.setting_is_enable_recursive_extract:
            stylesheet = _HIGHLIGHT_STYLESHEET
            self.float_button_rc.setToolTip('???:?????????(????)')
        else:
            stylesheet = _NORMAL_STYLESHEET
            self.float_button_rc.setToolTip('???:??????(????)')
        self.float_button_rc.setStyleSheet(stylesheet)

    def _click_do_button(self):
        """?????????"""
        # ????
        self.setting_is_enable_delete_origin = not self.setting_is_enable_delete_origin
        # ??????
        self._change_do_button_style()
        # ????????
        self.ChangeSettingDeleteOrigin.emit(self.setting_is_enable_delete_origin)

    def _change_do_button_style(self):
        """????????????"""
        if self.setting_is_enable_delete_origin:
            stylesheet = _HIGHLIGHT_STYLESHEET
            self.float_button_do.setToolTip('???:????????????(????)')
        else:
            stylesheet = _NORMAL_STYLESHEET
            self.float_button_do.setToolTip('???:?????(????)')
        self.float_button_do.setStyleSheet(stylesheet)

    def _click_tp_button(self):
        """????????"""
        # ????
        self.setting_is_enable_top_window = not self.setting_is_enable_top_window
        # ??????
        self._change_tp_button_style()
        # ????????
        self.ChangeSettingTopWindow.emit(self.setting_is_enable_top_window)

    def _change_tp_button_style(self):
        """???????????"""
        if self.setting_is_enable_top_window:
            stylesheet = _HIGHLIGHT_STYLESHEET
            self.float_button_tp.setToolTip('???:????(????)')
        else:
            stylesheet = _NORMAL_STYLESHEET
            self.float_button_tp.setToolTip('???:????(????)')
        self.float_button_tp.setStyleSheet(stylesheet)

    def _adjust_button_position(self):
        """?????????"""
        # ????????
        spacing = 5
        margin_left = 5
        margin_top = 5
        y = margin_top
        x_expand = margin_left
        self.float_button_expand.move(x_expand, y)

        x_temp = x_expand + _BUTTON_WIDTH + spacing
        self.float_button_temp_pws.move(x_temp, y)

        x_et = x_temp + _BUTTON_WIDTH + spacing
        self.float_button_et.move(x_et, y)

        x_du = x_et + _BUTTON_WIDTH + spacing
        self.float_button_du.move(x_du, y)

        x_rc = x_du + _BUTTON_WIDTH + spacing
        self.float_button_rc.move(x_rc, y)

        x_do = x_rc + _BUTTON_WIDTH + spacing
        self.float_button_do.move(x_do, y)

        x_tp = x_do + _BUTTON_WIDTH + spacing
        self.float_button_tp.move(x_tp, y)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._adjust_button_position()


if __name__ == "__main__":
    app_ = QApplication()
    program_ui = LabelIconWithFloatButton()
    program_ui.show()
    app_.exec()
