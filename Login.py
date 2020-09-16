
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class LoginTest():
    def __init__(self):
        pass

    #  Open Choice Browser of Chrome and Mozilla and Website of given URL
    def initial_setup(self, WEBSITE_PATH, DRIVER_PATH, BROWSWER_NAME="CHROME"):
        browser = BROWSWER_NAME.upper()
        try:
            if browser == "CHROME":
                self.browser = webdriver.Chrome()
            elif browser == "FIREFOX":
                self.browser = webdriver.Firefox()
            else:
                pass
        except Exception as err:
            print("Error Found: ", err)
        else:
            self.browser.maximize_window()
            self.browser.get(WEBSITE_PATH)

    

    #  VPC Login Form Attributes filling
    def fill_VPC_login_attributes(self, Email, Password, rememberMe):
            # Email input 
        email = WebDriverWait(self.browser, 10).until(EC.element_to_be_clickable((By.ID, "email")))
        self.browser.execute_script("arguments[0].click();", email)
        email.send_keys(Email)

            # Password input
        self.browser.find_element_by_id("password").send_keys(Password)

            # Unchecking Remember Me CheckBox 
        if rememberMe:
            remember = self.browser.find_element_by_id("remember")
            remember.click()


    # Triggering the Login Button 
    def clickVPVLoginButton(self):
        loginButton = self.browser.find_element_by_xpath("/html/body/div/div/div/div[2]/div/div/div/section/div[2]/form/div[3]/div/div/span/button")
        loginButton.click()
        time.sleep(5)

    # Login to Gmail Account 
    def loginToGmail(self, gmail_url, email, password):
        
        self.openGmail(gmail_url)
        self.fill_GMAIL_login_attributes(email, password)
        time.sleep(10)
        self.browser.refresh()

    # Open Gmail Login Page
    def openGmail(self, URL):
        self.browser.execute_script("window.open('');")
        url = "https://accounts.google.com/signin/v2/identifier?service=mail&passive=true&rm=false&continue=https%3A%2F%2Fmail.google.com%2Fmail%2F&ss=1&scc=1&ltmpl=default&ltmplcache=2&emr=1&osid=1&flowName=GlifWebSignIn&flowEntry=ServiceLogin"
        self.browser.switch_to.window(self.browser.window_handles[1])
        self.browser.get(url)

    
    def fill_GMAIL_login_attributes(self, email, password):
        # Email
        self.browser.find_element_by_id("identifierId").send_keys(email)
        nextToPassword = self.browser.find_element_by_xpath("//*[@id='identifierNext']/div/button/div[2]")
        nextToPassword.click()
        # Password

        pasd = WebDriverWait(self.browser, 10).until(EC.element_to_be_clickable((By.NAME, "password")))
        self.browser.execute_script("arguments[0].click();", pasd)
        pasd.send_keys(password)

        # password = self.browser.find_element_by_name("password").send_keys(password)
        enterPassword = self.browser.find_element_by_xpath("//*[@id='passwordNext']/div/button/div[2]")
        enterPassword.click()


    def fetch_TFA_PinCode(self):
        # Get  last Email
        lastEmail = WebDriverWait(self.browser, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "zA")))
        
        totalEmails=""
        
        # Get Pincode's total no of emails
        if (lastEmail):
            emailText = lastEmail.text
            emailCount = emailText[9:11]
            noOfEmails =  '\n' in emailCount
            if (noOfEmails):
                totalEmails = emailText[9:10]
            else:
                totalEmails = emailCount
        print("Total Emails counts : ",totalEmails)

        # Open Latest/Last Email
        self.browser.execute_script("arguments[0].click();", lastEmail)
        openedEmail = WebDriverWait(self.browser, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[7]/div[3]/div/div[2]/div[1]/div[2]/div/div/div/div/div[2]/div/div[1]/div/div[2]/div/table/tr/td[1]/div[2]/div[2]/div/div[3]/div["+totalEmails+"]/div/div/div/div/div[1]/div[2]/div[3]/div[3]/div[1]/table/tbody/tr/td/center/table/tbody/tr/td/table/tbody/tr[3]/td/div")))
        
        emailContent = openedEmail.text
        pinIndex = emailContent.find("?pin")
        pin = emailContent[pinIndex + 5: ]
        print("All the Email Content is here: ", emailContent)
        print("PrintIndex : ", pinIndex)
        print("Here is the Pin : ",pin)
        time.sleep(5)

        # Switch From Gmail window to VPC Pincode verification window
        self.browser.switch_to.window(self.browser.window_handles[0])

        # Input Fetched PinCode
        pinCodeInput = WebDriverWait(self.browser, 10).until(EC.element_to_be_clickable((By.ID, "pinCode")))
        self.browser.execute_script("arguments[0].click();", pinCodeInput)
        pinCodeInput.send_keys(pin)

        # Click on Verify Button
        verify = self.browser.find_element_by_xpath("/html/body/div/div/div/div[2]/div/div/div/section/div[2]/form/div[2]/div/div/span/button")
        verify.click()

    def closeBrowser(self):
        self.browser.quit()

    def closeCurrentTab(self):
        self.browser.close()



if __name__ == '__main__':

    # Browser Drivers
    CHROME_DRIVER_PATH = "/home/m_zakaria/Seleniym/chromedriver_linux64/chromedriver.sh"
    Firefox_DRIVER_PATH = "/home/m_zakaria/Selenium/geckodriver-v0.27.0-linux64/geckodriver.sh"

    # Base Url for First time opening the browser
    INSTANCE_PATH = "https://vpc-engg.wanclouds.net/user/login"

    # VPC Login Details
    VPC_EMAIL = "zakaria@wanclouds.net"
    VPC_PASSWORD = "zak@wanclouds33"
    VPC_REMEMBER_CHECKBOX = True  # True means to uncheck the Remember me Checkbox, By default It is checked, 
    
    # Gmail login Details
    GMAIL_URL = "https://accounts.google.com/signin/v2/identifier?service=mail&passive=true&rm=false&continue=https%3A%2F%2Fmail.google.com%2Fmail%2F&ss=1&scc=1&ltmpl=default&ltmplcache=2&emr=1&osid=1&flowName=GlifWebSignIn&flowEntry=ServiceLogin"
    GMAIL_EMAIL = "zakaria@wanclouds.net"
    GMAIL_PASSWORD = "zakWan33"  

    login = LoginTest()

    try:
        login.initial_setup(INSTANCE_PATH, CHROME_DRIVER_PATH, "CHROME")
        login.fill_VPC_login_attributes("zakaria@wanclouds.net", "zak@wanclouds33", True)
        login.clickVPVLoginButton()
        login.loginToGmail(GMAIL_URL, GMAIL_EMAIL, GMAIL_PASSWORD)
        login.fetch_TFA_PinCode()
        print("Login Test has been Successfully Completed.")
        time.sleep(5)
        login.closeBrowser()
        
    except Exception as err:
        print("There is some Error: ", err)
        login.closeBrowser()
