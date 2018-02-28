from appium import webdriver
from selenium.webdriver.common.by import By
from selenium import webdriver as seleniumdriver
import time
import Core
import ActionsLibrary

if __name__ == '__main__':
    descaps = {'platformName': 'iOS',
               'deviceName': 'iPhone Simulator',
               'app': '/Users/david/Automation/Builds/Release/axiom.app',
               'automationName': 'XCUITest'}

    core = Core.Core()

    core.start(descaps)

    core.shortWaiting()
    core.tapByID('settings')
    core.longSwipeDown()
    core.safeTapByID('Mesh ID')

    field = core.safeGetByClass('XCUIElementTypeTextField')
    field.clear()
    field.send_keys(core.meshname)

    core.tapByID('OK')
    core.tapByID('X')

    collection = core.safeGetByClass('XCUIElementTypeCollectionView')

    rows = core.getAllWithinByClass(collection, 'XCUIElementTypeCell')

    for row in rows:
        spacetext = core.getWithinByClass(row, 'XCUIElementTypeStaticText')
        core.spacenames.append(spacetext.get_attribute('name'))

    for space in core.spacenames:
        sbutton = core.driver.find_element_by_accessibility_id(space)
        sbutton.click()
        time.sleep(2)
        core.driver.find_element_by_accessibility_id('show space list').click()
        time.sleep(2)

    fake = core.getWithinByID(collection, 'fakeElementName')






