import pandas as pd
import json
import math
from pathlib import Path
from typing import List, Dict
import backend.config as cfg
import numpy as np

def process_csv_files(csv_paths: List[str]) -> None:
    """
    处理多个CSV文件，计算平均标签值，并更新JSON文件
    
    Args:
        csv_paths: CSV文件路径列表
        tone_path: 输出JSON文件路径
    """
    # 标签列表（除去FileName）
    label_columns = ['Gender', 'Age', 'Pitch', 'Warmth', 'Clarity', 
                    'Power', 'Thickness', 'Smoothness', 'Emotion']
    
    # 读取所有CSV文件并存储到列表中
    dataframes = []
    for csv_path in csv_paths:
        try:
            df = pd.read_csv(csv_path)
            dataframes.append(df)
        except Exception as e:
            print(f"读取CSV文件 {csv_path} 时出错: {str(e)}")
            continue
    
    if not dataframes:
        raise ValueError("没有成功读取任何CSV文件")
    
    # 计算平均值
    # 首先合并所有DataFrame
    all_data = pd.concat(dataframes)
    # 按FileName分组并计算平均值
    avg_data = all_data.groupby('FileName')[label_columns].mean()
    # 向上取整
    avg_data = np.ceil(avg_data)
    
    # 读取现有的JSON文件
    try:
        with open(cfg.CHARACTER_ORIGIN_PATH, 'r', encoding='utf-8') as f:
            tone_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        tone_data = {}
    
    # 更新每个文件的标签
    for filename in avg_data.index:
        file_id = filename.replace('.wav', '')
        
        # 如果文件ID不在tone_data中，创建新条目
        if file_id not in tone_data:
            print("err: " + file_id + " not exist")
            # tone_data[file_id] = {}
            
        # 更新标签值
        row = avg_data.loc[filename]
        tone_data[file_id].update({
            'gender': int(row['Gender']),
            'age': int(row['Age']),
            'pitch': int(row['Pitch']),
            'warmth': int(row['Warmth']),
            'clarity': int(row['Clarity']),
            'power': int(row['Power']),
            'thickness': int(row['Thickness']),
            'smoothness': int(row['Smoothness']),
            'emotion': int(row['Emotion'])
        })
    
    # 保存更新后的数据
    with open(cfg.CHARACTER_ORIGIN_PATH, 'w', encoding='utf-8') as f:
        json.dump(tone_data, f, indent=4, ensure_ascii=False)

# 使用示例
if __name__ == "__main__":
    # 假设CSV文件都在同一目录下
    csv_files = [
        "./backend/data/character/label/Sheet1.csv",
        "./backend/data/character/label/Sheet2.csv",
        "./backend/data/character/label/Sheet3.csv"
    ]
    
    try:
        process_csv_files(csv_files)
        print("成功处理CSV文件并更新标签")
    except Exception as e:
        print(f"处理CSV文件时发生错误: {str(e)}")