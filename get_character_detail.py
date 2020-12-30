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


fr = open("1.json", "r", encoding='utf-8')
character = json.load(fr)
fr.close()
fw = open("2.json", "w", encoding='utf-8')
new_character = {}
for name in character:
    url = "https://wiki.52poke.com/wiki/"+name
    browser = webdriver.Chrome()
    browser.get(url)
    xpath = '//*[@id="mw-content-text"]/div'
    try:
        elements = WebDriverWait(browser, 20).until(
            EC.presence_of_all_elements_located((By.XPATH, xpath)))
    except TimeoutException:
        elements = []
    temp = character[name]
    if "japanese_name" not in temp:
        for element in elements:
            text = element.text
            start = text.find("日文︰")
            end = min(text.find("，", start), text.find("）", start))
            temp["japanese_name"] = text[start+4:end]
            if text[end] != '）':
                new_start = text.find("英文︰", end)
                new_end = text.find("）", new_start)
                temp["english_name"] = text[new_start+3:new_end]
    xpath = '//*[@id="mw-content-text"]/div/table[1]/tbody'
    try:
        elements = WebDriverWait(browser, 20).until(
            EC.presence_of_all_elements_located((By.XPATH, xpath)))
    except TimeoutException:
        elements = []
        temp["gender"] = "unknown"
    for element in elements:
        text = element.text
        start = text.find("性别 ")
        end = text.find("\n", start)
        if len(text[start+3:end]) > 1:
            temp["gender"] = "unknown"
        else:
            temp["gender"] = text[start+3:end]
    print(temp)
    new_character[name] = temp
    fw = open("2.json", "w", encoding='utf-8')
    fw.write(json.dumps(new_character, ensure_ascii=False) + '\n')
    browser.close()
    time.sleep(10)


"""
url = "https://wiki.52poke.com/wiki/%E6%B4%9B%E4%BC%8A%E5%85%B9"
browser = webdriver.Chrome()
browser.get(url)
xpath = '//*[@id="mw-content-text"]/div/table[1]/tbody'
try:
    elements = WebDriverWait(browser, 20).until(
        EC.presence_of_all_elements_located((By.XPATH, xpath)))
except TimeoutException:
    elements = []
temp = {}
for element in elements:
    text = element.text

    print(text)
browser.close()
"""
