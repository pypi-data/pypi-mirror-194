from datetime import datetime
from ..useful.track import xml_track
from ..useful.cfg import config
from ..function.beautify.fold import Fold
from ..useful.log import logger

'''
名称	说明
levelno	打印日志级别的数值
levelname	打印日志级别名称
pathname	打印当前执行程序的路径，其实就是sys.argv[0]
filename	打印当前执行程序名
funcName	打印日志的当前函数
lineno	打印日志的当前行号
asctime	打印日志的记录时间
thread	打印线程ID
threadName	打印线程的名称
process	打印进程的ID
message	打印日志的信息
xmlFileName xml文件名称
xmlFilePath xml文件路径
xmlLine  xml文件行
xmlTag   xml标签
'''


class DebugPrinter(object):
    __format = config.get_config("debug_format")
    #     year month day hour minute second microsecond  filename filepath line tag msg timestamp
    # 格式化输出长度
    __format_str_length = config.get_config("format_str_length", int)

    @classmethod
    def __get_format_debug_log(cls, msg):
        """
        得到适合打印的文本
        :param msg:原始日志
        :return:
        """
        text = str(msg)
        if text is None:
            return "[None]"
        text = Fold.fold_text(text)
        if len(text) >= cls.__format_str_length != -1:
            text = "{}......".format(text[:cls.__format_str_length])
        _now = datetime.now()

        year = str(_now.year).zfill(4)
        month = str(_now.month).zfill(2)
        day = str(_now.day).zfill(2)
        hour = str(_now.hour).zfill(2)
        minute = str(_now.minute).zfill(2)
        second = str(_now.second).zfill(2)
        microsecond = str(_now.microsecond)
        timestamp = str(_now.timestamp())
        filename = xml_track.current_file_name()
        filepath = xml_track.current_file_path()
        line = xml_track.current_row()
        tag = xml_track.current_tag()
        msg = text
        log = cls.__format.format(year=year, month=month, day=day, hour=hour, minute=minute, second=second,
                                  microsecond=microsecond, filename=filename, filepath=filepath, line=line, tag=tag,
                                  msg=msg, timestamp=timestamp)
        # 把换行符转为一个空格
        return log

    @classmethod
    def debug(cls, msg):
        """
        debug日志
        :param msg:
        :return:
        """
        logger.debug(cls.__get_format_debug_log(msg))

    @classmethod
    def info(cls, msg):
        """
        debug日志
        :param msg:
        :return:
        """
        logger.info(cls.__get_format_debug_log(msg))

    @classmethod
    def warning(cls, msg):
        """
        debug日志
        :param msg:
        :return:
        """
        logger.warning(cls.__get_format_debug_log(msg))

    @classmethod
    def error(cls, msg):
        """
        debug日志
        :param msg:
        :return:
        """
        logger.error(cls.__get_format_debug_log(msg))
