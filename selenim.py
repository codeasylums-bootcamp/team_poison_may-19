import time
import gettext
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
  
browser = webdriver.Firefox()
browser.get("https://www.irctc.co.in/nget/train-search")

# username = browser.find_element_by_id("user_name")
# password = browser.find_element_by_id("password")
# from_station   = browser.find_element_by_id("origin")

from_station = browser.find_element_by_xpath('//*[@id="origin"]/span/input')
to_station = browser.find_element_by_xpath('//*[@id="destination"]/span/input')
date = browser.find_element_by_xpath('//input[@placeholder="Journey Date(dd-mm-yyyy)*"]')

from_station.click()
from_station.send_keys("RNC")
time.sleep(1)
from_station.send_keys(Keys.RETURN)

to_station.click()
to_station.send_keys("NDLS")
time.sleep(1)
to_station.send_keys(Keys.RETURN)

for i in range(10):
    date.send_keys(Keys.BACKSPACE)
date.send_keys('30-05-2019')
time.sleep(1)
date.send_keys(Keys.RETURN)

time.sleep(5)

# element = browser.find_elements_by_xpath("//span")
# browser.execute_script("arguments[0].style.visibility='hidden'", element)

time.sleep(2)

# status = browser.find_element_by_xpath('//a[@id="T_12453"]/../../../../div[3]/div[2]/div/span[@class="waitingstatus"].getText()')
# print(status)
found = browser.find_element_by_xpath('//a[@id="T_12453"]/../../../../div[3]/div[2]/div/div/button')
# found = browser.find_elements_by_xpath('//button[@id="check-availability"]')[0]
found.send_keys(Keys.RETURN)



time.sleep(10)
book_now = browser.find_elements_by_xpath('//button[@class="b1"]')[0]
book_now_text = book_now.get_attribute("aria-label")
book_list = book_now_text.split()
book_now.send_keys(Keys.RETURN)
time.sleep(6)
def check(word, book_list):
    if word in book_list:
        book_now.send_keys(Keys.RETURN)

check('RAC',book_list)
time.sleep(5)
login_Id = browser.find_element_by_id('userId')
login_Id.send_keys('rameleswar')
login_Id.send_keys(Keys.TAB)

login_pw = browser.find_element_by_id('pwd')
login_pw.send_keys('nsso(fod)')
login_pw.send_keys(Keys.TAB)

time.sleep(10)


captcha = browser.find_element_by_id('nlpAnswer')
captcha.send_keys("Invesco")
sign_in = browser.find_element_by_xpath('//button[@class="search_btn"]')
# captcha.send_keys(Keys.RETURN)

login_pw.click()
login_pw.send_keys(Keys.RETURN)


time.sleep(20)



psgn_name = "LAlitha"
psgn_age = "21"
psgn_gender = "female"

psgn = browser.find_element_by_id('psgn-name')
psgn = send_keys(psgn_name)


psgn.send_keys(Keys.Tab)
psgn.send_keys(psgn_age)
psgn.send_keys(Keys.Tab)

if psgn_gender == "Male":
    psgn.send_keys(Keys.ARROW_DOWN)
elif psgn_gender == "Female":
    psgn.send_keys(Keys.ARROW_DOWN)
    psgn.send_keys(Keys.ARROW_DOWN)


# book_now.send_keys(Keys.RETURN)
# book_now.send_keys('nsso(fod)')
# book_now.send_keys(Keys.RETURN)



# book_now.send_keys(Keys.RETURN)
# print(len(book_now))


  