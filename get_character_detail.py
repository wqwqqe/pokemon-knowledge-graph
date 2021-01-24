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
from zhconv import convert

fr = open("./data/character.json", "r", encoding='utf-8')
character = json.load(fr)
fr.close()
fr2 = open("./data/chracter_1.json", 'r', encoding='utf-8')
new_character = json.load(fr2)
fr2.close()
fr = open("./data/pokemon_detail.json", "r", encoding='utf-8')
pokemon = json.load(fr)
fr2.close()

with tqdm(total=len(character)) as qbar:
    for name in character:
        if name in new_character:
            qbar.update(1)
            continue
        temp = character[name]
        have_pokemon = []
        for i in range(2):
            if i == 0:
                new_name = name
            else:
                new_name = convert(name, 'zh-tw')
            url = url = "http://wiki.52poke.com/index.php?title=" + \
                new_name + "&action=edit"
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
                start = data.find("hometown=[[")
                end = data.find("]]", start)
                if start == -1:
                    temp["hometown"] = "Unknown"
                else:
                    temp["hometown"] = convert(
                        data[start + len("hometown=[["):end], 'zh-cn')
                start = data.find("region=[[")
                end = data.find("]]", start)
                if start == -1:
                    temp["region"] = "Unknown"
                else:
                    temp["region"] = convert(
                        data[start + len("region=[["):end], 'zh-cn')
                start = 0
                goal = "pokemon="
                while True:
                    start = data.find(goal, start+1)
                    if start == -1:
                        break
                    end = data.find("\n", start)
                    pokemon_name = data[start + len(goal):end]
                    pokemon_name = convert(pokemon_name, 'zh-cn')
                    if pokemon_name in pokemon and pokemon_name not in have_pokemon:
                        have_pokemon.append(pokemon_name)
                    end = data.find("|", start)
                    pokemon_name = data[start + len(goal):end]
                    pokemon_name = convert(pokemon_name, 'zh-cn')
                    if pokemon_name in pokemon and pokemon_name not in have_pokemon:
                        have_pokemon.append(pokemon_name)
                goal = "name="
                while True:
                    start = data.find(goal, start+1)
                    if start == -1:
                        break
                    end = data.find("\n", start)
                    pokemon_name = data[start + len(goal):end]
                    pokemon_name = convert(pokemon_name, 'zh-cn')
                    if pokemon_name in pokemon and pokemon_name not in have_pokemon:
                        have_pokemon.append(pokemon_name)
                    end = data.find("|", start)
                    pokemon_name = data[start + len(goal):end]
                    pokemon_name = convert(pokemon_name, 'zh-cn')
                    if pokemon_name in pokemon and pokemon_name not in have_pokemon:
                        have_pokemon.append(pokemon_name)
                goal = "pkmn="
                while True:
                    start = data.find(goal, start+1)
                    if start == -1:
                        break
                    end = data.find("\n", start)
                    pokemon_name = data[start + len(goal):end]
                    pokemon_name = convert(pokemon_name, 'zh-cn')
                    if pokemon_name in pokemon and pokemon_name not in have_pokemon:
                        have_pokemon.append(pokemon_name)
                    end = data.find("|", start)
                    pokemon_name = data[start + len(goal):end]
                    pokemon_name = convert(pokemon_name, 'zh-cn')
                    if pokemon_name in pokemon and pokemon_name not in have_pokemon:
                        have_pokemon.append(pokemon_name)
            browser.close()
            time.sleep(5)
        temp["pokemon"] = have_pokemon
        new_character[name] = temp
        fw = open("./data/chracter_1.json", "w", encoding='utf-8')
        fw.write(json.dumps(new_character, ensure_ascii=False) + '\n')
        fw.close()
        qbar.update(1)


"""
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
