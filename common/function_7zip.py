import os
import re
import subprocess

from common import function_queue, function_setting
from common.class_7zip import Result7zip
from common.function_extract import TEMP_EXTRACT_FOLDER

FAKE_PASSWORD = 'FAKEPASSWORD'
_CMD_PW_TEXT_FILE = 'cmd_pw.txt'
_process_running = None

_SPECIAL_PASSWORD_CHARS = ['*', ':', '<', '>', '?', '\\', '/', '|', '&', ';', '(', ')', '^', '%']


def get_7zip_path():
    """获取7zip路径"""
    path_setting = function_setting.get_7zip_path()
    if path_setting:
        return path_setting
    return r'./7-Zip/7z.exe'


def get_running_process():
    """获取正在运行的7zip进程，已结束则返回None"""
    print('当前运行线程', _process_running)
    if _process_running is not None and _process_running.poll() is None:
        return _process_running
    return None


def has_special_chars(text):
    """判断文本中是否包含需要特殊处理的字符"""
    for char in text:
        if char in _SPECIAL_PASSWORD_CHARS:
            return True
    return False


def has_special_chars_translate(text):
    """兼容旧调用：判断文本中是否包含需要特殊处理的字符"""
    return has_special_chars(text)


def is_need_local_pw_file(password):
    """判断密码是否需要通过临时文件传给7zip"""
    if has_special_chars(password):
        return True
    if ' ' in password:
        return True
    return False


def create_cmd_pw_file(password):
    """创建临时密码文件，用于处理带特殊字符或空格的密码"""
    with open(_CMD_PW_TEXT_FILE, 'w', encoding='utf-8') as file:
        file.write(password)


def delete_cmd_pw_file():
    """删除临时密码文件。

    当前版本保留空实现，以兼容既有调用并避免并发任务互相删除密码文件。
    """
    return


def _quote_path(path):
    """为路径添加引号"""
    return '"' + path + '"'


def _clean_command(command):
    """清理命令列表中的空参数"""
    cleaned_command = []
    for part in command:
        if part and part.strip():
            cleaned_command.append(part)
    return cleaned_command


def _join_command(command):
    """将命令列表组合为shell可执行的字符串"""
    cleaned_command = _clean_command(command)
    return ' '.join(cleaned_command)


def _get_password_part(password):
    """获取命令行中的密码参数"""
    if is_need_local_pw_file(password):
        create_cmd_pw_file(password)
        return '-y<' + _CMD_PW_TEXT_FILE
    return '-p' + password


def _get_inside_path_part(inside_path):
    """获取命令行中指定内部文件的参数"""
    if inside_path:
        return _quote_path(inside_path)
    return ''


def _build_check_command(mode, _7zip_path, file, password, inside_path):
    """构造l或t命令"""
    command = [
        _quote_path(_7zip_path),
        mode,
        _quote_path(file),
        _get_password_part(password),
        _get_inside_path_part(inside_path)
    ]
    return _join_command(command)


def _build_extract_command(_7zip_path, file, password, cover_model, output_folder, filter_rule):
    """构造x命令"""
    command = [
        _quote_path(_7zip_path),
        'x',
        _quote_path(file),
        '-bsp1',
        '-bse1',
        '-bso1',
        cover_model,
        _get_password_part(password),
        _quote_path('-o' + output_folder)
    ]

    if filter_rule:
        for rule in filter_rule:
            command.append(rule)

    return _join_command(command)


def _process_7zip_with_run(command):
    """使用run调用7zip，直接返回结果"""
    if isinstance(command, list):
        command = _join_command(command)

    print('调用7zip（run）：' + command)
    process = subprocess.run(command,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             creationflags=subprocess.CREATE_NO_WINDOW,
                             text=True,
                             shell=True)
    delete_cmd_pw_file()
    print('返回码', process.returncode)
    print('错误信息', process.stderr)
    return process


def _get_error_type_from_text(output):
    """根据7zip输出文本识别错误类型"""
    if 'Wrong password' in output:
        return Result7zip.WrongPassword()
    if 'Missing volume' in output:
        return Result7zip.MissingVolume()
    if 'Cannot open the file as' in output:
        return Result7zip.WrongFiletype()
    return None


def _get_result_by_return_code(return_code):
    """根据返回码获取固定类型的结果，无法判断时返回None"""
    if return_code == 1:
        return Result7zip.Warning()
    if return_code == 7:
        return Result7zip.ErrorCommand()
    if return_code == 8:
        return Result7zip.NotEnoughMemory()
    if return_code == 255:
        return Result7zip.UserStopped()
    return None


def _analyse_process_return(process):
    """分析run调用7zip的返回结果"""
    return_code = process.returncode
    if return_code == 0:
        return Result7zip.Success()

    if return_code == 2:
        output = str(process.stderr) + str(process.stdout)
        error_type = _get_error_type_from_text(output)
        if error_type is not None:
            return error_type
        print('未知错误：' + output)
        return Result7zip.UnknownError(str(process.stderr))

    result = _get_result_by_return_code(return_code)
    if result is not None:
        return result
    return Result7zip.UnknownError('未知错误')


def _run_check_command(mode, _7zip_path, file, password, inside_path):
    """执行l或t命令并分析结果"""
    command = _build_check_command(mode, _7zip_path, file, password, inside_path)
    process = _process_7zip_with_run(command)
    result = _analyse_process_return(process)

    if isinstance(result, Result7zip.Success):
        result.password = password

    return result


def process_7zip_l(_7zip_path, file, password, inside_path=''):
    """使用l命令测试指定文件的密码"""
    return _run_check_command('l', _7zip_path, file, password, inside_path)


def process_7zip_t(_7zip_path, file, password, inside_path=''):
    """使用t命令测试指定文件的密码"""
    return _run_check_command('t', _7zip_path, file, password, inside_path)


def _get_extract_error_type(output):
    """分析解压输出中的错误事件。

    返回三个值：错误类型、是否停止读取输出、是否为虚假成功。
    """
    if re.search('Wrong password', output):
        return Result7zip.WrongPassword(), True, False
    if re.search('Missing volume', output):
        return Result7zip.MissingVolume(), True, False
    if re.search('Cannot open the file as', output):
        return Result7zip.WrongFiletype(), False, False
    if re.search('No files to process', output):
        return Result7zip.UnknownError('No files to process'), True, True
    return None, False, False


def _read_process_line(process):
    """读取7zip输出的一行，遇到编码错误则忽略该行"""
    try:
        return process.stdout.readline()
    except UnicodeDecodeError:
        return ''


def _send_progress(queue_sender, output):
    """从输出文本中提取进度并发送"""
    match_progress = re.search(r'(\d{1,3})% *\d*', output)
    if not match_progress:
        return

    current_progress = int(match_progress.group(1))
    if current_progress:
        queue_sender.send_data(current_progress)


def _read_extract_output(process, queue_sender):
    """实时读取解压输出，提取错误类型和进度"""
    error_type = None
    last_output = ''
    is_fake_success = False
    is_read_stderr = True
    is_read_progress = True

    while True:
        output = _read_process_line(process)
        last_output = output

        if output.strip():
            print('7zip实时输出文本：\n' + output.strip())

        if output == '' and process.poll() is not None:
            break

        if is_read_stderr and output.strip():
            found_error_type, should_stop, found_fake_success = _get_extract_error_type(output)
            if found_error_type is not None:
                error_type = found_error_type
            if found_fake_success:
                is_fake_success = True
            if should_stop:
                is_read_stderr = False
                is_read_progress = False

        if is_read_progress and output:
            _send_progress(queue_sender, output)

    return error_type, is_fake_success, last_output


def _get_extract_result(return_code, error_type, output, password, is_fake_success):
    """根据解压结果生成结果对象"""
    if return_code == 0:
        if is_fake_success and error_type is not None:
            return error_type
        return Result7zip.Success(password)

    if return_code == 2:
        if error_type is not None:
            return error_type
        return Result7zip.UnknownError(output)

    result = _get_result_by_return_code(return_code)
    if result is not None:
        return result
    return Result7zip.UnknownError('未知错误')


def process_7zip_x(_7zip_path, file, password, cover_model, output_folder, filter_rule=None):
    """解压指定文件，并实时发送解压进度"""
    queue_sender = function_queue.get_sender()
    command = _build_extract_command(_7zip_path, file, password, cover_model, output_folder, filter_rule)

    print('调用7zip（Popen）：' + command)
    process = subprocess.Popen(command,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               creationflags=subprocess.CREATE_NO_WINDOW,
                               text=True,
                               shell=True)

    global _process_running
    _process_running = process

    error_type, is_fake_success, last_output = _read_extract_output(process, queue_sender)

    delete_cmd_pw_file()
    print('识别的错误类型', error_type)
    return_code = process.poll()
    return _get_extract_result(return_code, error_type, last_output, password, is_fake_success)


def get_temp_dirpath(dirpath):
    """获取根据传入路径计算的临时文件夹路径"""
    return os.path.normpath(os.path.join(dirpath, TEMP_EXTRACT_FOLDER))


def progress_7zip_x_with_temp_folder(_7zip_path, file, password, cover_model, output_folder, filter_rule=None):
    """解压指定文件到临时文件夹，并实时发送解压进度"""
    extract_dirpath_temp = get_temp_dirpath(output_folder)
    return process_7zip_x(_7zip_path, file, password, cover_model, extract_dirpath_temp, filter_rule)


def _find_first_line_index(lines, prefix):
    """查找第一行以指定文本开头的行号"""
    for index, line in enumerate(lines):
        if line.startswith(prefix):
            return index
    return None


def _find_last_line_index(lines, prefix):
    """查找最后一行以指定文本开头的行号"""
    for index in range(len(lines) - 1, -1, -1):
        if lines[index].startswith(prefix):
            return index
    return None


def _read_process_stdout_get_files(process):
    """从run结果的stdout中提取文件类型和内部文件路径"""
    files_dict: dict = {'filetype': None, 'paths': None}
    stdout = process.stdout
    if not stdout:
        return files_dict

    lines = stdout.splitlines()

    type_index = _find_first_line_index(lines, 'Type = ')
    if type_index is not None:
        files_dict['filetype'] = lines[type_index][len('Type = '):]

    start_index = _find_last_line_index(lines, '   Date')
    end_index = _find_last_line_index(lines, '----------')
    if start_index is None or end_index is None or end_index <= start_index:
        return files_dict

    name_index = lines[start_index].find('Name')
    if name_index < 0:
        return files_dict

    paths = []
    for line in lines[start_index + 2:end_index]:
        if 'D....' not in line:
            paths.append(line[name_index:])
    files_dict['paths'] = paths

    return files_dict


def _run_7zip_list(archive_path):
    """使用l命令获取压缩包列表信息"""
    command = [get_7zip_path(), 'l', archive_path, '-p' + FAKE_PASSWORD]
    return subprocess.run(command,
                          stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE,
                          creationflags=subprocess.CREATE_NO_WINDOW,
                          text=True,
                          universal_newlines=True)


def _find_list_boundaries(lines):
    """查找压缩包列表信息中表头和表尾的位置"""
    title_index = None
    end_index = None

    for index, line in enumerate(lines):
        if line.startswith('--------'):
            title_index = index - 1
            break

    for index in range(len(lines) - 1, -1, -1):
        if lines[index].startswith('--------'):
            end_index = index + 1
            break

    return title_index, end_index


def _get_list_columns(line):
    """根据分隔线计算各列的起止位置"""
    columns = []
    start = 0

    for _ in range(4):
        end = line.find(' -', start)
        if end < 0:
            return None
        columns.append((start, end))
        start = end + 1

    columns.append((start, start + 200))
    return columns


def _parse_file_lines(lines, columns):
    """解析压缩包列表中的文件信息"""
    date_range = columns[0]
    attr_range = columns[1]
    size_range = columns[2]
    compressed_range = columns[3]
    name_range = columns[4]

    infos = []
    for line in lines:
        data = line[date_range[0]:date_range[1]].strip()
        attr = line[attr_range[0]:attr_range[1]].strip()
        size_text = line[size_range[0]:size_range[1]].strip()
        compressed_text = line[compressed_range[0]:compressed_range[1]].strip()
        name = line[name_range[0]:name_range[1]].strip()

        if not size_text.isdigit() or not compressed_text.isdigit():
            continue

        info = {
            'data': data,
            'attr': attr,
            'size': int(size_text),
            'compressed': int(compressed_text),
            'name': name
        }
        infos.append(info)

    return infos


def get_smallest_file_in_archive(archive_path):
    """获取压缩文件中最小的文件内部路径"""
    print('提取压缩文件内部文件路径')
    result = _run_7zip_list(archive_path)

    if '--------' not in result.stdout:
        return None

    print(result.stdout)
    lines = result.stdout.split('\n')
    title_index, end_index = _find_list_boundaries(lines)
    if title_index is None or title_index < 0:
        return None
    if end_index is None or end_index <= title_index + 1:
        return None

    lines_info = lines[title_index:end_index]
    columns = _get_list_columns(lines_info[1])
    if columns is None:
        return None

    infos = _parse_file_lines(lines_info, columns)

    smallest_file = ''
    smallest_size = None
    for info in infos:
        if info['attr'] == 'D....':
            continue
        if smallest_size is None or info['size'] < smallest_size:
            smallest_file = info['name']
            smallest_size = info['size']

    return smallest_file
