
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.common.exceptions import NoSuchElementException
import sys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from skylive_requester import planet_location
import datetime
import random
# from decouple import config

from webdriver_manager.chrome import ChromeDriverManager # So that we don't have to keep downloading new drivers for chrome

from setup import INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD


# USRN = config(INSTAGRAM_USERNAME)
# PASS = config(INSTAGRAM_PASSWORD)

USRN = INSTAGRAM_USERNAME
PASS = INSTAGRAM_PASSWORD
FIRST_UPDATE = True


#Setting up the webdriver
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))
driver.maximize_window()
url = 'https://www.instagram.com/'
'''
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")
'''

driver.implicitly_wait(6)
driver.get(url)


#Login
username_field = WebDriverWait(driver,3).until(lambda d: d.find_element(By.CSS_SELECTOR, 'input[name="username"]')) # driver.find_element_by_css_selector('input[name="username"]') #driver.find_element_by_name('username')
# username_field = WebDriverWait(driver,3).until(lambda d: d.find_element_by_css_selector('input[name="username"]')) # driver.find_element_by_css_selector('input[name="username"]') #driver.find_element_by_name('username')
password_field = driver.find_element('css selector','input[name="password"]' ) #driver.find_element_by_name('password')
# password_field = driver.find_element_by_css_selector('input[name="password"]') #driver.find_element_by_name('password')
form = driver.find_element('id', 'loginForm')
# form = driver.find_element_by_id('loginForm')


username_field.send_keys(USRN)
password_field.send_keys(PASS)
form.submit()

WebDriverWait(driver,5).until(EC.staleness_of(username_field))
#Getting passed the "save login info"
not_now_button = driver.find_element(By.CSS_SELECTOR, 'button._acan._acao._acas._aj1-') #WebDriverWait(driver,3).until(lambda d: d.find_element_by_css_selector('button.sqdOP.yWX7d.y3zKF')) 
# not_now_button = driver.find_element_by_css_selector('button.sqdOP.yWX7d.y3zKF') #WebDriverWait(driver,3).until(lambda d: d.find_element_by_css_selector('button.sqdOP.yWX7d.y3zKF')) 

not_now_button.click()

#Getting passed the notifications
WebDriverWait(driver,5)
not_now_button2 = driver.find_element(By.CSS_SELECTOR, 'button._a9--._a9_1') #WebDriverWait(driver,3).until(lambda d: d.find_element_by_css_selector('button.aOOlW.HoLwm')) 
# not_now_button2 = driver.find_element_by_css_selector('button.aOOlW.HoLwm') #WebDriverWait(driver,3).until(lambda d: d.find_element_by_css_selector('button.aOOlW.HoLwm')) 

not_now_button2.click()

#Now in the home page
profile_link = driver.find_element(By.LINK_TEXT, USRN)
# profile_link = driver.find_element_by_link_text(USRN)

profile_link.click()

#Now in the profile page
edit_profile = driver.find_element(By.LINK_TEXT,'Edit Profile') #WebDriverWait(driver,3).until(lambda d:  d.find_element_by_link_text('Edit Profile'))
# edit_profile = driver.find_element_by_link_text('Edit Profile') #WebDriverWait(driver,3).until(lambda d:  d.find_element_by_link_text('Edit Profile'))

edit_profile.click()

#Now in the Edit Profile page
while True:
    if(not FIRST_UPDATE):
        time.sleep(60*10)

    planet_list = ['Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune']
    bio_textarea = driver.find_element(By.ID,'pepBio')
    # bio_textarea = driver.find_element_by_id('pepBio')


    planet_info = planet_location(random.choice(planet_list))
    new_bio = '{} RA|DEC|CO: {} | {} | {}\nWhen: {}'.format(planet_info[1],planet_info[2],planet_info[3], planet_info[7],datetime.datetime.now().strftime("%Y-%m-%d @ %H:%M:%S"))
    # other_text = 'Give me quotes! @ https://t.me/gimmequotes_bot\n'+ 'write @ https://syaz.substack.com\n' + '
    if(len(new_bio) < 150):
        bio_textarea.clear()
        bio_textarea.send_keys(new_bio)

    WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,'button._acan._acap._acas._aj1-')))
    bio_submit_button = driver.find_element(By.CSS_SELECTOR, 'button._acan._acap._acas._aj1-')
    # bio_submit_button = driver.find_element_by_css_selector('button.sqdOP.L3NKy.y3zKF')

    driver.execute_script("arguments[0].scrollIntoView(true);", bio_submit_button)
    bio_submit_button.click()

    FIRST_UPDATE = False
#driver.close()



