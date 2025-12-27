import torch
import torchvision.transforms as transforms
from torchvision.transforms import functional as TF
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

class DataAugmentation:
    def __init__(self):
        self.basic_transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize((0.1307,), (0.3081,))
        ])
        
        self.augmentation_transform = transforms.Compose([
            transforms.RandomRotation(10),
            transforms.RandomAffine(degrees=0, translate=(0.1, 0.1)),
            transforms.ToTensor(),
            transforms.Normalize((0.1307,), (0.3081,))
        ])
    
    def apply_augmentation(self, image, transform_type='basic'):
        """应用数据增强"""
        if transform_type == 'basic':
            return self.basic_transform(image)
        elif transform_type == 'augmented':
            return self.augmentation_transform(image)
        else:
            raise ValueError("未知的转换类型")
    
    def visualize_augmentations(self, image):
        """可视化不同的数据增强效果"""
        if isinstance(image, torch.Tensor):
            img = image.numpy()
            if img.shape[0] == 1:
                img = img.squeeze(0)
            img = (img * 255).astype(np.uint8)
            image = Image.fromarray(img)
        elif isinstance(image, np.ndarray):
            image = Image.fromarray(image)
        fig, axes = plt.subplots(3, 3, figsize=(10, 10))
        axes = axes.flatten()
        # 原始图像
        axes[0].imshow(image, cmap='gray')
        axes[0].set_title('原始图像')
        
        # 基本转换
        basic_img = self.basic_transform(image)
        axes[1].imshow(basic_img.squeeze(), cmap='gray')
        axes[1].set_title('基本归一化')
        
        # 旋转
        rotated = transforms.Compose([
            transforms.RandomRotation(15),
            transforms.ToTensor()
        ])(image)
        axes[2].imshow(rotated.squeeze(), cmap='gray')
        axes[2].set_title('随机旋转')
        
        # 平移
        shifted = transforms.Compose([
            transforms.RandomAffine(degrees=0, translate=(0.1, 0.1)),
            transforms.ToTensor()
        ])(image)
        axes[3].imshow(shifted.squeeze(), cmap='gray')
        axes[3].set_title('随机平移')
        
        # 缩放
        scaled = transforms.Compose([
            transforms.RandomAffine(degrees=0, scale=(0.9, 1.1)),
            transforms.ToTensor()
        ])(image)
        axes[4].imshow(scaled.squeeze(), cmap='gray')
        axes[4].set_title('随机缩放')
        
        # 剪切
        sheared = transforms.Compose([
            transforms.RandomAffine(degrees=0, shear=10),
            transforms.ToTensor()
        ])(image)
        axes[5].imshow(sheared.squeeze(), cmap='gray')
        axes[5].set_title('随机剪切')
        
        # 高斯噪声
        noise_img = self.basic_transform(image).numpy()
        noise = np.random.normal(0, 0.1, noise_img.shape)
        noisy = np.clip(noise_img + noise, 0, 1)
        axes[6].imshow(noisy.squeeze(), cmap='gray')
        axes[6].set_title('高斯噪声')
        
        # 随机擦除
        erased = transforms.Compose([
            transforms.ToTensor(),
            transforms.RandomErasing(p=0.5, scale=(0.02, 0.1))
        ])(image)
        axes[7].imshow(erased.squeeze(), cmap='gray')
        axes[7].set_title('随机擦除')
        
        # 所有增强组合
        augmented = self.augmentation_transform(image)
        axes[8].imshow(augmented.squeeze(), cmap='gray')
        axes[8].set_title('组合增强')
        
        for ax in axes:
            ax.axis('off')
            
        plt.tight_layout()
        plt.savefig('results/data_augmentation.svg')
        plt.show()
        
    def compare_original_vs_augmented(self, dataset, num_samples=5):
        """比较原始图像和增强后的图像"""
        fig, axes = plt.subplots(num_samples, 2, figsize=(8, 2*num_samples))
        
        for i in range(num_samples):
            image, label = dataset[i]
            
            # 原始图像
            axes[i, 0].imshow(image.squeeze(), cmap='gray')
            axes[i, 0].set_title(f'原始图像 - 标签:{label}')
            axes[i, 0].axis('off')
            
            # 增强图像
            augmented_image = self.apply_augmentation(Image.fromarray(np.array(image.squeeze()*255).astype(np.uint8)), 
                                                     'augmented')
            axes[i, 1].imshow(augmented_image.squeeze(), cmap='gray')
            axes[i, 1].set_title(f'增强图像 - 标签:{label}')
            axes[i, 1].axis('off')
        
        plt.tight_layout()
        plt.savefig('results/original_vs_augmented.svg')
        plt.show()