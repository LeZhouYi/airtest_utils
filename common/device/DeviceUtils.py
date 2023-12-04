from appium import webdriver
from Mobile import Android_Base,Andorid_Huawei,IOS_12,IOS_15,IOS_14
from Device import Operation
from common.run import RunEnv

def getMobilePhone(deviceName:str):
    '''
    获取设备对应的方法类
    '''
    phone = None
    android = ["Galaxy A9s","SM_J600G","SM_A9200","Pixel_4","OnePlus_5","HUAWEI Mate 10","HUAWEI Mate 30","HONOR Play4T"]
    huawei = ["HMA-AL00"]
    ios_15 = ["iPhone 7 Plus"]
    ios_12 = ["iPhone 7"]
    ios_14 = ["iPhone 7 14.2"]
    if deviceName in android:
        phone = Android_Base()
    elif deviceName in huawei:
        phone = Andorid_Huawei()
    elif deviceName in ios_15:
        phone = IOS_15()
    elif deviceName in ios_12:
        phone = IOS_12()
    elif deviceName in ios_14:
        phone = IOS_14()
    return phone

def operateDevice(driver:webdriver,operation:Operation,operParams=None):
    '''
    使用当前设备的系统应用进行操作
    operation为当前的操作类型，oper_params则为该操作所需的数据
    eg:
        Operation.ALLOCATE_PERMISSION,oper_params = {"appName":"testAppName","permisssions":["存储","位置"]}
        Operation.COMFIRM_PERMISSION,oper_params = Perrmission.GPS
    '''
    if RunEnv.isAndroid(driver):
        device_name = driver.caps['desired']['deviceName']
    else:
        device_name = driver.caps["deviceName"]
    phone = getMobilePhone(device_name)
    assert phone, str.format('"DeviceName":{},"ErrorMessage":No device found, please confirm whether the device has been defined',device_name)
    if operation == Operation.UPLOAD_IMAGE:
        phone.uploadImage(driver)
    elif operation == Operation.ALLOCATE_PERMISSION:
        phone.allocatePermission(driver,app_name=operParams['app_name'],permissions=operParams['permissions'])
    elif operation == Operation.COMFIRM_PERMISSION:
        phone.comfirmPermission(driver,operParams)