import pytest
import psutil
import pytz
from appium import webdriver
from appium.webdriver.common.mobileby import MobileBy
from datetime import datetime


# 设定全局变量，这些变量应根据你的应用和设备进行调整
DESKTOP_ID = 'Home'
RECENT_TASKS_ID = 'com.android.launcher3:id/overview_actions_view'
APP_ID = 'com.android.settings:id/homepage_title'
TIME_ID = 'com.android.systemui:id/clock'
SIGNAL_STRENGTH_ID = '假定的信号强度显示元素ID'
BATTERY_ID = '假定的电量显示元素ID'

# 定义一个fixture来初始化和关闭webdriver
@pytest.fixture(scope="module")
def driver():
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
        # 其他必要的capabilities
    }
    driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)
    yield driver
    driver.quit()

# 测试状态栏在不同界面的显示是否准确
@pytest.mark.parametrize('location', [(DESKTOP_ID, '桌面'), 
                                      (RECENT_TASKS_ID, '近期任务'), 
                                      (APP_ID, '应用界面')])
def test_status_bar_display(driver, location):
    element_id , context = location
    driver.find_element(MobileBy.ID, 'com.android.settings:id/homepage_title').click()  # 假定点击进入不同的界面   点击home键
    
    # 验证时间显示是否准确
    time_display = driver.find_element(MobileBy.ID, TIME_ID).text
    # 添加适当的方法来获取当前时区的时间，然后进行比较
    assert correct_time(time_display), f'在{context}中时间显示不准确'
    
    # 验证信号强度显示是否存在
    signal_strength_display = driver.find_element(MobileBy.ID, SIGNAL_STRENGTH_ID).is_displayed()
    assert signal_strength_display, f'在{context}中信号强度没有显示'
    
    # 验证电量显示是否准确
    battery_display = driver.find_element(MobileBy.ID, BATTERY_ID).text
    # 添加适当的方法来获取当前的电量百分比，然后进行比较
    assert correct_battery_level(int(battery_display)), f'在{context}中电量显示不准确'

# 以下是辅助函数，你需要根据实际情况实现它们
def correct_time(displayed_time, displayed_format, timezone='UTC'):
    """
    检查提供的时间字符串是否与当前时区时间一致。
    
    :param displayed_time: 字符串形式的时间。
    :param displayed_format: 显示时间的格式，例如 '%H:%M:%S'。
    :param timezone: 字符串形式的时区，默认为'UTC'。
    :return: 布尔值，如果时间一致则为True，否则为False。
    """
    # 将字符串形式的时间转换为datetime对象
    try:
        displayed_time = datetime.strptime(displayed_time, displayed_format)
    except ValueError:
        return False  # 如果时间格式不正确，则返回False
    
    # 获取当前时间，使用pytz模块来考虑时区
    current_time = datetime.now(pytz.timezone(timezone))
    is_correct = correct_time('15:30', '%H:%M', 'UTC')
    print(is_correct)
    
    # 将当前时间转换为与显示时间相同的格式
    current_time_str = current_time.strftime(displayed_format)
    
    # 对比两个时间
    return displayed_time.strftime(displayed_format) == current_time_str



def correct_battery_level(displayed_battery_level):
    # 获取系统电量信息
    battery = psutil.sensors_battery()
    # 检查电量信息是否可用
    if battery is None:
        return False  # 无法获取电量信息
    # 将显示的电量与系统电量进行比较
    return battery.percent == displayed_battery_level

# 使用方法：传入一个表示电量的整数
print(correct_battery_level(100))  # 假设显示电量为85%

# correct_battery_level()