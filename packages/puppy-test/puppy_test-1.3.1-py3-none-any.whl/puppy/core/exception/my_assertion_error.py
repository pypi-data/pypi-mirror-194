from ..useful.track import xml_track
from ..function.beautify.fold import Fold


class MyAssertionError(object):

    @staticmethod
    def raise_error(msg):
        file_path, row = xml_track.current_path_row()
        raise TAssertionError(msg,file_path,row)


class TAssertionError(AssertionError):

    def __init__(self, msg, file_path, row):
        self.__file_path, self.__row = file_path, row
        self.__msg = msg

    @property
    def msg(self):
        return self.__msg

    def __str__(self):
        msg = '''\n  File "{}", line {}\n    raise\nAssertionError:{}'''.format(self.__file_path, self.__row,
                                                                                self.__msg)
        return Fold.fold_text(msg)
