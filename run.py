import json
import os

while True:
    fr = open("./data/region_1.json", 'r', encoding='utf-8')
    a = json.load(fr)
    fr.close()
    fr = open("./data/region.json", 'r', encoding='utf-8')
    b = json.load(fr)
    fr.close()
    if len(a) == len(b):
        break
    try:
        os.system('python region_detail.py')
    except Exception as e:
        pass
