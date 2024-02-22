from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from tkinter import messagebox
import selenium.common.exceptions as exc
import time
import urllib3.exceptions

WAIT_TIME = 100
RUN_TIME = 300
SEC_INTERVAL = 2

def wait(my_driver):
    my_driver.implicitly_wait(WAIT_TIME)

def open_browser():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://orteil.dashnet.org/cookieclicker/")
    wait(driver)
    english_button = driver.find_element(By.XPATH, value='//*[@id="langSelect-EN"]')
    english_button.click()
    wait(driver)
    return  driver

def play_game(my_driver):
    cookie_button = my_driver.find_element(By.ID, value="bigCookie")
    end_time = int(time.time() + RUN_TIME)
    my_time = int(time.time())
    while my_time < end_time:
            cookies_div = my_driver.find_element(By.ID, value="cookies").text
            str_cookies = cookies_div.split('\n')[0].strip("cookies").rstrip().replace(",", "")
            cookies = int(str_cookies)
            clicks(cookie_button)

            buy = my_driver.find_element(By.ID, value="storeBulkBuy")
            buy_class_str = buy.get_attribute("class")

            mine = my_driver.find_element(By.ID, value="product3")
            mine_class_str = mine.get_attribute("class")

            check_boosters(my_time, my_driver, cookies, buy_class_str)
            check_upgrades(my_driver, cookies, mine_class_str)

            time_passed = int(time.time())
            difference = time_passed - my_time
            if difference >= 1:
                my_time += difference

    if my_time >= end_time:
        results = cookies_div.replace('\n', " ")
        messagebox.showinfo(title="Results", message=cookies_div)
        my_driver.quit()


def check_boosters(my_time, driver, cookies, buy_class_str):
    price_list = get_price_list(driver)
    if len(price_list) > 0 and buy_class_str.find("selected") != -1:
        max_price = max(price_list)
        if cookies >= max_price and my_time % SEC_INTERVAL == 0:
            max_index = price_list.index(max_price)
            products = get_products(driver)
            max_product = products[max_index]
            max_product.click()

def check_upgrades(driver, cookies, mine_class_str):
    if cookies > 100:
        upgrade = driver.find_element(By.ID, value="upgrade0")
        if upgrade != None:
                upgrade_class_str = upgrade.get_attribute("class")
                if upgrade_class_str.find("enabled") != -1:
                    upgrade.click()

def get_price_list(driver):
    price_list = []
    products = get_products(driver)
    for product in products:
        class_string = product.get_attribute("class")
        if class_string.find("unlocked") != -1:
            product_price = int(product.find_element(By.CLASS_NAME, value="price").text.replace(",",""))
            price_list.append(product_price)
    return  price_list

def get_products(driver):
    products = driver.find_elements(By.CLASS_NAME, value="product")
    return products


def clicks(cookie_button):
    cookie_button.click()
    cookie_button.click()
    cookie_button.click()
    cookie_button.click()

try:
    chrome_driver = open_browser()
    play_game(chrome_driver)

except exc.StaleElementReferenceException as st_err:
    print(st_err.msg)
    chrome_driver.quit()
    chrome_driver = open_browser()
    play_game(chrome_driver)
except exc.WebDriverException as wd_err:
    print(wd_err.msg)
    play_game(chrome_driver)
except urllib3.exceptions.MaxRetryError:
    pass
