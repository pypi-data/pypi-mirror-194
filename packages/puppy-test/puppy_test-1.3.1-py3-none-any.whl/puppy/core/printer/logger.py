import io
import logging
import os
from logging.handlers import TimedRotatingFileHandler
from ..useful.cfg import config


class LoggerManager():
    __instance = None
    __ch_handler_formatter = '%(message)s   (%(levelname)s)'
    __file_handler_formatter = '[%(asctime)s-%(levelname)s]%(message)s'

    @classmethod
    def __new__(cls, *args, **kwargs):
        if not getattr(cls, "_LoggerManager__instance"):
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self):
        if hasattr(self, "_LoggerManager__ch"):
            return
        # 创建logger，全局唯一
        self.__logger = logging.getLogger()
        # 默认日志登记最低
        self.__logger.setLevel(logging.NOTSET)
        # 创建控制台日志记录handler
        self.__ch = LoggerManager.create_console_handler()
        # 创建文件handler
        self.__fh = LoggerManager.create_file_handler()
        # 将handler加入
        self.add_handler("console")
        self.add_handler("file")

    @staticmethod
    def __get_useful_log_file_path():
        # 文件日志输出
        log_path = config.get_config("file_log_path")
        # 如果日志目录不存在，创建目录
        if not os.path.exists(log_path):
            os.makedirs(log_path)
        # 拼接日志文件全路径
        log_file_path = os.path.join(log_path, "log.txt")
        index = 1
        while not LoggerManager.__is_writeable(log_file_path):
            log_file_path = os.path.join(log_path, "log_{}.txt".format(index))
            index += 1
        return log_file_path

    @staticmethod
    def __is_writeable(path):
        try:
            if not os.path.exists(path):
                return True
            with open(path,"a") as f:
                f.write("")
            return True
        except io.UnsupportedOperation:
            return False

    @staticmethod
    def create_console_handler():
        # console log 控制台输出控制
        ch = logging.StreamHandler()
        ch.setLevel(LoggerManager.get_log_level(config.get_config("console_log_level")))
        ch.setFormatter(logging.Formatter(LoggerManager.__ch_handler_formatter))
        return ch

    @staticmethod
    def create_file_handler():
        log_file_path=LoggerManager.__get_useful_log_file_path()
        # 创建一个handler
        fh = TimedRotatingFileHandler(log_file_path, "midnight", backupCount=15, encoding="utf-8")
        # 设置日志输出等级
        fh.setLevel(LoggerManager.get_log_level(config.get_config("file_log_level")))
        # 定义输出格式
        fh.setFormatter(logging.Formatter(LoggerManager.__file_handler_formatter))
        return fh

    @staticmethod
    def get_log_level(level):
        if level == "notset":
            return logging.NOTSET
        elif level == "debug":
            return logging.DEBUG
        elif level == "info":
            return logging.INFO
        elif level == "warning":
            return logging.WARNING
        elif level == "error":
            return logging.ERROR
        else:
            raise Exception("配置错误，日志等级不能是{}".format(level))

    def add_handler(self, handler_type):
        if handler_type == "console":
            self.__logger.addHandler(self.__ch)
        elif handler_type == "file":
            self.__logger.addHandler(self.__fh)
        else:
            raise Exception("没有这个类型的日志handler:{}".format(handler_type))

    def remove_handler(self, handler_type):
        if handler_type == "console":
            self.__logger.removeHandler(self.__ch)
        elif handler_type == "file":
            self.__logger.removeHandler(self.__fh)
        else:
            raise Exception("没有这个类型的日志handler:{}".format(handler_type))

    def change_log_lever(self, level, handler_type="console"):
        if handler_type == "console":
            self.__ch.setLevel(LoggerManager.get_log_level(level))
        elif handler_type == "file":
            self.__fh.setLevel(LoggerManager.get_log_level(level))
        else:
            raise Exception("没有这个类型的日志handler:{}".format(handler_type))

    @property
    def logger(self):
        return self.__logger
