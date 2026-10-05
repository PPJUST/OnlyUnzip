from typing import Union

_FAKE_PASSWORD = 'FAKEPASSWORD'


class ModelArchive:
    """???????,??/??"""

    class Extract:
        """??"""
        value = 'extract'

    class Test:
        """??"""
        value = 'test'


class ModelPreFilter:
    """???????,??/???/???"""

    class Default:
        """??"""
        value = 'default'

    class BlackList:
        """???"""
        value = 'blacklist'

    class WhiteList:
        """???"""
        value = 'whitelist'


class ModelExtract:
    """????,????/????????/????"""

    class Smart:
        """????"""
        value = 'smart'

    class SameFolder:
        """????????"""
        value = 'same_folder'

    class Direct:
        """????"""
        value = 'direct'


class ModelCoverFile:
    """??????,??/??/??????/??????"""

    class Skip:
        """??"""
        text = '??????'
        value = 'skip'
        switch = '-aos'

    class Overwrite:
        """??"""
        text = '??????'
        value = 'overwrite'
        switch = '-aoa'

    class RenameNew:
        """??????"""
        text = '??????'
        value = 'rename_new'
        switch = '-aou'

    class RenameOld:
        """??????"""
        text = '??????'
        value = 'rename_old'
        switch = '-aot'


class ModelBreakFolder:
    """????????"""

    class MoveBottom:
        """????????????????????(?????????)"""
        text = '???????'
        value = 'move_bottom'

    class MoveToTop:
        """????????????????????????(????????,???????????)"""
        text = '???????'
        value = 'move_to_top'

    class MoveFiles:
        """?????????????(?????????)"""
        text = '?????'
        value = 'move_files'


class ArchiveRole:
    """?????,?????/?????(????)/?????(??????)"""

    class Normal:
        """?????"""

    class VolumeFirst:
        """?????(????)"""

    class VolumeMember:
        """?????(??????)"""


class Model7zip:
    """7zip????,l/t/x"""

    class L:
        """l,????"""
        value = 'l'

    class T:
        """t,????"""
        value = 't'

    class X:
        """x,????"""
        value = 'x'


class Result7zip:
    """zip????"""

    class Success:
        """??"""
        return_code = 0
        return_text = '??'  # success
        _7zip_return = 'No error'
        color = [0, 0, 0]
        result_state = '??'

        def __init__(self, password: str = None):
            if not password or password == _FAKE_PASSWORD:
                password = '???'
            self.password = password

    class Skip:
        """??"""
        return_code = None
        return_text = '??'  # skip
        _7zip_return = 'Skip'
        color = [255, 215, 0]
        result_state = '??'

    class Warning:
        """?????"""
        return_code = 1
        return_text = '?????'  # file occupied???????????
        _7zip_return = 'Warning (Non fatal error(s)).'
        color = [128, 0, 0]
        result_state = '??'

    class WrongPassword:
        """????"""
        return_code = 2
        return_text = '?????'  # wrong password
        _7zip_return = 'Fatal error'
        color = [178, 34, 34]
        result_state = '??'

    class MissingVolume:
        """?????"""
        return_code = 2
        return_text = '????'  # missing volume
        _7zip_return = 'Fatal error'
        color = [205, 92, 92]
        result_state = '??'

    class WrongFiletype:
        """???????(??????)"""
        return_code = 2
        return_text = '???????'  # wrong filetype
        _7zip_return = 'Fatal error'
        color = [255, 99, 71]
        result_state = '??'

    class UnknownError:
        """????"""
        return_code = 2
        return_text = '????'  # unknown error
        _7zip_return = 'Fatal error'
        color = [220, 20, 60]
        result_state = '??'

        def __init__(self, error_text: str):
            self.error_text = error_text

    class ErrorCommand:
        """7zip?????"""
        return_code = 7
        return_text = '??????'  # command line error
        _7zip_return = 'Command line error'
        color = [240, 128, 128]
        result_state = '??'

    class NotEnoughMemory:
        """?????????"""
        return_code = 8
        return_text = '??????'  # Not enough memory
        _7zip_return = 'Not enough memory for operation'
        color = [250, 128, 114]
        result_state = '??'

    class UserStopped:
        """??????"""
        return_code = 255
        return_text = '??????'  # user stopped
        _7zip_return = 'User stopped the process_7zip'
        color = [255, 160, 122]
        result_state = '??'


class Position:
    """??"""

    class Left:
        """??"""
        text = '???'

    class Right:
        """??"""
        text = '???'


TYPES_MODEL_ARCHIVE = Union[ModelArchive.Extract, ModelArchive.Test]

TYPES_MODEL_PRE_FILTER = Union[
    ModelPreFilter.Default, ModelPreFilter.BlackList, ModelPreFilter.WhiteList]

TYPES_MODEL_EXTRACT = Union[ModelExtract.Smart, ModelExtract.SameFolder, ModelExtract.Direct]

TYPES_MODEL_COVER_FILE = Union[ModelCoverFile.Skip, ModelCoverFile.Overwrite,
ModelCoverFile.RenameNew, ModelCoverFile.RenameOld]

TYPES_MODEL_BREAK_FOLDER = Union[ModelBreakFolder.MoveBottom, ModelBreakFolder.MoveToTop, ModelBreakFolder.MoveFiles]

TYPES_ARCHIVE_ROLE = Union[ArchiveRole.Normal, ArchiveRole.VolumeFirst, ArchiveRole.VolumeMember]

TYPES_MODEL_7ZIP = Union[Model7zip.L, Model7zip.T, Model7zip.X]

TYPES_RESULT_7ZIP = Union[Result7zip.Success, Result7zip.Skip,
Result7zip.Warning, Result7zip.WrongPassword,
Result7zip.MissingVolume, Result7zip.WrongFiletype,
Result7zip.UnknownError, Result7zip.ErrorCommand,
Result7zip.NotEnoughMemory, Result7zip.UserStopped]

TYPES_POSITION = Union[Position.Left, Position.Right]

CLASS_RESULT_7ZIP = [Result7zip.Success, Result7zip.Skip,
                     Result7zip.Warning, Result7zip.WrongPassword,
                     Result7zip.MissingVolume, Result7zip.WrongFiletype,
                     Result7zip.UnknownError, Result7zip.ErrorCommand,
                     Result7zip.NotEnoughMemory, Result7zip.UserStopped]

RESULT_STATE_ALL = '??'
RESULT_STATE_CACHE = '??'
RESULT_STATES = [RESULT_STATE_ALL, Result7zip.Success.result_state, Result7zip.Warning.result_state,
                 Result7zip.Skip.result_state, RESULT_STATE_CACHE]
