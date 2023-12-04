import unittest
import os
from common.hrun import HrunUtils
from common.run import RunUtils
from common.report import Report

def threadRunTest(reportPath,suite):
    with open(reportPath,"a") as report:
        runner = unittest.TextTestRunner(stream=report,verbosity=2)
        runner.run(suite)

if __name__ == '__main__':
    RunUtils.cleanReports() #清空报告
    suite = unittest.TestSuite()#加载所有用例
    suite.addTests(unittest.TestLoader().discover(start_dir=r'%s/testcases/instance/skip'%os.getcwd(),pattern='Test*.py').__iter__())
    print(suite.countTestCases())
    reportPath = Report.initLogger() #初始化日志并获得日志文件路径
    with open(reportPath,"a") as report:
        runner = unittest.TextTestRunner(stream=report,verbosity=2)
        runner.run(suite)