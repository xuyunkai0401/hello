# baseIni.py 文件内容
class BaseConfig:
    def __init__(self):
        self.desired_caps = {
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
    
    def get_desired_capabilities(self):
        return self.desired_caps

    def get_appium_server_url(self):
        return 'http://localhost:4723/wd/hub'