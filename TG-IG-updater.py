#  telegram-instagram bio updater

# For Telegram bot
import logging
# from telegram import Update
from telegram.ext import filters, ApplicationBuilder, MessageHandler, CommandHandler, ContextTypes, Updater, CallbackContext
import requests
import notion_client
from notion_client import Client
from datetime import datetime, timezone
import os
import json # to PARSE JSON string to return values
# import random # to randomise quotes selected from database
# import itertools
import time #to add delay to telegram bot

from telegram import __version__ as TG_VER

# To update IG bio
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

from setup import INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD, TEST


try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 5):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

#to start Flask WebApp
from flask import Flask, request

app = Flask(__name__)

# Declare variables
# declared in setup.py
API_TOKEN = TEST


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=" Hi! Welcome to update my IG Bio Bot")
    time.sleep(1)
    await context.bot.send_message(chat_id=update.effective_chat.id, text="This bot will help you update your IG bio correct to the second of posting, all via Telegram")
    time.sleep(1.8)
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Let's begin! \n\n" 
    + "/newbio - text for new bio\n"
    + "/update - update the bio")

async def newbio(update: Update, context: ContextTypes.DEFAULT_TYPE):
   await context.bot.send_message(chat_id=update.effective_chat.id, text="Cool! what you up to right now?")
   context.user_data['waiting_for_input'] = True
   
   return "WAITING_FOR_INPUT"

async def update(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message.text
    waiting_for_input = context.user_data.get('waiting_for_input')

    if waiting_for_input:
        # Do something with the user's input (e.g. save it to a variable)
        context.user_data['message'] = message
        await context.bot.send_message(chat_id=update.effective_chat.id, text="let's update that bio!\n\n") 
        del context.user_data['waiting_for_input']
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry! wasn't expecting input from you right now")

    

    time.sleep(1)

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

    # # Below is to find chrome driver, but we dont need since we are using the ChromeDriverManager
    # chrome_driver_path = '/Users/langston/Library/Application Support/Google/chromedriver'
    # driver = webdriver.Chrome(chrome_driver_path, options=options)

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

        # planet_list = ['Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn', 'Uranus', 'Neptune']
        bio_textarea = driver.find_element(By.ID,'pepBio')
        # bio_textarea = driver.find_element_by_id('pepBio')


        # planet_info = planet_location(random.choice(planet_list))
        # new_bio = '{} RA|DEC|CO: {} | {} | {}\nWhen: {}'.format(planet_info[1],planet_info[2],planet_info[3], planet_info[7],datetime.datetime.now().strftime("%Y-%m-%d @ %H:%M:%S"))
        # other_text = 'Give me quotes! @ https://t.me/gimmequotes_bot\n'+ 'write @ https://syaz.substack.com\n' + '
        new_bio = message + '\nWhen: {}'.format(datetime.datetime.now().strftime("%Y-%m-%d @ %H:%M:%S"))
        
        if(len(new_bio) < 150):
            bio_textarea.clear()
            bio_textarea.send_keys(new_bio)

        WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.CSS_SELECTOR,'button._acan._acap._acas._aj1-')))
        bio_submit_button = driver.find_element(By.CSS_SELECTOR, 'button._acan._acap._acas._aj1-')
        # bio_submit_button = driver.find_element_by_css_selector('button.sqdOP.L3NKy.y3zKF')

        driver.execute_script("arguments[0].scrollIntoView(true);", bio_submit_button)
        bio_submit_button.click()

        FIRST_UPDATE = False
        
        driver.close()

        await context.bot.send_message(chat_id=update.effective_chat.id, text="okay! all done! have a look to confirm? Thank you!\n\n") 
    

#declare ApplicationBuilder & Handlers below
if __name__ == '__main__':
    application = ApplicationBuilder().token(API_TOKEN).build()

    start_handler = CommandHandler('start', start)
    newbio_handler = CommandHandler('newbio', newbio)
    # update_handler = CommandHandler('update', update)

    # help_handler = CommandHandler('help', help)
    # receive_handler = CommandHandler('receive', receive)
    # give_handler = CommandHandler('give', give)
    update_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), update)
    # unknown_handler = MessageHandler(filters.COMMAND, unknown)

    application.add_handler(start_handler)
    application.add_handler(newbio_handler)
    application.add_handler(update_handler)
    # application.add_handler(quote_handler)
    # application.add_handler(receive_handler)
    # application.add_handler(give_handler)
    # application.add_handler(unknown_handler)

    application.run_polling()

    # https://api.telegram.org/bot5912247638:AAHo1kYgW2c6TWiOuJAlWuSfKouzoVAFTQE/setWebhook?url=https://git.heroku.com/gimmequotes.git

# Set up the Telegram bot updater and dispatcher
updater = Updater(token=API_TOKEN, use_context=True)
dispatcher = updater.dispatcher

import os
