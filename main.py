# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class TestRegister():

    CHROME_DRIVER_PATH = "C:\Selenium\ChromeDriverforPython\chromedriver.exe"
    INSTANCE_PATH = "https://vpc-engg.wanclouds.net/user/register"

    def __init__(self):
        pass

    def initial_setup(self):
        self.openChrome()
        self.browser.maximize_window()
        self.visitSite()

    def openChrome(self):
        self.browser = webdriver.Chrome(executable_path=TestRegister.CHROME_DRIVER_PATH)

    def visitSite(self):
        self.browser.get(TestRegister.INSTANCE_PATH)

    def fill_register_attributes(self, name, email, password, confirm):
        # self.browser.implicitly_wait(10)
        self.browser.find_element_by_xpath("//*[@id='auth']/div/div/div/section/div[2]/form/div[3]/div/div/span/a[2]").click()
        # Name
        nameElement = WebDriverWait(self.browser, 5).until(EC.element_to_be_clickable((By.ID,"name")))
        self.browser.execute_script("arguments[0].click();", nameElement)
        nameElement.send_keys(name)

        # Email
        emailElement = WebDriverWait(self.browser, 5).until(EC.element_to_be_clickable((By.ID, "email")))
        self.browser.execute_script("arguments[0].click();", emailElement)
        emailElement.send_keys(email)

        # Password
        passElement = WebDriverWait(self.browser, 5).until(EC.element_to_be_clickable((By.ID, "password")))
        self.browser.execute_script("arguments[0].click();", passElement)
        passElement.send_keys(password)

        # Confirm Password
        confirmElement = WebDriverWait(self.browser, 5).until(EC.element_to_be_clickable((By.ID, "confirm")))
        self.browser.execute_script("arguments[0].click();", confirmElement)
        confirmElement.send_keys(confirm)

        #CHeck termsAndConditions Box
        terms=self.browser.find_element_by_id("termsAndConditions")
        terms.click()

        # Click on Register
        register=self.browser.find_element_by_xpath("//*[@id='auth']/div/div/div/section/div[2]/form/div[6]/div/div/span/button")
        print(register)
        # register.click()
        time.sleep(10)

    def closeBrowser(self):
        self.browser.close()


if __name__ == '__main__':
    test = TestRegister()
    test.initial_setup()
    test.fill_register_attributes("M. Zakaria Nazir", "zakaria@wanclouds.net", "zakaria@wan1", "zakaria@wan1")
    test.closeBrowser()
