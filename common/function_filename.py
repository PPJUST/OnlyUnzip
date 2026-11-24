import re

# 从文件名中提取密码的规则，按原有顺序排列
PASSWORD_PATTERNS: list[str] = [
    r'#(.*?)\s',  # #xxx 格式
    r'@(.*?)\s',  # @xxx 格式
    r'【(.*?)】',  # 【xxx】格式
    r'\[(.*?)\]',  # [xxx] 格式
    r'\((.*?)\)',  # (xxx) 格式
    r'密码[:：]?\s*(\S+)\s',  # 密码xxx、密码:xxx、密码：xxx 格式
    r'解压码[:：]?\s*(\S+)\s',  # 解压码xxx、解压码:xxx、解压码：xxx 格式
    r'解压密码[:：]?\s*(\S+)\s',  # 解压密码xxx、解压密码:xxx、解压密码：xxx 格式
    r'pw[:：]?\s*(\S+)\s',  # pwxxx、pw:xxx、pw：xxx 格式
    r'PW[:：]?\s*(\S+)\s',  # PWxxx、PW:xxx、PW：xxx 格式
]


def read_password_from_filename(filetitle: str) -> set[str]:
    """从文件名中读取可能包含的密码

    :param filetitle: str，不含后缀的文件名
    :return: 提取到的密码集合
    """
    pws: set[str] = set()

    # 提取以空格分隔的首尾文本
    parts = filetitle.split(' ')
    pws.add(parts[0])
    pws.add(parts[-1])

    # 按规则逐项提取
    for pattern in PASSWORD_PATTERNS:
        pws.update(re.findall(pattern, filetitle))

    return pws
