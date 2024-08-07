## 快速上手
### 安装 anaconda
### 创建 python 3.9 环境
```bash
conda create -n Text2CV python=3.9
```
### 激活当前环境
```bash
conda activate Text2CV
```
### 切换至当前目录
```bash
cd Text2CharacterVox
```
### 安装python依赖
```bash
pip install -r requirement.txt
```
### 安装语言模型
```bash
python -m spacy download en_core_web_trf
```
### 写入Key -config.py

### 运行Demo
```bash
python main.py
```