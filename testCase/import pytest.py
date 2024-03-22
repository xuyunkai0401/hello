import pytest
import psutil
from appium import webdriver
import time
import re

from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# 设定Appium所需的desired capabilities
desired_caps = {
        'platformName': 'Android',
        'platformVersion': '14',  # 替换成您的设备 Android 版本
        'deviceName': 'X9 U',  # 替换成您的设备名称
        'appPackage': 'com.android.launcher3',  # 闹钟应用的包名
        'appActivity': 'com.android.searchlauncher.SearchLauncher',  # 闹钟应用的活动名称
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
    # 你的Appium配置
}

# 初始化webdriver
@pytest.fixture(scope="module")
def driver():
    driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)
    yield driver
    driver.quit()

def test_battery_level(driver):
    # 打开通知栏以获取电量信息
    driver.open_notifications()
    wait = WebDriverWait(driver, 10)  # 适当的等待时间确保通知栏已打开

    # 定位电量信息元素并获取其content-desc属性值
    battery_info_element = wait.until(EC.presence_of_element_located((MobileBy.ACCESSIBILITY_ID, "Battery charging, 100 percent.")))

    battery_info = battery_info_element.get_attribute("content-desc")


    # 打印content-desc属性值以进行调试
    print(f"Content-desc attribute value: {battery_info}")

    # 如果battery_info为None，则无法进行比较，需要调查为什么没有获取到属性
    if battery_info is None:
        raise ValueError("Failed to retrieve the content-desc attribute for the battery information element.")

    # 使用正则表达式从content-desc中提取电量百分比
    matches = re.search(r"\d+%", battery_info)
    if matches:
        battery_level = int(matches.group()[:-1])  # 去除末尾的百分号
        print(f"Battery level from UI: {battery_level}")
    else:
        raise ValueError("Battery percentage not found in content-desc attribute.")

    # 获取系统电量百分比并进行比较
    system_battery = psutil.sensors_battery()
    system_battery_level = system_battery.percent
    print(f"System battery level: {system_battery_level}")

    # 断言比较电量百分比是否匹配
    assert battery_level == system_battery_level, "电量显示不正确"