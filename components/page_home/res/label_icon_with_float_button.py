import lzytools_Qt
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QApplication, QToolButton

from common.class_7zip import ModelArchive, TYPES_MODEL_ARCHIVE
from components.page_home.res.icon_base64 import ICON_TEMP_PASSWORD
from components.page_home.res.label_icon import LabelIcon

_BUTTON_WIDTH = 20
_BUTTON_HEIGHT = 20
_BUTTON_SPACING = 5
_BUTTON_MARGIN_LEFT = 5
_BUTTON_MARGIN_TOP = 5

_HIGHLIGHT_STYLESHEET = "color: blue; font-weight: bold"
_NORMAL_STYLESHEET = "color: black; font-weight: normal"


class LabelIconWithFloatButton(LabelIcon):
    """用于显示图标的自定义label，附带悬浮的设置按钮"""

    OpenTempPasswords = Signal(name="打开临时密码")
    AskUpdateSetting = Signal(name="请求更新选项参数")
    ChangeSettingArchiveModel = Signal(object, name="设置模式选项")
    ChangeSettingTryUnknownFiletype = Signal(bool, name="设置处理未知格式文件选项")
    ChangeSettingRecursiveExtract = Signal(bool, name="设置递归解压选项")
    ChangeSettingDeleteOrigin = Signal(bool, name="设置删除源文件选项")
    ChangeSettingTopWindow = Signal(bool, name="设置置顶选项")

    def __init__(self, parent=None):
        super().__init__(parent)

        # 选项状态
        self.setting_archive_model: TYPES_MODEL_ARCHIVE = ModelArchive.Test()
        self.setting_is_enable_try_unknown_filetype = False
        self.setting_is_enable_recursive_extract = False
        self.setting_is_enable_delete_origin = False
        self.setting_is_enable_top_window = False

        # 打开临时密码管理器的按钮
        self.float_button_temp_pws = self._create_button('', self.OpenTempPasswords.emit)
        self.float_button_temp_pws.setIcon(
            lzytools_Qt.convert_base64_image_to_pixmap(ICON_TEMP_PASSWORD)
        )
        self.float_button_temp_pws.hide()

        # 展开或收缩设置按钮
        self.float_button_expand = self._create_button('<', self._expand_buttons)

        # 切换解压/测试模式
        self.float_button_et = self._create_button('解', self._click_et_button)

        # 切换各项设置
        self.float_button_du = self._create_button('未', self._click_du_button)
        self.float_button_rc = self._create_button('递', self._click_rc_button)
        self.float_button_do = self._create_button('删', self._click_do_button)
        self.float_button_tp = self._create_button('顶', self._click_tp_button)

        self._hide_setting_buttons()
        self._adjust_button_position()

    def _create_button(self, text: str, clicked_slot):
        """创建固定尺寸的悬浮按钮"""
        button = QToolButton()
        button.setFixedSize(_BUTTON_WIDTH, _BUTTON_HEIGHT)
        button.setText(text)
        button.setParent(self)
        button.clicked.connect(clicked_slot)
        return button

    def _get_all_buttons(self):
        """按显示顺序返回所有悬浮按钮"""
        return [
            self.float_button_expand,
            self.float_button_temp_pws,
            self.float_button_et,
            self.float_button_du,
            self.float_button_rc,
            self.float_button_do,
            self.float_button_tp,
        ]

    def _get_setting_buttons(self):
        """返回展开后才显示的按钮"""
        return [
            self.float_button_temp_pws,
            self.float_button_et,
            self.float_button_du,
            self.float_button_rc,
            self.float_button_do,
            self.float_button_tp,
        ]

    @staticmethod
    def _set_button_style(button: QToolButton, is_enable: bool):
        """根据选项状态设置按钮样式"""
        if is_enable:
            button.setStyleSheet(_HIGHLIGHT_STYLESHEET)
        else:
            button.setStyleSheet(_NORMAL_STYLESHEET)

    def update_setting(self, archive_model: TYPES_MODEL_ARCHIVE,
                       try_unknown_filetype: bool,
                       recursive_extract: bool,
                       delete_origin: bool,
                       top_window: bool):
        """更新选项参数"""
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
        """设置悬浮按钮是否可用"""
        self.float_button_expand.setEnabled(is_enable)
        if not is_enable:
            self.hide_buttons()

    def _expand_buttons(self):
        """展开或收缩按钮"""
        if self.float_button_expand.text() != '<':
            self.hide_buttons()
            return

        self.float_button_expand.setText('>')
        self._show_setting_buttons()
        self.AskUpdateSetting.emit()

    def hide_buttons(self):
        """隐藏左上的悬浮按钮"""
        self.float_button_expand.setText('<')
        self._hide_setting_buttons()

    def _hide_setting_buttons(self):
        """隐藏展开后才显示的按钮"""
        for button in self._get_setting_buttons():
            button.hide()

    def _show_setting_buttons(self):
        """显示展开后的设置按钮"""
        for button in self._get_setting_buttons():
            button.show()

    def _click_et_button(self):
        """点击解压/测试按钮"""
        if isinstance(self.setting_archive_model, ModelArchive.Test):
            self.setting_archive_model = ModelArchive.Extract()
        elif isinstance(self.setting_archive_model, ModelArchive.Extract):
            self.setting_archive_model = ModelArchive.Test()

        self._change_et_button_style()
        self.ChangeSettingArchiveModel.emit(self.setting_archive_model)

    def _click_et_buton(self):
        """兼容原有方法名"""
        self._click_et_button()

    def _change_et_button_style(self):
        """修改解压/测试按钮的样式"""
        if isinstance(self.setting_archive_model, ModelArchive.Extract):
            self.float_button_et.setText('解')
        else:
            self.float_button_et.setText('测')

    def _click_du_button(self):
        """点击处理未知格式文件按钮"""
        self.setting_is_enable_try_unknown_filetype = not self.setting_is_enable_try_unknown_filetype
        self._change_du_button_style()
        self.ChangeSettingTryUnknownFiletype.emit(self.setting_is_enable_try_unknown_filetype)

    def _change_du_button_style(self):
        """修改处理未知格式文件按钮的样式"""
        self._set_button_style(self.float_button_du, self.setting_is_enable_try_unknown_filetype)

    def _click_rc_button(self):
        """点击递归解压按钮"""
        self.setting_is_enable_recursive_extract = not self.setting_is_enable_recursive_extract
        self._change_rc_button_style()
        self.ChangeSettingRecursiveExtract.emit(self.setting_is_enable_recursive_extract)

    def _change_rc_button_style(self):
        """修改递归解压按钮的样式"""
        self._set_button_style(self.float_button_rc, self.setting_is_enable_recursive_extract)

    def _click_do_button(self):
        """点击删除源文件按钮"""
        self.setting_is_enable_delete_origin = not self.setting_is_enable_delete_origin
        self._change_do_button_style()
        self.ChangeSettingDeleteOrigin.emit(self.setting_is_enable_delete_origin)

    def _change_do_button_style(self):
        """修改删除源文件按钮的样式"""
        self._set_button_style(self.float_button_do, self.setting_is_enable_delete_origin)

    def _click_tp_button(self):
        """点击置顶窗口按钮"""
        self.setting_is_enable_top_window = not self.setting_is_enable_top_window
        self._change_tp_button_style()
        self.ChangeSettingTopWindow.emit(self.setting_is_enable_top_window)

    def _change_tp_button_style(self):
        """修改置顶窗口按钮的样式"""
        self._set_button_style(self.float_button_tp, self.setting_is_enable_top_window)

    def _adjust_button_position(self):
        """依次排列悬浮按钮"""
        x = _BUTTON_MARGIN_LEFT
        y = _BUTTON_MARGIN_TOP
        for button in self._get_all_buttons():
            button.move(x, y)
            x += _BUTTON_WIDTH + _BUTTON_SPACING

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._adjust_button_position()


if __name__ == "__main__":
    app_ = QApplication()
    program_ui = LabelIconWithFloatButton()
    program_ui.show()
    app_.exec()
