from selenium.webdriver.support.ui import WebDriverWait
from http.cookies import SimpleCookie

import undetected_chromedriver.v2 as uc
import random as rd
import time
import ctypes
import winreg

class WindowSort:
    def __init__(self, chrome_width, chrome_height):
        self.chrome_width = chrome_width
        self.chrome_height = chrome_height
        self.user32 = ctypes.windll.user32

        self.user32.SetProcessDPIAware()

    def __call__(self, drivers):
        x, y = 1, 1
        window_width = self.user32.GetSystemMetrics(0)

        for driver in drivers:
            driver.set_window_rect(x, y, self.chrome_width, self.chrome_height)
            time.sleep(.5)

            x += self.chrome_width + 105
            window_width -= x
            
            if not window_width < self.chrome_width: continue

            x = 1
            y += self.chrome_height + 5
            window_width = self.user32.GetSystemMetrics(0)

class ChromePlus(uc.Chrome):
    timeout = 30
    script_timeout = 9999
    page_load_timeout = 60

    def __init__(self, options=None, user_agent=None, profile_data=None, **kwargs):
        self.save_your_pwd(False)

        if not options: options = uc.ChromeOptions()
        
        options.add_argument('--disable-notifications')

        if user_agent or profile_data:
            if user_agent: options.add_argument(f'--user-agent={user_agent}')
                
            if len(profile_data):
                user_dir = profile_data[0]
                options.user_data_dir = user_dir
                options.add_argument(f'--user-data-dir={user_dir}')

                if len(profile_data) > 1: options.add_argument(f'--profile-directory={profile_data[1]}')

        super().__init__(options=options, keep_alive=True, **kwargs)
        
        self.set_script_timeout(self.script_timeout)
        self.set_page_load_timeout(self.page_load_timeout)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.save_your_pwd()
        super().__exit__(exc_type, exc_val, exc_tb)

    def send_keys(self, element, value, interval=.08):
        for char in value:
            element.send_keys(char)
            time.sleep(interval)

    def execute_elements(self, commands):
        for command in commands:
            method = command[0]
            element = WebDriverWait(self, self.timeout).until(method)

            time.sleep(1.5)

            if isinstance(element, list) and len(command[1:]) > 2:
                element = element[command[1]]

            if len(command) > 1 and len(command) < 3:
                callback = command[-1]
                callback(element)
            else:
                value, callback = command[2 if len(command[1:]) > 2 else 1:]
                if not isinstance(value, int):
                    callback(element, value)
                    continue

                callback(element[value])
    
    def get_cookie_str(self):
        cookies = self.get_cookies()
        result = ''

        for cookie in cookies:
            result += f'{cookie["name"]}={cookie["value"]};'

        return result

    def get_user_agent(self):
        return self.execute_script('return navigator.userAgent')

    def add_cookie_str(self, value):
        cookie = SimpleCookie()
        cookie.load(value)

        for key, morsel in cookie.items():
            self.add_cookie({
                'name': key,
                'value': morsel.value
            })
                
        time.sleep(.5)
        self.refresh()

    def save_your_pwd(self, value=True):
        key = winreg.CreateKeyEx(winreg.HKEY_LOCAL_MACHINE,
                                    r'SOFTWARE\Policies\Google\Chrome')
        winreg.SetValueEx(key, 'PasswordManagerEnabled',
                            0, winreg.REG_DWORD, 1 if value else 0)
        winreg.CloseKey(key)