import torch
import torch.nn as nn
import numpy as np
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
import seaborn as sns
import cv2
from torch.nn import functional as F

'''
浅色区域表示边缘
'''
class FeatureVisualization:
    def __init__(self, model, device):
        self.model = model
        self.device = device
        self.activation = {}
        
    def get_activation(self, name):
        def hook(model, input, output):
            self.activation[name] = output.detach()
        return hook
    
    def register_hooks(self):
        """为CNN模型的各层注册钩子"""
        if isinstance(self.model, nn.Module):
            # 注册卷积层
            if hasattr(self.model, 'conv1'):
                self.model.conv1.register_forward_hook(self.get_activation('conv1'))
            if hasattr(self.model, 'conv2'):
                self.model.conv2.register_forward_hook(self.get_activation('conv2'))
            if hasattr(self.model, 'conv3'):
                self.model.conv3.register_forward_hook(self.get_activation('conv3'))
                
            # 注册全连接层
            if hasattr(self.model, 'fc1'):
                self.model.fc1.register_forward_hook(self.get_activation('fc1'))
        else:
            print("模型类型不支持")
    
    def visualize_filters(self, layer_name='conv1', num_filters=16):
        """可视化卷积滤波器"""
        try:
            # 获取卷积层的权重
            if layer_name == 'conv1' and hasattr(self.model, 'conv1'):
                filters = self.model.conv1.weight.data.cpu().numpy()
            elif layer_name == 'conv2' and hasattr(self.model, 'conv2'):
                filters = self.model.conv2.weight.data.cpu().numpy()
            elif layer_name == 'conv3' and hasattr(self.model, 'conv3'):
                filters = self.model.conv3.weight.data.cpu().numpy()
            else:
                print(f"找不到层: {layer_name}")
                return
                
            # 计算大小并创建图表
            n_filters = min(num_filters, filters.shape[0])
            n_cols = 4
            n_rows = n_filters // n_cols + (1 if n_filters % n_cols != 0 else 0)
            
            fig, axes = plt.subplots(n_rows, n_cols, figsize=(12, 2*n_rows))
            axes = axes.flatten()
            
            for i in range(n_filters):
                # 对多通道卷积核，取第一个通道显示
                img = filters[i][0]
                img = (img - img.min()) / (img.max() - img.min() + 1e-8)  # 归一化
                axes[i].imshow(img, cmap='viridis')
                axes[i].axis('off')
                axes[i].set_title(f'Filter {i+1}')
                
            # 隐藏多余的子图
            for i in range(n_filters, len(axes)):
                axes[i].axis('off')
                
            plt.tight_layout()
            plt.savefig(f'results/{layer_name}_filters.svg')
            plt.show()
            
        except Exception as e:
            print(f"可视化滤波器时出错: {e}")
    
    def visualize_feature_maps(self, image, layer_name='conv1', num_maps=16):
        """可视化特征图"""
        self.register_hooks()
        
        # 确保图像是4D张量 [batch_size, channels, height, width]
        if len(image.shape) == 3:
            image = image.unsqueeze(0)
            
        image = image.to(self.device)
        
        # 前向传播
        self.model.eval()
        with torch.no_grad():
            _ = self.model(image)
        
        # 获取特定层的激活
        if layer_name in self.activation:
            feature_maps = self.activation[layer_name].cpu().numpy()
            
            # 选取第一个样本
            feature_maps = feature_maps[0]
            
            # 计算子图数量和大小
            n_features = min(num_maps, feature_maps.shape[0])
            n_cols = 4
            n_rows = n_features // n_cols + (1 if n_features % n_cols != 0 else 0)
            
            fig, axes = plt.subplots(n_rows, n_cols, figsize=(12, 2*n_rows))
            axes = axes.flatten()
            
            for i in range(n_features):
                feature_map = feature_maps[i]
                # 归一化
                feature_map = (feature_map - feature_map.min()) / (feature_map.max() - feature_map.min() + 1e-8)
                axes[i].imshow(feature_map, cmap='viridis')
                axes[i].axis('off')
                axes[i].set_title(f'Map {i+1}')
            
            # 隐藏多余的子图
            for i in range(n_features, len(axes)):
                axes[i].axis('off')
                
            plt.tight_layout()
            plt.savefig(f'results/{layer_name}_feature_maps.svg')
            plt.show()
        else:
            print(f"找不到层激活: {layer_name}")
    
    def visualize_embeddings(self, data_loader, n_samples=1000, method='tsne'):
        """可视化高维嵌入"""
        self.model.eval()
        features = []
        labels = []
        
        with torch.no_grad():
            for data, target in data_loader:
                if len(features) >= n_samples:
                    break
                    
                data = data.to(self.device)
                # 获取倒数第二层输出作为特征
                if hasattr(self.model, 'fc1'):
                    # 先获取所有中间输出
                    self.register_hooks()
                    output = self.model(data)
                    
                    # 使用fc1层的输出
                    if 'fc1' in self.activation:
                        batch_features = self.activation['fc1'].cpu().numpy()
                        features.extend(batch_features)
                        labels.extend(target.numpy())
        
        # 裁剪到所需样本数量
        features = features[:n_samples]
        labels = labels[:n_samples]
        
        # 转为numpy数组
        features = np.array(features)
        labels = np.array(labels)
        # 降维可视化
        if method == 'tsne':
            embedded = TSNE(n_components=2, random_state=42).fit_transform(features)
        elif method == 'pca':
            embedded = PCA(n_components=2).fit_transform(features)
        else:
            print(f"未知的嵌入方法: {method}")
            return
            
        # 可视化
        plt.figure(figsize=(10, 8))
        scatter = plt.scatter(embedded[:, 0], embedded[:, 1], c=labels, cmap='tab10', alpha=0.6)
        plt.colorbar(scatter, ticks=range(10))
        plt.title(f'特征嵌入可视化 ({method.upper()})', fontsize=14)
        plt.xlabel('维度 1')
        plt.ylabel('维度 2')
        plt.grid(alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(f'results/embeddings_{method}.svg')
        plt.show()
    
    def grad_cam(self, image, target_class=None):
        """GradCAM可解释性分析"""
        self.model.eval()

        # 确保图像是4D张量 [batch_size, channels, height, width]
        if len(image.shape) == 3:
            image = image.unsqueeze(0)

        image = image.to(self.device)
        image.requires_grad_()

        # 选择最后一个卷积层
        if hasattr(self.model, 'conv3'):
            target_layer = self.model.conv3
        elif hasattr(self.model, 'conv2'):
            target_layer = self.model.conv2
        else:
            print("模型结构不支持GradCAM")
            return

        activations = []
        gradients = []

        def forward_hook(module, input, output):
            if isinstance(output, tuple):
                activations.append(output[0])
                if output[0].requires_grad:
                    output[0].retain_grad()
            else:
                activations.append(output)
                if output.requires_grad:
                    output.retain_grad()

        def backward_hook(module, grad_input, grad_output):
            if isinstance(grad_output, tuple):
                gradients.append(grad_output[0])
            else:
                gradients.append(grad_output)

        handle_f = target_layer.register_full_backward_hook(forward_hook)
        handle_b = target_layer.register_full_backward_hook(backward_hook)

        # 前向传播
        output = self.model(image)
        if target_class is None:
            target_class = torch.argmax(output, dim=1).item()

        # 反向传播
        self.model.zero_grad()
        one_hot = torch.zeros_like(output)
        one_hot[0, target_class] = 1
        output.backward(gradient=one_hot)

        # 获取激活和梯度
        act = activations[0].detach().cpu()
        grad = gradients[0].detach().cpu()

        # 计算权重
        print('grad shape:', grad.shape)
        weights = grad.mean(dim=(2, 3), keepdim=True)  # [batch, C, 1, 1]
        cam = (weights * act).sum(dim=1).squeeze()     # [H, W]

        # 释放钩子
        handle_f.remove()
        handle_b.remove()

        # 可视化热力图
        cam = np.maximum(cam, 0)
        cam = cv2.resize(cam.numpy(), (28, 28))
        cam = cam / (cam.max() + 1e-8)

        img = image.squeeze().cpu().detach().numpy()

        plt.figure(figsize=(12, 4))
        plt.subplot(1, 3, 1)
        plt.imshow(img, cmap='gray')
        plt.title('原始图像')
        plt.axis('off')

        plt.subplot(1, 3, 2)
        plt.imshow(cam, cmap='jet')
        plt.title('GradCAM热力图')
        plt.axis('off')

        plt.subplot(1, 3, 3)
        plt.imshow(img, cmap='gray')
        plt.imshow(cam, cmap='jet', alpha=0.5)
        plt.title('叠加结果')
        plt.axis('off')

        plt.tight_layout()
        plt.savefig(f'results/gradcam_class_{target_class}.svg')
        plt.show()

        return target_class, cam