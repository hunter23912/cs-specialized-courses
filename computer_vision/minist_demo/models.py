import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
from torch.utils.data import DataLoader, Subset
import matplotlib.pyplot as plt
from tqdm import tqdm
import time
import numpy as np

'''
算法类型：基于卷积神经网络(CNN)和多层感知机(MLP)的深度学习分类算法
模型结构：
    1. CNN模型：三层卷积层+池化层+全连接层，包含约22万参数
    2. MLP模型：三层全连接神经网络，输入层784节点，隐藏层128和64节点，输出层10节点
优化方法：随机梯度下降(SGD)
损失函数：交叉熵损失函数(CrossEntropyLoss)
数据集：MNIST手写数字识别数据集(60,000训练样本，10,000测试样本)
实验目的：验证不同数据规模对模型训练时间和准确率的影响，展示GPU计算加速效果
'''

# 定义简单的全连接神经网络
class SimpleMLP(nn.Module): # 继承自nn.Module类，用于定义一个简单的多层感知器MLP
    def __init__(self):
        super(SimpleMLP, self).__init__()
        self.fc1 = nn.Linear(28 * 28, 128) # 将输入的28*28的图像展平为一维向量，并映射到128个神经元
        self.fc2 = nn.Linear(128, 64) # 将128个神经元映射到64个神经元
        self.fc3 = nn.Linear(64, 10) # 将64个神经元映射到10个神经元，对应10个类别的概率分布

    # 定义前向传播过程，
    def forward(self, x):
        x = x.view(-1, 28 * 28) # 输入展平成二维张量，-1表示自动计算batch_size
        x = torch.relu(self.fc1(x)) # 激活函数对前两层进行非线性变换
        x = torch.relu(self.fc2(x))
        x = self.fc3(x) # 第三层通常交给损失函数处理
        return x

# 定义卷积神经网络模型
class CNNModel(nn.Module):
    def __init__(self):
        super(CNNModel, self).__init__()
        # 第一个卷积层，32个3x3卷积核
        self.conv1 = nn.Conv2d(1, 32, kernel_size=3, padding=1)
        # 第二个卷积层，64个3x3卷积核
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        # 第三个卷积层，128个3x3卷积核
        self.conv3 = nn.Conv2d(64, 128, kernel_size=3, padding=1)
        # 全连接层
        self.fc1 = nn.Linear(128 * 7 * 7, 512)
        self.fc2 = nn.Linear(512, 10)
        # 池化层
        self.pool = nn.MaxPool2d(2)
        self.dropout = nn.Dropout(0.25)
    
    def forward(self, x):
        x = torch.relu(self.conv1(x))
        x = self.pool(x)
        x = torch.relu(self.conv2(x))
        x = self.pool(x)
        x = torch.relu(self.conv3(x))
        x = x.view(-1, 128 * 7 * 7)
        x = torch.relu(self.fc1(x))
        x = self.dropout(x)
        x = self.fc2(x)
        return x

# 装饰器函数，用于计算函数执行时间
def timer(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        cost = end_time - start_time
        print(f"Function '{func.__name__}' took {cost:.4f} seconds")
        wrapper.execution_time = cost
        return result
    wrapper.execution_time = 0.0 # 初始化执行时间属性
    return wrapper