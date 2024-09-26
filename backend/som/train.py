import numpy as np
from minisom import MiniSom
import pickle
from scipy.spatial.distance import euclidean
import json
import backend.config as cfg

# 1. 读取和处理数据
def load_data(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    
    impression_vectors = np.array([item['impression'] for item in data])
    embedding_vectors = np.array([item['embedding'] for item in data])
    
    return impression_vectors, embedding_vectors

# 假设数据保存在 'voice_data.json' 文件中
impression_vectors, embedding_vectors = load_data(cfg.CHARACTER_PATH)

# 数据归一化
impression_vectors = (impression_vectors - impression_vectors.min(axis=0)) / (impression_vectors.max(axis=0) - impression_vectors.min(axis=0))

# 2. 创建和训练SOM
som_dim = (12, 16)  # SOM网格大小,可以根据需要调整
som = MiniSom(som_dim[0], som_dim[1], impression_vectors.shape[1], sigma=1.0, learning_rate=0.5)
som.train_random(impression_vectors, 10000)  # 训练10000次迭代

# 3. 将embedding_vectors映射到SOM
som_mapping = {}
for i, iv in enumerate(impression_vectors):
    winner = som.winner(iv)
    som_mapping[winner] = embedding_vectors[i]

# 4. 保存训练好的SOM和映射
with open(cfg.SOM_MODEL_PATH, 'wb') as f:
    pickle.dump(som, f)
with open(cfg.SOM_MAPPING_PATH, 'wb') as f:
    pickle.dump(som_mapping, f)