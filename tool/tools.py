#!/usr/bin/python
from appium import webdriver
from tool import adb_shell
from core.read_config import config
import os


def get_yaml_path(filename):
    yaml_path = os.path.join(config.BASE_DIR, "data", filename)
    return yaml_path


def get_host(port=None):
    host = "http://127.0.0.1:4723/wd/hub"
    if port:
        host = "http://127.0.0.1:{}/wd/hub".format(port)
    return host


def get_capabilities(**kwargs):
    app_path = os.path.join(config.BASE_DIR, 'app', 'tzkt.apk')
    capabilities = {
        # 平台：Android / iOS
        'platformName': 'Android',
        # 设备地址
        'deviceName': '127.0.0.1:62001',
        # 模拟器或手机的版本
        'platformVersion': '7.1.2',
        # apk包名
        'appPackage': 'com.sgkt.phone',
        # apk的launcherActivity
        'appActivity': 'com.sgkt.phone.ui.activity.AppStartActivity',
        'app': app_path,
    }
    if kwargs:
        capabilities.update(**kwargs)
    return capabilities


def get_appium_driver(port=None, **kwargs):
    host = get_host(port)
    capabilities = get_capabilities(**kwargs)
    driver = webdriver.Remote(host, capabilities)
    return driver


if __name__ == '__main__':
    get_appium_driver()
