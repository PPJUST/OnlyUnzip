import subprocess


def stop_process(process: subprocess.Popen):
    """终止调用"""
    print('中断调用')
    if process:
        process.terminate()
