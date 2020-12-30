import json

fr = open("pokemon_detail.json", 'r', encoding='utf-8')
pokemon = json.load(fr)
fr.close()
new_pokemon = {}
for name in pokemon:
    temp = pokemon[name]

    t = temp['type']
    new_t = []
    for item in t:
        if item not in new_t:
            new_t.append(item)
    temp['type'] = new_t

    t = temp['ability']
    new_t = []
    for item in t:
        if item not in new_t:
            new_t.append(item)
    temp['ability'] = new_t

    t = temp['隐藏特性']
    new_t = []
    for item in t:
        if item not in new_t:
            new_t.append(item)
    temp['隐藏特性'] = new_t

    new_pokemon[name] = temp

fw = open("3.json", "w", encoding='utf-8')
fw.write(json.dumps(new_pokemon, ensure_ascii=False))
fw.close()
