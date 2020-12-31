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


fr = open("character.json", "r", encoding='utf-8')
character = json.load(fr)
for name in character:
    url = 'https://wiki.52poke.com/wiki/' + name
    browser = webdriver.Chrome()
    browser.get(url)
    for i in range(1, 50):
        xpath = '//*[@id="mw-content-text"]/div/p[' + str(i) + ']'
        try:
            elements = WebDriverWait(browser, 20).until(
                EC.presence_of_all_elements_located((By.XPATH, xpath)))
        except TimeoutException:
            elements = []
        if len(elements) == 0:
            break
        for element in elements:
            if len(element.text) < 20:
                continue
            fw = open("document.txt", "a", encoding='utf-8')
            fw.write(element.text+"\n")
            print(element.text)
            fw.close()
    browser.close()
    time.sleep(5)
