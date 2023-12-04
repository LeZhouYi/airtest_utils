import os
import re
from typing import List

class DataStep(object):
    '''测试用例步骤数据结构'''
    def __init__(self) -> None:
        self.startTime = None
        self.type = None
        self.value = None

    def setExtra(self,extra:str):
        self.extra = extra

    def setValue(self,value:str):
        self.value = value

    def setType(self,type:str):
        self.type = type

    def setControl(self,control:str):
        self.control = control

    def setStartTime(self,time:str):
        self.startTime = time

    def setScreenShot(self,screenshot:str):
        self.screenshot = screenshot

    def getScreenShot(self)->str:
        return self.screenshot

    def getStartTime(self)->str:
        return self.startTime

    def getControl(self)->str:
        return self.control

    def getType(self)->str:
        return self.type

    def getValue(self)->str:
        return self.value

    def getExtra(self)->str:
        return self.extra

class DataTest(object):
    '''测试用例数据结构'''
    def __init__(self) -> None:
        self.name = None
        self.startTime = None
        self.teststeps = []
        self.apiScript = None
        self.scriptTime = 0
        self.errorInfo = []
        self.udid = None

    def setUdid(self,udid:str):
        self.udid = udid

    def getUdid(self)->str:
        return self.udid

    def getErrorInfo(self)->List[str]:
        return self.errorInfo

    def addErrorInfo(self,info)->None:
        self.errorInfo.append(info)

    def getEndTime(self)->str:
        if self.teststeps!=None and len(self.teststeps)>0:
            return self.teststeps[-1].getStartTime()
        return self.startTime

    def addApiScript(self,apiScript:str)->None:
        self.apiScript = apiScript
        self.scriptTime+=1

    def getStartTime(self)->str:
        return self.startTime

    def getRunTime(self)->int:
        return self.scriptTime

    def getApiScript(self)->str:
        return self.apiScript

    def getStepAmount(self)->int:
        return len(self.teststeps)

    def getTeststep(self,index)->DataStep:
        if self.teststeps!=None and len(self.teststeps)>index:
            return self.teststeps[index]

    def getTeststeps(self)->List[DataStep]:
        return self.teststeps

    def addTeststep(self,teststep:DataStep):
        self.teststeps.append(teststep)

    def setStartTime(self,time:str):
        self.startTime = time

    def setName(self,name:str):
        self.name = name

    def getName(self)->str:
        return self.name

class DataLog(object):
    '''日志数据结构'''

    def __init__(self,reportPath:str) -> None:
        self.reportPath = reportPath #日志文件路径
        self.testcases = []

    def loadLog(self)->None:
        '''加载日志并解析'''
        with open(self.reportPath,'r') as file:
            lines = file.readlines()
        isErrorInfo = False
        for line in lines:
            if isErrorInfo and re.search('INFO',line)==None:
                self.addErrorInfo(line,isHeader=False)
            else:
                isErrorInfo=False

            if re.search('RunTest:[\S ]+$',line):
                self.addTestCase(line)
            elif re.search('extra:',line):
                self.addTestStep(line)
            elif re.search('RunApiTestCase',line):
                self.addApiScript(line)
            elif re.search('ERROR',line):
                self.addErrorInfo(line)
                isErrorInfo=True
            elif re.search('^ok$',line):
                break

    def addErrorInfo(self,line:str,isHeader:bool=True)->None:
        if self.testcases!=None and len(self.testcases)>0:
            testcase = self.testcases[-1]
            if isHeader:
                result = re.search("ERROR[\S ]+$",line)
                if result!=None:
                    testcase.addErrorInfo(result[0][6:])
                else:
                    testcase.addErrorInfo("ERROR:")
            else:
                testcase.addErrorInfo(line)

    def addApiScript(self,line:str)->None:
        if self.testcases!=None and len(self.testcases)>0:
            testcase = self.testcases[-1]
            testcase.addApiScript(re.search("[^:]+.yml$",line)[0])

    def addTestStep(self,line:str)->None:
        '''添加测试步骤'''
        if self.testcases==None or len(self.testcases)==0:
            return
        dataStep = DataStep()
        dataStep.setStartTime(re.search("start:[0-9.]+$",line)[0][6:])
        dataStep.setScreenShot(re.search("screenshot:[\S]+.png",line)[0][11:])
        dataStep.setControl(re.search("INFO [\S^:]+",line)[0][5:-1])
        type = re.search("type:[\S ]+value:",line)
        if type!=None:
            dataStep.setType(type[0][5:-6])
            dataStep.setValue(re.search("value:[\S ]+ extra",line)[0][6:-7])
        self.getTestCases()[-1].addTeststep(dataStep)
        dataStep.setExtra(re.search("extra:[\S ]+ screenshot:",line)[0][6:-12])

    def addTestCase(self,line:str)->None:
        '''添加测试用例'''
        test = DataTest()
        test.setStartTime(re.search("start:[0-9.]+$",line)[0][6:])
        test.setName(re.search("RunTest:[\S ]+udid",line)[0][8:-5])
        test.setUdid(re.search("udid:[\S]+ start:",line)[0][5:-7])
        self.testcases.append(test)

    def getTestCases(self)->List[DataTest]:
        return self.testcases