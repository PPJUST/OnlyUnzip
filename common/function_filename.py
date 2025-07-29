import re


def read_password_from_filename(filetitle: str) -> set:
    """从文件名中读取可能包含的密码
    :param filetitle: str，不含后缀的文件名"""
    pws = set()
    # 提取两端的文本（以空格为界）
    splits = filetitle.split(' ')
    pws.add(splits[0])
    pws.add(splits[-1])

    # 提取"#xxx "格式
    pattern = r'#(.*?)\s'
    matches = re.findall(pattern, filetitle)
    pws.update(matches)

    # 提取"@xxx "格式
    pattern = r'@(.*?)\s'
    matches = re.findall(pattern, filetitle)
    pws.update(matches)

    # 提取"【xxx】"格式
    pattern = r'【(.*?)】'
    matches = re.findall(pattern, filetitle)
    pws.update(matches)

    # 提取"[xxx]"格式
    pattern = r'\[(.*?)\]'
    matches = re.findall(pattern, filetitle)
    pws.update(matches)

    # 提取"(xxx)"格式
    pattern = r'\((.*?)\)'
    matches = re.findall(pattern, filetitle)
    pws.update(matches)

    # 提取"密码xxx "、"密码:xxx "、"密码：xxx "格式
    pattern = r'密码[:：]?\s*(\S+)\s'
    matches = re.findall(pattern, filetitle)
    pws.update(matches)

    # 提取"解压码xxx "、"解压码:xxx "、"解压码：xxx "格式
    pattern = r'解压码[:：]?\s*(\S+)\s'
    matches = re.findall(pattern, filetitle)
    pws.update(matches)

    # 提取"解压密码xxx "、"解压密码:xxx "、"解压密码：xxx "格式
    pattern = r'解压密码[:：]?\s*(\S+)\s'
    matches = re.findall(pattern, filetitle)
    pws.update(matches)

    # 提取"pwxxx "、"pw:xxx "、"pw：xxx "格式
    pattern = r'pw[:：]?\s*(\S+)\s'
    matches = re.findall(pattern, filetitle)
    pws.update(matches)

    # 提取"PWxxx "、"PW:xxx "、"PW：xxx "格式
    pattern = r'PW[:：]?\s*(\S+)\s'
    matches = re.findall(pattern, filetitle)
    pws.update(matches)

    return pws
