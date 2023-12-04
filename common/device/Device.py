# -*- coding: utf-8 -*-

from appium import webdriver
from abc import ABC,abstractclassmethod

class Device(ABC):
    '''
    设备基类
    '''

    @abstractclassmethod
    def uploadImage(self,driver:webdriver):
        '''
        上传图片文件
        '''
        pass

    def allocatePermission(self,driver:webdriver,app_name,permissions):
        '''
        进入手机的应用管理，分配该APP的权限(适用于Appium预分配对手机失效的情况,如华为)
        '''
        pass

    def comfirmPermission(self,driver:webdriver,permission:str):
        '''
        同意权限
        '''

class Operation(object):
    '''
    手机操作类型
    '''
    UPLOAD_IMAGE = 'upload_image'
    ALLOCATE_PERMISSION = 'allocate_permission'
    COMFIRM_PERMISSION = 'comfirm_permission'

class Permission(object):
    '''
    手机权限类型
    '''
    NOTICE = 'notice'
    GPS = 'gps'
    PHOTO = 'photo'
    RECORD = 'record'