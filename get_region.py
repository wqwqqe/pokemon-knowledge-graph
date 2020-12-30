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

url = 'https://wiki.52poke.com/wiki/%E5%9C%B0%E7%82%B9%E5%88%97%E8%A1%A8'
browser = webdriver.Chrome()
browser.get(url)

region = {}

xpath = '//*[@id="mw-content-text"]/div/table['
for i in range(2, 28):
    flag1 = True
    for j in range(1, 50):
        temp = {}
        flag = False
        for k in range(1, 4):
            #xpath = '//*[@id="mw-content-text"]/div/table[3]/tbody/tr[1]'
            xpath = '//*[@id="mw-content-text"]/div/table[' + \
                str(i) + ']/tbody/tr[' + str(j) + ']/td['+str(k)+']'
            try:
                elements = WebDriverWait(browser, 20).until(
                    EC.presence_of_all_elements_located((By.XPATH, xpath)))
            except TimeoutException:
                elements = []
            if len(elements) == 0:
                flag1 = False
                break
            for element in elements:
                regions = element.text.split("\n")
                cnt = len(regions)
                if not flag:
                    for l in range(cnt):
                        temp[l] = []
                    flag = True
                for l in range(cnt):
                    temp[l].append(regions[l])
        if not flag1:
            break
        for t in temp:
            l = temp[t]
            print(l)
            a = {}
            if l[0] == '冠军之路（B2W2）':
                continue
            a["chinese_name"] = l[0]
            a['japanese_name'] = l[1]
            a['english_name'] = l[2]
            region[l[0]] = a
        print(temp)
        fw = open("region.json", "w", encoding='utf-8')
        fw.write(json.dumps(region, ensure_ascii=False))
        fw.close()
browser.close()
