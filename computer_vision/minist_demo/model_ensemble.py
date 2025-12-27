import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from models import CNNModel, SimpleMLP
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, classification_report
import seaborn as sns
from experiment import Experiment

class AdvancedCNN(nn.Module):
    def __init__(self):
        super(AdvancedCNN, self).__init__()
        self.conv1 = nn.Conv2d(1, 32, kernel_size=5, padding=2)
        self.bn1 = nn.BatchNorm2d(32)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.bn2 = nn.BatchNorm2d(64)
        self.conv3 = nn.Conv2d(64, 128, kernel_size=3, padding=1)
        self.bn3 = nn.BatchNorm2d(128)
        self.fc1 = nn.Linear(128 * 7 * 7, 256)
        self.bn4 = nn.BatchNorm1d(256)
        self.fc2 = nn.Linear(256, 10)
        self.dropout = nn.Dropout(0.3)
        
    def forward(self, x):
        x = F.relu(self.bn1(self.conv1(x)))
        x = F.max_pool2d(x, 2)
        x = F.relu(self.bn2(self.conv2(x)))
        x = F.max_pool2d(x, 2)
        x = F.relu(self.bn3(self.conv3(x)))
        x = x.view(-1, 128 * 7 * 7)
        x = F.relu(self.bn4(self.fc1(x)))
        x = self.dropout(x)
        x = self.fc2(x)
        return x

class ResidualBlock(nn.Module):
    def __init__(self, in_channels, out_channels):
        super(ResidualBlock, self).__init__()
        self.conv1 = nn.Conv2d(in_channels, out_channels, kernel_size=3, padding=1)
        self.bn1 = nn.BatchNorm2d(out_channels)
        self.conv2 = nn.Conv2d(out_channels, out_channels, kernel_size=3, padding=1)
        self.bn2 = nn.BatchNorm2d(out_channels)
        
        self.shortcut = nn.Sequential()
        if in_channels != out_channels:
            self.shortcut = nn.Sequential(
                nn.Conv2d(in_channels, out_channels, kernel_size=1),
                nn.BatchNorm2d(out_channels)
            )
            
    def forward(self, x):
        residual = x
        x = F.relu(self.bn1(self.conv1(x)))
        x = self.bn2(self.conv2(x))
        x += self.shortcut(residual)
        x = F.relu(x)
        return x

class ResNetMNIST(nn.Module):
    def __init__(self):
        super(ResNetMNIST, self).__init__()
        self.conv1 = nn.Conv2d(1, 16, kernel_size=3, padding=1)
        self.bn1 = nn.BatchNorm2d(16)
        self.layer1 = ResidualBlock(16, 32)
        self.layer2 = ResidualBlock(32, 64)
        self.layer3 = ResidualBlock(64, 128)
        self.avgpool = nn.AdaptiveAvgPool2d((7, 7))
        self.fc = nn.Linear(128 * 7 * 7, 10)
        
    def forward(self, x):
        x = F.relu(self.bn1(self.conv1(x)))
        x = self.layer1(x)
        x = F.max_pool2d(x, 2)
        x = self.layer2(x)
        x = F.max_pool2d(x, 2)
        x = self.layer3(x)
        x = self.avgpool(x)
        x = x.view(-1, 128 * 7 * 7)
        x = self.fc(x)
        return x

class ModelEnsemble:
    def __init__(self, experiment):
        self.experiment = experiment
        self.models = {}
        self.device = experiment.device
        
    def add_model(self, model_name, model):
        """添加模型到集成"""
        self.models[model_name] = model.to(self.device)
        
    def train_all_models(self, train_loader, data_size):
        """训练所有模型"""
        results = {}
        for name, model in self.models.items():
            print(f"训练模型: {name}")
            trained_model, training_time = self.experiment.train_model(model, train_loader, data_size)
            self.models[name] = trained_model
            accuracy = self.experiment.test_model(trained_model)
            results[name] = {
                "training_time": training_time,
                "accuracy": accuracy
            }
        return results
    
    def ensemble_predict(self, data_loader, method='voting'):
        """集成预测"""
        all_predictions = {}
        all_targets = []
        
        # 获取每个模型的预测
        with torch.no_grad():
            for name, model in self.models.items():
                model.eval()
                predictions = []
                
                for data, target in data_loader:
                    if len(all_targets) < len(data_loader.dataset):
                        all_targets.extend(target.numpy())
                        
                    data = data.to(self.device)
                    output = model(data)
                    _, preds = torch.max(output, 1)
                    predictions.extend(preds.cpu().numpy())
                    
                all_predictions[name] = np.array(predictions)
        
        # 集成方法
        if method == 'voting':
            # 多数投票
            final_predictions = []
            for i in range(len(all_predictions[list(all_predictions.keys())[0]])):
                votes = [all_predictions[name][i] for name in all_predictions]
                final_predictions.append(np.argmax(np.bincount(votes)))
                
            return np.array(final_predictions), np.array(all_targets)
        
        else:
            raise ValueError(f"未知的集成方法: {method}")
    
    def compare_models(self):
        """比较不同模型的性能"""
        accuracies = {}
        for name, model in self.models.items():
            accuracy = self.experiment.test_model(model)
            accuracies[name] = accuracy
            
        # 计算集成模型准确率
        ensemble_preds, targets = self.ensemble_predict(self.experiment.test_loader)
        ensemble_accuracy = 100 * np.sum(ensemble_preds == targets) / len(targets)
        accuracies["Ensemble"] = ensemble_accuracy
        
        # 绘制比较图
        plt.figure(figsize=(10, 6))
        models = list(accuracies.keys())
        accs = [accuracies[model] for model in models]
        
        bars = plt.bar(models, accs, color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728'])
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                    f'{height:.2f}%', ha='center', va='bottom')
            
        plt.ylabel('准确率 (%)', fontsize=12)
        plt.title('各模型准确率比较', fontsize=14, fontweight='bold')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.ylim(min(accs) - 3, max(accs) + 3)
        
        plt.tight_layout()
        plt.savefig('results/model_comparison.svg')
        plt.show()
        
        # 返回结果
        return accuracies
    
    def visualize_confusion_matrix(self):
        """可视化混淆矩阵"""
        ensemble_preds, targets = self.ensemble_predict(self.experiment.test_loader)
        
        plt.figure(figsize=(10, 8))
        cm = confusion_matrix(targets, ensemble_preds)
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
        plt.xlabel('预测标签')
        plt.ylabel('真实标签')
        plt.title('集成模型混淆矩阵', fontsize=14)
        
        plt.tight_layout()
        plt.savefig('results/confusion_matrix.svg')
        plt.show()
        
        # 打印分类报告
        report = classification_report(targets, ensemble_preds, digits=3)
        print("集成模型分类报告:")
        print(report)