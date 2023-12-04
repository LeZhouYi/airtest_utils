import os
import re
import math
import logging
import datetime
import time
from PIL import Image, ImageDraw
from typing import List

from appium import webdriver

from common.run import RunEnv

class ControlType(object):
    Find = '寻找元素'
    Click = '点击元素'
    Tap = '相对点击'
    Wait = '等待元素'
    Swipe = '滑动屏幕'
    KeyCode = '按键操作'

def stepWebInfo(key:str,text:str,extra:str=None)->None:
    '''输出报告'''
    logging.getLogger().info("By:%s Value:%s Extra:%s"%(key,text,extra))

def testWebInfo(text:str)->None:
    '''输出报告'''
    logging.getLogger().info(text)

def errorInfo(text:str)->None:
    '''输出报告'''
    logging.getLogger().error(text)

def funcInfo(text:str)->None:
    '''输出报告'''
    logging.getLogger().info(text)

def testCaseInfo(driver:webdriver,caseName:str)->None:
    '''输出测试用例的报告头'''
    udid = driver.caps["deviceUDID"] if RunEnv.isAndroid(driver) else driver.caps["udid"]
    logging.getLogger().info("RunTest:%s udid:%s start:%s"%(caseName,udid,time.time()))

def initLogger()->str:
    '''初始化日志'''
    # now = datetime.datetime.now().strftime('%Y-%m-%d_%H_%M_%S')
    reportPath = '%s/reports/report.log'%os.getcwd()
    #LOG日志记录
    log_file_name = '%s/reports/report.log'%(os.getcwd())
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(levelname)s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        filename=log_file_name,
                        filemode='w')
    return reportPath

def pushInfo(control:str,type:str,value:str,extra:str,screenshot:str=None):
    '''输出报告'''
    if screenshot!=None:
        screenshot = re.search("[^/]+.png$",screenshot)[0]
    if control in [ControlType.Find,ControlType.Click,ControlType.Wait]:
        logging.getLogger().info('%s:  type:%s  value:%s, extra:%s screenshot:%s start:%s'%(control,type,value,extra,screenshot,time.time()))
    elif control in [ControlType.Tap,ControlType.Swipe,ControlType.KeyCode]:
        logging.getLogger().info('%s:  extra:%s screenshot:%s start:%s'%(control,extra,screenshot,time.time()))

def saveScreenshots(driver:webdriver):
    '''截图'''
    imgFolder = '%s/reports/screenshots'%os.getcwd()
    nowTime = datetime.datetime.now().strftime('%Y-%m-%d_%H_%M_%S_%f')
    outFile = '%s/%s.png'%(imgFolder,nowTime)
    driver.get_screenshot_as_file(outFile)
    return outFile

def drawClickScreenshot(driver:webdriver,imagePath:str, bounds:list=None, tap: list = [0.5, 0.5])->None:
    '''
    根据当前对元素的操作，在对应的截图中进行渲染
    '''
    image = Image.open(imagePath).convert('RGB')
    windowSize = driver.get_window_size()
    draw = ImageDraw.Draw(image)
    if bounds!=None:
        #绘制检索的控件和点击位置
        #调整尺寸，手机显示的分辨率与截图的分辨率不一定一致(如IOS)
        if RunEnv.isIOS(driver):
            bounds[0]*=(float(image.width)/windowSize["width"])
            bounds[2]*=(float(image.width)/windowSize["width"])
            bounds[1]*=(float(image.height)/windowSize["height"])
            bounds[3]*=(float(image.height)/windowSize["height"])
        #绘制图形
        draw.rectangle(bounds, fill=None, outline="red", width=8)
        if tap:
            x = bounds[0] + (bounds[2]-bounds[0])*tap[0]
            y = bounds[1] + (bounds[3]-bounds[1])*tap[1]
            draw.ellipse((x-25, y-25, x+25, y+25),fill=None, outline="red", width=10)
    elif tap!=None:
        #绘制点击屏幕的位置
        x = image.width*tap[0]
        y = image.height*tap[1]
        draw.ellipse((x-25, y-25, x+25, y+25),fill=None, outline="red", width=10)
    del draw
    image.save(imagePath)

def drawSwipeScreenshot(driver:webdriver,imagePath:str,vector:List[float]=None):
    '''
    绘制滑动的起始和终点，滑动方向;
    vector=[startX,startY,endX,endY];
    eg:vector=[0,0,100,100],即PointX(0,0)滑动至PointY(100,100)
    '''
    if vector==None or len(vector)!=4:
        return
    image = Image.open(imagePath).convert('RGB')
    windowSize = driver.get_window_size()
    #调整尺寸，手机显示的分辨率与截图的分辨率不一定一致(如IOS)
    if RunEnv.isIOS(driver):
        vector[0]*=(float(image.width)/windowSize["width"])
        vector[2]*=(float(image.width)/windowSize["width"])
        vector[1]*=(float(image.height)/windowSize["height"])
        vector[3]*=(float(image.height)/windowSize["height"])
    #绘制
    draw = ImageDraw.Draw(image)
    draw.ellipse((vector[0]-25, vector[1]-25, vector[0]+25, vector[1]+25),fill=None, outline="red", width=10)
    draw.line(vector,fill="red",width=10)
    #箭头
    if math.fabs(vector[2]-vector[0])>math.fabs(vector[3]-vector[1]):
        startX = vector[2]-(25 if vector[2]>vector[0] else -25)
        startY_1,startY_2 = vector[3]+25,vector[3]-25
        draw.line([startX,startY_1,vector[2],vector[3]],fill="red",width=10)
        draw.line([startX,startY_2,vector[2],vector[3]],fill="red",width=10)
    else:
        startY = vector[3]-(25 if vector[3]>vector[1] else -25)
        startX_1,startX_2 = vector[2]+25,vector[2]-25
        draw.line([startX_1,startY,vector[2],vector[3]],fill="red",width=10)
        draw.line([startX_2,startY,vector[2],vector[3]],fill="red",width=10)
    del draw
    image.save(imagePath)
