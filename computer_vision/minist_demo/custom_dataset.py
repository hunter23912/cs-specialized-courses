import torch
from torch.utils.data import Dataset, DataLoader
import matplotlib.pyplot as plt
import numpy as np
import cv2
import os
import random
from PIL import Image, ImageDraw
import tkinter as tk
from tkinter import messagebox
from torchvision import transforms
from pathlib import Path

class DrawingApp:
    def __init__(self, root, save_path='custom_data'):
        self.root = root
        self.root.title("手写数字绘制工具")
        
        self.save_path = Path(save_path)
        self.save_path.mkdir(exist_ok=True, parents=True)
        
        self.canvas_width = 280
        self.canvas_height = 280
        
        self.setup_ui()
        self.setup_canvas()
        
        self.current_digit = 0
        self.sample_count = 0
        self.update_info_label()
        
    def setup_ui(self):
        # 创建框架
        self.left_frame = tk.Frame(self.root)
        self.left_frame.pack(side=tk.LEFT, padx=10, pady=10)
        
        self.right_frame = tk.Frame(self.root)
        self.right_frame.pack(side=tk.RIGHT, padx=10, pady=10)
        
        # 标签显示当前数字
        self.info_label = tk.Label(self.right_frame, text="", font=("Arial", 12))
        self.info_label.pack(pady=10)
        
        # 按钮
        self.clear_btn = tk.Button(self.right_frame, text="清除", command=self.clear_canvas)
        self.clear_btn.pack(fill=tk.X, pady=5)
        
        self.save_btn = tk.Button(self.right_frame, text="保存当前数字", command=self.save_digit)
        self.save_btn.pack(fill=tk.X, pady=5)
        
        self.next_btn = tk.Button(self.right_frame, text="下一个数字", command=self.next_digit)
        self.next_btn.pack(fill=tk.X, pady=5)
        
        # 数字选择按钮
        digit_frame = tk.Frame(self.right_frame)
        digit_frame.pack(pady=10)
        
        for i in range(10):
            btn = tk.Button(digit_frame, text=str(i), width=3, 
                            command=lambda d=i: self.select_digit(d))
            btn.pack(side=tk.LEFT, padx=2)
    
    def setup_canvas(self):
        self.canvas = tk.Canvas(self.left_frame, width=self.canvas_width, height=self.canvas_height,
                               bg='black')
        self.canvas.pack()
        
        self.canvas.bind("<B1-Motion>", self.paint)
        self.canvas.bind("<ButtonRelease-1>", lambda e: None)
        
        self.old_x = None
        self.old_y = None
    
    def paint(self, event):
        x, y = event.x, event.y
        r = 10  # 笔刷半径
        
        if self.old_x and self.old_y:
            self.canvas.create_line(self.old_x, self.old_y, x, y, 
                                   width=r*2, fill='white', capstyle=tk.ROUND, smooth=tk.TRUE)
        
        self.canvas.create_oval(x-r, y-r, x+r, y+r, fill='white', outline='white')
        
        self.old_x = x
        self.old_y = y
    
    def clear_canvas(self):
        self.canvas.delete("all")
        self.old_x = None
        self.old_y = None
    
    def select_digit(self, digit):
        self.current_digit = digit
        self.clear_canvas()
        self.update_info_label()
    
    def next_digit(self):
        self.current_digit = (self.current_digit + 1) % 10
        self.clear_canvas()
        self.update_info_label()
    
    def update_info_label(self):
        self.info_label.config(text=f"当前绘制数字: {self.current_digit}\n已保存样本数: {self.sample_count}")
    
    def save_digit(self):
        # 获取画布上的图像
        self.root.update()
        x = self.canvas.winfo_rootx() + self.canvas.winfo_x()
        y = self.canvas.winfo_rooty() + self.canvas.winfo_y()
        x1 = x + self.canvas_width
        y1 = y + self.canvas_height
        
        # 截取画布区域
        img = ImageGrab.grab().crop((x, y, x1, y1))
        
        # 调整大小到28x28，转换为灰度图
        img = img.resize((28, 28)).convert('L')
        
        # 保存图像
        digit_dir = self.save_path / str(self.current_digit)
        digit_dir.mkdir(exist_ok=True)
        
        filename = digit_dir / f"{self.current_digit}_{self.sample_count}.png"
        img.save(filename)
        
        self.sample_count += 1
        self.update_info_label()
        messagebox.showinfo("保存成功", f"数字 {self.current_digit} 已保存!")
        self.clear_canvas()

class CustomDigitDataset(Dataset):
    def __init__(self, data_dir='custom_data', transform=None):
        self.data_dir = Path(data_dir)
        self.transform = transform or transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize((0.1307,), (0.3081,))
        ])
        
        self.samples = []
        for digit in range(10):
            digit_dir = self.data_dir / str(digit)
            if not digit_dir.exists():
                continue
                
            for img_path in digit_dir.glob('*.png'):
                self.samples.append((str(img_path), digit))
        
        print(f"加载了 {len(self.samples)} 个自定义样本")
    
    def __len__(self):
        return len(self.samples)
    
    def __getitem__(self, idx):
        img_path, label = self.samples[idx]
        img = Image.open(img_path).convert('L')
        
        if self.transform:
            img = self.transform(img)
            
        return img, label
    
    def visualize_samples(self, num_samples=10):
        indices = random.sample(range(len(self.samples)), min(num_samples, len(self.samples)))
        
        fig, axes = plt.subplots(1, len(indices), figsize=(2*len(indices), 3))
        if len(indices) == 1:
            axes = [axes]
            
        for i, idx in enumerate(indices):
            img_path, label = self.samples[idx]
            img = Image.open(img_path)
            axes[i].imshow(img, cmap='gray')
            axes[i].set_title(f"标签: {label}")
            axes[i].axis('off')
            
        plt.tight_layout()
        plt.savefig('results/custom_samples.svg')
        plt.show()
        
    def test_model_on_custom(self, model, device):
        """测试模型在自定义数据上的表现"""
        dataloader = DataLoader(self, batch_size=32, shuffle=False)
        
        model.eval()
        correct = 0
        total = 0
        predictions = []
        ground_truths = []
        images = []
        
        with torch.no_grad():
            for data, target in dataloader:
                data, target = data.to(device), target.to(device)
                output = model(data)
                _, predicted = torch.max(output.data, 1)
                
                total += target.size(0)
                correct += (predicted == target).sum().item()
                
                # 收集结果用于可视化
                predictions.extend(predicted.cpu().numpy())
                ground_truths.extend(target.cpu().numpy())
                images.extend(data.cpu().numpy())
        
        accuracy = 100 * correct / total
        print(f"自定义数据集准确率: {accuracy:.2f}%")
        
        # 可视化一些预测结果
        indices = random.sample(range(len(predictions)), min(10, len(predictions)))
        
        fig, axes = plt.subplots(1, len(indices), figsize=(2*len(indices), 3))
        if len(indices) == 1:
            axes = [axes]
            
        for i, idx in enumerate(indices):
            img = images[idx].squeeze()
            pred = predictions[idx]
            true = ground_truths[idx]
            
            axes[i].imshow(img, cmap='gray')
            color = 'green' if pred == true else 'red'
            axes[i].set_title(f"预测: {pred}\n实际: {true}", color=color)
            axes[i].axis('off')
            
        plt.tight_layout()
        plt.savefig('results/custom_predictions.svg')
        plt.show()
        
        return accuracy

# 使用PIL的ImageGrab模块用于截图
try:
    from PIL import ImageGrab
except ImportError:
    print("无法导入ImageGrab，在Linux系统上可能需要额外设置")
    
def launch_drawing_app():
    """启动绘图应用程序"""
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()
    
if __name__ == "__main__":
    launch_drawing_app()