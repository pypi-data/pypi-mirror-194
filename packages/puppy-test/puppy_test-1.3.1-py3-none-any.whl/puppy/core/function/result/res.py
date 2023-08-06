import json
import os

from ...useful.cfg import config


class ResRecord(object):

    def __init_record(self):
        if not hasattr(self, "_ResRecord__test_res_data"):
            # 创建存储文件
            # 文件日志目录
            log_path = config.get_config("file_log_path")
            # 如果日志目录不存在，创建目录
            if not os.path.exists(log_path):
                os.makedirs(log_path)
            # 拼接测试结果全路径
            self.__test_res_file_path = os.path.join(log_path, "test_res.txt")
            if os.path.exists(self.__test_res_file_path):
                os.remove(self.__test_res_file_path)
        # 数据存储
        self.__test_res_data = dict()

    @property
    def file_path(self):
        if not hasattr(self,"_ResRecord__test_res_file_path"):
            return None
        return self.__test_res_file_path

    @staticmethod
    def __need_save():
        return not config.get_config("single_testing", bool)

    def __save_to_file(self):
        with open(self.__test_res_file_path, "a", encoding="utf-8") as file:
            json.dump(self.__test_res_data, file, ensure_ascii=False)
            file.write("\n")

    def start_single_test(self):
        if self.__need_save():
            self.__init_record()

    def end_single_test(self):
        if self.__need_save():
            self.__save_to_file()

    def place_data(self, key, data, _type="case",is_new_interface=False):
        """
        #_type:case interfaces asserts
        """
        if data is None:
            return
        if self.__need_save():
            if _type in ["interfaces", "asserts"]:
                if self.__test_res_data.get("interfaces") is None:
                    self.__test_res_data["interfaces"] = list()
                interface_list: list = self.__test_res_data.get("interfaces")
                if len(interface_list) == 0 or is_new_interface:
                    interface_list.append(dict())
                interface_data: dict = interface_list[-1]
                if _type == "interfaces":
                    interface_data[key] = data
                else:
                    if interface_data.get("asserts") is None:
                        interface_data["asserts"] = list()
                    interface_data.get("asserts").append(data)
            else:
                self.__test_res_data[key] = data

    def read(self):
        path = self.__test_res_file_path
        with open(path, "r", encoding="utf-8") as f:
            for line in f.readlines():
                data = json.loads(line)
                print(data)
