from appium import webdriver
from selenium.webdriver.common.by import By
from selenium import webdriver as seleniumdriver
import time
import Core

if __name__ == '__main__':
    descaps = {'platformName': 'Android',
               'deviceName': 'Google Pixel 2 XL',
               #'deviceName': 'Android Emulator',
               #'avd': 'Nexus_5X_API_27',
               'app': '/Users/david/android-kotlin-experiment/app/build/outputs/apk/debug/app-debug.apk'}

    core = Core.Core()
    driver = webdriver.Remote(command_executor='http://localhost:4723/wd/hub', desired_capabilities=descaps)
    core.start(driver, descaps)

    core.shortWaiting()

    core.safeTapByID('com.bowerswilkins.liberty:id/temp_start_onboarding')
    driver.find_element_by_id('com.bowerswilkins.liberty:id/temp_start_onboarding').click()
    time.sleep(2)
    driver.press_keycode(4)
    time.sleep(2)

    driver.find_element_by_id('com.bowerswilkins.liberty:id/temp_start_style_guide').click()

    core.safeTapByClass('android.widget.TextView')
    driver.press_keycode(4)





