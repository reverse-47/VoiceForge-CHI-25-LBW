import json
import csv
import backend.config as cfg
import pandas as pd

with open(cfg.CHARACTER_ORIGIN_PATH) as json_file:
    data = json.load(json_file)

first_key = list(data.keys())[0]

# 创建列名
all_columns = ['file', 'gender', 'age', 'pitch', 'warmth', 'clarity', 
                            'power', 'thickness', 'smoothness', 'emotion', 'embedding']

# 准备数据
rows = []
for id_, values in data.items():
    row = [
        id_+".wav",
        values['gender'],
        values['age'],
        values['pitch'],
        values['warmth'],
        values['clarity'],
        values['power'],
        values['thickness'],
        values['smoothness'],
        values['emotion'],
        values['ebd']
    ]
    rows.append(row)

# 创建DataFrame
df = pd.DataFrame(rows, columns=all_columns)

# 保存为CSV
df.to_csv('./backend/data/character/tone.csv', index=False)
print(f"已将数据保存")