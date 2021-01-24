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

fr = open("./data/character.json", 'r', encoding='utf-8')
character = json.load(fr)
fr.close()
fr = open("./data/pokemon_detail.json", 'r', encoding='utf-8')
pokemon = json.load(fr)
fr.close()
with tqdm(total=len(character)) as qbar:
    for name in character:
        character_detail = character[name]
        fr = open("./data/character_1.json", "r", encoding='utf-8')
        new_character = json.load(fr)
        fr.close()
        if name in new_character:
            qbar.update(1)
            continue
        if "region" in character_detail and "hometown" in character_detail and len(character_detail["pokemon"]) != 0:
            new_character[name] = character_detail
            fw = open("./data/character_1.json", 'w', encoding='utf-8')
            fw.write(json.dumps(new_character, ensure_ascii=False) + '\n')
            fw.close()
            qbar.update(1)
            continue
        if "region" not in character_detail:
            character_detail["region"] = "Unknown"
        if "hometown" not in character_detail:
            character_detail["hometown"] = "Unknown"
        if len(character_detail["pokemon"]) == 0:
            have_pokmemon = []
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
                    data = data.split('|')
                    for word in data:
                        if word in pokemon and word not in have_pokmemon:
                            have_pokmemon.append(word)
                browser.close()
                time.sleep(5)
            character_detail["pokemon"] = have_pokmemon
        new_character[name] = character_detail
        fw = open("./data/character_1.json", 'w', encoding='utf-8')
        fw.write(json.dumps(new_character, ensure_ascii=False) + '\n')
        fw.close()
        qbar.update(1)
