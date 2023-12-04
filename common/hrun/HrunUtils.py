import logging
import os
from pathlib import Path
from httprunner.api import HttpRunner
import threading

class TestCaseThread(threading.Thread):

    def __init__(self,testcase_path):
        threading.Thread.__init__(self)
        self.testcase_path = testcase_path
        self.result=None

    def run(self):
        try:
            self.result = run(self.testcase_path)
        except Exception as e:
            logging.getLogger().info(str(e))

    def get_result(self):
        '''获取结果'''
        return self.result

def run(testcase_path: str)-> dict:
    '''
    方便airtest ide在xxx.air目录调用项目位于项目根目录的api测试脚本
    如果没有这个辅助函数，测试人员需要根据工作目录（位于项目根目录，或者xxx.air目录），
    分别处理，才能调用API测试脚本。
    '''
    try:
        previous_working_dir = os.getcwd()
        runner = HttpRunner(failfast=True)
        while not Path(testcase_path).exists():
            if Path('Pipfile').exists(): # 已经到达项目根目录，停止向上搜索，抛出文件不存在的异常
                raise FileNotFoundError(testcase_path)
            else:
                os.chdir('..')

        print('absolute path of testscase: ' + Path(testcase_path).absolute().as_posix())
        summary = runner.run(testcase_path)
        return summary["details"][0]["in_out"]["out"]
    except Exception as e:
        raise Exception(e)
    finally:
        os.chdir(previous_working_dir)

def run_until_success(testcase_path,check_param):
    '''
    运行API脚本并检查是否执行成功
    '''
    time = 5
    result = None
    #失败用例会重新执行(最多5次-time)
    #失败的情况：
    # 1、网络问题(conntect aborted)，result不为None但result[check_param]为None
    # 2、线程卡死(即不运行也无报错),result为None
    while time and ((result==None) or (check_param==None) or (check_param not in result) or (not result[check_param])):
        time-=1
        logging.getLogger().info('RunApiTestCase_%s:%s'%(5-time,testcase_path))
        #执行测试用例有时卡住(即无报错也不继续执行),未设置该进程的终止(只设置为守护进程)
        testcase_thread = TestCaseThread(testcase_path)
        testcase_thread.setDaemon(True)
        testcase_thread.start()
        testcase_thread.join(30) #理论上API脚本30秒已完成，超过30秒表示进程已卡住
        result = testcase_thread.get_result()
    assert result,'执行脚本并尝试五次均失败'
    logging.getLogger().info(str.format('RunApiSuccess:{}',str(result)))
    return result