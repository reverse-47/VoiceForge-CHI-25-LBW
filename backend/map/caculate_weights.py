import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression, Lasso
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import mutual_info_regression
import json
import torch
import backend.config as cfg

def load_data(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    
    impressions = np.array([item['impression'] for item in data])
    embeddings = np.array([item['embedding'] for item in data])
    return impressions, embeddings

def custom_normalize_impressions(impressions):
    """
    根据每个dimension的实际范围进行归一化
    将每个维度的值归一化到[0,1]范围
    """
    # 定义每个dimension的范围
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
    
    normalized = np.zeros_like(impressions, dtype=np.float32)
    
    for i, (min_val, max_val) in enumerate(ranges):
        # 将每个维度归一化到[0,1]
        normalized[:, i] = (impressions[:, i] - min_val) / (max_val - min_val)
    
    return normalized

def analyze_feature_importance(file_path):
    # 1. 加载数据
    impressions, embeddings = load_data(file_path)
    print("\nData shape:")
    print(f"Impressions shape: {impressions.shape}")
    print(f"Embeddings shape: {embeddings.shape}")
    
    # 2. 数据归一化 - 使用自定义归一化替代StandardScaler
    impressions_normalized = custom_normalize_impressions(impressions)
    
    # 打印归一化前后的统计信息
    # print("\nImpression statistics before and after normalization:")
    # for i, dim in enumerate(['gender', 'age', 'pitch', 'warmth', 'clarity', 
    #                        'power', 'thickness', 'smoothness', 'emotion']):
    #     print(f"\n{dim}:")
    #     print(f"Original - min: {impressions[:, i].min():.2f}, max: {impressions[:, i].max():.2f}, "
    #           f"mean: {impressions[:, i].mean():.2f}, std: {impressions[:, i].std():.2f}")
    #     print(f"Normalized - min: {impressions_normalized[:, i].min():.2f}, max: {impressions_normalized[:, i].max():.2f}, "
    #           f"mean: {impressions_normalized[:, i].mean():.2f}, std: {impressions_normalized[:, i].std():.2f}")
    
    # 3. 多元线性回归分析
    def linear_regression_importance(X, y):
        model = LinearRegression()
        importance_matrix = np.zeros((X.shape[1], y.shape[1]))
        for i in range(y.shape[1]):
            model.fit(X, y[:, i])
            importance_matrix[:, i] = np.abs(model.coef_)
        return np.mean(importance_matrix, axis=1)
    
    lr_importance = linear_regression_importance(impressions_normalized, embeddings)
    
    # 4. LASSO回归分析
    def lasso_importance(X, y, alpha=0.01):
        model = Lasso(alpha=alpha)
        importance_matrix = np.zeros((X.shape[1], y.shape[1]))
        for i in range(y.shape[1]):
            model.fit(X, y[:, i])
            importance_matrix[:, i] = np.abs(model.coef_)
        return np.mean(importance_matrix, axis=1)
    
    lasso_importance = lasso_importance(impressions_normalized, embeddings)
    
    # 5. 随机森林特征重要性分析
    def random_forest_importance(X, y):
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        importance_matrix = np.zeros((X.shape[1], y.shape[1]))
        for i in range(y.shape[1]):
            model.fit(X, y[:, i])
            importance_matrix[:, i] = model.feature_importances_
        return np.mean(importance_matrix, axis=1)
    
    rf_importance = random_forest_importance(impressions_normalized, embeddings)
    
    # 6. 互信息分析
    def mutual_info_importance(X, y):
        importance_matrix = np.zeros((X.shape[1], y.shape[1]))
        for i in range(y.shape[1]):
            importance_matrix[:, i] = mutual_info_regression(X, y[:, i])
        return np.mean(importance_matrix, axis=1)
    
    mi_importance = mutual_info_importance(impressions_normalized, embeddings)
    
    # 创建结果DataFrame
    dimension_names = ['gender', 'age', 'pitch', 'warmth', 'clarity', 
                      'power', 'thickness', 'smoothness', 'emotion']
    
    # 将所有权重归一化到0-1范围
    def normalize_weights(weights):
        return weights / np.sum(weights)
    
    # 计算LASSO权重并归一化
    lasso_weights_normalized = normalize_weights(lasso_importance)
    
    # 使用LASSO权重计算加权后的impressions
    weighted_impressions = np.multiply(impressions_normalized, lasso_weights_normalized)
    
    # # 创建结果DataFrame用于显示所有方法的结果
    # dimension_names = ['gender', 'age', 'pitch', 'warmth', 'clarity', 
    #                   'power', 'thickness', 'smoothness', 'emotion']
    
    # results = pd.DataFrame({
    #     'Dimension': dimension_names,
    #     'Linear_Regression': normalize_weights(lr_importance),
    #     'Lasso': lasso_weights_normalized,
    #     'Random_Forest': normalize_weights(rf_importance),
    #     'Mutual_Information': normalize_weights(mi_importance)
    # })
    
    # 打印每种方法的权重结果
    # print("\n1. Linear Regression Weights:")
    # for dim, weight in zip(dimension_names, results['Linear_Regression']):
    #     print(f"{dim}: {weight:.4f}")
        
    # print("\n2. Lasso Regression Weights:")
    # for dim, weight in zip(dimension_names, results['Lasso']):
    #     print(f"{dim}: {weight:.4f}")
        
    # print("\n3. Random Forest Weights:")
    # for dim, weight in zip(dimension_names, results['Random_Forest']):
    #     print(f"{dim}: {weight:.4f}")
        
    # print("\n4. Mutual Information Weights:")
    # for dim, weight in zip(dimension_names, results['Mutual_Information']):
    #     print(f"{dim}: {weight:.4f}")

    # 保存LASSO权重
    weight_dict = {
        'weights': torch.FloatTensor(lasso_weights_normalized),
        'dimension_names': dimension_names
    }
    print(weight_dict)
    torch.save(weight_dict, cfg.PROCESSED_DATA_PATH+'lasso_weights.pt')
    print("\nLASSO weights have been saved to 'lasso_weights.pt'")
    
    # 保存加权后的数据
    data_dict = {
        'weighted_impressions': torch.FloatTensor(weighted_impressions),
        'embeddings': torch.FloatTensor(embeddings)
    }
    print(data_dict)
    torch.save(data_dict, cfg.PROCESSED_DATA_PATH+'weighted_data.pt')
    print("\nWeighted data has been saved to 'weighted_data.pt'")

    # 打印保存的数据结构
    # print("\nSaved data structures:")
    # print("\nlasso_weights.pt contains:")
    # print("- weights: tensor of shape", weight_dict['weights'].shape)
    # print("- dimension_names: list of dimension names")
    
    # print("\nweighted_data.pt contains:")
    # print("- weighted_impressions: tensor of shape", data_dict['weighted_impressions'].shape)
    # print("- embeddings: tensor of shape", data_dict['embeddings'].shape)

    # return results

if __name__ == "__main__":
    file_path = cfg.CHARACTER_FORMAT_PATH  # 请确保更改为你的数据文件路径
    results = analyze_feature_importance(cfg.CHARACTER_FORMAT_PATH)