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

url = "https://wiki.52poke.com/wiki/%E4%BA%BA%E7%89%A9%E5%88%97%E8%A1%A8"
browser = webdriver.Chrome()
browser.get(url)

character = {}
fw = open("character.json", "w", encoding='utf-8')

for i in range(1, 9):
    xpath = '//*[@id="mw-content-text"]/div/table[' + str(i) + ']/tbody/tr'
    if i == 8:
        for j in range(2, 36):
            new_xpath = xpath + '[' + str(j) + ']'
            temp_dict = {}
            for k in range(1, 4):
                new_xpath1 = new_xpath + '/td[' + str(k) + ']'
                try:
                    elements = WebDriverWait(browser, 20).until(
                        EC.presence_of_all_elements_located((By.XPATH, new_xpath1)))
                except TimeoutException:
                    elements = []
                if len(elements) == 0:
                    print("break")
                    break
                for element in elements:
                    if k == 1:
                        temp_dict["chinese_name"] = element.text.strip("*")
                    elif k == 2:
                        temp_dict["japanese_name"] = element.text
                    else:
                        temp_dict["english_name"] = element.text
                        character[temp_dict["chinese_name"]] = temp_dict
                        print(temp_dict)
    else:
        for j in range(1, 4):
            new_xpath = xpath + "/td[" + str(j) + "]/table/tbody/tr"
            for l in range(2, 50):
                new_xpath1 = new_xpath + "[" + str(l) + "]"
                temp_dict = {}
                for k in range(1, 4):
                    new_xpath2 = new_xpath1 + "/td[" + str(k) + "]"
                    try:
                        elements = WebDriverWait(browser, 20).until(
                            EC.presence_of_all_elements_located((By.XPATH, new_xpath2)))
                    except TimeoutException:
                        elements = []
                    if len(elements) == 0:
                        print("break")
                        break
                    for element in elements:
                        if k == 1:
                            temp_dict["chinese_name"] = element.text.strip("*")
                        elif k == 2:
                            temp_dict["japanese_name"] = element.text
                        else:
                            temp_dict["english_name"] = element.text
                            character[temp_dict["chinese_name"]] = temp_dict
                            print(temp_dict)
fw.write(json.dumps(character, ensure_ascii=False) + '\n')
fw.close()
browser.close()
