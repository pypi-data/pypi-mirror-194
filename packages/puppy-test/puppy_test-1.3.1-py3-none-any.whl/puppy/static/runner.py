import os
import sys
import time
import unittest

import puppy
from puppy.core import HTMLTestRunner, ResourcePool, config
from puppy.core.useful.res import res_record

__version__ = "1.3.1"
# 切勿修改上述属性，否则可能导致脚本异常！！！
puppy.check_version(__version__)
if __name__ == '__main__':
    # 开始测试
    config.start_test()
    # 启用资源管理线程
    ResourcePool().start()
    param = sys.argv
    if len(param) == 2:
        if param[1] == "allCases":
            config.all_cases()
        else:
            config.set_config("cases", param[1])
    now = time.strftime("%Y-%m-%d-%H-%M-%S")
    # 按脚本执行时间创建对应文件夹
    report_dir = os.path.join(config.get_config("report_path"), now)
    os.makedirs(report_dir)
    # 在对应的文件夹下生成测试报告
    file_name = os.path.join(report_dir, "{}_{}.html".format(now, config.get_config("report_name")))
    with open(file_name, 'wb') as fp:
        suit = unittest.TestSuite()
        for case in config.cases:
            suit.addTest(unittest.TestLoader().discover(config.get_config("cases_path"), pattern=case))
        runner = HTMLTestRunner.HTMLTestRunner(
            stream=fp,
            title=config.get_config("report_name"),
            description=config.get_config("report_name"))
        runner.run(suit)
    print("\n\n${报告路径:%s}" % file_name)
    print("\n\n${结果路径:%s}" % (res_record.file_path))
    # 执行结束
    config.end_test()
