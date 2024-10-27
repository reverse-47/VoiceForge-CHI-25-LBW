import json
import backend.config as cfg

def convert_json_format(input_json):
    """
    将输入的JSON数据转换为新的格式，impression包含9个维度
    
    Args:
        input_json: 字符串或字典形式的输入JSON数据
    
    Returns:
        list: 转换后的数据列表
    """
    # 如果输入是字符串，则解析为字典
    if isinstance(input_json, str):
        data = json.loads(input_json)
    else:
        data = input_json
    
    # 创建结果列表
    result = []
    
    # 遍历输入JSON的每个条目
    for key, entry in data.items():
        # 创建新的数据条目
        new_entry = {
            "impression": [
                entry["gender"],
                entry["age"],
                entry["pitch"],
                entry["warmth"],
                entry["clarity"],
                entry["power"],
                entry["thickness"],
                entry["smoothness"],
                entry["emotion"]  # 将emotion作为第9个维度
            ],
            "embedding": entry["ebd"]
        }
        
        result.append(new_entry)
    
    return result

# 使用示例
if __name__ == "__main__":
    with open(cfg.CHARACTER_ORIGIN_PATH, 'r', encoding='utf-8') as f:
        input_data = json.load(f)
    
    # 转换数据
    converted_data = convert_json_format(input_data)
    
    # 写入输出文件
    with open(cfg.CHARACTER_FORMAT_PATH, 'w', encoding='utf-8') as f:
        json.dump(converted_data, f, indent=2)