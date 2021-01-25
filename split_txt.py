import os
from tqdm import tqdm
import json

fr = open("./data/document.txt", 'r', encoding='utf-8')
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

new_document = {}
cnt = 0


def find_entities(sentence):
    entity = []
    length = len(sentence)
    for i in range(length):
        for j in range(10):
            name = sentence[i: min(i + j, length)]
            if (name in pokemon or name in region or name in character) and (name not in entity):
                entity.append(name)
    return entity


with tqdm(total=len(lines)) as qbar:
    for line in lines:
        line = line.strip("\n")
        if len(line) > 400:
            k = 0
            while True:
                temp = {}
                sentence = line[k * 400: min((k + 1) * 400, len(line))]
                entity = find_entities(sentence)
                temp["sentence"] = sentence
                temp["entity"] = entity
                k += 1
                new_document[cnt] = temp
                cnt += 1
                if k * 400 >= len(line):
                    break
        else:
            temp = {}
            temp['sentence'] = line
            entity = find_entities(line)
            temp['entity'] = entity
            new_document[cnt] = temp
            cnt += 1
        qbar.update(1)
fw = open('./data/document.json', 'w', encoding='utf-8')
fw.write(json.dumps(new_document, ensure_ascii=False))
fw.close()
