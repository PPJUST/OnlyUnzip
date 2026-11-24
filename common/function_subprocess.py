"""子进程相关操作。"""

import subprocess


def stop_process(process: subprocess.Popen) -> None:
    """终止仍在运行的子进程；进程为空或已结束时不做任何操作。

    :param process: 需要终止的子进程对象，允许传入 None
    """
    if process is None:
        return

    # 进程可能在调用前已经自然结束，此时无需再发送终止信号
    if process.poll() is not None:
        return

    print(f'中断调用：进程 {process.pid}')
    try:
        process.terminate()
    except OSError as exc:
        # 进程可能在检查状态与终止之间退出，属于正常竞态，无需向外抛出
        print(f'终止进程时进程已退出：{exc}')
