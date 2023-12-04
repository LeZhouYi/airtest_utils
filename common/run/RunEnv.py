import os
import re
import sys
import yaml
import logging
import inspect
import traceback
import functools
from appium import webdriver
from common.report import Report

Android = 'Android'
IOS = 'iOS'

def isAndroid(driver:webdriver):
    '''安卓环境'''
    return driver.caps["platformName"]==Android

def isIOS(driver:webdriver):
    '''IOS环境'''
    return driver.caps['platformName']==IOS

def runEnv(env=None):
    '''
    装饰器,env=None即所有环境均可执行
    env="Android"则只有安卓能执行，IOS等跳过
    env="iOS"则与上边相反
    '''
    def decorator(func):
        def wrapper(*args,**kwargs):
            envDriver = None
            print(args)
            if args!=None and len(args)>1 and isinstance(args[0],webdriver.webdriver.WebDriver) and args[0].caps!=None:
                envDriver = args[0].caps["platformName"]
            if env==None or env==envDriver:
                return func(*args, **kwargs)
        return wrapper
    return decorator

def retry(target=None, times=1, func_prefix="test"):
    '''
    一个装饰器，用于unittest执行测试用例出现失败后，自动重试执行
    '''
    def decorator(func_or_cls):
        if inspect.isfunction(func_or_cls):
            @functools.wraps(func_or_cls)
            def wrapper(*args, **kwargs):
                n = 0
                while n <= times:
                    try:
                        n += 1
                        func_or_cls(*args, **kwargs)
                        return
                    except Exception:  # 可以修改要捕获的异常类型
                        if n <= times:
                            trace = sys.exc_info()
                            traceback_info = str()
                            for trace_line in traceback.format_exception(trace[0], trace[1], trace[2], 3):
                                traceback_info += trace_line
                            Report.errorInfo(traceback_info)  # 输出组装的错误信息
                            args[0].tearDown()
                            args[0].setUp()
                        else:
                            trace = sys.exc_info()
                            traceback_info = str()
                            for trace_line in traceback.format_exception(trace[0], trace[1], trace[2], 3):
                                traceback_info += trace_line
                            Report.errorInfo(traceback_info)  # 输出组装的错误信息
                            raise

            return wrapper
        elif inspect.isclass(func_or_cls):
            for name, func in list(func_or_cls.__dict__.items()):
                if inspect.isfunction(func) and name.startswith(func_prefix):
                    setattr(func_or_cls, name, decorator(func))
            return func_or_cls
        else:
            raise AttributeError

    if target:
        return decorator(target)
    else:
        return decorator

def loadYamlFile(yamlPath):
    '''
    加载YAML
    '''
    data = {}
    with open(file=yamlPath,mode="rb") as yf:
        data = yaml.load(yf,Loader=yaml.FullLoader)
    return data

BaseConfig = loadYamlFile(str.format('{}/config/config.yaml',os.getcwd()))
devicesDesiredCaps = loadYamlFile(str.format('{}/config/devices.yaml',os.getcwd()))

def getDesiredCaps(platformName:str):
    if BaseConfig!=None:
        if platformName == 'Android' and "android_desired_caps" in BaseConfig:
            return BaseConfig['android_desired_caps']
        if platformName == 'iOS' and "ios_desired_caps" in BaseConfig:
            return BaseConfig['ios_desired_caps']

def getOperParams():
    if BaseConfig!=None and 'oper_params' in BaseConfig:
        return BaseConfig['oper_params']

def getDeviceDesiredCaps(udid:str):
    if devicesDesiredCaps!=None and udid in devicesDesiredCaps:
        return devicesDesiredCaps[udid]
    return {}

def getConnectDeviceCaps():
    '''
    返回第一个匹配的设备的desired_caps
    '''
    pattern = "[0-9a-zA-Z]+[0-9]+[0-9a-zA-Z]+"
    androidCmd = str(os.popen('adb devices').read())
    iosCmd = str(os.popen('idevice_id -l').read())
    for cmd in [androidCmd,iosCmd]:
        logging.getLogger().info("FindDevicesResult:\n"+cmd)
        result = re.search(pattern,cmd)
        if result!=None:
            udid = cmd[result.span()[0]:result.span()[1]]
            deviceCaps = getDeviceDesiredCaps(udid)
            logging.getLogger().info("FindDeviceUdid:"+udid)
            if deviceCaps:
                logging.getLogger().info("FindDeviceCaps:"+str(deviceCaps))
                return deviceCaps
    return {}

def initAppiumServer()->None:
    '''启动Appium'''
    os.system('appium -p %s -bp %s -U 127.0.0.1:62001 --session-override'%(4723,4724))

def getDriverSign()->str:
    '''返回浏览器标志'''
    envConfig = loadYamlFile(str.format('{}/config/env.yaml',os.getcwd()))
    return envConfig["driver"]
