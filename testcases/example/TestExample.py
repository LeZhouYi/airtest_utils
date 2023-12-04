from random import Random
from time import sleep
import unittest
from selenium import webdriver
from selenium.webdriver.chromium.service import ChromiumService
from webdrivermanager.chrome import ChromeDriverManager
from webdrivermanager.edgechromium import EdgeChromiumDriverManager
from webdrivermanager.gecko import GeckoDriverManager

from common.run import RunEnv
from common.report import Report

class CouponDealTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        driverSign = RunEnv.getDriverSign()
        if driverSign=="Chrome":
            manager = ChromeDriverManager();
            intallReuslt = manager.download_and_install()
            cls.driver = webdriver.Chrome(service=ChromiumService(intallReuslt[0]))
        elif driverSign=="FireFox":
            cls.driver = webdriver.Firefox(GeckoDriverManager().download_and_install())
        elif driverSign=="Safari":
            cls.driver = webdriver.Safari()
        elif driverSign=="Edge":
            cls.driver = webdriver.Edge(EdgeChromiumDriverManager().download_and_install())
        cls.driver.maximize_window()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    @RunEnv.retry(times=2)
    def testRun(self):
        Report.testWebInfo("打开浏览器并访问对应网址")
        self.driver.get('https://www.baidu.com/')
        sleep(20)