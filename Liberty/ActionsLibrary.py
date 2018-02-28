from appium import webdriver
import time
from . import Core

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

        core.start(descaps)

    def finish(self):
        core.finish()

    def getRandomOptions(self):
        return core.getRandomOptions()


    ## iOS for now

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
        core.silenceLog = True
        core.veryShortWaiting()
        while True:
            core.safeTapByID('X')
            core.safeTapByID('show space list')
            core.safeTapByID('Cancel')
            core.safeTapByClass('XCUIElementTypeButton')
            navBar = core.safeGetByClass('XCUIElementTypeNavigationBar')
            if navBar.get_attribute('name') == 'My home':
                core.silenceLog = False
                core.logEvent('Done backing all the way out.')
                break
        core.longWaiting()

    def goToOOBE(self):
        core.logEvent('Going to OOBE now through Settings.')
        #core.safeTapByID('settings')
        core.tapByNameAndClass('settings', 'XCUIElementTypeButton')
        time.sleep(2)
        core.tapByNameAndClass('settings', 'XCUIElementTypeButton')
        time.sleep(2)
        core.safeTapByID('Add device')
        time.sleep(8)


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
        

    def doOOBE(self, options):
        core.logOptions(options)

        self.goToOOBE()

        if options['checkHelp']:
            self.checkOOBEHelp()

        self.tapLibertyButton()

        if options['acceptEULA']:
            self.acceptPage()
        else:
            self.rejectPage()
            core.logEvent('EULA has been rejected, so OOBE flow is stopping here.')
            return

        if options['acceptData']:
            self.acceptPage()
            core.logEvent('Data agreement accepted.')
        else:
            self.rejectPage()
            core.logEvent('Data agreement rejected.')

        if options['useCurrentNetwork']:
            self.acceptPage()
            self.enterWiFiPassword(options['password'])
        else:
            self.useOtherNetwork(options['ssid'], options['password'])

        self.submitAndWaitForWiFi()

        if self.checkForDesiredSpace(options['spacename']):
            core.safeTapByID(options['spacename'])
        else:
            self.useCustomSpace(options['spacename'])

        self.finishOOBE()
        self.endTest('OOBE')

    ###

    def endTest(self, name):
        if core.lastTestFailed:
            core.lastTestFailed = False
            core.reportResults(name, 'FAILED')
        else:
            core.reportResults(name, 'SUCCEEDED')

    def checkOOBEHelp(self):
        core.safeTapByID('speakers_missing')
        time.sleep(2)
        core.safeTapByID('Add Speakers')
        time.sleep(2)

    def tapLibertyButton(self):
        core.logEvent('Tapping Liberty button now.')
        core.usbSerial.write('oobectl\n\r'.encode('utf-8'))
        time.sleep(8)
        if self.checkIfAtEULA():
            core.logEvent('Paired. We made it to EULA.')
        else:
            core.logEvent('We have not made it to EULA for some reason.')
        core.logEvent('Breaking out of oobectl now.')
        core.usbSerial.write('\x03')


    def acceptPage(self):
        core.safeTapByID('accept')
        time.sleep(3)

    def rejectPage(self):
        core.safeTapByID('reject')
        time.sleep(3)

    def enterWiFiPassword(self, password):
        field = core.safeGetByClass('XCUIElementTypeSecureTextField')
        field.click()
        field.send_keys(password)
        time.sleep(2)

    def submitAndWaitForWiFi(self):
        core.safeTapByID('Return')
        time.sleep(20)
        ## Are we there yet?
        try:
            core.driver.find_element_by_accessibility_id('header_space_assign')
        except:
            core.logEvent('! Having trouble connecting to WiFi !')

    def useOtherNetwork(self, ssid, password):
        core.safeTapByID('reject')
        ## We need to catch SSIDs never showing up here
        time.sleep(10)

        if not self.findSSID(ssid):
            core.lastTestFailed = True
            self.endTest('OOBE')
            return

        time.sleep(2)
        field = core.safeGetByClass('XCUIElementTypeSecureTextField')
        core.safeClick(field)
        field.send_keys(password)
        time.sleep(2)

    def findSSID(self, ssid):
        core.veryShortWaiting()
        # Milisecond time limit
        timeLimit = 20000
        startTime = time.time()
        endTime = 0
        core.silenceLog = True

        while (time.time() < (timeLimit + startTime)):

            core.shortSwipeDown()
            if core.safeTapByID(ssid):
                break
            endTime = time.time()

        core.silenceLog = False
        core.longWaiting()
        if endTime > (timeLimit + startTime):
            core.logEvent("!!! We could never find the SSID.")
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
        field.click()
        # Let the keyboard come up
        time.sleep(3)
        field.send_keys(spacename)
        time.sleep(2)
        core.safeTapByID('Next:')
        time.sleep(2)

    def finishOOBE(self):
        try:
            core.driver.find_element_by_accessibility_id('header_done')
        except:
            core.logEvent('! We could not finish OOBE for some reason !')
        core.safeTapByID('accept')
        core.logEvent('OOBE WAS COMPLETED!\n')
        time.sleep(2)

    def wipeAndReboot(self):
        core.logEvent('Wiping and rebooting the device now.')
        core.usbSerial.write('rm -r /var/appdata/*\n\r'.encode('utf-8'))
        core.usbSerial.write('reboot\n\r'.encode('utf-8'))
        self.backAllTheWayOut()
        core.tapByNameAndClass('settings', 'XCUIElementTypeButton')
        time.sleep(2)
        core.logEvent('Resetting Global Mesh Settings now.')
        core.safeTapByID('Reset Global Mesh Settings')
        time.sleep(1)
        core.safeTapByID('Done')
        time.sleep(1)
        self.backAllTheWayOut()
        time.sleep(45)
