import os
import json
from tqdm import tqdm

fr = open("./data/relation.txt", 'r', encoding='utf-8')
lines = fr.readlines()
fr.close()
fr = open('./data/pokemon_detail.json', 'r', encoding='utf-8')
pokemon = json.load(fr)
fr.close()
fr = open("./data/region.json", 'r', encoding='utf-8')
region = json.load(fr)
fr.close()
fr = open("./data/character.json", 'r', encoding='utf-8')
character = json.load(fr)
fr.close()

c_c = ["敌对", "伙伴", "亲戚", "挑战"]
c_p = ["拥有"]
p_p = ['友好', '敌意']
c_r = ["来自", "位于"]
p_r = ['出没']
p_c = []
fw = open('./data/new_relation.txt', 'a+', encoding='utf-8')

with tqdm(total=len(lines)) as qbar:
    for line in lines:
        name1, name2, relation = line.strip('\n').split(',')
        temp = ""

        if name1 in character:
            temp = 'c'
        elif name1 in pokemon:
            temp = 'p'
        else:
            continue
        temp += '_'
        if name2 in character:
            temp += 'c'
        elif name2 in pokemon:
            temp += 'p'
        elif name2 in region:
            temp += 'r'

        if relation in eval(temp):
            fw.write(line)
        qbar.update(1)

fw.close()
