import json
from backend.configure import OBJECT_JSON_PATH, SKILL_JSON_PATH, NPC_SCHEDULE_JSON_PATH, TASK_JSON_PATH, ME_JSON_PATH

def load_skill():
    with open(SKILL_JSON_PATH, 'r') as file:
        skill_list = json.load(file)

    return skill_list

def load_object():
    with open(OBJECT_JSON_PATH, 'r') as file:
        obj_list = json.load(file)

    return obj_list

def load_me():
    with open(ME_JSON_PATH, 'r') as file:
        me_list = json.load(file)

    return me_list

def load_object_alias():
    object_list = []
    with open(OBJECT_JSON_PATH, 'r') as file:
        obj_list = json.load(file)

    for item in obj_list:
        tmp_json = {}
        tmp_json['ID'] = item['ID']
        tmp_json['Name'] = item['Name']
        tmp_json['AssociatedObjectsIDs'] = item['AssociatedObjectsIDs']
        object_list.append(tmp_json)
        for alias in item['Aliass']:
            tmp_json = {}
            tmp_json['ID'] = item['ID']
            tmp_json['Name'] = alias
            tmp_json['AssociatedObjectsIDs'] = item['AssociatedObjectsIDs']
            object_list.append(tmp_json)

    return object_list

def load_npc_schedule():
    with open(NPC_SCHEDULE_JSON_PATH, 'r') as file:
        npc_schedule = json.load(file)

    return npc_schedule 

def load_task():
    with open(TASK_JSON_PATH, 'r') as file:
        task_list = json.load(file)

    return task_list