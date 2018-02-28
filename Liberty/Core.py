from appium import webdriver
from selenium.webdriver.common.by import By
from selenium import webdriver as seleniumdriver
import time
import serial
import Logger as logger
import random


class Core:

    def __init__(self):
        self.running = 1

    def start(self, descaps):
        self.driver = webdriver.Remote(command_executor='http://localhost:4723/wd/hub', desired_capabilities=descaps)
        self.spacenames = []
        self.deviceLists = []
        self.silenceLog = False
        self.lastTestFailed = False
        self.log = logger.Logger()
        self.log.start()
        self.openSerial()

    def finish(self):
        self.log.finish()

    def openSerial(self):
        self.logEvent('Opening serial now.')
        self.usbSerial = serial.Serial(port='/dev/tty.SLAB_USBtoUART', baudrate='115200', timeout=15)
        self.logEvent('Serial open? ' + str(self.usbSerial.is_open))

    def closeSerial(self):
        self.logEvent('Closing serial now.')
        self.usbSerial.close()


    def getRandomOptions(self):
        random.seed()
        trueOrFalse = [True, False]
        randomWords = ['Red', 'Apple', 'Bowers', 'Billiard', 'Dinosaur', 'Blue', 'Media', 'Foyer', 'Atrium', 'Bottle',
                       'Cake']

        acceptData = random.choice(trueOrFalse)
        useCurrentNetwork = random.choice(trueOrFalse)
        checkHelp = random.choice(trueOrFalse)
        acceptEULA = random.choice(trueOrFalse)

        wordlist = random.sample(randomWords, 3)
        spaceName = ''
        for word in wordlist:
            spaceName = spaceName + word + ' '

        options = {'acceptData': acceptData,
                   'useCurrentNetwork': useCurrentNetwork,
                   'checkHelp': checkHelp,
                   'acceptEULA': acceptEULA,
                   'ssid': 'Rhamphorynchus',
                   'password': 'dinosaur',
                   'spacename': spaceName
                   }

        return options

    def shortWaiting(self):
        self.driver.implicitly_wait(3)
        self.logEvent('Going to short waiting.')

    def veryShortWaiting(self):
        self.driver.implicitly_wait(1)
        self.logEvent('Going to very short waiting.')

    def longWaiting(self):
        self.driver.implicitly_wait(6)
        self.logEvent('Going to long waiting.')

    def veryLongWaiting(self):
        self.driver.implicitly_wait(12)
        self.logEvent('Going to very long waiting.')

    def tapByID(self, id):
        button = self.driver.find_element_by_accessibility_id(id)
        button.click()

    def longSwipeDown(self):
        self.driver.swipe(60, 550, 0, -300, duration=1000)
        time.sleep(5)

    def shortSwipeDown(self):
        self.driver.swipe(60, 550, 0, -50, duration=2000)
        time.sleep(1)

    def dragElementDown(self, el):
        self.driver.swipe(el.location.x, el.location.y, 0, -150, duration=2000)
        time.sleep(5)

    def safeTapByID(self, id):
        try:
            time.sleep(1)
            el = self.driver.find_element_by_accessibility_id(id)
            el.click()
            return True
        except:
            self.logEvent(str("We could not tap the " + id + " element by accessibility ID."))
            self.handleFailure()
            return False

    def safeTapByClass(self, name):
        try:
            time.sleep(1)
            el = self.driver.find_element_by_class_name(name)
            el.click()
            return True
        except:
            self.logEvent(str("We could not tap the " + name + " element by class name."))
            self.handleFailure()
            return False

    def safeGetByClass(self, name):
        try:
            time.sleep(1)
            el = self.driver.find_element_by_class_name(name)
            return el
        except:
            self.logEvent(str("We could not get the " + name + " element by class name."))
            self.handleFailure()

    def safeGetByID(self, name):
        try:
            time.sleep(1)
            el = self.driver.find_element_by_accessibility_id(name)
            return el
        except:
            self.logEvent(str("We could not get the " + name + " element by accessibility ID."))
            self.handleFailure()

    def safeGetAllByClass(self, name):
        try:
            time.sleep(1)
            els = self.driver.find_elements_by_class_name(name)
            return els
        except:
            self.logEvent(str("We could not get the " + name + " elements by class name."))
            self.handleFailure()

    def safeGetAllByID(self, name):
        try:
            time.sleep(1)
            els = self.driver.find_elements_by_accessibility_id(name)
            return els
        except:
            self.logEvent(str("We could not get the " + name + " elements by accessibility ID."))
            self.handleFailure()

    def getAllWithinByClass(self, target, name):
        try:
            time.sleep(1)
            els = target.find_elements_by_class_name(name)
            return els
        except:
            self.logEvent(str("We could not get " + name + " elements within " + target.get_attribute('type') + " by class name."))
            self.handleFailure()

    def getWithinByClass(self, target, name):
        try:
            time.sleep(1)
            el = target.find_element_by_class_name(name)
            return el
        except:
            self.logEvent(str("We could not get " + name + " element within " + target.get_attribute('type') + " by class name."))
            self.handleFailure()

    def getAllWithinByID(self, target, name):
        try:
            time.sleep(1)
            els = target.find_elements_by_accessibility_id(name)
            return els
        except:
            self.logEvent(str("We could not get " + name + " elements within " + target.get_attribute('type') + " by ID."))
            self.handleFailure()

    def getWithinByID(self, target, name):
        try:
            time.sleep(1)
            el = target.find_element_by_accessibility_id(name)
            return el
        except:
            self.logEvent(str("We could not get " + name + " element within " + target.get_attribute('type') + " by ID."))
            self.handleFailure()

    def safeClick(self, el):
        try:
            time.sleep(1)
            el.click()
            return el
        except:
            try:
                self.logEvent(str("We could not safeclick the " + el.get_attribute('type') + " element"))
            except:
                self.logEvent('logEvent failed.')
            self.handleFailure()

    def tapByNameAndClass(self, name, type):
        try:
            time.sleep(1)
            els = self.driver.find_elements_by_class_name(type)
            for el in els:
                if el.get_attribute('name') == name:
                    el.click()
                    return True
            # If we got here, the element was not present; let's except
            assert 1 == 0
        except:
            self.logEvent(str("We could not tap element with name: " + name + " and class: " + type + "."))
            self.handleFailure()
            return False

    def findByNameAndClass(self, name, type):
        try:
            time.sleep(1)
            els = self.driver.find_elements_by_class_name(type)
            for el in els:
                if el.get_attribute('name') == name:
                    return True
        except:
            self.logEvent(str("We could not find element with name: " + name + " and class: " + type + "."))
            self.handleFailure()
            return False

    def findByID(self, id):
        try:
            time.sleep(1)
            if self.driver.find_element_by_accessibility_id(id):
                return True
        except:
            self.logEvent(str("We could not find element with ID: " + id + "."))
            self.handleFailure()
            return False

    def logEvent(self, string):
        if not self.silenceLog:
            self.log.addLine(string, 3)

    def reportResults(self, testName, result):
        self.log.reportResults(testName, result)

    def handleFailure(self):
        if not self.silenceLog:
            self.lastTestFailed = True
            self.log.markLine()

    def markLine(self):
        self.log.markLine()

    def logOptions(self, options):
        self.log.logOptions(options)