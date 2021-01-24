import os
import json
import random
from tqdm import tqdm

root = "./data/outputs/3.json"
deepke_output_root = './data'
output_train_file = os.path.join(deepke_output_root, 'train.csv')
output_valid_file = os.path.join(deepke_output_root, 'valid.csv')
output_test_file = os.path.join(deepke_output_root, 'test.csv')
output_relation_file = os.path.join(deepke_output_root, 'relation.csv')
if not os.path.exists(deepke_output_root):
    os.makedirs(deepke_output_root)
instance_header = 'sentence,relation,head,head_offset,tail,tail_offset'
relation_header = 'head_type,tail_type,relation,index\nNone,None,None,0'


def load_content(root):
    fr = open(root, 'r', encoding='utf-8')
    data = json.load(fr)
    fr.close()
    return data["content"]


def load_entities(root):
    fr = open(root, 'r', encoding='utf-8')
    data = json.load(fr)
    fr.close()
    return data["outputs"]["annotation"]["T"]


def process_content(content):
    sentences = content.split("\n")
    sentences_offset = [0]
    for sentence in sentences:
        end_idx = sentences_offset[-1]+len(sentence)+1
        sentences_offset.append(end_idx)
    return sentences, sentences_offset


def global2sent_offset(start, end, sentences_offset):
    r"""将相对于全文(content)的offset转换为相对于所在句子的offset
    Arguments:
        start (int): The start offset relative to the content.
        end (int): The end offset relative to the content.
    Returns:
        sent_id (int): The sentence id where contains start and end.
        sent_start (int): The start offset relative to the sentence.
        sent_end (int): The start offset relative to the sentence.
    Examples::
        >>> head_sent_id, head_offset, head_offset_end = f(head_item['start'], head_item['end'])
    """
    for idx, i in enumerate(sentences_offset[:-1]):
        if start >= sentences_offset[idx] and start < sentences_offset[idx+1]:
            sent_id = idx
            sent_start, sent_end = start-i, end-i
            break

    return sent_id, sent_start, sent_end


def process_vivrecard_entities(entities_list, content):
    r"""解析vivrecard标注文件中的所有entities数据.
    实体数据的标注格式实例
    [
        "",
        {
            "attributes": [],
            "end": 7,
            "id": 1,
            "name": "人",
            "start": 0,
            "type": "T",
            "value": "蒙其·D·路飞"
        },
    ]
    Arguments:
        entities_list (list): Entities list in vivre card
            annotation file.
    Returns:
        entities_dict (dict): A dict, key is entity id,
            value is corresponding entity item.
        entities_type_name_dict (dict): A dict, key is entity type,
            value is entity names that belong to this type.
        annot_entity_sentid_set (set): The sentence id that 
            has been annotated with entity.
    Examples::
        >>> entities_dict = process_vivrecard_entities(entities_list)
    """
    cnt = 0
    entity_type_set = set()
    entities_name_set = set()
    entities_name_list = list()
    entities_dict = dict()

    # key为实体名字(item['value']), value为一个set，set里面包含对应的实体类型，
    # 主要用于纠错，判断是否一个实体对应了多个类型
    entities_name_type_dict = dict()
    entities_type_name_dict = dict()
    annot_entity_sentid_set = set()  # 被annot实体的句子集合
    _, sentences_offset = process_content(content)
    for item in entities_list:
        if not isinstance(item, dict):
            continue

        entity_id = item['id']
        entity_name = item['value']
        entity_type = item['name']

        entity_type_set.add(entity_type)
        entities_name_set.add(entity_name)
        entities_name_list.append(entity_name)

        entities_dict[entity_id] = item

        sent_id, _, _ = global2sent_offset(
            item['start'], item['end'], sentences_offset)
        annot_entity_sentid_set.add(sent_id)

        if entity_name not in entities_name_type_dict.keys():
            entities_name_type_dict[entity_name] = set()
        entities_name_type_dict[entity_name].add(entity_type)

        if entity_type not in entities_type_name_dict.keys():
            entities_type_name_dict[entity_type] = set()
        entities_type_name_dict[entity_type].add(entity_name)

    print('Entity type: {}'.format(entity_type_set))
    print('Entity type Number: {}'.format(len(entity_type_set)))
    print('Diff Entities name Number: {}'.format(len(entities_name_set)))
    print('Valid Entities name Number: {}'.format(len(entities_name_list)))

    # 进行检查，每一个实体只能对应一种类型
    for name in entities_name_type_dict:
        type_set = entities_name_type_dict[name]
        if len(type_set) != 1:
            print('[ERROR] Entity [{}] has more than one type: {}'.format(
                name, type_set))
            exit(-1)

    for etype in entities_type_name_dict:
        name_list = sorted(list(entities_type_name_dict[etype]))
        entities_type_name_dict[etype] = name_list

    return entities_dict, entities_type_name_dict, annot_entity_sentid_set


if __name__ == '__main__':
    entities = load_entities(root)
    content = load_content(root)
    entities_dict = process_vivrecard_entities(entities, content)
    print(entities)
