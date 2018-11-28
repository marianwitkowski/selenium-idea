from selenium import  webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from smsapi.client import SmsApiPlClient
import time, traceback

def save_balance(balance):
    try:
        with open('prev-balance.txt', 'w') as inp:
            inp.write(str(balance))
            inp.close()
    except Exception:
        pass

def prev_balance():
    try:
        with open('prev-balance.txt', 'r') as inp:
            val = float(inp.read())
            inp.close()
            return val
    except Exception:
        return None

driver = webdriver.Chrome()

# config variables
CLIENT_ID = "12345678"
PASSWORD = "MySecretPassword"
PHONE_NUMBER = "+48500600700"
ACCESS_TOKEN = "Z3BaZqmfZef9FO********************"

# open bank's webpage
driver.get("https://sso.cloud.ideabank.pl/#/login")

# find login input and type client ID
elem = driver.find_element_by_name("login")
elem.send_keys(CLIENT_ID)
elem.send_keys(Keys.ENTER)
time.sleep(2)

# find password input and type value
elem = driver.find_element_by_name("password")
elem.send_keys(PASSWORD)

# press ENTER - send form
elem.send_keys(Keys.ENTER)

try:

    # wait for visibility of element with "account-current-balance" class
    element = WebDriverWait(driver, 300).until(
        EC.presence_of_element_located((By.CLASS_NAME, "account-current-balance"))
    )

    # get value from "account-current-balance" element
    value = driver.execute_script(" return document.getElementsByClassName('account-current-balance')[0].innerText; ")
    currBalance = float(str(value).replace(" ","").replace("PLN","").replace(",",".") )
    prevBalance = prev_balance()

    # send SMS only in current balance and previous balance is not equal
    if prevBalance is None or currBalance<>prev_balance:
        print currBalance
        save_balance(currBalance)

        client = SmsApiPlClient(access_token=ACCESS_TOKEN)
        r = client.sms.send(to=PHONE_NUMBER, message="Stan konta {0:.2f} PLN:".format(currBalance))

except Exception as e:
    traceback.print_exc()
finally:
    driver.quit
