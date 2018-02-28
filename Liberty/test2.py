from appium import webdriver
from selenium.webdriver.common.by import By
from selenium import webdriver as seleniumdriver
import time
import ActionsLibrary

if __name__ == '__main__':
    descaps = {'platformName': 'iOS',
               'deviceName': 'iPhone Simulator',
               'app': '/Users/david/Automation/Builds/Release/axiom.app',
               'automationName': 'XCUITest'}

    options = {'acceptData':True,
               'useCurrentNetwork':False,
               'checkHelp':False,
               'acceptEULA':True,
               'ssid':'Rhamphorynchus',
               'password':'dinosaur',
               'spacename':'dterry'
               }

    lib = ActionsLibrary.Library()

    lib.start(descaps)

    lib.shortWaiting()

    lib.changeMeshIDto('dterry')

    lib.backAllTheWayOut()

    lib.goToOOBE()

    lib.backAllTheWayOut()

    lib.getAllSpaceNames()

    lib.tapFirstSpaceName()

    lib.backAllTheWayOut()

    lib.getAllDevices()



    #fake = core.getWithinByID(collection, 'fakeElementName')





