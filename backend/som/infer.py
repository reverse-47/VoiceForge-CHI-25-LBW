import numpy as np
from minisom import MiniSom
import pickle
from scipy.spatial.distance import euclidean
import backend.config as cfg

min_values = np.array([1, 1, 1, 1, 1, 1, 1, 1])
max_values = np.array([3, 5, 5, 5, 5, 5, 5, 5])

def generate_new_impression():
    new_impression = np.zeros(8, dtype=int)
    new_impression[0] = np.random.randint(1, 4)  # 第一个值范围是1-3
    new_impression[1:] = np.random.randint(1, 6, size=7)  # 后7个值范围是1-5
    return new_impression

# 找到k个最近邻并计算加权平均
def get_k_nearest_neighbors(som, som_mapping, input_vector, k=5):
    distances = np.array([euclidean(input_vector, som._weights[i, j]) 
                          for i in range(som._weights.shape[0]) 
                          for j in range(som._weights.shape[1])])
    
    nearest_indices = distances.argsort()
    
    k_nearest_embeddings = []
    k_nearest_distances = []
    for idx in nearest_indices:
        i, j = idx // som._weights.shape[1], idx % som._weights.shape[1]
        if (i, j) in som_mapping:
            k_nearest_embeddings.append(som_mapping[(i, j)])
            k_nearest_distances.append(distances[idx])
        if len(k_nearest_embeddings) == k:
            break
    
    return np.array(k_nearest_embeddings), np.array(k_nearest_distances)

# 预测函数
def predict_embedding_weighted(impression_vector, k=5):
    # 加载SOM模型和映射
    with open(cfg.SOM_MODEL_PATH, 'rb') as f:
        som = pickle.load(f)
    with open(cfg.SOM_MAPPING_PATH, 'rb') as f:
        som_mapping = pickle.load(f)
    
    # 归一化输入向量
    impression_vector = (impression_vector - min_values) / (max_values - min_values)
    
    # 获取前k个最近的邻居
    nearest_embeddings, distances = get_k_nearest_neighbors(som, som_mapping, impression_vector, k)
    if(len(nearest_embeddings)==0):
        print("no matching")
    # 计算加权平均
    weights = 1 / (distances + 1e-6)  # 防止除以零
    weights /= np.sum(weights)  # 归一化权重
    
    weighted_embedding = np.average(nearest_embeddings, axis=0, weights=weights)
    
    return weighted_embedding

# 普通预测函数
def predict_embedding(impression_vector):
    # 加载保存的模型和映射
    with open(cfg.SOM_MODEL_PATH, 'rb') as f:
        som = pickle.load(f)
    with open(cfg.SOM_MAPPING_PATH, 'rb') as f:
        som_mapping = pickle.load(f)
    
    # 归一化输入向量
    impression_vector = (impression_vector - impression_vector.min()) / (impression_vector.max() - impression_vector.min())
    
    # 找到最佳匹配单元(BMU)
    winner = som.winner(impression_vector)
    
    # 返回对应的timbre向量
    return som_mapping.get(winner, "No matching timbre found")

# 普通预测使用示例
# new_impression = np.random.rand(8)  # 新的印象向量
# predicted_timbre = predict_timbre(new_impression)
# print("Predicted timbre vector:", predicted_timbre)

# 权重预测使用示例
# new_impression = generate_new_impression()
# predicted_embedding = predict_embedding_weighted(new_impression, k=5)
# print("Predicted weighted embedding vector:", predicted_embedding)