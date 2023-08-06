import os
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType, os_type
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriver
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.firefox.options import Options
import time


class SelEx:
    driver = webdriver.Chrome
    remote = False
    huburl = None
    browser = ""
    browserversion = None
    os = None
    osversion = None
    device = None
    deviceorientation = None

    # def __init__(self, attr):
    # self.driver = attr

    @staticmethod
    def FrameworkInitialize():
        SelEx.GetExecutionDetails()

    @staticmethod
    def LaunchDriver(desiredCap=None, driverOptions=None):
        # SelEx.GetExecutionDetails()
        if not SelEx.remote:
            if SelEx.browser.lower() == "chrome":
                if driverOptions is None:
                    driverOptions = webdriver.ChromeOptions()
                    prefs = {'download.prompt_for_download': False}
                    driverOptions.add_experimental_option("prefs", prefs)
                    driverOptions.add_argument('disable-web-security')
                    driverOptions.add_argument('ignore-certificate-errors')
                    driverOptions.add_argument('disable-infobars')
                else:
                    prefs = {'download.prompt_for_download': False}
                    driverOptions.add_experimental_option("prefs", prefs)
                    driverOptions.add_argument('disable-web-security')
                    driverOptions.add_argument('ignore-certificate-errors')
                if desiredCap is None:
                    desiredCap = webdriver.DesiredCapabilities.CHROME.copy()
                    desiredCap['acceptSslCerts'] = True
                else:
                    desiredCap['acceptSslCerts'] = True

                SelEx.driver = webdriver.Chrome(ChromeDriverManager().install(),
                                                desired_capabilities=desiredCap, chrome_options=driverOptions)
            elif SelEx.browser.lower() == "firefox":
                if driverOptions is None:
                    driverOptions = Options()
                if desiredCap is None:
                    desiredCap = webdriver.DesiredCapabilities.FIREFOX.copy()
                    desiredCap['marionette'] = True
                else:
                    desiredCap['marionette'] = True

                SelEx.driver = webdriver.Firefox(executable_path=GeckoDriverManager().install(),
                                                 desired_capabilities=desiredCap, options=driverOptions)
            elif SelEx.browser.lower() == "edge":
                if desiredCap is None:
                    desiredCap = webdriver.DesiredCapabilities.EDGE.copy()
                    desiredCap['acceptSslCerts'] = True
                    desiredCap['javascriptEnabled'] = True
                    # SelEx.driver =
                else:
                    desiredCap['acceptSslCerts'] = True
                    desiredCap['javascriptEnabled'] = True
                    SelEx.driver = webdriver.Edge(executable_path=EdgeChromiumDriverManager().install(),
                                                  capabilities=desiredCap)
            SelEx.driver.maximize_window()
        else:
            if 'browserstack' in SelEx.huburl:
                desiredCap = SelEx.ConstructBrowserStackCapabilities(SelEx.os, SelEx.browser, SelEx.browserversion,
                                                                     SelEx.osversion, 'false', SelEx.device,
                                                                     SelEx.deviceorientation)
            if desiredCap is None:
                if SelEx.browser.lower() == "chrome":
                    desiredCap = webdriver.DesiredCapabilities.CHROME
                    desiredCap['acceptSslCerts'] = True
                elif SelEx.browser.lower() == "firefox":
                    desiredCap = webdriver.DesiredCapabilities.FIREFOX
                elif SelEx.browser.lower() == "safari":
                    desiredCap = webdriver.DesiredCapabilities.SAFARI
                elif SelEx.browser.lower() == "edge":
                    desiredCap = webdriver.DesiredCapabilities.EDGE
            if driverOptions is None:
                if SelEx.browser.lower() == "chrome":
                    driverOptions = webdriver.ChromeOptions()
                    driverOptions.add_argument('disable-web-security')
                    driverOptions.add_argument('ignore-certificate-errors')
                elif SelEx.browser.lower() == "firefox":
                    driverOptions = webdriver.FirefoxOptions
            SelEx.driver = webdriver.Remote(SelEx.huburl, desired_capabilities=desiredCap)

        return SelEx.driver

    @staticmethod
    def WaitForPageLoad(timeOut=50):
        wait = WebDriverWait(SelEx.driver, 2)
        start_time = time.time()
        state = SelEx.driver.execute_script('return document.readyState') == 'complete'
        while not state:
            current_time = time.time()
            elapsed_time = current_time - start_time
            state = SelEx.driver.execute_script('return document.readyState') == 'complete'
            if elapsed_time > timeOut | state:
                break

    @staticmethod
    def WaitForElement(element):
        wait = WebDriverWait(SelEx.driver, 2)
        wait.until(EC.visibility_of_element_located(element))

    @staticmethod
    def GetProjectPath():
        return os.path.realpath('')

    @staticmethod
    def GetWorkingDirectory():
        return os.path.dirname(__file__)

    @staticmethod
    def GetExecutionDetails():
        dir = SelEx.GetProjectPath()
        executionenvironmentpath = os.path.join(dir, 'TestData\executionenvironment.txt')
        file = open(executionenvironmentpath, 'r')
        executiondetails = file.readlines()
        for str in executiondetails:
            command = str.split('|')[0]
            value = str.split('|')[1].strip('\n')
            if value.lower() is 'none':
                value = None
            elif value is '':
                value = None
            if command == 'remote':
                if value == 'true':
                    SelEx.remote = True
                else:
                    SelEx.remote = False
            elif command == 'huburl':
                SelEx.huburl = value
            elif command == 'browser':
                SelEx.browser = value
            elif command == 'browserversion':
                SelEx.browserversion = value
            elif command == 'os':
                SelEx.os = value
            elif command == 'osversion':
                SelEx.osversion = value
            elif command == 'device':
                SelEx.device = value
            elif command == 'orientation':
                SelEx.deviceorientation = value

    @staticmethod
    def ConstructBrowserStackCapabilities(OS, browser, browserVersion=None, OSVersion=None, browserStackLocal='false',
                                          device=None, deviceOrientation=None):
        desiredCap = {
            "OS": OS,
            "browser": browser,
            "browserstack.local": browserStackLocal
        }

        if OSVersion != 'None':
            desiredCap['os_version'] = OSVersion
        if browserVersion != 'None':
            desiredCap['browser_version'] = browserVersion
        if device != 'None':
            desiredCap['device'] = device
            desiredCap['real_mobile'] = "true"
        if deviceOrientation is not None:
            desiredCap['deviceOrientation'] = deviceOrientation

        return desiredCap

    """
    @staticmethod
    def HighlightElement(element):
        script = r"arguments[0].style.cssText = ""border-width: 4px; border-style: solid; border-color: red""; "
        SelEx.driver.execute_script(script, element)
        time.sleep(2)
        clearscript = r"arguments[0].style.cssText = ""border-width: 0px; border-style: solid; border-color: red""; "
        SelEx.driver.execute_script(clearscript, element)"""
