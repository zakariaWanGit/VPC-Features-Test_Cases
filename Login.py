
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LoginTest():
    CHROME_DRIVER_PATH = "C:\Selenium\ChromeDriverforPython\chromedriver.exe"
    INSTANCE_PATH = "https://vpc-engg.wanclouds.net/user/login"

    def __init__(self):
        # self.browser = webdriver.Chrome(executable_path=LoginTest.CHROME_DRIVER_PATH)
        pass

    def initial_setup(self, WEBSITE_PATH, DRIVER_PATH, BROWSWER_NAME="CHROME"):
        browser = BROWSWER_NAME.upper()

        try:
            if browser == "CHROME":
                self.browser = webdriver.Chrome(executable_path=DRIVER_PATH)
            elif browser == "FIREFOX":
                self.browser = webdriver.Firefox(executable_path=DRIVER_PATH)
            elif browser == "OPERA":
                self.browser = webdriver.Opera(executable_path=DRIVER_PATH)
            else:
                pass
        except Exception as err:
            print("Error Found: ", err)

        self.browser.maximize_window()
        self.browser.get(WEBSITE_PATH)

    def fill_login_attributes(self, Email, Password):
        # Email Attribute
        email = WebDriverWait(self.browser, 10).until(EC.element_to_be_clickable((By.ID, "email")))
        self.browser.execute_script("arguments[0].click();", email)
        email.send_keys(Email)

        # Password
        self.browser.find_element_by_id("password").send_keys(Password)

        # Remember Me CheckBox
        remember = self.browser.find_element_by_id("remember")
        remember.click()


    def clickLogin(self):
        loginClick = self.browser.find_element_by_xpath("//*[@id='auth']/div/div/div/section/div[2]/form/div[4]/div/div/span/button")
        # loginClick.click()
        print(loginClick)

    def closeBrowser(self):
        self.browser.close()



if __name__ == '__main__':
    CHROME_DRIVER_PATH = "C:\Selenium\ChromeDriverforPython\chromedriver.exe"
    INSTANCE_PATH = "https://vpc-engg.wanclouds.net/user/login"
    login = LoginTest()
    try:
        login.initial_setup(INSTANCE_PATH, CHROME_DRIVER_PATH, "Chrome")
        login.fill_login_attributes("zakaria@wanclouds.net", "zak@wanclouds33")
        login.clickLogin()
        print("Login Test has been Successfully Completed.")
        time.sleep(5)
        login.closeBrowser()
    except Exception as err:
        print("There is some Error: ", err)
        login.closeBrowser()
