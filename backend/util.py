import json
import torch
from backend.dataloader import load_skill, load_object
from torch.nn.functional import cosine_similarity

def _parse_json(res):
    tmp_json_str = ""
    res_json_data = {}
    for item in res:
        if item == "{":
            tmp_json_str = item
            continue
        tmp_json_str += item
        if item == "}":
            res_json_data = json.loads(tmp_json_str)
            break
    print(res_json_data)
    return res_json_data

def _parse_json_list(res):
    tmp_json_str = ""
    json_list = []
    for item in res:
        if item == "{":
            tmp_json_str = item
            continue
        tmp_json_str += item
        if item == "}":
            res_json_data = json.loads(tmp_json_str)
            json_list.append(res_json_data)

    return json_list

def _time_int_to_str(time) :
    hour = _time_format(str(time // 60))
    minute = _time_format(str(time % 60))
    return hour + ":" + minute

def _time_format(time):
    if (len(time) <= 1):
        time = "0" + time
    return time

def _get_entity_phrase(token):
    # Get the single entity
    mod_phrase = ""
    entity_phrase = token.text
    for child in token.children:
        if child.dep_ in ['amod', 'compound', 'poss']:
            mod_phrase += ' ' + _get_mod_phrase(child)
    if mod_phrase != "":
        entity_phrase = mod_phrase + ' ' + entity_phrase
    
    return entity_phrase

def _get_mod_phrase(token):
    # Get the modification before the object
    mod_phrase = token.text
    for child in token.children:
        if child.dep_ in ['amod', 'compound', 'advmod']:
            mod_phrase = _get_mod_phrase(child)+ ' ' + mod_phrase

    return mod_phrase

def _match_word(ebd_model, word, embedding_path):
    word_embedding = torch.tensor(ebd_model.encode(word.lower()))
    word_matrix = torch.load(embedding_path)
    word_similarities = cosine_similarity(word_matrix, word_embedding)
    max_word_similarity = torch.max(word_similarities).item()
    word_index = torch.argmax(word_similarities).item()

    return word_index, max_word_similarity

def _concat_skill_info():
    skill_info = ""
    skill_list = load_skill()
    for skill in skill_list:
        skill_info = str(skill['SkillID'])+" - "+skill['SkillName']+'\n'

    return skill_info

def _concat_all_env_info(env_info):
    env_text = ""
    for env_obj in env_info:
        if 'status' in env_obj:
            env_text += env_obj['name']+' - '+ env_obj['status']+'\n'
    return env_text

def _concat_contained_env_info(object_list, env_info):
    env_text = ""
    for object in object_list:
        for env_obj in env_info:
            if object == env_obj['id']:
                env_text += env_obj['name']+' - '+ env_obj['status']+'\n'
    return env_text

def _concat_object_des(object_list):
    object_info  = ""
    all_object_list = load_object()
    for object in object_list:
        for obj in all_object_list:
            if object == obj['ID']:
                object_info += obj['Name']+' - '+ obj['Description']+'\n'
    return object_info