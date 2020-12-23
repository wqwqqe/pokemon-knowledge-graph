from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.options import Options
import json
import time
import random
import argparse

url = "https://wiki.52poke.com/wiki/Category:%E5%8A%A8%E7%94%BB%E7%99%BB%E5%9C%BA%E8%A7%92%E8%89%B2"
browser = webdriver.Chrome()
browser.get(url)

fr = open("character.json", "r", encoding='utf-8')
character = json.load(fr)
fw = open("1.json", "w", encoding='utf-8')
cnt = 2
k = 2
while True:
    xpath = '//*[@id="mw-pages"]/div/div/div[' + str(k) + ']/ul'
    try:
        elements = WebDriverWait(browser, 20).until(
            EC.presence_of_all_elements_located((By.XPATH, xpath)))
    except TimeoutException:
        elements = []
    if len(elements) == 0:
        try:
            click_path = '//*[@id="mw-pages"]/a[' + str(cnt) + ']'
            if cnt == 2:
                cnt += 2
            browser.find_element_by_xpath(click_path).click()
            print("next page")
            k = 1
        except NoSuchElementException:
            break
    else:
        for element in elements:
            t = element.text.split("\n")
            for name in t:
                if name in character:
                    print("break")
                    continue
                temp = {}
                temp["chinese_name"] = name
                print(temp)
                character[name] = temp
        k += 1

fw.write(json.dumps(character, ensure_ascii=False) + '\n')
fw.close()

browser.close()
