# coding: utf-8
import json
import pandas as pd
import random


def get_data(path, data):
    fr = open(path, 'r', encoding='utf-8')
    annot = json.load(fr)
    fr.close()
    document = annot['content'].split("\n")
    entities = annot['outputs']['annotation']['T']
    relations = annot['outputs']['annotation']['R']
    id_to_entity = {}
    for entity in entities:
        if entity is not None and len(entity) != 0:
            temp = {}
            temp["name"] = entity['value']
            temp['start'] = entity['start']
            temp['end'] = entity['end']
            id_to_entity[entity['id']] = temp
    sentence_len = [0]
    new_document = []
    for sentence in document:
        if len(sentence) > 300:
            cnt = 0
            length = len(sentence)
            while True:
                new_sentence = sentence[cnt *
                                        300: min((cnt + 1) * 300, length)]
                a = len(new_sentence) + sentence_len[-1]
                sentence_len.append(a)
                new_document.append(new_sentence)
                cnt += 1
                if cnt * 300 > length:
                    break
        else:
            a = len(sentence) + sentence_len[-1]
            sentence_len.append(a)
            new_document.append(sentence)
    document = new_document
    n = len(sentence_len)-1
    for relation in relations:
        if relation is not None and len(relation) != 0:
            head_id = relation['from']
            tail_id = relation['to']
            head = id_to_entity[head_id]
            tail = id_to_entity[tail_id]
            for i in range(n):
                if head['start'] >= sentence_len[i] and head['start'] < sentence_len[i + 1]:
                    if tail['start'] < sentence_len[i] or tail['start'] >= sentence_len[i + 1]:
                        break
                    data["sentence"].append(document[i])
                    data["relation"].append(relation['name'])
                    data["head"].append(head["name"])
                    data["head_offset"].append(head["start"]-sentence_len[i])
                    data["tail"].append(tail['name'])
                    data['tail_offset'].append(tail['start']-sentence_len[i])
                    break


data = {"sentence": [],
        "relation": [],
        "head": [],
        "head_offset": [],
        "tail": [],
        "tail_offset": []}
for i in range(1, 4, 1):
    path = "./data/outputs/" + str(i) + '.json'
    get_data(path, data)


train_ratio = 0.7
valild_ratio = 0.1
num = len(data["sentence"])
order = ["sentence",
         "relation",
         "head",
         "head_offset",
         "tail",
         "tail_offset"]
new_data = []

for i in range(num):
    temp_data = []
    for name in order:
        if name == 'sentence':
            temp_data.append(data[name][i].strip("\r"))
        else:
            temp_data.append(data[name][i])
    new_data.append(temp_data)
random.shuffle(new_data)
train_data = new_data[: int(num * train_ratio)]
test_data = new_data[int(num * train_ratio): int(num * (1 - valild_ratio))]
valid_data = new_data[int(num * (1 - valild_ratio)):]


def change_to_dataframe(data):
    new_data = {"sentence": [],
                "relation": [],
                "head": [],
                "head_offset": [],
                "tail": [],
                "tail_offset": []}
    order = ["sentence",
             "relation",
             "head",
             "head_offset",
             "tail",
             "tail_offset"]
    for temp in data:
        for i in range(6):
            new_data[order[i]].append(temp[i])
    return pd.DataFrame(new_data)


train_data = change_to_dataframe(train_data)
test_data = change_to_dataframe(test_data)
valid_data = change_to_dataframe(valid_data)
train_data.to_csv("./data/train.csv", index=False)
test_data.to_csv("./data/test.csv", index=False)
valid_data.to_csv("./data/valid.csv", index=False)
