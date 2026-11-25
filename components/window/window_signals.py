# 窗口模块共用的信号定义与中转逻辑

from PySide6.QtCore import Signal

from common.class_file_info import FileInfo, FileInfoList


class WindowSignals:
    """窗口模块共用的信号定义，供模型和线程继承"""

    StepInfo = Signal(str, name='步骤信息')
    SignalCurrentFile = Signal(str, name='当前处理的文件名')
    SignalTaskCount = Signal(int, name='需要处理的文件总数')
    SignalTaskIndex = Signal(int, name='当前处理的文件索引')
    SignalCurrentPw = Signal(str, name='当前使用的密码')
    SignalPwCount = Signal(int, name='待测试密码总数')
    SignalPwIndex = Signal(int, name='当前使用的密码索引')
    SignalResult = Signal(FileInfo, name='自定义文件信息类')
    SignalStart = Signal(name='开始')
    SignalFinish = Signal(FileInfoList, name='结束，传递最终的文件信息类清单')


def relay_signals(source, target):
    """把 source 的信号连接到 target 的同名信号，实现逐级中转"""
    source.StepInfo.connect(target.StepInfo)
    source.SignalCurrentFile.connect(target.SignalCurrentFile)
    source.SignalTaskCount.connect(target.SignalTaskCount)
    source.SignalTaskIndex.connect(target.SignalTaskIndex)
    source.SignalCurrentPw.connect(target.SignalCurrentPw)
    source.SignalPwCount.connect(target.SignalPwCount)
    source.SignalPwIndex.connect(target.SignalPwIndex)
    source.SignalResult.connect(target.SignalResult)
    source.SignalStart.connect(target.SignalStart)
    source.SignalFinish.connect(target.SignalFinish)
