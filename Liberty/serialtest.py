from appium import webdriver
from selenium.webdriver.common.by import By
from selenium import webdriver as seleniumdriver
import time
import ActionsLibrary
import random
import Core


if __name__ == '__main__':
    descaps = {
  "app": "/Users/david/Automation/Builds/Archived/axiom.app",
  "udid": "auto",
  "platformName": "iOS",
  "automationName": "XCUITest",
  "deviceName": "iPhone 7",
  "xcodeOrgId": "7P67GQ3YVX",
  "xcodeSigningId": "iPhone Developer"
}

    core = Core.Core()
    core.openSerial()
    #core.usbSerial.write('oobectl\n\r'.encode('utf-8'))
    #time.sleep(8)

    #time.sleep(8)
    #core.logevent('x03')
    core.usbSerial.write('\x03')

