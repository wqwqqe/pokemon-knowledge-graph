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

fr = open('./data/character.json', "r", encoding='utf-8')
character = json.load(fr)
fr.close()
fr = open('./data/region.json', 'r', encoding='utf-8')
region = json.load(fr)
fr.close()

with tqdm(total=len(region)) as qbar:
    for name in region:
        fr = open("./data/region_1.json", 'r', encoding='utf-8')
        new_region = json.load(fr)
        temp = region[name]
        fr.close()
        if name in new_region:
            qbar.update(1)
            continue
        have_character = []
        for i in range(2):
            if i == 0:
                new_name = convert(name, 'zh-tw')
            else:
                new_name = name
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
                start = 0
                while True:
                    start = data.find('name', start)
                    if start == -1:
                        break
                    start = data.find('=', start)
                    if start == -1:
                        break
                    end = data.find('\n', start)
                    character_name = data[start + 1:end]
                    character_name = convert(character_name, 'zh-cn')
                    if character_name in character and character_name not in have_character:
                        have_character.append(character_name)
            browser.close()
            time.sleep(5)
        temp['character'] = have_character
        new_region[name] = temp
        fw = open('./data/region_1.json', 'w', encoding='utf-8')
        fw.write(json.dumps(new_region, ensure_ascii=False) + '\n')
        fw.close()
        qbar.update(1)
