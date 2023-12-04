import re
import random
from typing import List
from appium import webdriver

from common.run import RunEnv

@RunEnv.runEnv(RunEnv.IOS)
def isValueEmpty(driver:webdriver,element:webdriver.WebElement)->bool:
    '''检查控件的value属性是否为空#用于检查输入框是否删除干净'''
    return element.get_attribute("value")==None

def isVisible(driver:webdriver,element)->bool:
    '''检查控件是否可见'''
    if RunEnv.isAndroid(driver):
        return element.get_attribute("focusable")== 'true'
    return element.get_attribute("visible")== 'true'

def getBounds(driver:webdriver,element)->List[int]:
    '''获取元素的位置和大小'''
    if RunEnv.isAndroid(driver):
        boundStr = element.get_attribute("bounds") #Android环境对应的属性
        boundList = re.findall("[0-9]+",boundStr)
        return list([int(value) for value in boundList])
    else:
        rectStr = element.get_attribute("rect") #IOS环境对应的属性
        rectList = re.findall("[0-9]+",rectStr)
        rect = list([int(value) for value in rectList])
        bounds = [rect[1],rect[0],rect[1]+rect[2],rect[0]+rect[3]]
        return bounds

def extractItemByRand(elements:list,rand:List[int]=None):
    '''
    在Rand的截取范围内随机选取一项并返回；
    若截取范围在数据长度范围外，则随机选取
    '''
    if rand == None:
        pass
    elif len(rand) == 1:
        # 正向截取且截取长度小于元素长度
        if rand[0] >= 0 and rand[0]<len(elements):
            return random.choice(elements[rand[0]:])
        # 反向截取，若截取长度为0则随机返回一项【适用于任意长度时排除最后项】
        elif rand[0]<0 and len(elements)+rand[0] > 0:
            return random.choice(elements[:rand[0]])
    elif len(rand) == 2:
        # 范围内截取成功，未处理Rand[1]为负数的情况
        if rand[1]<len(elements):
            return random.choice(elements[rand[0]:rand[1]])
    return random.choice(elements)