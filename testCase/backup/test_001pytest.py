from appium import webdriver
from appium.webdriver.common.mobileby import MobileBy
import pytest
import time
import os
from time import sleep
import allure
from allure_commons.types import AttachmentType
from allure_commons.reporter import AllureReporter

# For W3C actions
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput

@pytest.fixture(scope="module")
def driver():
    desired_caps = {
        'platformName': 'Android',
        'platformVersion': '14',  # 替换成您的设备 Android 版本
        'deviceName': 'X9 U',  # 替换成您的设备名称
        'appPackage': 'com.android.deskclock',  # 闹钟应用的包名
        'appActivity': '.DeskClock',  # 闹钟应用的活动名称
        'automationName': 'UiAutomator2',
        'noReset': True,
        'appium:unicodeKeyboard': True,
        'appium:resetKeyboard': True,
        'appium:noReset': True,
        'appium:skipUnlock': True,
        'appium:ensureWebviewsHavePages': True,
        'appium:nativeWebScreenshot': True,
        'appium:newCommandTimeout': 3600,
        'appium:connectHardwareKeyboard': True
        }
        # Instantiate the Appium driver
    driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)
    yield driver
        # Teardown the Appium driver
    driver.quit()


        # Test function to add an alarm using the Alarm Clock app

@allure.feature('Alarm Clock Tests')
@allure.story('Add Alarm Test')
@pytest.mark.alarm
def test_add_alarm(driver):
    driver.implicitly_wait(10)

    with allure.step('Click Add Alarm Button'):
        driver.find_element(MobileBy.ID, 'com.android.deskclock:id/floating_button').click()
        time.sleep(1)

    with allure.step('Set Alarm Time'):
        def adb_swipe():
            os.system("adb shell input swipe 675 620 675 463 200")
            sleep(3.0)
        adb_swipe()

    with allure.step('Confirm Alarm'):
        actions = ActionChains(driver)
        actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        actions.w3c_actions.pointer_action.move_to_location(803, 2184)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.pause(0.1)
        actions.w3c_actions.pointer_action.release()
        actions.perform()
        time.sleep(59)

    with allure.step('Verify Alarm Notification'):
        driver.open_notifications()
        time.sleep(4)
        snooze_button = driver.find_elements(MobileBy.XPATH,'//android.widget.Button[@content-desc="Snooze"]')
        assert len(snooze_button) > 0, "未检测到闹钟响起的通知"

    # Optionally take a screenshot for Allure report
    allure.attach(driver.get_screenshot_as_png(), name="screenshot", attachment_type=AttachmentType.PNG)

    def tearDown(self):
        if hasattr(self, 'driver'):
            self.driver.quit()