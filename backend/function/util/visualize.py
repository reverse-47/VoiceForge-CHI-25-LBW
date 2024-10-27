import backend.config as cfg
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

def visualize_impression_distributions(data):
    # 将数据转换为DataFrame格式
    dimensions = ['gender', 'age', 'pitch', 'warmth', 'clarity', 
                 'power', 'thickness', 'smoothness', 'emotion']
    
    # 提取impression向量
    impressions = [d['impression'] for d in data]
    df = pd.DataFrame(impressions, columns=dimensions)
    
    # 创建3x3的子图布局
    fig, axes = plt.subplots(3, 3, figsize=(20, 20))
    fig.suptitle('Distribution Analysis of Impression Dimensions', fontsize=16, y=1.02)
    
    # 用于存储统计信息的字典
    stats_info = {}
    
    # 为每个维度创建分布图
    for idx, (dim, ax) in enumerate(zip(dimensions, axes.ravel())):
        # 绘制直方图和核密度估计
        sns.histplot(data=df[dim], kde=True, ax=ax, bins=15)
        
        # 计算统计信息
        mean = df[dim].mean()
        median = df[dim].median()
        
        # 设置图形标题和标签
        ax.set_title(f'{dim.capitalize()} Distribution')
        ax.set_xlabel('Value')
        ax.set_ylabel('Count')
        
        # 添加均值和中位数的垂直线
        ax.axvline(mean, color='red', linestyle='--', alpha=0.5, label='Mean')
        ax.axvline(median, color='green', linestyle='--', alpha=0.5, label='Median')
        ax.legend()

    # 调整子图之间的间距
    plt.tight_layout()
    
    # 保存图片
    plt.savefig('./backend/data/character/impression_distributions.png', 
                bbox_inches='tight',
                dpi=300,
                format='png')
    
    return plt

if __name__ == "__main__":
    with open(cfg.CHARACTER_FORMAT_PATH, 'r') as f:
        data = json.load(f)
    plt = visualize_impression_distributions(data)
    plt.show()