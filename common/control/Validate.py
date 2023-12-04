from typing import List
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
import Control

def assertExist(driver:webdriver,type:str,value:str):
    '''判断是否存在某元素'''
    assert Control.checkElement(driver,type,value)

def assertNotExist(driver:webdriver,type:str,value:str):
    '''判断不存在某元素'''
    assert len(driver.find_elements(type,value))==0

def assertContentEqual(driver:webdriver,element,expect:str):
    '''判断某元素的文本符合预期'''
    assert str(element.get_attribute('content-desc'))==expect

def assertExistScroll(driver:webdriver,type:str,value:str,vector:List[float]=[0.5, 0.75, 0.5, 0.25]):
    '''滚动查找并判断'''
    assert Control.scrollFindElements(driver,type,value,vector)!=None