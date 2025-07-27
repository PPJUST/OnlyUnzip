import os
import re
import subprocess
from typing import Union

from common import function_queue
from common.class_7zip import Result7zip, TYPES_RESULT_7ZIP
from common.function_extract import TEMP_EXTRACT_FOLDER

FAKE_PASSWORD = 'FAKEPASSWORD'
_7ZIP_PATH = r'./7-Zip/7z.exe'


def _process_7zip_with_run(_7zip_command: Union[str, list]):
    """使用run调用7zip执行传入语句（直接返回结果，不需要实时读取管道信息）
    :param _7zip_command: 7zip命令行"""
    # 清理一次命令行
    if isinstance(_7zip_command, list):
        _7zip_command = [i for i in _7zip_command if i.strip()]

    print(f'调用7zip：{_7zip_command}')
    process = subprocess.run(_7zip_command,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             creationflags=subprocess.CREATE_NO_WINDOW,
                             text=True,
                             universal_newlines=True)
    return process


def process_7zip_l(_7zip_path: str, file: str, password: str, inside_path: str = None):
    """测试指定文件的密码
    :param _7zip_path: 7zip路径
    :param file: 需要测试的文件路径
    :param password: 需要测试的密码
    :param inside_path: 单独测试的内部文件路径
    :return: 7zip结果类"""
    command = [_7zip_path, 'l', file, '-p' + password]
    if inside_path:
        command.append(inside_path)
    process = _process_7zip_with_run(command)
    _7zip_result = _analyse_process_return(process)
    print('测试结果', _7zip_result)
    # 结果为”成功“时将正确密码写入结果类中
    if isinstance(_7zip_result, Result7zip.Success):
        _7zip_result.password = password

    return _7zip_result


def process_7zip_t(_7zip_path: str, file: str, password: str, inside_path: str = ''):
    """测试指定文件的密码
    :param _7zip_path: 7zip路径
    :param file: 需要测试的文件路径
    :param password: 需要测试的密码
    :param inside_path: 如果测试的文件是压缩文件，则可以尝试仅测试压缩文件内部的其中1个文件
    :return: 7zip结果类"""
    command = [_7zip_path, 't', file, '-p' + password, inside_path]
    process = _process_7zip_with_run(command)
    _7zip_result = _analyse_process_return(process)
    print('测试结果', _7zip_result)
    # 结果为”成功“时将正确密码写入结果类中
    if isinstance(_7zip_result, Result7zip.Success):
        _7zip_result.password = password

    return _7zip_result


def process_7zip_x(_7zip_path: str, file: str, password: str, cover_model: str, output_folder: str,
                   filter_rule: str = ''):
    """解压指定文件
    :param _7zip_path: 7zip路径
    :param file: 需要解压的文件路径
    :param password: 解压时使用的密码（附带测试功能）
    :param cover_model: 重名文件的覆盖模式
    :param output_folder: 解压输出目录
    :param filter_rule: 文件过滤器规则
    :return: 7zip结果类"""
    # 实例化发送数据的队列
    queue_sender = function_queue.get_sender()

    # 同时读取stdout和stderr会导致管道堵塞，所以需要将两个输出流重定向至同一个管道中（使用switch：'bso1','bsp1',bse1'）
    command = [_7zip_path, 'x', file, '-bsp1', '-bse1', '-bso1', cover_model, '-p' + password, '-o' + output_folder,
               filter_rule]
    # 清理一次命令行
    if isinstance(command, list):
        command = [i for i in command if i.strip()]

    print(f'调用7zip：{" ".join(command)}')
    process = subprocess.Popen(command,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               creationflags=subprocess.CREATE_NO_WINDOW,
                               text=True,
                               universal_newlines=True)

    # 实时读取输出流，提取信息
    # （使用Popen调用7zip时，返回码为2时的报错信息为"<_io.TextIOWrapper name=4 encoding='cp936'>"，
    # 无法根据该报错信息判断错误类型，所以需要在输出流中分析信息进行判断）
    error_type: TYPES_RESULT_7ZIP = None
    is_read_stderr = True  # 是否读取stderr流，出现报错事件/读取到进度信息后不再需要读取
    is_read_progress = True  # 是否读取进度信息，出现报错事件后不再需要读取
    while True:
        try:
            output = process.stdout.readline()
            if output.strip():
                print(f'7zip实时输出文本：\n{output.strip()}')  # 测试用
        except UnicodeDecodeError:  # UnicodeDecodeError: 'gbk' codec can't decode byte 0xaa in position 32: illegal multibyte sequence
            output = ''
        if output == '' and process.poll() is not None:  # 读取到空文本或返回码时，结束读取操作
            break

        # 读取错误事件
        if is_read_stderr and output.strip():
            is_wrong_password = re.search('Wrong password', output)
            is_missing_volume = re.search('Missing volume', output)
            is_cannot_open_the_file = re.search('Cannot open the file as', output)
            if is_wrong_password:
                error_type = Result7zip.WrongPassword()
                is_read_stderr = False
                is_read_progress = False
            elif is_missing_volume:
                error_type = Result7zip.MissingVolume()
                is_read_stderr = False
                is_read_progress = False
            elif is_cannot_open_the_file:
                # 如果是后缀名错误的问题，7zip会自动尝试以正确的后缀名进行解压，不需要停止读取
                error_type = Result7zip.WrongFiletype()

        # 读取进度事件
        if is_read_progress and output:
            # 单文件进度输出示例：34% - 061-090；多文件进度输出示例：19% 10 - 031-060。适用正则表达式 '(\d{1,3})% *\d* - '
            # 部分压缩文件的输出示例：80% 13。适用正则表达式 '(\d{1,3})% *\d*'
            match_progress = re.search(r'(\d{1,3})% *\d*', output)
            if match_progress:
                # is_read_stderr = False  # 读取到进度后直接不读取错误信息，可能会由于zip格式压缩包解压空文件但是有解压进度而无法正常读取错误信息
                current_progress = int(match_progress.group(1))  # 提取进度百分比（不含%）
                queue_sender.send_data(current_progress)

    # 结束后读取返回码
    print('识别的错误类型', error_type)
    return_code = process.poll()
    if return_code == 0:
        return Result7zip.Success(password)
    elif return_code == 1:
        return Result7zip.Warning()
    elif return_code == 2:
        if not error_type:
            error_type = Result7zip.UnknownError(output)
        return error_type
    elif return_code == 7:
        return Result7zip.ErrorCommand()
    elif return_code == 8:
        return Result7zip.NotEnoughMemory()
    elif return_code == 255:
        return Result7zip.UserStopped()
    else:  # 兜底
        return Result7zip.UnknownError('未知错误')


def get_temp_dirpath(dirpath: str):
    """获取根据传入路径计算的临时文件夹路径"""
    return os.path.normpath(os.path.join(dirpath, TEMP_EXTRACT_FOLDER))


def progress_7zip_x_with_temp_folder(_7zip_path: str, file: str, password: str, cover_model: str, output_folder: str,
                                     filter_rule: str = ''):
    """解压指定文件（解压至临时文件夹中）
    :param _7zip_path: 7zip路径
    :param file: 需要解压的文件路径
    :param password: 解压时使用的密码（附带测试功能）
    :param cover_model: 重名文件的覆盖模式
    :param output_folder: 解压输出目录
    :param filter_rule: 文件过滤器规则
    :return: 7zip结果类"""
    extract_dirpath_temp = get_temp_dirpath(output_folder)
    return process_7zip_x(_7zip_path, file, password, cover_model, extract_dirpath_temp, filter_rule)


def _analyse_process_return(process: subprocess.CompletedProcess):
    """分析调用7zip的返回结果
    :param process: subprocess调用结果对象
    :return: 7zip结果类"""
    return_code = process.returncode
    if return_code == 0:
        return Result7zip.Success()
    elif return_code == 1:
        return Result7zip.Warning()
    elif return_code == 2:
        output = str(process.stderr) + str(process.stdout)
        if 'Wrong password' in output:
            return Result7zip.WrongPassword()
        elif 'Missing volume' in output:
            return Result7zip.MissingVolume()
        elif 'Cannot open the file as' in output:
            return Result7zip.WrongFiletype()
        else:
            print(f'未知错误：{output}')
            return Result7zip.UnknownError(str(process.stderr))
    elif return_code == 7:
        return Result7zip.ErrorCommand()
    elif return_code == 8:
        return Result7zip.NotEnoughMemory()
    elif return_code == 255:
        return Result7zip.UserStopped()
    else:
        return Result7zip.UnknownError('未知错误')


def _read_process_stdout_get_files(process: subprocess.CompletedProcess):
    """读取process的stdout管道，提取其中包含的文件列表信息"""
    stdout = process.stdout
    files_dict = {'filetype': None, 'paths': None}
    if stdout:
        text_splits = stdout.splitlines()
    else:
        return files_dict

    # 提取文件类型
    cut_splits = [i for i in text_splits if i.startswith('Type = ')]
    if cut_splits:
        cut_text = [i for i in text_splits if i.startswith('Type = ')][0]
        filetype = cut_text[len('Type = '):]
        files_dict['filetype'] = filetype

    # 提取内部文件路径
    start_index = None
    end_index = None
    for index, i in enumerate(text_splits):
        if i.startswith('   Date'):
            start_index = index
        if i.startswith('----------'):
            end_index = index
    if start_index or end_index:
        column_name_index = text_splits[start_index].find('Name')
        cut_text = text_splits[start_index + 2:end_index]
        paths = [i[column_name_index:] for i in cut_text if 'D....' not in i]
        files_dict['paths'] = paths

    return files_dict


def get_smallest_file_in_archive(archive_path: str):
    """获取压缩文件中最小的文件内部路径"""
    print('提取压缩文件内部文件路径')
    # 测试一次压缩文件，读取返回信息
    command = [_7ZIP_PATH, "l", archive_path, f"-p{FAKE_PASSWORD}"]  # 需要指定密码，否则7zip会卡在输入密码阶段
    result = subprocess.run(command,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            text=True,
                            universal_newlines=True)

    # 解析返回信息，提取文件结构
    if "--------" not in result.stdout:
        return None
    # 内部文件信息在两行“--------”之间，表头在第一行“--------”的上一行
    # print(result.stdout)
    print(result.stdout)
    lines = result.stdout.split("\n")
    # 先找表头索引
    for index, line in enumerate(lines):
        if line.startswith("--------"):
            index_title = index - 1
            break
    # 再找表尾索引
    for index, line in enumerate(lines[::-1]):
        if line.startswith("--------"):
            index_end = len(lines) - index
            break
    # 测试一次索引号，如果不存在则直接返回空
    try:
        index_title
        index_end
    except NameError:
        return None
    # 提取信息行
    lines_info = lines[index_title:index_end]
    # 解析信息行中每列的起始索引和结束索引
    line_split = lines_info[1]
    start_data_time = 0
    end_data_time = line_split.find(' -')
    start_attr = end_data_time + 1
    end_attr = line_split.find(' -', start_attr)
    start_size = end_attr + 1
    end_size = line_split.find(' -', start_size)
    start_compressed = end_size + 1
    end_compressed = line_split.find(' -', start_compressed)
    start_name = end_compressed + 1
    end_name = start_name + 200
    # 转换为dict格式
    infos: list[dict] = []
    for line in lines_info:
        data = line[start_data_time: end_data_time].strip()
        attr = line[start_attr: end_attr].strip()
        size = line[start_size: end_size].strip()
        compressed = line[start_compressed: end_compressed].strip()
        name = line[start_name: end_name].strip()
        if size.isdigit() and compressed.isdigit():
            size = int(size)
            compressed = int(compressed)
            line_dict = {"data": data, "attr": attr, "size": size, "compressed": compressed, "name": name}
            infos.append(line_dict)

    # 根据size排序列表
    infos_sorted = sorted(infos, key=lambda x: x['size'])

    # 提取最小文件（排除文件夹）
    smallest_file = ''
    for info_dict in infos_sorted:
        if info_dict['attr'] == 'D....':
            continue
        else:
            smallest_file = info_dict['name']

    return smallest_file
