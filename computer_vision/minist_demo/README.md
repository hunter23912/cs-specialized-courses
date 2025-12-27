# MNIST手写数字识别项目

## 项目概述
本项目基于PyTorch框架，使用MNIST手写数字数据集，实现了卷积神经网络(CNN)和多层感知器(MLP)模型用于手写数字识别任务。项目不仅包含基本的训练和测试功能，还实现了数据增强、模型集成、特征可视化、自定义数据集收集与标注等计算机视觉领域常用技术。

## 项目特点
1. **多种模型架构**：CNN模型、MLP模型、带批归一化的高级CNN和ResNet变体
2. **数据增强与预处理**：随机旋转、平移、噪声等增强技术
3. **综合性能评估**：训练时间、准确率、不同数据规模的影响等
4. **特征可视化**：卷积滤波器、特征图、GradCAM可解释性分析
5. **模型集成**：组合多个模型提高性能
6. **自定义数据收集与标注**：实现交互式手写数字标注工具
7. **实际应用演示**：从摄像头或图像文件识别手写数字

## 项目结构
```
minist_demo/
├── main.py                 # 主程序入口
├── models.py               # 神经网络模型定义
├── experiment.py           # 实验管理类
├── visualizer.py           # 结果可视化
├── data_augmentation.py    # 数据增强
├── model_ensemble.py       # 模型集成
├── features.py             # 特征可视化
├── custom_dataset.py       # 自定义数据集管理
├── real_world_demo.py      # 实际应用演示
├── model_dict/             # 模型和结果存储
│   ├── mnist_model.pth
│   ├── training_results_cpu.json
│   └── training_results_gpu.json
├── data/                   # MNIST数据集
├── custom_data/            # 自定义手写数字数据
└── results/                # 生成的结果图像
```

## 使用方法

### 安装依赖
```bash
pip install torch torchvision numpy matplotlib seaborn scikit-learn opencv-python pillow tqdm
```

### 运行模式
项目支持多种运行模式，通过命令行参数`--mode`指定：

1. **训练模式**
```bash
python main.py --mode train --data_size 10000 --epochs 5
```

2. **可视化结果**
```bash
python main.py --mode visualize --results model_dict/training_results_gpu.json
```

3. **数据增强演示**
```bash
python main.py --mode augment
```

4. **模型集成**
```bash
python main.py --mode ensemble --data_size 10000
```

5. **特征可视化**
```bash
python main.py --mode features --model model_dict/mnist_model.pth
```

6. **自定义数据集标注和测试**
```bash
python main.py --mode custom
```

7. **实际应用演示**
```bash
python main.py --mode demo --model model_dict/mnist_model.pth
```

## 项目核心技术

### 1. 卷积神经网络模型
- 三层卷积层+池化层+全连接层
- 约22万参数
- 准确率可达99%

### 2. 数据增强
- 随机旋转、平移、缩放
- 高斯噪声、随机擦除
- 帮助模型提高泛化能力

### 3. 特征可视化与模型解释
- 可视化卷积核和特征图
- t-SNE和PCA降维展示高维特征
- GradCAM热力图解释模型决策

### 4. 模型集成
- 结合CNN、MLP、高级CNN和ResNet的预测结果
- 使用多数投票方式进行最终预测
- 提高模型的鲁棒性和准确率

## 实验结果
- 模型在MNIST测试集上的准确率可达99%
- 数据规模为60000时，训练时间约为100秒(GPU)
- 模型集成可进一步提高准确率0.2-0.5个百分点

## 致谢
- [MNIST数据集](http://yann.lecun.com/exdb/mnist/)
- [PyTorch框架](https://pytorch.org/)
- [计算机视觉课程]