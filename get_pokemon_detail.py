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


fr = open("pokemon_name.csv", "r", encoding='utf-8')
fr2 = open("pokemon_detail.json", "r", encoding='utf-8')
pokemon = json.load(fr2)
fr2.close()
cnt = 0
for line in fr:
    cnt += 1
    if line.strip("\n") in pokemon:
        continue

    url = "http://wiki.52poke.com/index.php?title=" + \
        line.strip("\n") + "&action=edit"

    browser = webdriver.Chrome()
    browser.get(url)
    xpath = '//*[@id="wpTextbox1"]'
    temp = {}
    temp["chinese_name"] = line.strip("\n")
    temp['id'] = cnt

    try:
        elements = WebDriverWait(browser, 20).until(
            EC.presence_of_all_elements_located((By.XPATH, xpath)))
    except TimeoutException:
        elements = []
    for element in elements:
        data = element.text
        start = data.find("{{寶可夢信息框")
        end = data.find("{{N", start)
        data = data[start:end]

        s = data.find("jname")
        e = data.find("\n", s)
        temp["japanese_name"] = data[s + 6:e]

        s = data.find("enname")
        e = data.find("\n", s)
        temp["english_name"] = data[s + 7:e]

        s = data.find("height")
        e = data.find("\n", s)
        temp["height"] = data[s + 7:e]

        s = data.find("weight")
        e = data.find("\n", s)
        temp["weight"] = data[s + 7:e]
        t = 0
        shuxing = []
        while t != -1:
            s = data.find("type", t)
            if s == -1:
                t = -1
                break
            else:
                t = s+5
            if data[s: s + 5] == 'typen':
                continue
            else:
                s = data.find("=", s)
                e = data.find("\n", s)
                shuxing.append(data[s + 1:e])
        temp["type"] = shuxing

        t = 0
        texing = []
        yingcang = []
        while t != -1:
            s = data.find("ability", t)
            if s == -1:
                t = -1
                break
            else:
                t = s + 7
            if data[s: s + 8] == 'abilityn':
                continue
            if data[s: s + 8] == 'abilityd':
                s = data.find("=", s)
                e = data.find("\n", s)
                if data[s+1:e] not in yingcang:
                    yingcang.append(data[s + 1:e])
            else:
                s = data.find("=", s)
                e = data.find("\n", s)
                if data[s+1:e] not in texing:
                    texing.append(data[s + 1:e])
        temp["ability"] = texing
        temp["隐藏特性"] = yingcang
        print(temp)
        pokemon[line.strip("\n")] = temp
        fw = open("pokemon_detail.json", "w", encoding='utf-8')
        fw.write(json.dumps(pokemon, ensure_ascii=False))
        fw.close()
    browser.close()
    time.sleep(10)
fr.close()
