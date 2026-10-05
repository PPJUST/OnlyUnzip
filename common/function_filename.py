import re


def read_password_from_filename(filetitle: str) -> set:
    """??????????????
    :param filetitle: str,????????"""
    pws = set()
    # ???????(?????)
    splits = filetitle.split(' ')
    pws.add(splits[0])
    pws.add(splits[-1])

    # ??"#xxx "??
    pattern = r'#(.*?)\s'
    matches = re.findall(pattern, filetitle)
    pws.update(matches)

    # ??"@xxx "??
    pattern = r'@(.*?)\s'
    matches = re.findall(pattern, filetitle)
    pws.update(matches)

    # ??"?xxx?"??
    pattern = r'?(.*?)?'
    matches = re.findall(pattern, filetitle)
    pws.update(matches)

    # ??"[xxx]"??
    pattern = r'\[(.*?)\]'
    matches = re.findall(pattern, filetitle)
    pws.update(matches)

    # ??"(xxx)"??
    pattern = r'\((.*?)\)'
    matches = re.findall(pattern, filetitle)
    pws.update(matches)

    # ??"??xxx "?"??:xxx "?"??:xxx "??
    pattern = r'??[::]?\s*(\S+)\s'
    matches = re.findall(pattern, filetitle)
    pws.update(matches)

    # ??"???xxx "?"???:xxx "?"???:xxx "??
    pattern = r'???[::]?\s*(\S+)\s'
    matches = re.findall(pattern, filetitle)
    pws.update(matches)

    # ??"????xxx "?"????:xxx "?"????:xxx "??
    pattern = r'????[::]?\s*(\S+)\s'
    matches = re.findall(pattern, filetitle)
    pws.update(matches)

    # ??"pwxxx "?"pw:xxx "?"pw:xxx "??
    pattern = r'pw[::]?\s*(\S+)\s'
    matches = re.findall(pattern, filetitle)
    pws.update(matches)

    # ??"PWxxx "?"PW:xxx "?"PW:xxx "??
    pattern = r'PW[::]?\s*(\S+)\s'
    matches = re.findall(pattern, filetitle)
    pws.update(matches)

    return pws
