from Device import Device
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from common.device.KeyCode import KeyCode
from common.control import Control
from common.device.Device import Permission

class Android_Base(Device):
    def uploadImage(self,driver:webdriver):
        Control.waitElement(driver,AppiumBy.XPATH,'//*[@text="All view"]')
        Control.clickElement(driver,AppiumBy.XPATH,'//*[@text="All view"]')
        Control.clickElementsByRand(driver,AppiumBy.CLASS_NAME,'android.widget.ImageView',rand=[1])
        Control.clickElement(driver,AppiumBy.XPATH,'//*[@content-desc="done"]')

class Andorid_Huawei(Device):
    def uploadImage(self,driver:webdriver):
        Control.clickElement(driver,AppiumBy.XPATH,'//*[@text="All view"]')
        Control.clickElementsByRand(driver,AppiumBy.CLASS_NAME,'android.widget.ImageView',rand=[1])
        Control.clickElement(driver,AppiumBy.XPATH,'//*[@content-desc="done"]')

    def allocatePermission(self,driver:webdriver,app_name,permissions:list):
        #回到主页，避免通知下拉框页面遮挡
        Control.devicePress(driver,KeyCode.KEYCODE_HOME)
        #重启设置
        driver.start_activity('com.android.settings','com.android.settings.HWSettings')

        #进入APP权限设置
        Control.clickElement(driver,AppiumBy.ACCESSIBILITY_ID,'搜索查询')
        Control.adbInputText(driver,'应用管理')
        Control.clickElement(driver,AppiumBy.XPATH,'//android.widget.TextView[@text="应用管理"]')
        Control.waitElement(driver,AppiumBy.ACCESSIBILITY_ID,'搜索查询')
        Control.clickElement(driver,AppiumBy.ACCESSIBILITY_ID,'搜索查询')
        Control.adbInputText(driver,app_name)
        Control.clickElement(driver,AppiumBy.XPATH,str.format('//android.widget.TextView[contains(@text,"{}")]',app_name))
        Control.clickElement(driver,AppiumBy.XPATH,'//*[@text="权限"]')

        #依次搜索并设置权限
        for permission_name in permissions:
            #权限在当前设置页面
            Control.waitElement(driver,AppiumBy.XPATH,'//*[contains(@text,"已允许")]')
            if Control.checkClickElement(driver,AppiumBy.XPATH,'//android.widget.TextView[contains(@text,"%s")]/../../..'%permission_name):
                Control.checkClickElement(driver,AppiumBy.XPATH,'//android.widget.RadioButton[@text="允许"]')
                Control.devicePress(driver,KeyCode.KEYCODE_BACK)
            #或许在所有权限中
            elif Control.checkClickElement(driver,AppiumBy.XPATH,'//*[contains(@text,"查看所有权限")]'):
                Control.scroll_to_find_elements(driver,AppiumBy.XPATH,'//*[@text="%s"]'%permission_name)
                Control.focus_tap_element(driver,AppiumBy.XPATH,'//*[@text="%s"]/../..'%permission_name,vector=[0.9,0.5])
                Control.devicePress(driver,KeyCode.KEYCODE_BACK)

class IOS_15(Device):

    def uploadImage(self,driver:webdriver):
        Control.clickElementsByRand(driver,AppiumBy.XPATH,'//XCUIElementTypeCell[contains(@name,"photo_cell")]')
        Control.clickElement(driver,AppiumBy.ACCESSIBILITY_ID,'Done (1)')

    def comfirmPermission(self,driver:webdriver,permission:str):
        if permission == Permission.NOTICE:
            Control.checkClickElement(driver,AppiumBy.XPATH,'//XCUIElementTypeButton[@name="允許"]')
        elif permission == Permission.GPS:
            Control.checkClickElement(driver,AppiumBy.XPATH,'//XCUIElementTypeButton[@name="使用App時允許"]')
        elif permission == Permission.PHOTO:
            Control.checkClickElement(driver,AppiumBy.XPATH,'//XCUIElementTypeButton[@name="允許取用所有相片"]')
        elif permission == Permission.RECORD:
            Control.checkClickElement(driver,AppiumBy.XPATH,'//XCUIElementTypeButton[@name="好"]')

class IOS_14(Device):

    def uploadImage(self,driver:webdriver):
        Control.clickElementsByRand(driver,AppiumBy.XPATH,'//XCUIElementTypeCell[contains(@name,"photo_cell")]')
        Control.clickElement(driver,AppiumBy.ACCESSIBILITY_ID,'Done (1)')

    def comfirmPermission(self,driver:webdriver,permission:str):
        if permission == Permission.NOTICE:
            Control.checkClickElement(driver,AppiumBy.XPATH,'//XCUIElementTypeButton[@name="允许"]')
        elif permission == Permission.GPS:
            Control.checkClickElement(driver,AppiumBy.XPATH,'//XCUIElementTypeButton[@name="使用App时允许"]')
        elif permission == Permission.PHOTO:
            Control.checkClickElement(driver,AppiumBy.XPATH,'//XCUIElementTypeButton[@name="允许访问所有照片"]')
        elif permission == Permission.RECORD:
            Control.checkClickElement(driver,AppiumBy.XPATH,'//XCUIElementTypeButton[@name="好"]')

class IOS_12(Device):

    def uploadImage(self,driver:webdriver):
        Control.clickElementsByRand(driver,AppiumBy.XPATH,'//XCUIElementTypeCell[contains(@name,"photo_cell")]')
        Control.clickElement(driver,AppiumBy.ACCESSIBILITY_ID,'Done (1)')

    def comfirmPermission(self,driver:webdriver,permission:str):
        if permission == Permission.NOTICE:
            Control.checkClickElement(driver,AppiumBy.XPATH,'//XCUIElementTypeButton[@name="允许"]')
        elif permission == Permission.GPS:
            Control.checkClickElement(driver,AppiumBy.XPATH,'//XCUIElementTypeButton[@name="允许"]')
        elif permission == Permission.PHOTO:
            Control.checkClickElement(driver,AppiumBy.XPATH,'//XCUIElementTypeButton[@name="好"]')
        elif permission == Permission.RECORD:
            Control.checkClickElement(driver,AppiumBy.XPATH,'//XCUIElementTypeButton[@name="好"]')