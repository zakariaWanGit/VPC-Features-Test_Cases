
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.expected_conditions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait


class LoginTest():
    def __init__(self):
        pass

    #  Open Choice Browser of Chrome and Mozilla and Website of given URL
    def initial_setup(self, WEBSITE_PATH,BROWSWER_NAME="CHROME"):
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

    
    def check_pinCode_page(self):
        current_url = self.browser.current_url
        # return WebDriverWait(self.browser, 10).until(EC.url_contains("https://vpc-engg.wanclouds.net/user/two-factor-auth"))
        if "https://vpc-engg.wanclouds.net/user/two-factor-auth" in current_url:
            return True
        else:
            return False
        

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
        
        print(lastEmail)
        totalEmails=""
        for i, e in enumerate(lastEmail.text):
            print(i, e)
        
        # Get Pincode's total no of emails
        if (lastEmail):
            emailText = lastEmail.text
            emailCount = emailText[9:11]
            noOfEmails =  '\n' in emailCount
            if (noOfEmails):
                totalEmails = emailText[9:10]
            elif '\n' == emailText[9:9]:
                totalEmails = emailText[9:9]
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

        # Closes Gmail Tab
        self.closeCurrentTab()

        # Switch From Gmail window to VPC Pincode verification window
        self.browser.switch_to.window(self.browser.window_handles[0])

        # Input Fetched PinCode
        pinCodeInput = WebDriverWait(self.browser, 10).until(EC.element_to_be_clickable((By.ID, "pinCode")))
        self.browser.execute_script("arguments[0].click();", pinCodeInput)
        pinCodeInput.send_keys(pin)

        # Click on Verify Button
        verify = self.browser.find_element_by_xpath("/html/body/div/div/div/div[2]/div/div/div/section/div[2]/form/div[2]/div/div/span/button")
        verify.click()



                                                # IBM VPC CLOUD


    def click_SummaryPage_addButton(self):
        if self.browser.current_url == "https://vpc-engg.wanclouds.net/summary":
            addButton = WebDriverWait(self.browser, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div/div[2]/section/section/main/div/div[1]/div/div/div/a")))
            self.browser.execute_script("arguments[0].click()", addButton)
        else:
            raise Exception("Couldn't find this URL: https://vpc-engg.wanclouds.net/summary  For Adding Cloud.")

        # self.browser.find_element_by_xpath("/html/body/div[1]/div/div/div[2]/section/section/main/div/div[1]/div/div/div/a").click()
        

    def add_IBM_VPC_Cloud(self, NAME, API_KEY, INSTANCE_ID):
        requiredURL = "https://vpc-engg.wanclouds.net/cloud-accounts/ibm-cloud"
        # if self.browser.current_url == requiredURL:
        assert self.browser.current_url == requiredURL, "The Required URL is missing : " + requiredURL
        name = WebDriverWait(self.browser,10).until(EC.element_to_be_clickable((By.ID, "name")))
        self.browser.execute_script("arguments[0].click()", name)
        name.send_keys(NAME)
        error = WebDriverWait(self.browser,2).until(EC.invisibility_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div[2]/section/section/main/main/div/div/div[1]/div[2]/form/div[1]/div[2]/div/div")))
        print(error)
        if error == True:
            self.browser.find_element_by_id("apiKey").send_keys(API_KEY)
            self.browser.find_element_by_id("resourceInstanceId").send_keys(INSTANCE_ID)
        else:
            error = WebDriverWait(self.browser,2).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div/div[2]/section/section/main/main/div/div/div[1]/div[2]/form/div[1]/div[2]/div/div")))
            assert error.text != "Cloud Account with same name already exists", "Cloud Account with same name already exists"
        # else:
        #     raise Exception("The Required URL is missing : ", requiredURL)
    def check_cloudInfo(self):
            pass

    def display_cloudAdding_message(self):
        print("Waiting for Cloud to Add")
        WebDriverWait(self.browser, 30).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "html body div div.ant-notification.ant-notification-bottomRight span div.ant-notification-notice.ant-notification-notice-closable")))
        message = self.browser.find_element_by_css_selector("div > div > div > div.ant-notification-notice-description")
        assert message.text != 'A cloud account with same API Key already exists', 'A cloud account with same API Key already exists'
        print(message.text)

    def check_addedAccount(self, vpc_name):
        alreadyAddedAccounts =self.browser.find_elements_by_xpath("/html/body/div[1]/div/div/div[2]/section/section/main/main/div/div/div/div/div/div/div/ul/li")
        for ele in alreadyAddedAccounts:
            element = ele.text
            elementText = element.split("\n")
            username = elementText[0]
            status = elementText[1]
            if(vpc_name == username):
                print("Receltly Added ACCOUNT username : ", username)
                print("Recently added account status : ", status)


                                                # Cloud Common Functions

    # To add a new Account from "Cloud Accounts" page
    def click_Cloud_AddButton(self):
        self.browser.find_element_by_xpath("/html/body/div[1]/div/div/div[2]/section/section/main/main/div/div/button").click()

    # To Add a new Account after credentials input
    def click_AddCloudAccount(self):
        self.browser.find_element_by_xpath("/html/body/div[1]/div/div/div[2]/section/section/main/main/div/div/div[1]/div[2]/form/div[4]/div/div/span/span[1]/button").click()

    # To cancel adding new account 
    def click_CancelAddingCloudAccount(self):
        self.browser.find_element_by_xpath("/html/body/div[1]/div/div/div[2]/section/section/main/main/div/div/div[1]/div[2]/form/div[4]/div/div/span/span[2]/button").click()

    

                                                # IBM Classis Cloud 

    def click_ClassicCloud(self):
        self.browser.find_element_by_xpath("/html/body/div[1]/div/div/div[2]/section/section/main/ul/li[4]/a").click()
        # self.click_Cloud_AddButton()

    def click_Classic_getStarted(self):
        try:
            get = WebDriverWait(self.browser, 2).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "html body div#root div#app-wrapper div div section.ant-layout.ant-layout-has-sider section.ant-layout main#main-content.ant-layout-content main#cloud-accounts.content-wrapper.ant-layout-content div.ant-card.card-wrapper.ant-card-bordered div.ant-card-body div.ant-row.margin-top-lg div.ant-col.ant-col-24.gutter-row.align-center")))
            print("Get Started",get)
            # if get == True:
            getStarted = WebDriverWait(self.browser, 2).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div/div[2]/section/section/main/main/div/div/div/div/button")))
            self.browser.execute_script("arguments[0].click()", getStarted)
            # else:
        except Exception as er:
            self.browser.find_element_by_xpath("/html/body/div[1]/div/div/div[2]/section/section/main/main/div/div/button").click()
            

        # addButton = WebDriverWait(self.browser, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "html body div#root div#app-wrapper div div section.ant-layout.ant-layout-has-sider section.ant-layout main#main-content.ant-layout-content main#cloud-accounts.content-wrapper.ant-layout-content div.ant-card.card-wrapper.ant-card-bordered div.ant-card-body button.ant-btn.add-button.margin-bottom-lg.float-right.margin-y-md.ant-btn-primary")))
        # print(addButton.text)
        # if(addButton.text == "Add Account"):
        #     self.browser.find_element_by_xpath("/html/body/div[1]/div/div/div[2]/section/section/main/main/div/div/button").click()
        # else:
        #     getStarted = WebDriverWait(self.browser, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div/div[2]/section/section/main/main/div/div/div/div/button")))
        #     self.browser.execute_script("arguments[0].click()", getStarted)

    
    def add_IBM_Classic_Cloud(self, NAME, USERNAME, API_KEY):
        name = WebDriverWait(self.browser,10).until(EC.element_to_be_clickable((By.ID, "name")))
        self.browser.execute_script("arguments[0].click()", name)
        name.send_keys(NAME)
        error = WebDriverWait(self.browser,2).until(EC.invisibility_of_element_located((By.XPATH, "//*[@id='cloud-accounts']/div/div/div[1]/div[2]/form/div[1]/div[2]/div/div")))
        print(error)
        if error == True:
            self.browser.find_element_by_id("username").send_keys(USERNAME)
            usernameError = WebDriverWait(self.browser,2).until(EC.invisibility_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div[2]/section/section/main/main/div/div/div[1]/div[2]/form/div[2]/div[2]/div/div")))
            print(usernameError)
            if(usernameError == True):
                self.browser.find_element_by_id("apiKey").send_keys(API_KEY)
            else:
                error = WebDriverWait(self.browser,2).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div/div[2]/section/section/main/main/div/div/div[1]/div[2]/form/div[2]/div[2]/div/div")))
                assert error.text != "Cloud Account with same username already exists", "Cloud Account with same username already exists"
        else:
            error = WebDriverWait(self.browser,2).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='cloud-accounts']/div/div/div[1]/div[2]/form/div[1]/div[2]/div/div")))
            assert error.text != "Cloud Account with same name already exists", "Cloud Account with same name already exists"
            # html body div div.ant-notification.ant-notification-bottomRight span div.ant-notification-notice.ant-notification-notice-closable div.ant-notification-notice-content div.ant-notification-notice-with-icon div.ant-notification-notice-description
        
            # html body div div.ant-notification.ant-notification-bottomRight span
    def display_classicAdding_message(self):
        print("Waiting for Cloud to Add")
        message = WebDriverWait(self.browser, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".ant-notification-notice-description")))
        # message = self.browser.find_element_by_css_selector("div > div > div > div.ant-notification-notice-description")
        assert message.text != 'A cloud account with same API Key already exists', 'A cloud account with same API Key already exists'
        print(message.text)

    def check_classic_status(self):
        # /html/body/div[1]/div/div/div[2]/section/section/main/main/div/div/div/div/div/div/div/ul
        pass

    # Add Cloud for IBM VPC Cloud 
    def run_adding_IBM_VPC(self, VPC_NAME, VPC_API_KEY, VPC_INSTANCE_ID):
        self.add_IBM_VPC_Cloud(VPC_NAME, VPC_API_KEY, VPC_INSTANCE_ID)
        self.click_AddCloudAccount()
        self.check_cloudInfo()
        self.display_cloudAdding_message()
        self.browser.refresh()
        self.check_addedAccount(VPC_NAME)

    # # Add Cloud for Classic Account
    def run_adding_IBM_Classic_Cloud(self,CLASSIC_NAME,CLASSIC_USERNAME, CLASSIC_API_KEY):
        self.click_ClassicCloud()
        self.click_Classic_getStarted()
        self.add_IBM_Classic_Cloud(CLASSIC_NAME, CLASSIC_USERNAME, CLASSIC_API_KEY)
        self.click_AddCloudAccount()
        self.display_classicAdding_message()
        self.check_addedAccount(CLASSIC_NAME)



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



                                            # Add Cloud Details

    # IBM VPC Cloud Addition Details
    VPC_NAME = "IBM VPC Cloud Testing "
    # VPC_API_KEY = "z@wnlo2"
    VPC_API_KEY = "A0DzQwj2nqV6gmzxme8-koVvDPIfeCWHwNagfEPbyCpB"
    VPC_INSTANCE_ID = "crn:v1:bluemix:public:cloud-object-storage:global:a/c2cbcb5ab2e6440c93810f3df7a74e94:9df4937d-e811-47fc-aeb2-aa0c4a7f9679::"

    # IBM Classic Cloud Addition Details
    CLASSIC_NAME = "Zakaria Testing Classi"
    CLASSIC_USERNAME = "danny@wanclouds"
    CLASSIC_API_KEY= "a65d423fa9ec1dff9bf9806d3c3e5d09e1f1a394d9289db418e7c72633244cb9"


    login = LoginTest()

    try:
        login.initial_setup(INSTANCE_PATH,"firefox")
        login.fill_VPC_login_attributes("zakaria@wanclouds.net", "zak@wanclouds33", True)
        login.clickVPVLoginButton()
        TFA_required = login.check_pinCode_page()
        if TFA_required:
            login.loginToGmail(GMAIL_URL, GMAIL_EMAIL, GMAIL_PASSWORD)
            login.fetch_TFA_PinCode()
            print("Login with 2 Factor-Authentication Test has been Successfully Completed.")
            time.sleep(5)

        login.click_SummaryPage_addButton()

        
                                                        # Add Cloud 

        # # Add Cloud for IBM VPC Cloud 
        login.run_adding_IBM_VPC(VPC_NAME,VPC_API_KEY, VPC_INSTANCE_ID)

        # # Add Cloud for Classic Account
        # login.run_adding_IBM_Classic_Cloud(CLASSIC_NAME, CLASSIC_USERNAME, CLASSIC_API_KEY)

        login.closeCurrentTab()
        
    except Exception as err:
        print("Test Case Fails \nError: ", err)
    finally: 
        login.closeBrowser()
