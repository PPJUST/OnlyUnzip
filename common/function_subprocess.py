import subprocess


def stop_process(process: subprocess.Popen):
    """????"""
    print('????')
    if process:
        process.terminate()
