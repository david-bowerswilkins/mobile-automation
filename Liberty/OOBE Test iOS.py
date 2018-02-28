from appium import webdriver
import time


import importlib.util
spec = importlib.util.spec_from_file_location("ActionsLibrary", "/Users/david/Automation/mobile-automation/Liberty/ActionsLibrary.py")
foo = importlib.util.module_from_spec(spec)
spec.loader.exec_module(foo)

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





