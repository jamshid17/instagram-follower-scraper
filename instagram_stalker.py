from operator import index
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd 


login_details = {
    'email': 'jamshidjabbarov101@gmail.com',
    'password': 'mucklab17',
}

usernames = ["itsmejamshid", "ow_academy", "ruslanmedia"]

def scrolling(driver, scroll_pause=2):
    fBody = driver.find_element_by_xpath("//div[@class='isgrP']")
    # Get scroll height
    last_height = driver.execute_script("return document.body.getElementsByClassName('isgrP')[0].scrollHeight")

    while True:
        # Scroll down to bottom
        driver.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].scrollHeight;', fBody)
        # Wait to load page
        time.sleep(scroll_pause)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.getElementsByClassName('isgrP')[0].scrollHeight")
        if new_height == last_height:
            time.sleep(scroll_pause)
            break
        last_height = new_height

def login(driver):
    #inputing logins 
    input_username = driver.find_element_by_xpath("//input[@name='username']")
    input_username.send_keys(login_details["email"])

    password_input = driver.find_element_by_xpath("//input[@name='password']")
    password_input.send_keys(login_details["password"])

    btn = driver.find_element_by_xpath("//button[@type='submit']")
    btn.click()
    time.sleep(4)
    #save info 
    btn_save = driver.find_elements_by_xpath("//button[@type='button']")[0]
    btn_save.click()
    time.sleep(1)

def get_users(driver, username_stalker, action):
    driver.get("https://www.instagram.com/{}".format(username_stalker))
    #following
    following_btn = driver.find_elements_by_xpath("//a[@href='/{}/following/']".format(username_stalker))[0]
    following_btn.click()
    time.sleep(3)
    ul_item = driver.find_element_by_xpath("//ul[@class='jSC57  _6xe7A']")
    action.move_to_element(ul_item)
    action.perform()
    #detecting links 
    scrolling(driver)
    #experiment

    usernames = ul_item.find_elements_by_xpath(".//a[@class='FPmhX notranslate  _0imsa ']")
    fullnames = ul_item.find_elements_by_xpath(".//div[@class='wFPL8 ']")
    list_username = []
    list_fullname = []
    for username, fullname in zip(usernames, fullnames):
        list_username.append(username.text)
        list_fullname.append(fullname.text)
    #refreshing 
    driver.refresh()
    time.sleep(10)
    #followers 
    follower_btn = driver.find_elements_by_xpath("//a[@href='/{}/followers/']".format(username_stalker))[0]
    follower_btn.click()
    time.sleep(3)
    ul_item = driver.find_element_by_xpath("//ul[@class='jSC57  _6xe7A']")
    action.move_to_element(ul_item)
    action.perform()
    #detecting links 
    scrolling(driver)

    usernames_followers = ul_item.find_elements_by_xpath(".//a[@class='FPmhX notranslate  _0imsa ']")
    fullnames_followers = ul_item.find_elements_by_xpath(".//div[@class='wFPL8 ']")
    list_username_follower = []
    list_fullname_follower = []
    for username, fullname in zip(usernames_followers, fullnames_followers):
        list_username_follower.append(username.text)
        list_fullname_follower.append(fullname.text)

    df1 = pd.DataFrame()
    df1["username"] = list_username
    df1["fullname"] = list_fullname
    df1.to_csv("following_{}.csv".format(username_stalker), index=False)
    df2 = pd.DataFrame()
    df2["username"] = list_username_follower
    df2["fullname"] = list_fullname_follower
    df2.to_csv("follower_{}.csv".format(username_stalker), index=False)   



def launchBrowser():
    s=Service('D:\PROJECTS\chromedriver')
    chrome_options = Options()
    chrome_options.add_argument("start-maximized")
    driver = webdriver.Chrome(service=s, options=chrome_options)

    driver.get('https://www.instagram.com/')
    action = webdriver.ActionChains(driver)
    time.sleep(1)

    login(driver) 
    for username in usernames:
        get_users(driver, username, action)

    return driver
driver = launchBrowser()