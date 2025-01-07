import json
import matplotlib.pyplot as plt
import backend.config as cfg
import pandas as pd
import seaborn as sns
import umap
import numpy as np

def visualize_impression_distributions(data, save_path, dpi):
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
    plt.savefig(save_path, 
                bbox_inches='tight',
                dpi=dpi,
                format='png')

# 读取JSON文件
def load_timbre_data(json_data):
    # 将JSON字符串转换为字典
    if isinstance(json_data, str):
        data = json.loads(json_data)
    else:
        data = json_data
    
    # 提取向量数据和标签
    vectors = []
    labels = []
    for key, value in data.items():
        vectors.append(value['ebd'])
        labels.append(key)
    
    return np.array(vectors), labels

def load_impression_data(json_data):
    # 将JSON字符串转换为字典
    if isinstance(json_data, str):
        data = json.loads(json_data)
    else:
        data = json_data
    
    # 提取向量数据和标签
    vectors = []
    labels = []
    for item in data:
        vectors.append(item['impression'])
        labels.append("1")
    
    return np.array(vectors), labels

def visualize_umap(title, vectors, labels, save_path=None, dpi=300):
    # Configure UMAP
    reducer = umap.UMAP(
        n_components=2,
        n_neighbors=15,
        min_dist=0.1,
        metric='euclidean',
        random_state=42
    )
    
    # Perform dimensionality reduction
    embedding = reducer.fit_transform(vectors)
    
    # Set plot style
    plt.style.use('seaborn')
    plt.figure(figsize=(12, 8))
    
    # Create scatter plot
    scatter = plt.scatter(
        embedding[:, 0],
        embedding[:, 1],
        c=np.arange(len(labels)),
        cmap='viridis',
        alpha=0.6
    )
    
    # Add title and labels with improved font settings
    plt.title(title, fontsize=16, pad=20)
    plt.xlabel('UMAP Dimension 1', fontsize=12)
    plt.ylabel('UMAP Dimension 2', fontsize=12)
    
    # Add colorbar with improved formatting
    cbar = plt.colorbar(scatter)
    cbar.set_label('Sample Index', fontsize=12)
    
    # Improve tick label size
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)
    
    # Set layout
    plt.tight_layout()
    
    # Save the figure if path is provided
    if save_path:
        plt.savefig(save_path, dpi=dpi, bbox_inches='tight')

def visualize_umap_by_attribute(data, attribute, title, save_path=None, dpi=300):
    # 提取向量和属性值
    vectors = np.array([v['ebd'] for k, v in data.items()])
    attr_values = np.array([v[attribute] for k, v in data.items()])
    
    # 配置UMAP
    reducer = umap.UMAP(
        n_components=2,
        n_neighbors=15,
        min_dist=0.1,
        metric='euclidean',
        random_state=42
    )
    
    # 执行降维
    embedding = reducer.fit_transform(vectors)
    
    # 设置图形样式
    plt.style.use('seaborn')
    plt.figure(figsize=(12, 8))
    
    # 根据属性类型选择合适的颜色映射方案
    if attribute == 'gender':
        # 性别使用离散颜色
        unique_values = np.unique(attr_values)
        colors = ['#FF9999', '#99FF99', '#9999FF']  # 分别对应女性、中性、男性
        cmap = plt.matplotlib.colors.ListedColormap(colors[:len(unique_values)])
        scatter = plt.scatter(
            embedding[:, 0],
            embedding[:, 1],
            c=attr_values,
            cmap=cmap,
            alpha=0.6
        )
        # 添加图例
        gender_labels = ['Female', 'Neutral', 'Male']
        legend_elements = [plt.Line2D([0], [0], marker='o', color='w', 
                                    markerfacecolor=color, label=label, markersize=10)
                         for color, label in zip(colors, gender_labels)]
        plt.legend(handles=legend_elements)
    else:
       # 将连续值转换为三个档位
        colors = ['#FF9999', '#99FF99', '#9999FF']  # 使用相同的颜色方案
        
        # 定义档位的边界
        bins = [0, 3, 6, 10]  # 1-3, 4-6, 7-10
        labels = ['1-3', '4-6', '7-10']
        
        # 将连续值转换为档位类别
        categories = pd.cut(attr_values, 
                          bins=bins, 
                          labels=labels, 
                          include_lowest=True)
        
        # 将类别转换为数值以用于着色
        category_to_num = {label: i for i, label in enumerate(labels)}
        color_values = [category_to_num[cat] for cat in categories]
        
        # 创建颜色映射
        cmap = plt.matplotlib.colors.ListedColormap(colors)
        
        scatter = plt.scatter(
            embedding[:, 0],
            embedding[:, 1],
            c=color_values,
            cmap=cmap,
            alpha=0.6
        )
        
        # 添加图例
        legend_elements = [plt.Line2D([0], [0], marker='o', color='w',
                                    markerfacecolor=color, label=label, markersize=10)
                        for color, label in zip(colors, labels)]
        plt.legend(handles=legend_elements)
    
    # 设置标题和标签
    plt.title(f'UMAP Visualization by {attribute.capitalize()}', fontsize=16, pad=20)
    plt.xlabel('UMAP Dimension 1', fontsize=12)
    plt.ylabel('UMAP Dimension 2', fontsize=12)
    
    # 改进刻度标签大小
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)
    
    # 设置布局
    plt.tight_layout()
    
    # 如果提供了保存路径则保存图像
    if save_path:
        plt.savefig(save_path, dpi=dpi, bbox_inches='tight')
    plt.close()

def create_all_attribute_umaps(data, save_dir, dpi=300):
    attributes = ['gender', 'age', 'pitch', 'warmth', 'clarity',
                 'power', 'thickness', 'smoothness']
    
    for attr in attributes:
        save_path = f"{save_dir}/umap_{attr}_visualization.png"
        visualize_umap_by_attribute(
            data=data,
            attribute=attr,
            title=f'UMAP Visualization by {attr.capitalize()}',
            save_path=save_path,
            dpi=dpi
        )

def heatmap(data, save_path, dpi):
    # 转换数据为DataFrame格式
    df = pd.DataFrame([(k, v['gender'], v['age']) for k, v in data.items()],
                    columns=['id', 'gender', 'age'])

    # 创建交叉表
    heatmap_data = pd.crosstab(df['age'], df['gender'])

    # 创建图形
    plt.figure(figsize=(10, 8))

    # 绘制热力图
    sns.heatmap(heatmap_data, 
                annot=True,      # 显示数值
                fmt='d',         # 数值格式为整数
                cmap='YlOrRd',   # 色彩方案
                cbar_kws={'label': 'Count'})  # 颜色条标签

    # 设置标题和标签
    plt.title('Gender-Age Distribution', pad=20)
    plt.xlabel('Gender')
    plt.ylabel('Age')

    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=dpi, bbox_inches='tight')

if __name__ == "__main__":
    # 读取JSON文件
    with open(cfg.CHARACTER_ORIGIN_PATH, 'r') as file:
        origin_data = json.load(file)
        
    with open(cfg.CHARACTER_FORMAT_PATH, 'r') as f:
        format_data = json.load(f)
        
    create_all_attribute_umaps(origin_data, save_dir='./visualization', dpi=300)
    
    # heatmap(origin_data, save_path = "./visualization/gender_age_distribution.png", dpi=300)
    # visualize_impression_distributions(format_data, save_path= './visualization/impression_distributions.png', dpi=300)
    
    # vectors, labels = load_impression_data(format_data)
    # visualize_umap('UMAP Visualization of Impression Vectors', vectors, labels, save_path='./visualization/umap_impression_visualization.png', dpi=300)
    
    # vectors, labels = load_timbre_data(origin_data)
    # visualize_umap('UMAP Visualization of Timbre Vectors', vectors, labels, save_path='./visualization/umap_timbre_visualization.png', dpi=300)