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
from tqdm import tqdm

fr = open("./data/pokemon_detail.json", "r", encoding='utf-8')
fr2 = open("./data/pokemon_detail_1.json", "r", encoding='utf-8')
pokemon = json.load(fr)
new_pokemon = json.load(fr2)
fr.close()
fr2.close()

shuxing = ["一般", "格斗", "飞行", "毒", "地面", "岩石", "虫", "幽灵",
           "钢", "火", "水", "草", "电", "超能力", "冰", "龙", "恶", "妖精"]
with tqdm(total=len(pokemon)) as qbar:
    for name in pokemon:
        if name in new_pokemon:
            qbar.update(1)
            continue
        temp = pokemon[name]
        url = url = "http://wiki.52poke.com/index.php?title=" + \
            name + "&action=edit"
        browser = webdriver.Chrome()
        browser.get(url)
        xpath = '//*[@id="wpTextbox1"]'
        try:
            elements = WebDriverWait(browser, 20).until(
                EC.presence_of_all_elements_located((By.XPATH, xpath)))
        except TimeoutException:
            elements = []
        for element in elements:
            data = element.text
            start = data.find("===属性相性===")
            start = data.find('<div class="tabbertab" title="一般">', start)
            if start == -1:
                temp["属性相性"] = None
            end = data.find('</div>', start)
            data = data[start:end]
            shuxingxiangxing = {}
            for item in shuxing:
                start = data.find(item + "=")
                if item != "妖精":
                    end = data.find("|", start)
                else:
                    end = data.find("}}", start)
                try:
                    shuxingxiangxing[item] = float(
                        data[start + len(item) + 1:end])
                except ValueError:
                    shuxingxiangxing[item] = None
        temp["属性相性"] = shuxingxiangxing
        new_pokemon[name] = temp
        fw = open('./data/pokemon_detail_1.json', 'w', encoding='utf-8')
        fw.write(json.dumps(new_pokemon, ensure_ascii=False))
        fw.close()
        qbar.update(1)
        browser.close()
        time.sleep(5)

"""
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
"""
