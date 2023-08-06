# -*- encoding=utf-8 *-*
"""
    author: Li Junxian
    function: frame config class
"""
import os
import sys

import puppy
from ..express.express import Express
from .my_configparser import MyConfigParser
from ..utils.utils import Utils
from ...useful.track import xml_track
from ...exception.my_exception import MyException


class ConfigLoader(object):
    """
    项目的配置加载器，将一次性读取所有的配置
    """
    __env_type_number_dict = {
        "$global": 1,
        "$scene": 2,
        "$case": 3
    }

    def __init__(self):
        # 取到项目根目录
        self.__base_path = ConfigLoader.get_base_path()
        # puppy框架目录
        self.__puppy_path = puppy.__path__[0]
        # 用来存储读取的原始配置
        self.__config = {
            "cases_path": os.path.join(self.__base_path, 'test_case'),
            "test_data_path": os.path.join(self.__base_path, 'test_data'),
            "flow_path": os.path.join(self.__base_path, 'flow'),
            "report_path": os.path.join(self.__base_path, "report"),
            "api_file_path": os.path.join(self.__base_path, "interface"),
            "jar_file_path": os.path.join(self.__base_path, "file/jar"),
            "js_file_path": os.path.join(self.__base_path, "file/js"),
            "file_path": os.path.join(self.__base_path, "file"),
            "inner_function_file": os.path.join(self.__puppy_path, "core", "function", "express", "function.py"),
            "outer_function_file": os.path.join(self.__base_path, "file/func.py"),
            "package_for_selenium": os.path.join(self.__base_path, "seleniums"),
            "browser": "Chrome",
            "driver": "None",
            "base_path": self.__base_path,
            "project_path": self.__base_path,
            "puppy_path": self.__puppy_path,
            "format_str_length": "-1",
            "report_name": "API自动化测试报告",
            "cases": "test*.py",
            "http_connection_timeout": "50",
            "http_read_timeout": "50",
            "tcp_timeout": "60",
            "tcp_encoding": "utf-8",
            "max_number_non_select_sql": "10",
            "resource_thread_sleep_time": "1",
            "progress_thread_sleep_time": "1",
            "db_keep_connection_time": "30",
            "testing": "false",
            "single_testing": "true",
            "the_global_inspection": "false",
            "the_global_inspection_type": "auto",
            "beautify": "true",
            "fold_text": "false",
            "fold_text_when_more_than_lines": "5",
            "debug_format": "{year}-{month}-{day} {hour}:{minute}:{second}.{microsecond} {filename} - <{tag}> <{line}>: {msg}",
            "env": "config",
            "console_log_level": "info",  # notset|debug|info|warning|error|close
            "file_log_level": "notset",  # notset|debug|info|warning|error|close
            "file_log_path": os.path.join(self.__base_path, "log"),
            "length_for_expect": "1000"
        }
        # 用来存储读取的原始变量
        self.__vars = dict()
        # 环境堆栈
        self.__env_stack = list()
        # 环境是否切换标志
        self.__env_is_changed = False
        # 当前执行的模块
        self.__module = None
        # 当前执行的案例id
        self.__case_id = None
        # 当前执行的案例名称
        self.__case = None
        # 读取和计算文件内的配置及变量
        self.__load_config_from_file()

    def __load_config_from_file(self):
        """
        用来载入文件内的配置和变量
        """
        config_file = "{}/file/conf/config.cfg".format(self.__base_path)
        if not os.path.exists(config_file):
            return
        # 构造一个配置对象
        conf_loader = MyConfigParser()
        # 读取文件里的配置和变量
        if config_file:
            conf_loader.read(config_file, encoding='utf-8')
        sections = conf_loader.sections()
        for section in sections:
            options = conf_loader.options(section)
            section_dict = dict()
            for option in options:
                if section == "config" and option in self.__config.keys():
                    self.__config[option] = Express.calculate_in_config(conf_loader.get(section, option), self.__config)
                else:
                    section_dict[option] = Express.calculate_in_config(conf_loader.get(section, option), section_dict)
            self.__vars[section] = section_dict
        # 记录当前环境
        self.push_env(self.get_config("env"), "$global")

    @staticmethod
    def get_base_path():
        path = sys.path[0]
        cwd=os.getcwd()
        if path.endswith("test_case"):
            return os.path.dirname(path)
        elif path.endswith("puppy.exe"):
            sys.path.insert(0,cwd)
            return os.getcwd()
        return path

    @staticmethod
    def __process_config(name, cfg, _type):
        """处理配置"""
        if type(cfg) is not _type:
            if _type is bool:
                if cfg in ["True", "1", "true"]:
                    return True
                elif cfg in ["False", "0", "false"]:
                    return False
                else:
                    raise MyException(" {} 配置项配置不正确，只能是True或False，不能是 {}".format(name, cfg))
            elif _type is int:
                if Utils.is_number(cfg):
                    return int(cfg)
                else:
                    raise MyException(" {} 配置项不正确，只能是数字，不能是 {}".format(name, cfg))
            elif _type is float:
                if Utils.is_float(cfg):
                    return float(cfg)
                else:
                    raise MyException(" {} 配置项不正确，只能是数字，不能是 {}".format(name, cfg))
        return cfg

    def get_config(self, name, _type=str):
        """
        得到配置项，返回_type指定类型
        :param _type:
        :param name:
        :return: 如果配置不存在则返回None
        """
        if name not in self.__config.keys():
            raise MyException("配置不存在：{}".format(name))
        return self.__process_config(name, self.__config.get(name), _type)

    def have_config(self, name):
        """
        判断是否存在配置
        :param name:
        :return:
        """
        try:
            self.get_config(name)
            return True
        except:
            return False

    def set_config(self, name, value):
        """
        设置配置项，该配置项不会被写入文件。
        :param name:
        :param value:
        :return:
        """
        self.__config[name] = value

    def get_var(self, name):
        """
        得到变量，不存在则报错
        :param name:
        :return: 如果配置不存在则返回None
        """
        if name not in self.vars.keys():
            raise MyException("变量不存在：{}".format(name))
        return self.vars.get(name)

    def have_var(self, name):
        """
        判断是否存在该变量
        :param name:
        :return:
        """
        try:
            self.get_var(name)
            return True
        except:
            return False

    def all_cases(self):
        self.set_config("cases", "test*.py")

    def start_test(self):
        from ...useful.log import LoggerManager, logger
        logger.warning("自动化脚本测试开始！")
        self.set_config("fold_text", False)
        self.set_config("format_str_length", -1)
        self.set_config("testing", True)
        self.set_config("single_testing", False)
        self.set_config("the_global_inspection", True)
        self.set_config("console_log_level", "warning")
        LoggerManager().change_log_lever("warning")

    def end_test(self):
        from ...useful.log import logger
        logger.warning("自动化脚本测试结束！")
        self.set_config("testing", False)

    def set_module(self, module):
        self.__module = module

    def start_test_by_single_case(self, case_id, case_name, case_data):
        """单个用例测试开始"""
        from ...useful.res import res_record
        from ...useful.log import logger
        from ...printer.debug_printer_ import DebugPrinter
        self.__case_id = case_id
        self.__case = case_name
        xml_track.clear()
        xml_track.push_source_data(case_data, "case")
        if not self.get_config("single_testing", bool):
            logger.warning("执行案例：{} {}、{}".format(self.__module, case_id, case_name))
        DebugPrinter.info("执行案例：{}-{}".format(case_id, case_name))
        res_record.start_single_test()
        module_number, module_name, scene_number, scene_name = Utils.extract_module_and_scene(self.__module)
        res_record.place_data("module_number", module_number)
        res_record.place_data("module_name", module_name)
        res_record.place_data("scene_number", scene_number)
        res_record.place_data("scene_name", scene_name)
        res_record.place_data("case_number", case_id)
        res_record.place_data("case_name", case_name)

    def end_test_by_single_case(self):
        """单个用例测试结束"""
        from ...useful.res import res_record
        from ...printer.debug_printer_ import DebugPrinter
        self.pop_env("$case")
        DebugPrinter.info("案例执行结束：{}-{}".format(self.__case_id, self.__case))
        xml_track.pop()
        res_record.end_single_test()

    def push_env(self, env, env_type):
        """
        环境入栈，每次入栈时，将该环境和环境的类型组装成元组一起推入
        :param env_type: 类型- $global全局 $scene场景  $case案例
        :param env:环境
        :return:
        """
        env_type_number = self.__get_env_type_number(env_type)
        if env not in self.__vars.keys():
            raise MyException("{} 环境不存在".format(env))
        stack_env = None
        if len(self.__env_stack) > 0:
            stack_env = self.__env_stack[-1][0]
        if env != stack_env:
            self.__env_stack.append((env, env_type_number))
            self.__env_is_changed = True

    @classmethod
    def __get_env_type_number(cls, env_type):
        if env_type not in cls.__env_type_number_dict.keys():
            raise Exception(" {} 不是正确的环境类型！".format(env_type))
        return cls.__env_type_number_dict.get(env_type)

    def pop_env(self, env_type):
        """
        将栈顶推出到指定类型
        将栈顶及与栈顶同一类型的环境全部pop出
        :param env_type:
        :return:
        """
        env_type_number = self.__get_env_type_number(env_type)
        if len(self.__env_stack) == 0:
            raise Exception("环境不存在！")
        top_env = self.__env_stack[-1][0]
        while len(self.__env_stack) > 0 and self.__env_stack[-1][1] >= env_type_number:
            self.__env_stack.pop()
        if len(self.__env_stack) == 0:
            self.__env_is_changed = True
        elif self.__env_stack[-1][0] != top_env:
            self.__env_is_changed = True

    @property
    def env(self):
        if len(self.__env_stack) == 0:
            raise Exception("环境不存在！")
        return self.__env_stack[-1][0]

    @property
    def env_is_changed(self):
        """被调用用，该状态将变为False"""
        self.__env_is_changed = False
        return self.__env_is_changed

    @property
    def report_name(self):
        return self.get_config("report_name")

    @property
    def cases(self):
        cases = self.get_config("cases")
        cases_list = cases.split("|")
        return cases_list

    @property
    def configs(self):
        return self.__config

    @property
    def vars(self):
        '''
        返回当前环境变量指定的变量组
        '''
        return self.__vars.get(self.env)
