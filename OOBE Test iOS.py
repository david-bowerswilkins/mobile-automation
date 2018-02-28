from appium import webdriver
from selenium.webdriver.common.by import By
from selenium import webdriver as seleniumdriver
import time
import random

from Liberty import ActionsLibrary

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


    lib = ActionsLibrary.Library()

    lib.start(descaps)

    lib.shortWaiting()

    while True:
        options = lib.getRandomOptions()
        options['acceptEULA'] = True

        if not lib.doOOBE(options):
            lib.checkFailureReason()
            lib.reportOOBEFailure()
        else:
            lib.reportOOBESuccess()

        lib.wipeAndReboot()


    lib.finish()



    #fake = core.getWithinByID(collection, 'fakeElementName')





