from appium import webdriver
import time

from Liberty import ActionsLibrary


import random


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

    lib.longWaiting()

    for x in range(3):
        options = lib.getRandomOptions()
        options['acceptEULA'] = True
        lib.doOOBE(options)
        lib.wipeAndReboot()

    lib.finish()



    #fake = core.getWithinByID(collection, 'fakeElementName')





