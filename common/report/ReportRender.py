import os
import re
import time
import shutil
from jinja2 import Template
from pathlib import Path

from DataLog import DataLog
from common.run import RunEnv

class ReportRender(object):
    '''汇总报告'''

    def __init__(self) -> None:
        self.time = "%.3f" % (time.time() - time.time())
        self.dataLog = None
        self.testcaseList = []
        self.tasks = []
        self.loadDataLog()

    def loadDataLog(self):
        '''加载日志数据'''
        path = '%s/reports'%os.getcwd()
        #加载日志
        for fileName in os.listdir(path):
            if re.search(".log$",fileName):
                self.dataLog = DataLog("%s/%s"%(path,fileName))
                self.dataLog.loadLog()
        count= 0
        for testcase in self.dataLog.getTestCases():
            #记录用例
            resultPrefix = "F:" if len(testcase.getErrorInfo())>0 else "P:"
            self.testcaseList.append("%s%s"%(resultPrefix,testcase.getName()))
            #加载设备信息
            desiredCaps = RunEnv.getDeviceDesiredCaps(testcase.getUdid())
            platform_name = 'Android' if "platformName" not in desiredCaps else desiredCaps["platformName"]
            desiredCaps.update(RunEnv.getDesiredCaps(platform_name))
            #生成测试用例数据
            task = {
                "is_success": False if len(testcase.getErrorInfo())>0 else True,
                "report_path": "%s/reports/logs/%02d/log.html"%(os.getcwd(),count),
                "testcase":{
                    "name": testcase.getName()
                },
                "device":{
                    "udid": testcase.getUdid(),
                    "brand": 'Instrumentation/Uiautomator' if platform_name=="Android" else "Uiautomation",
                    "model": desiredCaps["deviceName"],
                    "platform": platform_name,
                    "version": desiredCaps["platformVersion"]
                }
            }
            self.tasks.append(task)
            count+=1

    def getStartTime(self)->str:
        '''开始时间'''
        timeStamp = float(self.dataLog.getTestCases()[0].getStartTime())+8*60*60#手动修正时区
        return time.strftime("%Y-%m-%d %H:%M:%S",time.gmtime(timeStamp))

    def getConsumeTime(self)->str:
        '''耗时'''
        nowTime = time.time()
        timeStamp = nowTime-float(self.dataLog.getTestCases()[0].getStartTime())
        return time.strftime("%H:%M:%S",time.gmtime(timeStamp))

    def successCount(self) -> int:
        '''成功的测试用例数'''
        successCount = 0
        for testcase in self.testcaseList:
            if re.search("^P:",testcase):
                successCount+=1
        return successCount

    def totalCount(self) -> int:
        '''总测试用例数'''
        nameList = []
        for testcase in self.testcaseList:
            if re.search("^P:",testcase):
                nameList.append(testcase[2:])
        for testcase in self.testcaseList:
            if re.search("^F:",testcase) and testcase[2:] not in nameList:
                nameList.append(testcase[2:])
        totalCount = len(nameList)
        return totalCount

    def render_html(self, html_file_path: Path, projectName:str) -> None:
        '''生成对应报告'''
        with open('common/report/template/summary_report_template.html') as file:
            data = {
                "start_all": self.getStartTime(),
                "time": self.getConsumeTime(),
                "success_count": self.successCount(),
                "total_count": self.totalCount(),
                "tasks": self.tasks
            }
            html = Template(file.read()).render(data=data)
        with open("%s/report.html"%html_file_path, "w", encoding = "utf-8") as f:
            f.write(html)
        #生成每一测试用例的具体报告
        with open('common/report/template/case_report_template.html') as file:
            log = file.read()
        count=0
        for testcase in self.dataLog.getTestCases():
            caseData ={
                "data":{
                    "steps":[],
                    "test_result": "true" if len(testcase.getErrorInfo())>0 else "false",
                    "run_end": testcase.getEndTime(),
                    "run_start": testcase.getStartTime()
                },
                "customData":{
                    "title": projectName,
                    "info_title": testcase.getName(),
                    "status": 0 if len(testcase.getErrorInfo())>0 else 1,
                    "author": "lztest",
                    "python_file": "None",
                    "python_file_name":"None",
                    "steps": len(testcase.getTeststeps())
                }
            }
            for teststep in testcase.getTeststeps():
                step = {
                    "title": teststep.getControl(),
                    "time": teststep.getStartTime(),
                    "screen": {
                        "src": "../../screenshots/%s"%teststep.getScreenShot()
                    },
                    "code":{
                        "name": teststep.getControl(),
                        "args": [
                            {
                                "key": "Control Info",
                                "value":{
                                    "type": "None" if teststep.getType()==None else teststep.getType(),
                                    "value": "None" if teststep.getValue()==None else teststep.getValue(),
                                    "extra": "None" if teststep.getExtra()==None else str(teststep.getExtra())
                                }
                            }
                        ]
                    },
                    "traceback": 1
                }
                caseData["data"]["steps"].append(step)
            #添加报错信息
            if len(testcase.getTeststeps())>0:
                if len(testcase.getErrorInfo())>0:
                    caseData["data"]["steps"][-1]["traceback"]=0
                    caseData["data"]["steps"][-1]["code"]["args"].append({"key":"Error Info","value":testcase.getErrorInfo()})
            elif len(testcase.getErrorInfo())>0: #没有步骤时存在报错信息
                step = {
                    "title": "运行脚本",
                    "time": testcase.getStartTime(),
                    "code":{"name": "运行脚本","args":[{"key":"Error Info","value":testcase.getErrorInfo()}]},
                    "traceback": 0
                }
                caseData["data"]["steps"].append(step)
            folder,count = "%s/logs/%02d"%(html_file_path,count), count+1
            os.makedirs(folder,exist_ok=True)
            html = Template(log).render(data=caseData) #输入log.html
            with open("%s/log.html"%folder, "w", encoding = "utf-8") as f:
                f.write(html)