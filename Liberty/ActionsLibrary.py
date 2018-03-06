from appium import webdriver
from selenium.webdriver.common.by import By
from selenium import webdriver as seleniumdriver
import time
from . import Core
import asyncio


class Library:

    global core
    core = Core.Core()

    def __init__(self):
        self.running = 1

    def start(self, descaps):
        #self.meshname = 'dterry'
        self.meshname = 'eva.mesh.default'
        self.os = descaps['platformName']
        self.spacenames = []
        self.messages = False

        #loop = asyncio.get_event_loop()
        #loop.run_until_complete(self.readSerial(loop))

        core.start(descaps)

    def finish(self):
        core.finish()
        #self.loop.close()

    def getRandomOptions(self):
        return core.getRandomOptions()

    def shortWaiting(self):
        core.shortWaiting()

    def veryLongWaiting(self):
        core.veryLongWaiting()

    def longWaiting(self):
        core.longWaiting()

    def changeMeshIDto(self, ID):
        core.tapByID('settings')
        time.sleep(2)
        core.longSwipeDown()
        core.safeTapByID('Mesh ID')

        field = core.safeGetByClass('XCUIElementTypeTextField')
        field.clear()
        field.send_keys(ID)
        core.tapByID('OK')

    def getAllSpaceNames(self):
        collection = core.safeGetByClass('XCUIElementTypeCollectionView')

        rows = core.getAllWithinByClass(collection, 'XCUIElementTypeCell')

        for row in rows:
            spacetext = core.getWithinByClass(row, 'XCUIElementTypeStaticText')
            core.spacenames.append(spacetext.get_attribute('name'))

    def tapAllSpaceNames(self):
        for space in core.spacenames:
            sbutton = core.driver.find_element_by_accessibility_id(space)
            sbutton.click()
            time.sleep(2)
            core.driver.find_element_by_accessibility_id('show space list').click()
            time.sleep(2)

    def tapFirstSpaceName(self):
        core.safeTapByID(core.spacenames[0])

    def backAllTheWayOut(self):
        core.logEvent('Backing all the way out now.')
        core.silenceLog = False
        core.veryShortWaiting()
        limit = 120
        start = time.time()
        success = False

        while time.time() < (start + limit):
            # if core.safeTapByID('X'):
            #     continue
            # if core.safeTapByID('show space list'):
            #     continue
            # if core.safeTapByID('Cancel'):
            #     continue
            # if core.safeTapByID('Done'):
            #     continue
            # if core.safeTapByID('Ignore'):
            #     continue
            core.safeTapByClass('XCUIElementTypeButton')
            core.safeTapByID('OK')
            core.safeTapByID('X')
            core.safeTapByID('show space list')
            core.safeTapByID('Cancel')
            core.safeTapByID('Done')
            core.safeTapByID('Ignore')
            core.safeTapByID('Dismiss')
            core.safeTapByID('Close')
            navBar = core.safeGetByClass('XCUIElementTypeNavigationBar')
            try:
                if navBar.get_attribute('name') == 'My home':
                    core.silenceLog = False
                    core.logEvent('Done backing all the way out.')
                    core.shortWaiting()
                    success = True
                    return True
            except:
                one = 1

        return success

    def goToOOBE(self):
        core.logEvent('Going to OOBE now through Settings.')
        timeLimit = 30
        startTime = time.time()
        core.silenceLog = True
        success = False

        while (time.time() < (timeLimit + startTime)):
            if success:
                break
            if core.safeTapByID('settings'):
                success = True
                break
            try:
                els = core.safeGetAllByClass('XCUIElementTypeButton')
                for el in els:
                    if el.get_attribute('name') == 'settings':
                        el.click()
                        success = True
                        break

                    if el.get_attribute('label') == 'settings':
                        el.click()
                        success = True
                        break
            except:
                core.silenceLog = True
                core.logEvent('Could not hit the Settings button. Trying again.')
                core.silenceLog = False

        core.silenceLog = False
        time.sleep(2)
        if not self.scrollDownAndFind('Add device', 30):
            return False
        time.sleep(8)
        return True

    def getAllDevices(self):
        for space in core.spacenames:
            deviceList = []
            core.safeTapByID(space.get_attribute('accessibility id'))
            time.sleep(2)
            els = core.safeGetAllByClass('XCUIElementTypeStaticText')
            for el in els:
                if el.get_attribute('accessibility id') == 'My home':
                    continue
                # Add the spacename first, so we know which devices are tied to what
                deviceList.append(space)
                # Add the devices
                deviceList.append(el.get_attribute('accessibility id'))
            core.deviceLists.append(deviceList)
            self.backAllTheWayOut()
            time.sleep(2)

    def tapAllDevices(self):
        for list in core.deviceLists:
            core.safeTapByID(list[0])
            time.sleep(2)
            for device in list:
                if device == list[0]:
                    continue
                core.safeTapByID(device)
                time.sleep(3)
                el = core.safeGetByID('drag_button')
                core.dragElementDown(el)
            core.safeTapByID('show space list')

    def doSoftwareUpdate(self):
        core.tapByID('settings')
        time.sleep(2)
        core.safeTapByID('System update')

    def checkIfAtEULA(self):
        if core.findByID('header_eula'):
            return True
        else:
            return False

    def checkIfAtDataOptIn(self):
        core.silenceLog = True
        try:
            el = core.safeGetByID('header_dataoptin')
            if el.get_attribute('value') == 'Data Opt-in':
                core.silenceLog = False
                return True
            if el.get_attribute('label') == 'Data Opt-in':
                core.silenceLog = False
                return True
            core.silenceLog = False
        except:
            core.silenceLog = False
            return False

    def doOOBE(self, options):
        core.logOptions(options)
        self.swapMessagesLogging(True)

        if not self.goToOOBE():
            return False

        if options['checkHelp']:
            self.checkOOBEHelp()

        if not self.connectToLWM():
            core.logEvent("LWM won't connect with us.")
            return False

        while not self.checkIfOnWiFi():

            if self.checkIfAtEULA():
                self.acceptPage()
            if self.checkIfAtDataOptIn():
                if options['acceptData']:
                    self.acceptPage()
                    core.logEvent('Data agreement accepted.')
                else:
                    self.rejectPage()
                    core.logEvent('Data agreement rejected.')

        if self.checkIfOnWiFi():
            core.logEvent('We made it to WiFi Setup.')
        else:
            core.logEvent('We should be at WiFi Setup here. But we are not. Something has gone terribly wrong. Call the president.')
            return False

        if options['useCurrentNetwork']:
            self.acceptPage()
            self.enterWiFiPassword(options['password'])
        else:
            self.rejectPage()
            self.useOtherNetwork(options['ssid'], options['password'])

        if not self.submitAndWaitForWiFi():
            return False

        if not core.findByID('header_space_assign'):
            core.logEvent('We somehow did not make it to space assignment by now. Something has gone terribly wrong. Call the president.')
            return False

        core.logEvent('We are now at space naming.')

        if self.checkForDesiredSpace(options['spacename']):
            core.safeTapByID(options['spacename'])
        else:
            self.useCustomSpace(options['spacename'])

        self.finishOOBE()
        #self.endTest('OOBE')

        return True

    def endTest(self, name):
        if core.lastTestFailed:
            core.lastTestFailed = False
            core.reportResults(name, 'FAILED')
        else:
            core.reportResults(name, 'SUCCEEDED')

    def checkOOBEHelp(self):
        core.safeTapByID('speakers_missing')
        time.sleep(1)
        core.safeTapByID('Add Speakers')
        time.sleep(1)

    def checkIfOnWiFi(self):
        core.silenceLog = True
        el = core.safeGetByID('header_dataoptin')
        try:
            if el.get_attribute('value') == 'Would you like to use your current network?':
                core.silenceLog = False
                return True
            if el.get_attribute('label') == 'Would you like to use your current network?':
                core.silenceLog = False
                return True
        except:
            one = 1
        core.silenceLog = False
        return False

    def connectToLWM(self):
        self.swapMessagesLogging(False)

        timeLimit = 45
        startTime = time.time()
        success = False
        forwardHeaders = ['header_dataoptin', 'header_eula']

        while (time.time() < (timeLimit + startTime)):
            core.logEvent('Tapping Liberty button now.')
            core.usbSerial.write('oobectl liberty\n'.encode('utf-8'))
            time.sleep(8)

            if core.findByID('header_pressbutton', True):
                core.logEvent('We have not connected to LWM yet. Trying to tap again.')
                core.usbSerial.write('\x03'.encode('utf-8'))
                time.sleep(2)
                continue

            if self.checkIfAtAny(forwardHeaders):
                core.logEvent('Successfully connected to LWM!')
                success = True
                break

        time.sleep(2)
        self.swapMessagesLogging(True)
        return success

    def checkIfAtAny(self, IDs):
        for ID in IDs:
            if core.findByID(ID):
                return True
        return False

    def acceptPage(self):
        core.safeTapByID('accept')
        time.sleep(3)

    def rejectPage(self):
        core.safeTapByID('reject')
        time.sleep(3)

    def enterWiFiPassword(self, password):
        field = core.safeGetByClass('XCUIElementTypeSecureTextField')
        try:
            field.click()
        except:
            return False
        field.send_keys(password)
        time.sleep(2)

    def submitAndWaitForWiFi(self):
        core.safeTapByID('Return')
        time.sleep (2)
        if core.findByID('header_connecting'):
            core.logEvent('Connecting to WiFi right now. Giving it some time.')
        time.sleep(20)
        ## Are we there yet?
        try:
            core.driver.find_element_by_accessibility_id('header_space_assign')
        except:
            core.logEvent('! Having trouble connecting to WiFi !')
            return False
        return True

    def useOtherNetwork(self, ssid, password):
        ## We need to catch SSIDs never showing up here
        time.sleep(10)

        if not self.findSSID(ssid):
            core.lastTestFailed = True
            #self.endTest('OOBE')
            return

        time.sleep(2)
        field = core.safeGetByClass('XCUIElementTypeSecureTextField')
        if not core.safeClick(field):
            return False
        field.send_keys(password)
        time.sleep(2)

    def findSSID(self, ssid):
        core.veryShortWaiting()

        timeLimit = 45  # Time to try in seconds

        startTime = time.time()
        core.silenceLog = True
        success = False

        while (time.time() < (timeLimit + startTime)):

            if core.safeTapByID(ssid):
                success = True
                break
            core.shortSwipeDown()

        core.silenceLog = False
        core.shortWaiting()
        if not success:
            core.logEvent("!!! We could never find the SSID !!!")
            return False

        return True

    def checkForDesiredSpace(self, spacename):
        try:
            el = core.driver.find_element_by_accessibility_id(spacename)
            return True
        except:
            core.logEvent("Spacename doesn't exist, creating a custom one.")
            return False

    def useCustomSpace(self, spacename):
        core.safeTapByID('custom')
        time.sleep(2)
        field = core.safeGetByClass('XCUIElementTypeTextField')
        try:
            field.click()
        except:
            return False
        # Let the keyboard come up
        time.sleep(3)
        field.send_keys(spacename)
        time.sleep(2)
        core.safeTapByID('Next:')
        time.sleep(2)

    def checkFailureReason(self):
        if core.findByID('Ignore', True):
            core.failureReason = 'Test failed because of a native iOS modal alert.'
            return True

    def finishOOBE(self):
        try:
            core.driver.find_element_by_accessibility_id('header_done')
        except:
            core.logEvent('! We could not finish OOBE for some reason !')
            return False
        core.safeTapByID('accept')
        core.logEvent('OOBE WAS COMPLETED!\n')
        time.sleep(1)
        return True

    def wipeAndReboot(self):
        self.swapMessagesLogging(False)

        core.usbSerial.write('\x03'.encode('utf-8'))
        core.logEvent('Wiping and rebooting the device now.')
        core.usbSerial.write('\nrm -r /var/appdata/*\n'.encode('utf-8'))
        core.usbSerial.write('\nreboot\n'.encode('utf-8'))

        self.backAllTheWayOut()
        core.tapByNameAndClass('settings', 'XCUIElementTypeButton')
        time.sleep(2)

        self.wipeGlobalMeshSettings()
        time.sleep(1)

        core.safeTapByID('Done')
        time.sleep(1)

        if not core.safeTapByID('X'):
            self.backAllTheWayOut()

        start = time.time()

        # Sleep and keep Appium alive for some seconds
        core.veryShortWaiting()
        while time.time() < start + 40:
            if time.time() % 10 == 0:
                core.findByID('complete bullshit', True)
                core.logEvent('Keeping Appium alive through reboot.')
        core.logEvent('Done keeping alive.')

        core.shortWaiting()
        self.swapMessagesLogging(True)

    def wipeGlobalMeshSettings(self):
        core.logEvent('Resetting Global Mesh Settings now.')
        success = False
        #core.silenceLog = True
        startTime = time.time()
        timeLimit = 25
        core.veryShortWaiting()
        while (time.time() < (timeLimit + startTime)):
            core.shortSwipeDown()
            if core.safeTapByID('Reset Global Mesh Settings'):
                success = True
                break
        core.shortWaiting()
        #core.silenceLog = False
        #if not success:
            #core.logEvent('We could not find the Reset Global Mesh Settings button.')
        return success

    def scrollDownAndFind(self, ID, limit):
        success = False
        startTime = time.time()
        timeLimit = limit
        core.veryShortWaiting()
        while (time.time() < (timeLimit + startTime)):
            if core.safeTapByID(ID):
                success = True
                break
            core.shortSwipeDown()
        core.shortWaiting()
        return success

    def reportOOBEFailure(self):
        core.handleFailure()
        core.logEvent('!!!OOBE TEST FAILED!!!')
        core.reportResults('OOBE', 'FAILED')

    def reportOOBESuccess(self):
        core.logEvent('OOBE TEST SUCCEEDED!')
        core.reportResults('OOBE', 'SUCCEEDED')

    def swapMessagesLogging(self, enabled):
        if enabled == True:
            self.messages = True
            core.usbSerial.write('\x03'.encode('utf-8'))
            core.usbSerial.write('\ntail -f /var/log/messages\n'.encode('utf-8'))
            time.sleep(1)
        if enabled == False:
            self.messages = False
            core.usbSerial.write('\x03'.encode('utf-8'))
            core.usbSerial.write('\x03'.encode('utf-8'))
            time.sleep(1)

    @asyncio.coroutine
    def readSerial(self, loop):
        while True:
            core.logEvent('readSerial is going.')
            if self.messages:
                core.readSerial()
            yield
