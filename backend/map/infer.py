import torch
import numpy as np
import backend.config as cfg

def custom_normalize_impression(impression):
    """
    对单个impression进行归一化
    """
    ranges = [
        (1, 3),    # gender: 1-3
        (1, 10),   # age: 1-10
        (1, 10),   # pitch: 1-10
        (1, 10),   # warmth: 1-10
        (1, 10),   # clarity: 1-10
        (1, 10),   # power: 1-10
        (1, 10),   # thickness: 1-10
        (1, 10),   # smoothness: 1-10
        (1, 6)     # emotion: 1-6
    ]
    
    normalized = np.zeros_like(impression, dtype=np.float32)
    for i, (min_val, max_val) in enumerate(ranges):
        normalized[i] = (impression[i] - min_val) / (max_val - min_val)
    
    return normalized

def find_similar_weighted_impressions(query_impression, weighted_data, k=3):
    """
    找到最相似的k个weighted_impression，只使用前8个维度
    """
    # 获取所有加权印象和对应的embeddings
    all_weighted_impressions = weighted_data['weighted_impressions']
    all_embeddings = weighted_data['embeddings']
    
    # 只使用前8个维度计算相似度
    query_impression = query_impression[:8]
    all_weighted_impressions = all_weighted_impressions[:, :8]
    
    # 计算余弦相似度
    query_norm = torch.norm(query_impression)
    all_norms = torch.norm(all_weighted_impressions, dim=1)
    
    # 归一化向量
    query_normalized = query_impression / query_norm
    all_normalized = all_weighted_impressions / all_norms.unsqueeze(1)
    
    # 计算余弦相似度
    similarities = torch.matmul(all_normalized, query_normalized)
    
    # 获取最相似的k个索引
    top_k_similarities, top_k_indices = torch.topk(similarities, k)
    print(top_k_indices)
    
    # 获取对应的embeddings
    similar_embeddings = all_embeddings[top_k_indices]
    
    return similar_embeddings, top_k_similarities

def generate_embedding(query_impression, k=3):
    """
    根据新的impression生成对应的embedding
    """
    # 1. 加载保存的权重和数据
    weights_data = torch.load(cfg.PROCESSED_DATA_PATH+'lasso_weights.pt')
    weighted_data = torch.load(cfg.PROCESSED_DATA_PATH+'weighted_data.pt')
    
    # 2. 对输入impression进行归一化
    normalized_impression = custom_normalize_impression(query_impression)
    
    # 3. 应用权重
    weights = weights_data['weights']
    weighted_impression = torch.FloatTensor(normalized_impression * weights.numpy())
    
    # 4. 找到最相似的k个weighted_impression对应的embedding
    similar_embeddings, similarities = find_similar_weighted_impressions(weighted_impression, weighted_data, k)
    
    # 5. 计算相似度作为权重
    # 如果存在完全相同的样本(similarity=1)，直接使用该样本的embedding
    if torch.max(similarities) > 0.9999:
        max_idx = torch.argmax(similarities)
        return similar_embeddings[max_idx]
    
    # 否则使用softmax将相似度转换为权重
    weights = torch.softmax(similarities / 0.05, dim=0)  # temperature=0.1 控制权重分布的峰度
    
    # 6. 加权平均得到新的embedding
    new_embedding = torch.sum(similar_embeddings * weights.unsqueeze(1), dim=0)
    
    return new_embedding

def get_most_similar_embedding(query_impression):
    """
    找到最相似的样本并直接返回其embedding
    """
    # 1. 加载保存的权重和数据
    weights_data = torch.load(cfg.PROCESSED_DATA_PATH+'lasso_weights.pt')
    weighted_data = torch.load(cfg.PROCESSED_DATA_PATH+'weighted_data.pt')
    
    # 2. 对输入impression进行归一化
    normalized_impression = custom_normalize_impression(query_impression)
    
    # 3. 应用权重（只取前8个维度）
    weights = weights_data['weights'][:2]  # 只取前8个维度的权重
    weighted_impression = torch.FloatTensor(normalized_impression[:2] * weights.numpy())  # 只用前8个维度
    
    # 4. 找到最相似的weighted_impression对应的embedding
    all_weighted_impressions = weighted_data['weighted_impressions'][:, :2]  # 只用前8个维度
    all_embeddings = weighted_data['embeddings']
    
    # 计算余弦相似度
    query_norm = torch.norm(weighted_impression)
    all_norms = torch.norm(all_weighted_impressions, dim=1)
    
    # 归一化向量
    query_normalized = weighted_impression / query_norm
    all_normalized = all_weighted_impressions / all_norms.unsqueeze(1)
    
    # 计算余弦相似度
    similarities = torch.matmul(all_normalized, query_normalized)
    
    # 获取最相似的索引
    max_similarity, max_idx = torch.max(similarities, dim=0)
    print(max_idx)
    
    return all_embeddings[max_idx]

if __name__ == "__main__":
    # 测试用例
    test_impression = np.array([2, 5, 7, 6, 8, 7, 5, 6, 3])  # 示例输入
    new_embedding = generate_embedding(test_impression, k=3)
    print(f"Generated embedding shape: {new_embedding.shape}")
    
    # 如果需要可以保存结果
    # torch.save(new_embedding, 'new_embedding.pt')