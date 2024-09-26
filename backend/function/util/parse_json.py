import json
import ast

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

def _parse_list(input_str):
    start_idx = input_str.find('[')
    end_idx = input_str.find(']')
    
    if start_idx == -1 or end_idx == -1:
        return None  # 如果没有找到 [ 或 ]，返回 None 或者适当的错误处理
    
    # 提取包含列表的部分
    list_str = input_str[start_idx:end_idx+1]
    
    try:
        # 使用 ast 模块的 literal_eval 函数来将字符串转换为列表
        extracted_list = ast.literal_eval(list_str)
        return extracted_list
    except ValueError:
        return None  # 如果字符串不是有效的 Python 表达式，返回 None