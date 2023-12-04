from operator import index
import random
from time import sleep
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common import action_chains

from common.report import Report

def checkElement(driver:webdriver,by:str,value:str)->bool:
    '''查看某元素是否存在'''
    return len(driver.find_elements(by,value))>0

def validateTextEqual(driver:webdriver,by:str,value:str,text:str):
    '''校验该元素的文本是否相等'''
    element = driver.find_element(by,value)
    assert element.text.find(text)>=0

def validateNotExistElement(driver:webdriver,by:str,value:str,delay:int=1):
    '''校验某元素不存在'''
    Report.stepWebInfo(by,value,"delay:%s"%delay)
    assert len(driver.find_elements(by,value))==0

def validateExistElement(driver:webdriver,by:str,value:str,delay:int=30):
    '''校验某元素存在'''
    Report.stepWebInfo(by,value,"delay:%s"%delay)
    for i in range(int(delay/0.5)):
        if len(driver.find_elements(by,value))>0:
            return
        sleep(0.5)
    assert len(driver.find_elements(by,value))>0

def wait_element(driver:webdriver,by:str,value:str,delay:int=30):
    '''等待某元素'''
    Report.stepWebInfo(by,value)
    for i in range(int(delay/0.5)):
        if len(driver.find_elements(by,value))>0:
            return
        sleep(0.5)
    driver.find_element(by,value)

def extraElementByIndex(driver:webdriver,by:str,value:str,index:int=0)->WebElement:
    '''根据index找到并返回某元素'''
    elements = driver.find_elements(by,value)
    Report.stepWebInfo(by,value,"index:%s, findCount:%s"%(index,len(elements)))
    return elements[index]

def extraElementByRand(driver:webdriver,by:str,value:str)->WebElement:
    '''根据index找到并返回某元素'''
    elements = driver.find_elements(by,value)
    index = random.randint(0,len(elements)-1)
    Report.stepWebInfo(by,value,"index:%s, findCount:%s"%(index,len(elements)))
    return elements[index]

def clickElementByIndex(driver:webdriver,by:str,value:str,index:int=0,delay:int=1):
    '''根据index找到并点击某元素'''
    elements = driver.find_elements(by,value)
    Report.stepWebInfo(by,value,"index:%s, findCount:%s"%(index,len(elements)))
    driver.execute_script("arguments[0].scrollIntoView();",elements[index])
    action_chains.ActionChains(driver).move_to_element(elements[index]).click(elements[index]).perform()
    sleep(delay)

def clickElementByRand(driver:webdriver,by:str,value:str,delay:int=1):
    '''根据随机的index找到并点击某元素'''
    elements = driver.find_elements(by,value)
    index = random.randint(0,len(elements)-1)
    while(elements[index].location_once_scrolled_into_view==None or not elements[index].is_displayed()):
        index = random.randint(0,len(elements)-1)
    Report.stepWebInfo(by,value,"index:%s, findCount:%s"%(index,len(elements)))
    driver.execute_script("arguments[0].scrollIntoView();",elements[index])
    elements[index].click()
    sleep(delay)

def clickInputElement(driver:webdriver,element:WebElement,text:str,delay:int=1):
    '''点击元素并输入'''
    Report.stepWebInfo(None,None,"input:%s,delay:%s"%(text,delay))
    driver.execute_script("arguments[0].scrollIntoView();",element)
    action_chains.ActionChains(driver).click(element).perform()
    element.send_keys(text)
    sleep(delay)

def keyPress(element:WebElement,keys:Keys,delay:int=1):
    ''''''
    Report.stepWebInfo(None,None,"input:%s,delay:%s"%(keys,delay))
    element.send_keys(keys)
    sleep(delay)

def clearInputElement(element:WebElement,text:str,delay:int=1):
    Report.stepWebInfo(None,None,"input:%s,delay:%s"%(text,delay))
    element.click()
    length = 50 if text==None else int(len(text)*2)
    for i in range(length):
        element.send_keys(Keys.RIGHT)
        element.send_keys(Keys.BACK_SPACE)
    sleep(delay)

def clickElement(driver:webdriver,by:str,value:str,delay:int=1):
    '''点击元素'''
    Report.stepWebInfo(by,value,"delay:%s"%delay)
    element = driver.find_element(by,value)
    driver.execute_script("arguments[0].scrollIntoView();",element)
    action_chains.ActionChains(driver).move_to_element(element).perform()
    driver.execute_script("arguments[0].click();",element)
    sleep(delay)

def scrollElementByIndex(driver:webdriver,by:str,value:str,index:int=-1):
    '''滚动页面并调整元素，使其出现在合适的位置上'''
    target = driver.find_elements(by,value)
    driver.execute_script("arguments[0].scrollIntoView();",target[0])


def scrollElement(driver:webdriver,by:str,value:str):
    '''滚动页面并调整元素，使其出现在合适的位置上'''
    target = driver.find_element(by,value)
    driver.execute_script("arguments[0].scrollIntoView();",target)

def findElementIndex(driver:webdriver,by:str,value:str,findStr:str)->int:
    '''查找符合条件元素中该元素的位置'''
    elements = driver.find_elements(by,value)
    print(len(elements))
    for i in range(len(elements)):
        print(elements[i].text)
        if str(elements[i].text).find(findStr)>=0:
            return i-len(elements)
    return None

def clickElementPos(driver:webdriver,element:WebElement,tap:list=[0.5,0.5],delay:int=1):
    '''根据元素点击相对位置'''
    driver.execute_script("arguments[0].scrollIntoView();",element)
    x = element.size["width"]*tap[0]
    y = element.size["height"]*tap[1]
    action_chains.ActionChains(driver).move_to_element_with_offset(element,x,y).click().perform()

def scrollPageBottom(driver:webdriver):
    '''滑动页面至底部'''
    js = "window.scrollTo(0,document.body.scrollHeight);"
    driver.execute_script(js)