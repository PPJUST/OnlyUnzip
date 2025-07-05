from typing import Union


def read_password_from_filename(filename: str):
    """从文件名中读取可能包含的密码
    :param filename: str，不含后缀的文件名"""
    pws = set()
    # 密码类型 - 整个文件名
    pws.add(filename)
    # 密码类型 - 以空格为分隔符，拆分文件名
    split = filename.split(' ')
    pws.update(split)
    # 密码类型 - 拆分的文件名字段，剔除标识符#
    pws.update(_deal_split_set(split, left_edge_str='#'))
    # 密码类型 - 拆分的文件名字段，剔除标识符@
    pws.update(_deal_split_set(split, left_edge_str='@'))
    # 密码类型 - 拆分的文件名字段，剔除标识符【】
    pws.update(_deal_split_set(split, left_edge_str='【', right_edge_str='】'))
    # 密码类型 - 拆分的文件名字段，剔除标识符[]
    pws.update(_deal_split_set(split, left_edge_str='[', right_edge_str=']'))
    # 密码类型 - 拆分的文件名字段，剔除标识符()
    pws.update(_deal_split_set(split, left_edge_str='(', right_edge_str=')'))
    # 密码类型 - 拆分的文件名字段，剔除文本"密码"
    pws.update(_deal_split_set(split, left_edge_str='密码'))
    # 密码类型 - 拆分的文件名字段，剔除文本"密码："
    pws.update(_deal_split_set(split, left_edge_str='密码：'))
    # 密码类型 - 拆分的文件名字段，剔除文本"解压"
    pws.update(_deal_split_set(split, left_edge_str='解压'))
    # 密码类型 - 拆分的文件名字段，剔除文本"解压："
    pws.update(_deal_split_set(split, left_edge_str='解压：'))
    # 密码类型 - 拆分的文件名字段，剔除文本"解压码"
    pws.update(_deal_split_set(split, left_edge_str='解压码'))
    # 密码类型 - 拆分的文件名字段，剔除文本"解压码："
    pws.update(_deal_split_set(split, left_edge_str='解压码：'))
    # 密码类型 - 拆分的文件名字段，剔除文本"解压密码"
    pws.update(_deal_split_set(split, left_edge_str='解压密码'))
    # 密码类型 - 拆分的文件名字段，剔除文本"解压密码："
    pws.update(_deal_split_set(split, left_edge_str='解压密码：'))
    # 密码类型 - 拆分的文件名字段，剔除文本"pw"
    pws.update(_deal_split_set(split, left_edge_str='pw'))
    # 密码类型 - 拆分的文件名字段，剔除文本"pw："
    pws.update(_deal_split_set(split, left_edge_str='pw：'))

    return pws


def _deal_split_set(splits: Union[list, set], left_edge_str: str = '', right_edge_str: str = ''):
    """处理拆分的字符段"""
    f_splits = set()  # 处理结果
    for i in splits:
        i: str
        if len(i) <= len(left_edge_str) + len(right_edge_str):  # 大于左右两端字符数才进行处理
            continue

        if left_edge_str:
            if i.startswith(left_edge_str):
                i = i[len(left_edge_str):]
            else:
                continue

        if right_edge_str:
            if i.endswith(right_edge_str):
                i = i[:-len(right_edge_str)]
            else:
                continue

        f_splits.add(i)

    return f_splits
