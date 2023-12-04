import os
import re
import base64
import math
from typing import List
from time import sleep
from appium import webdriver
from appium.webdriver import WebElement
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.wait import WebDriverWait

from common.report  import Report
from common.report.Report import ControlType
from common.device.KeyCode import KeyCode
from common.run import RunEnv
import ControlUtils

##通用操作

def focusTap(driver: webdriver, element:WebElement, tap:List[float]=[0.5,0.5], delay:int=1)->None:
    '''
    根据获取的元素，按相对位置进行点击
    其中x,y为相对值，[0,1]则在元素内点击,其余则在元素外
    '''
    bounds = ControlUtils.getBounds(driver,element)
    tapX = bounds[0] + (bounds[2]-bounds[0])*tap[0]
    tapY = bounds[1] + (bounds[3]-bounds[1])*tap[1]
    screenshot = Report.saveScreenshots(driver)
    Report.pushInfo(ControlType.Tap,None,None,'[%s,%s]'%(tapX,tapY),screenshot)
    bounds = ControlUtils.getBounds(driver,element)
    Report.drawClickScreenshot(driver,screenshot,bounds,tap)
    driver.tap([(tapX, tapY)])
    sleep(delay)

def focusTapElement(driver:webdriver,type:str,value:str,tap:List[int],delay:int=1):
    '''
    根据获取的元素，按相对位置进行点击
    其中x,y为相对值，[0,1]则在元素内点击,其余则在元素外
    '''
    Report.saveScreenshots(driver)
    element = driver.find_element(type, value)
    focusTap(driver, element, tap, delay)

def focusTapScreen(driver:webdriver,tap:List[int],delay:int=1):
    '''点击屏幕的相对坐标'''
    tapX = driver.get_window_size()['width']*tap[0]
    tapY = driver.get_window_size()['height']*tap[1]
    screenshot = Report.saveScreenshots(driver)
    Report.pushInfo(ControlType.Tap,None,None,'[%s,%s]'%(tapX,tapY),screenshot)
    Report.drawClickScreenshot(driver,screenshot,None,tap)
    driver.tap([(tapX, tapY)])
    sleep(delay)

def clickElement(driver: webdriver, type:str, value:str, delay: int = 1)->None:
    '''点击元素'''
    screenshot = Report.saveScreenshots(driver)
    Report.pushInfo(ControlType.Find,type,value,None,screenshot)
    element = driver.find_element(type,value)
    focusTap(driver,element,[0.5,0.5],delay)

def clickElementsByIndex(driver:webdriver,type:str,value:str,index:int=-1,delay:int=1):
    '''存在多个元素时(可能)，根据index进行选取并点击'''
    screenshoot = Report.saveScreenshots(driver)
    elements = driver.find_elements(type, value)
    Report.pushInfo(ControlType.Find,type,value,'[length:%s,index:%s]'%(len(elements),index),screenshoot)
    element = elements[index]
    focusTap(driver,element,[0.5,0.5],delay)

def clickElementsByRand(driver: webdriver, type:str, value:str, rand:List[int] = None, delay: int = 1)->None:
    '''存在多个元素时(可能),在rand范围内点击最后一个'''
    elements = driver.find_elements(type, value)
    screenshoot = Report.saveScreenshots(driver)
    Report.pushInfo(ControlType.Find,type,value,'[length:%s,rand:%s]'%(len(elements),rand),screenshoot)
    element = ControlUtils.extractItemByRand(elements,rand)
    focusTap(driver,element,[0.5,0.5],delay)

def checkElement(driver:webdriver,type:str,value:str)->bool:
    '''检查元素是否存在'''
    screenshot = Report.saveScreenshots(driver)
    Report.pushInfo(ControlType.Find,type,value,None,screenshot)
    elements = driver.find_elements(type, value)
    if len(elements) > 0 and ControlUtils.isVisible(driver,elements[0]):
        bounds = ControlUtils.getBounds(driver,elements[0])
        Report.drawClickScreenshot(driver,screenshot,bounds,None)
        return True
    return False

def checkClickElement(driver:webdriver,type:str,value:str,delay:int=1)->bool:
    '''若存在该元素，则点击'''
    if checkElement(driver,type,value):
        clickElement(driver,type,value,delay)
        return True
    return False

def clickElementUntilNoCheck(driver:webdriver,type:str,value:str,times:int=1,delay:int=1):
    '''重复点击直至该元素搜索不到，用于点击某按键(但因网络问题点击失效，无法跳转导致的用例失败)'''
    times = times if times>1 else 1
    while checkElement(driver,type,value) and times:
        times-=1
        clickElement(driver,type,value,delay)

def extractElement(driver:webdriver,type:str,value:str,rand:List[int]=None):
    '''存在多个元素时(可能),在rand范围内随机提取一个'''
    screenshot = Report.saveScreenshots(driver)
    elements = driver.find_elements(type, value)
    Report.pushInfo(ControlType.Find,type,value,'[length:%s,rand:%s]'%(len(elements),rand),screenshot)
    element = ControlUtils.extractItemByRand(elements,rand)
    bounds = ControlUtils.getBounds(driver,element)
    Report.drawClickScreenshot(driver,screenshot,bounds,None)
    return element

def extractElementByIndex(driver:webdriver,type:str,value:str,index:int=-1):
    '''存在多个元素时(可能)，根据index导出元素'''
    screenshot = Report.saveScreenshots(driver)
    elements = driver.find_elements(type, value)
    Report.pushInfo(ControlType.Find,type,value,'[length:%s,index:%s]'%(len(elements),index),screenshot)
    element = elements[index]
    bounds = ControlUtils.getBounds(driver,element)
    Report.drawClickScreenshot(driver,screenshot,bounds,None)
    return element

def waitElement(driver:webdriver, type:str,value:str,delay=60):
    '''等待加载元素成功'''
    screenshot = Report.saveScreenshots(driver)
    Report.pushInfo(ControlType.Wait,type,value,'[delay:%s]'%(delay),screenshot)
    times = int(delay/2)
    while(times>0):
        elements = driver.find_elements(type,value)
        if len(elements)>0 and ControlUtils.isVisible(driver,elements[0]):
            break
        sleep(1)
        times-=1
    screenshot = Report.saveScreenshots(driver)
    Report.pushInfo(ControlType.Wait,type,value,'[delay:%s]'%(delay),screenshot)
    element = driver.find_element(type, value)
    bounds = ControlUtils.getBounds(driver,element)
    Report.drawClickScreenshot(driver,screenshot,bounds,None)

def swipeScreen(driver:webdriver,vector:List[float]=[0.5,0.75,0.5,0.5],delay:int=1):
    '''滑动手机屏幕'''
    screenshot = Report.saveScreenshots(driver)
    Report.pushInfo(ControlType.Swipe,None,None,'[vector:%s]'%(vector),screenshot)
    size = driver.get_window_size()
    startX,startY,endX,endY = size['width']*vector[0], size['height']*vector[1],size['width']*vector[2], size['height']*vector[3]
    Report.drawSwipeScreenshot(driver,screenshot,[startX,startY,endX,endY])
    driver.swipe(startX,startY,endX,endY, 500)
    sleep(delay)

def closeNotification(driver:webdriver):
    '''滑动屏幕以关闭通知'''
    if RunEnv.isAndroid(driver):
        driver.open_notifications()
        sleep(1)
        driver.press_keycode(KeyCode.KEYCODE_BACK)
        sleep(2)
    else:
        swipeScreen(driver,vector=[0.5,0.01,0.5,0.85])
        sleep(1)
        swipeScreen(driver,vector=[0.5,0.99,0.5,0.01])
        sleep(2)

def scrollFindElements(driver:webdriver,type:str,value:str,vector:List[float]=[0.5, 0.75, 0.5, 0.25]):
    '''
    向下/上滚动，直至找到element元素并返回
    返回list
    '''
    screenshot = Report.saveScreenshots(driver)
    Report.pushInfo(ControlType.Find,type,value,None,screenshot)
    size = driver.get_window_size()
    oldPage = driver.page_source
    times = 5 # 检查五次是否到了尽头
    elements = driver.find_elements(type, value)
    while len(elements) == 0 or not ControlUtils.isVisible(driver,elements[0]):
        #滑动，根据Vector决定滑动方向
        driver.swipe(size['width']*vector[0], size['height']*vector[1],size['width']*vector[2], size['height']*vector[3], 500)
        sleep(2)
        #检查全局，找不到则跳出
        newPage = driver.page_source
        if oldPage == newPage:
            times -= 1
            if not times:
                break
        oldPage = newPage
        #搜寻元素
        elements = driver.find_elements(type, value)
    sleep(1)
    screenshot = Report.saveScreenshots(driver)
    elements = driver.find_elements(type, value)
    bounds = ControlUtils.getBounds(driver,elements[0])
    Report.drawClickScreenshot(driver,screenshot, bounds, None)
    Report.pushInfo(ControlType.Find,type,value,None,screenshot)
    return elements[0]

def scrollRelativePosition(driver:webdriver,startElement,endElement,shift:float):
    '''根据start_element的位置，调整该控件至end_element的相对位置'''
    startBounds = ControlUtils.getBounds(driver,startElement)
    endBounds = ControlUtils.getBounds(driver,endElement)
    startY = startBounds[1] if shift >= 0.0 else startBounds[3]
    startX = (startBounds[2]+startBounds[0])/2.0
    endY = endBounds[1] if shift >= 0.0 else endBounds[3]
    endY = (endY-startY)*math.fabs(shift)+startY
    vector = [startX,startY,startX,endY]

    screenshot = Report.saveScreenshots(driver)
    Report.pushInfo(ControlType.Swipe,None,None,'[vector:%s]'%(vector),screenshot)
    Report.drawSwipeScreenshot(driver,screenshot,[startX,startY,startX,endY])
    driver.swipe(startX, startY, startX, endY, 1000)
    Report.saveScreenshots(driver)
    sleep(1)

def devicePress(driver:webdriver, keycode:int, delay:int=1):
    '''按键操作'''
    screenshot = Report.saveScreenshots(driver)
    Report.pushInfo(ControlType.KeyCode,None,None,'[keycode:%s]'%keycode,screenshot)
    driver.press_keycode(keycode)
    sleep(delay)

def restartApp(driver:webdriver):
    '''重启当前应用'''
    driver.close_app()
    sleep(1)
    driver.launch_app()
    sleep(6)

@RunEnv.runEnv(RunEnv.Android)
def adbInputText(driver:webdriver, text:str)->None:
    '''使用ADBKeyboard并输入文本'''
    charsb64 = str(base64.b64encode(text.encode('utf-8')))[1:]
    os.system("adb shell am broadcast -a ADB_INPUT_B64 --es msg %s"%charsb64)
    sleep(1)

@RunEnv.runEnv(RunEnv.Android)
def runFakeGpsApp(driver:webdriver):
    '''启动GPS模拟应用'''
    cmd = str(os.popen('adb shell pm list packages "fake"').read())
    if re.search('com.lexa.fakegps',cmd):
        driver.start_activity('com.lexa.fakegps','com.lexa.fakegps.ui.Main')
        sleep(3)
        if not checkClickElement(driver,AppiumBy.ID,'com.lexa.fakegps:id/action_start'):
            devicePress(driver,KeyCode.KEYCODE_BACK)
            clickElement(driver,AppiumBy.ID,'com.lexa.fakegps:id/action_start')
    elif re.search('com.lerist.fakelocation',cmd):
        driver.start_activity('com.lerist.fakelocation','com.lerist.fakelocation.ui.activity.MainActivity')
        waitElement(driver,AppiumBy.XPATH,'//*[@text="启动模拟"]/..')
        clickElement(driver,AppiumBy.XPATH,'//*[@text="启动模拟"]/..')
        waitElement(driver,AppiumBy.XPATH,'//*[@text="停止模拟"]/..')

@RunEnv.runEnv(RunEnv.IOS)
def closeKeyBoard(driver:webdriver,tap:List[float]=[0.99,-0.05]):
    '''关闭键盘，适用于IOS'''
    if not checkClickElement(driver,AppiumBy.XPATH,'//XCUIElementTypeButton[@name="Done"]'):
        keyboard = extractElement(driver,AppiumBy.XPATH,'//XCUIElementTypeKeyboard')
        focusTap(driver,keyboard,tap)

def clickInputText(driver:webdriver,element:WebElement,text:str,delay:int=1,close_kb:bool=True):
    '''点击并输入文本'''
    focusTap(driver,element,[0.5,0.5],delay)
    if RunEnv.isAndroid(driver):
        if text!=None and text!="":
            adbInputText(driver,text)
    else:
        if text!=None and text!="":
            element.send_keys(text)
        if close_kb:
            closeKeyBoard(driver)

def clearInputText(driver:webdriver,element:WebElement,text:str,delay:int=2):
    '''点击并清除文本'''
    if RunEnv.isAndroid(driver):
        focusTap(driver,element,[0.5,0.5],delay)
        for char in str(text):
            driver.press_keycode(KeyCode.KEYCODE_DPAD_RIGHT)
            driver.press_keycode(KeyCode.KEYCODE_DEL)
        # driver.press_keycode(KeyCode.KEYCODE_ESCAPE)
    else:
        times = int(len(text)/8)+2
        while(times>0):
            focusTap(driver,element,[0.8,0.5],delay)
            delElements = driver.find_elements(AppiumBy.ACCESSIBILITY_ID,"delete")
            if len(delElements)==0:
                delElements = driver.find_elements(AppiumBy.ACCESSIBILITY_ID,"删除")
            for i in range(8):
                delElements[-1].click()
            times-=1
        closeKeyBoard(driver)
    sleep(delay)

@RunEnv.runEnv(RunEnv.Android)
def setIme(driver:webdriver):
    '''设定输入法，适用Android'''
    os.system("adb -s %s shell ime set com.android.adbkeyboard/.AdbIME"%(driver.caps["deviceUDID"]))