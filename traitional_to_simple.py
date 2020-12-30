from zhconv import convert
import json

fr = open("pokemon_detail.json", "r", encoding='utf-8')
character = json.load(fr)
fr.close()
new_character = {}
for name in character:
    temp = character[name]
    new_name = convert(name, 'zh-cn')
    temp['chinese_name'] = new_name

    t = temp["type"]
    new_type = []
    for item in t:
        new_type.append(convert(item, 'zh-cn'))
    temp['type'] = new_type

    a = temp['ability']
    new_ability = []
    for item in a:
        new_ability.append(convert(item, 'zh-cn'))
    temp['ability'] = new_ability

    s = temp['隐藏特性']
    new_yin = []
    for item in s:
        new_yin.append(convert(item, 'zh-cn'))
    temp['隐藏特性'] = new_yin

    new_character[name] = temp

fw = open('3.json', 'w', encoding='utf-8')
fw.write(json.dumps(new_character, ensure_ascii=False))
fw.close()
