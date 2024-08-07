import json
import torch
import random
from backend.util import _parse_json, _parse_json_list, _get_entity_phrase, _match_word, _concat_all_env_info, _concat_contained_env_info, _concat_object_des, _concat_skill_info
from backend.dataloader import load_skill, load_object, load_task, load_object_alias
from backend.configure import OBJECT_EBD_PATH, SKILL_EBD_PATH, THRESHOLD, ME_EBD_PATH
import torch.nn.functional as F

from langchain.prompts import (
    ChatPromptTemplate,
    PromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)

BACKGROUND = "My name is NaNa. This is a spacious bar with dim lighting. Besides myself, the only other occupants are a bartender behind the counter and a heavily intoxicated customer slumped over a round table. Empty bottles litter the floor near the customer's feet. In the customer area of the bar, there are only two round tables and a few chairs. The bartender stands behind the counter, guarding the bar counter barrier—the sole entrance and exit." 

def _is_skill_required(llm, whisper_content):

    # res_data = True

    text_template = "An agent is going to {whisper_content}, decide if this is an everyday activity that anyone can do, or if it requires a particular skill.\n\
    For Example, open a drawer is an everyday activity, drive a car requires skill.\n\
    Output the response to the prompt above in json which includes one key: type.\n\
    If this is an everyday activity, value of the key is 0, else 1."
    
    prompt = PromptTemplate.from_template(text_template)
    prompt_text = prompt.format(whisper_content=whisper_content)
    msg = HumanMessage(content=prompt_text)
    res = llm.get_res(msg)
    res_json = _parse_json(res)

    res_data = False

    if 'type' in res_json:
        if str(res_json['type']) == '1':
            res_data = True
            
    return res_data

def _get_skill_required(llm, whisper_content):

    # res_data = {"id":1, "name":"painting"}

    text_template = "An agent is going to {whisper_content}, decide which kind of skill is most likely to be used.\n\
    Below are the skill types and their corresponding code names:\n\
    {skill_info}\
    Output the response to the prompt above in json which includes one key: type.\n\
    For Example, if analysis is most likely to be used, value of the key is 103."

    prompt = PromptTemplate.from_template(text_template)
    prompt_text = prompt.format(whisper_content=whisper_content, skill_info = _concat_skill_info())
    msg = HumanMessage(content=prompt_text)
    res = llm.get_res(msg)
    res_json = _parse_json(res)

    skill_list = load_skill()

    res_data = {}
    res_data['id'] = skill_list[0]['SkillID']
    res_data['name'] = skill_list[0]['SkillName']

    if 'type' in res_json:
        for skill in skill_list:
            if str(skill['SkillID']) == str(res_json['type']):
                res_data['id'] = skill['SkillID']
                res_data['name'] = skill['SkillName']

    return res_data


def GetSkillUsed(llm, whisper_content, my_skill_list):

    # res_data = {"type": 0, "skill":{"id":1, "name":"painting"}, "compare_data":{"real_num":20, "random_num":80, "res":1}}

    res_data = {}
    res_data['type'] = 0
    if _is_skill_required(llm, whisper_content):
        res_data['compare_data'] = {}
        res_data['compare_data']['real_num'] = 0
        res_data['skill'] = _get_skill_required(llm, whisper_content)

        for skill in my_skill_list:
            if skill['id'] == res_data['skill']['id']:
                res_data['compare_data']['real_num'] = skill['num']
        res_data['compare_data']['random_num'] = random.randint(0,100)
        if res_data['compare_data']['random_num'] <= res_data['compare_data']['real_num']:
            res_data['type'] = 1
        else:
            res_data['type'] = 2
    

    return res_data

def _get_object_list(nlp, ebd_model, whisper_content):

    object_list = []
    obj_list = load_object_alias()
    print(obj_list)
    doc = nlp(whisper_content)
    for token in doc:
        if token.pos_ == 'NOUN' or 'PROPN':
            object = _get_entity_phrase(token)
            index, max_similarity = _match_word(ebd_model, object, OBJECT_EBD_PATH)
            if max_similarity >= THRESHOLD:
                if obj_list[index]['ID'] in object_list:
                    continue
                else:
                    print(obj_list[index]['ID'])
                    object_list.append(obj_list[index]['ID'])
                    for id in obj_list[index]['AssociatedObjectsIDs']:
                        if id in object_list:
                            continue
                        else:
                            object_list.append(id)
    print(object_list)
    
    return object_list

def _match_reply_object(ebd_model, reply_res):

    reply_list = []
    obj_list = load_object_alias()
    for item in reply_res:
        index, max_similarity = _match_word(ebd_model, item['name'], OBJECT_EBD_PATH)
        if max_similarity >= THRESHOLD:
            res_data = {}
            res_data['id']= obj_list[index]['ID']
            if 'response' in item:
                res_data['response'] = item['response']
            if 'status' in item:
                res_data['status'] = item['status']
            reply_list.append(res_data)
        else:
            index, max_similarity = _match_word(ebd_model, item['name'], ME_EBD_PATH)
            if max_similarity >= THRESHOLD:
                res_data = {}
                res_data['id']= -1
                if 'response' in item:
                    res_data['response'] = item['response']
                if 'status' in item:
                    res_data['status'] = item['status']
                reply_list.append(res_data)
    
    return reply_list

def GetTextReply(llm, inputText, personality, lastConversation):

    text_template = "Here is your personality: \n\
    {personality} \n\
    Here's the last conversation: \n\
    {lastConversation} \n\
    Now, please answer to the following: \n\
    {inputText} \n\
    Output the response in json format with the key 'response'."

    prompt = PromptTemplate.from_template(text_template)
    prompt_text = prompt.format(personality=personality, lastConversation=lastConversation, inputText=inputText)
    print(prompt_text)
    msg = HumanMessage(content=prompt_text)
    res = llm.get_res(msg)
    res_json = _parse_json(res)

    return res_json['response']

def GetWhisperResult(llm, env_info, step):

    text_template = "【The following events occur in a virtual game scenario.】\n\
    Here's the current status in the scenario: \n\
    {env_text}\
    Now, My task is : {task_info}.\n\
    As long as one of the following conditions is met, it is judged to be a pass: \n\
    {method}\
    Judge if I have already passed the task.\n\
    Output the response to the prompt above in json, which includes two keys: result and hint.\n\
    If I passed, value of the result is 1, else 0. hint should not be direct."

    task_list = load_task()

    prompt = PromptTemplate.from_template(text_template)
    prompt_text = prompt.format(env_text = _concat_all_env_info(env_info), task_info = task_list[step]['Task'], method = task_list[step]['Method'])
    print(prompt_text)
    msg = HumanMessage(content=prompt_text)
    res = llm.get_res(msg)
    res_json = _parse_json(res)

    return res_json