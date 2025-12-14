import lzytools._qt_pyside6
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
    """用于显示图标的自定义label，附带悬浮的button"""
    OpenTempPasswords = Signal(name="打开临时密码")
    AskUpdateSetting = Signal(name="请求更新选项参数")
    ChangeSettingArchiveModel = Signal(object, name="设置模式选项")
    ChangeSettingTryUnknownFiletype = Signal(bool, name="设置处理未知格式文件选项")
    ChangeSettingRecursiveExtract = Signal(bool, name="设置递归解压选项")
    ChangeSettingDeleteOrigin = Signal(bool, name="设置删除原文件选项")
    ChangeSettingTopWindow = Signal(bool, name="设置置顶选项")

    def __init__(self, parent=None):
        super().__init__(parent)
        # 创建左上悬浮按钮，用于打开临时密码管理器
        self.float_button_temp_pws = QToolButton()
        self.float_button_temp_pws.setFixedSize(_BUTTON_WIDTH, _BUTTON_HEIGHT)
        self.float_button_temp_pws.setIcon(lzytools._qt_pyside6.base64_to_pixmap(ICON_TEMP_PASSWORD))
        self.float_button_temp_pws.setParent(self)
        self.float_button_temp_pws.clicked.connect(self.OpenTempPasswords.emit)
        self.float_button_temp_pws.hide()

        # 创建左上悬浮按钮，用于快速勾选选项
        # 用于展开和收缩的按钮
        self.float_button_expand = QToolButton()
        self.float_button_expand.setFixedSize(_BUTTON_WIDTH, _BUTTON_HEIGHT)
        self.float_button_expand.setText('<')
        self.float_button_expand.setParent(self)
        self.float_button_expand.clicked.connect(self._expand_buttons)
        # 修改解压/测试选项的按钮
        self.setting_archive_model: TYPES_MODEL_ARCHIVE = ModelArchive.Test()
        self.float_button_et = QToolButton()
        self.float_button_et.setFixedSize(_BUTTON_WIDTH, _BUTTON_HEIGHT)
        self.float_button_et.setText('解')
        self.float_button_et.setParent(self)
        self.float_button_et.clicked.connect(self._click_et_buton)
        self.float_button_et.hide()
        # 修改处理未知格式文件选项的按钮
        self.setting_is_enable_try_unknown_filetype: bool = False
        self.float_button_du = QToolButton()
        self.float_button_du.setFixedSize(_BUTTON_WIDTH, _BUTTON_HEIGHT)
        self.float_button_du.setText('未')
        self.float_button_du.setParent(self)
        self.float_button_du.clicked.connect(self._click_du_button)
        self.float_button_du.hide()
        # 修改递归解压选项的按钮
        self.setting_is_enable_recursive_extract: bool = False
        self.float_button_rc = QToolButton()
        self.float_button_rc.setFixedSize(_BUTTON_WIDTH, _BUTTON_HEIGHT)
        self.float_button_rc.setText('递')
        self.float_button_rc.setParent(self)
        self.float_button_rc.clicked.connect(self._click_rc_button)
        self.float_button_rc.hide()
        # 修改删除原文件选项的按钮
        self.setting_is_enable_delete_origin: bool = False
        self.float_button_do = QToolButton()
        self.float_button_do.setFixedSize(_BUTTON_WIDTH, _BUTTON_HEIGHT)
        self.float_button_do.setText('删')
        self.float_button_do.setParent(self)
        self.float_button_do.clicked.connect(self._click_do_button)
        self.float_button_do.hide()
        # 修改置顶窗口选项的按钮
        self.setting_is_enable_top_window: bool = False
        self.float_button_tp = QToolButton()
        self.float_button_tp.setFixedSize(_BUTTON_WIDTH, _BUTTON_HEIGHT)
        self.float_button_tp.setText('顶')
        self.float_button_tp.setParent(self)
        self.float_button_tp.clicked.connect(self._click_tp_button)
        self.float_button_tp.hide()

        # 调整按钮初始位置
        self._adjust_button_position()

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
        if self.float_button_expand.text() == '<':
            self.float_button_expand.setText('>')
            self._show_buttons()
            self.AskUpdateSetting.emit()
        else:
            self.hide_buttons()

    def hide_buttons(self):
        """隐藏左上的悬浮按钮"""
        self.float_button_expand.setText('<')
        self.float_button_temp_pws.hide()
        self.float_button_et.hide()
        self.float_button_du.hide()
        self.float_button_rc.hide()
        self.float_button_do.hide()
        self.float_button_tp.hide()

    def _show_buttons(self):
        """显示更多悬浮按钮"""
        self.float_button_temp_pws.show()
        self.float_button_et.show()
        self.float_button_du.show()
        self.float_button_rc.show()
        self.float_button_do.show()
        self.float_button_tp.show()

    def _click_et_buton(self):
        """点击解压/测试按钮"""
        # 反转选项
        if isinstance(self.setting_archive_model, ModelArchive.Test):
            self.setting_archive_model = ModelArchive.Extract()
        elif isinstance(self.setting_archive_model, ModelArchive.Extract):
            self.setting_archive_model = ModelArchive.Test()
        # 修改按钮样式
        self._change_et_button_style()
        # 发送新选项的信号
        self.ChangeSettingArchiveModel.emit(self.setting_archive_model)

    def _change_et_button_style(self):
        """修改解压/测试按钮的样式"""
        text = '解' if isinstance(self.setting_archive_model, ModelArchive.Extract) else '测'
        self.float_button_et.setText(text)

    def _click_du_button(self):
        """点击处理未知格式文件按钮"""
        # 反转选项
        self.setting_is_enable_try_unknown_filetype = not self.setting_is_enable_try_unknown_filetype
        # 修改按钮样式
        self._change_du_button_style()
        # 发送新选项的信号
        self.ChangeSettingTryUnknownFiletype.emit(self.setting_is_enable_try_unknown_filetype)

    def _change_du_button_style(self):
        """修改处理未知格式文件按钮的样式"""
        stylesheet = _HIGHLIGHT_STYLESHEET if self.setting_is_enable_try_unknown_filetype else _NORMAL_STYLESHEET
        self.float_button_du.setStyleSheet(stylesheet)

    def _click_rc_button(self):
        """点击递归解压按钮"""
        # 反转选项
        self.setting_is_enable_recursive_extract = not self.setting_is_enable_recursive_extract
        # 修改按钮样式
        self._change_rc_button_style()
        # 发送新选项的信号
        self.ChangeSettingRecursiveExtract.emit(self.setting_is_enable_recursive_extract)

    def _change_rc_button_style(self):
        """修改递归解压按钮的样式"""
        stylesheet = _HIGHLIGHT_STYLESHEET if self.setting_is_enable_recursive_extract else _NORMAL_STYLESHEET
        self.float_button_rc.setStyleSheet(stylesheet)

    def _click_do_button(self):
        """点击删除原文件按钮"""
        # 反转选项
        self.setting_is_enable_delete_origin = not self.setting_is_enable_delete_origin
        # 修改按钮样式
        self._change_do_button_style()
        # 发送新选项的信号
        self.ChangeSettingDeleteOrigin.emit(self.setting_is_enable_delete_origin)

    def _change_do_button_style(self):
        """修改删除原文件按钮的样式"""
        stylesheet = _HIGHLIGHT_STYLESHEET if self.setting_is_enable_delete_origin else _NORMAL_STYLESHEET
        self.float_button_do.setStyleSheet(stylesheet)

    def _click_tp_button(self):
        """点击置顶窗口按钮"""
        # 反转选项
        self.setting_is_enable_top_window = not self.setting_is_enable_top_window
        # 修改按钮样式
        self._change_tp_button_style()
        # 发送新选项的信号
        self.ChangeSettingTopWindow.emit(self.setting_is_enable_top_window)

    def _change_tp_button_style(self):
        """修改置顶窗口按钮的样式"""
        stylesheet = _HIGHLIGHT_STYLESHEET if self.setting_is_enable_top_window else _NORMAL_STYLESHEET
        self.float_button_tp.setStyleSheet(stylesheet)

    def _adjust_button_position(self):
        """调整悬浮按钮的位置"""
        # 设置左上按钮位置
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
