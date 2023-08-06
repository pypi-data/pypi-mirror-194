# -*- coding:utf-8 -*-
"""
    author: Li Junxian
    function:format print information
"""
from datetime import datetime

from .color import Color
from ..useful.cfg import config
from ..api.common.res_data import ResData
from ..function.beautify.beautify import Beautify
from ..function.beautify.fold import Fold
from ..function.utils.utils import Utils
from .debug_printer_ import DebugPrinter
from ..useful.res import res_record


class Printer(object):
    # 标题
    __color_of_title = Color.green_front
    # 默认
    __default = Color.default
    # 关键性
    __color_of_key = Color.purple
    __format_str_length = config.get_config("format_str_length", int)
    # 空白
    __blank_char = Utils.BLANK_CHAR
    # 中文空白
    __blank_char_by_cn = Utils.BLANK_CHAR_BY_CN

    @staticmethod
    def __to_good_str(string):
        string = str(string)
        string = Fold.fold_text(string)
        if len(string) >= Printer.__format_str_length != -1:
            string = "{}......".format(string[:Printer.__format_str_length])
        return string

    @staticmethod
    def print_request_info(protocol, desc, address, header, data, data_type, file=None, param=None, cookies=None,
                           auth=None):
        """
        格式化打印请求信息
        :param protocol: HTTP的GET或者POST，或者其他协议
        :param desc: 接口的描述
        :param address: 接口的地址
        :param header:请求头
        :param data: 请求体
        :param data_type: 请求体数据类型
        :param file: 文件接口发送的文件
        :param param: 请求参数
        :param cookies: cookie信息
        :param auth: 认证信息
        :return:
        """
        if config.get_config("beautify", bool):
            data = Beautify(data, data_type).beautify()
            if protocol in ['GET', 'POST']:
                header = Beautify(header, "key_value").beautify()
        res_record.place_data("req_data", str(data), "interfaces")
        res_record.place_data("req_header",str(header),"interfaces")
        print_info = ">>>>请求[{}]: {}\n".format(protocol, desc)
        req_time=datetime.now()
        print_info += "{}请求时间: {}\n".format(Printer.__blank_char * 4, req_time)
        res_record.place_data("req_time", str(req_time), "interfaces")
        print_info += "{}地{}址: {}\n".format(Printer.__blank_char * 4, Printer.__blank_char_by_cn * 2,
                                            Printer.__to_good_str(address))
        res_record.place_data("req_address",address,"interfaces")
        print_info += "{}请{}求头: {}\n".format(Printer.__blank_char * 4, Printer.__blank_char_by_cn,
                                             "无自定义请求头" if header is None else Printer.__to_good_str(header))
        if cookies is not None:
            print_info += "    Cookies: {}\n".format(Printer.__to_good_str(cookies))
            res_record.place_data("req_cookies",str(cookies),"interfaces")
        if auth is not None:
            print_info += "{}认{}证: {}\n".format(Printer.__blank_char * 4, Printer.__blank_char_by_cn * 2,
                                                Printer.__to_good_str(auth))
        if param is not None:
            print_info += "{}请求参数: {}\n".format(Printer.__blank_char * 4, Printer.__to_good_str(param))
            res_record.place_data("req_param",param,"interfaces")
        print_info += "{}请求数据: {}\n".format(Printer.__blank_char * 4,
                                            "无请求数据" if data is None else Printer.__to_good_str(data))
        if file is not None:
            print_info += "{}上传文件: {}\n".format(Printer.__blank_char * 4, Printer.__to_good_str(str(file)))
            res_record.place_data("req_file",str(file),"interfaces")
        print_info += "{}数据格式: {}".format(Printer.__blank_char * 4, data_type)
        res_record.place_data("req_data_type",data_type,"interfaces")
        DebugPrinter.debug(print_info)
        print(print_info)

    @staticmethod
    def print_response_info(protocol, res: ResData):
        """
        格式化打印响应信息
        :param res:
        :param protocol:
        :return:
        """
        code = res.code
        header = res.header
        _type = res.re_type
        if config.get_config("beautify", bool):
            data = Beautify(res.text, _type).beautify()
        else:
            data = res.text
        res_record.place_data("res_data",str(data),"interfaces")
        res_record.place_data("res_header",str(header),"interfaces")
        res_time=datetime.now()
        res_record.place_data("res_time",str(res_time),"interfaces")
        res_record.place_data("res_status",code,"interfaces")
        data = Printer.__to_good_str(data)
        print_info = "<<<<响应[{}]:\n".format(protocol)
        print_info += "{}响应时间: {}\n".format(Printer.__blank_char * 4,res_time )
        print_info += "{}状{}态: {}\n".format(Printer.__blank_char * 4, Printer.__blank_char_by_cn * 2, code)
        print_info += "{}响{}应头: {}\n".format(Printer.__blank_char * 4, Printer.__blank_char_by_cn, header)
        print_info += "{}响应数据: {}{}{}".format(Printer.__blank_char * 4, Printer.__color_of_title, data,
                                              Printer.__default)
        DebugPrinter.debug(print_info)
        print(print_info)

    @staticmethod
    def print_info(info):
        info = Printer.__to_good_str(info)
        print(info)

    @staticmethod
    def print_post_info(desc, value):
        var_type = type(value)
        value = Printer.__to_good_str(value)
        info = "[{}]后置处理器打印的值为：[{}{}{}]，值的类型为：{}".format(desc, Printer.__color_of_key, value, Printer.__default,
                                                         var_type.__name__)
        DebugPrinter.debug(info)
        print(info)

    @staticmethod
    def print_pre_info(desc, value):
        var_type = type(value)
        value = Printer.__to_good_str(value)
        info = "[{}]前置处理器打印的值为：[{}{}{}]，值的类型为：{}".format(desc, Printer.__color_of_key, value, Printer.__default,
                                                         var_type.__name__)
        DebugPrinter.debug(info)
        print(info)
