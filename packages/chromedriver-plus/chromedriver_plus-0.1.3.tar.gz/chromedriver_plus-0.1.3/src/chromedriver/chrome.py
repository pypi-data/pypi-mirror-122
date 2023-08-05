from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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
    scripts = {
        'get_user_agent': 'return navigator.userAgent',
    }

    def __init__(self, options=None, user_agent=None, profile_data=None, **kwargs):
        self.delay_per_command = rd.randint(int(.5), 1)

        self.save_password(False)

        if not options: options = uc.ChromeOptions()
        
        options.add_argument('--disable-notifications')

        if user_agent or profile_data:
            if user_agent: options.add_argument(f'--user-agent={user_agent}')
                
            if profile_data:
                user_dir = profile_data[0]
                options.user_data_dir = user_dir
                options.add_argument(f'--user-data-dir={user_dir}')

                if len(profile_data) > 1:
                    profile_dir = profile_data[1]
                    options.add_argument(f'--profile-directory={profile_dir}')

        super().__init__(options=options, keep_alive=True, **kwargs)
        
        self.set_script_timeout(self.script_timeout)
        self.set_page_load_timeout(self.page_load_timeout)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.save_password()
        super().__exit__(exc_type, exc_val, exc_tb)

    def send_keys(self, element, value, interval=.08):
        for char in value:
            element.send_keys(char)
            time.sleep(interval)

    def execute_elements(self, commands):
        commands = dict(sorted(commands.items()))

        for _, dict_value in commands.items():
            by, index, name = dict_value[:3]
            value = dict_value[-1]

            elements = self.find_elements(by, name)
            self.send_keys(elements[index], value, .05)
            time.sleep(self.delay_per_command)
    
    def get_cookie_string(self):
        cookies = self.get_cookies()
        result = ''

        for cookie in cookies:
            result += f'{cookie["name"]}={cookie["value"]};'

        return result

    def get_user_agent(self):
        result = self.execute_script(self.scripts['get_user_agent'])
        return result

    def add_cookie_string(self, value):
        cookies = value.split(';')

        for cookie in cookies:
            item = cookie.split('=')

            if len(item) > 1:
                name, cookie_value = item
                self.add_cookie({'name': name, 'value': cookie_value})

        time.sleep(.5)
        self.refresh()

    def save_password(self, save=True):
        key = winreg.CreateKeyEx(winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\Policies\Google\Chrome')
        winreg.SetValueEx(key, 'PasswordManagerEnabled', 0, winreg.REG_DWORD, 1 if save else 0)
        winreg.CloseKey(key)