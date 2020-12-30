import json

fr = open("2.json", "r", encoding='utf-8')
character = json.load(fr)
fr.close()

for name in character:
    temp = character[name]
    japanese_name = temp.get('japanese_name', 'unknown')
    if len(japanese_name) >= 20:
        temp['japanese_name'] = 'unknown'
    else:
        temp['japanese_name'] = japanese_name
    english_name = temp.get("english_name", 'unknown')
    if len(english_name) >= 20:
        temp['english_name'] = 'unknown'
    else:
        temp['english_name'] = english_name

    character[name] = temp
    print(temp)
fw = open("3.json", "w", encoding='utf-8')
fw.write(json.dumps(character, ensure_ascii=False))
fw.close()
