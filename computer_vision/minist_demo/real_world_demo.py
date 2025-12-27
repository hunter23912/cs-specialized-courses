import cv2
import numpy as np
import torch
import matplotlib.pyplot as plt
from PIL import Image
from torchvision import transforms
import tkinter as tk
from tkinter import filedialog, Button, Label
from PIL import ImageTk, Image as PILImage
import os
from models import CNNModel

class RealWorldDemo:
    def __init__(self, model_path='model_dict/mnist_model.pth'):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        
        # 加载模型
        self.model = CNNModel()
        self.model.load_state_dict(torch.load(model_path))
        self.model.to(self.device)
        self.model.eval()
        
        self.transform = transforms.Compose([
            transforms.Resize((28, 28)),
            transforms.ToTensor(),
            transforms.Normalize((0.1307,), (0.3081,))
        ])
        
    def preprocess_image(self, image_path):
        """预处理图像，将自然图像处理成适合模型的格式"""
        # 读取图像
        if isinstance(image_path, str):
            img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        else:
            # 假设图像已经是numpy数组
            img = image_path
            if len(img.shape) > 2:
                img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # 阈值处理，转为二值图像
        _, thresh = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY_INV)
        
        # 查找轮廓
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # 如果没有找到轮廓，返回原图
        if not contours:
            return Image.fromarray(thresh)
            
        # 找到最大的轮廓，假设它是数字
        c = max(contours, key=cv2.contourArea)
        
        # 获取边界框
        x, y, w, h = cv2.boundingRect(c)
        
        # 添加边距
        padding = 5
        x = max(0, x - padding)
        y = max(0, y - padding)
        w = min(img.shape[1] - x, w + 2 * padding)
        h = min(img.shape[0] - y, h + 2 * padding)
        
        # 裁剪图像
        digit = thresh[y:y+h, x:x+w]
        
        # 调整大小到正方形
        size = max(w, h)
        square_img = np.zeros((size, size), dtype=np.uint8)
        x_offset = (size - w) // 2
        y_offset = (size - h) // 2
        square_img[y_offset:y_offset+h, x_offset:x_offset+w] = digit
        
        return Image.fromarray(square_img)
    
    def predict_digit(self, image):
        """对预处理后的图像进行预测"""
        # 转换图像
        img_tensor = self.transform(image).unsqueeze(0).to(self.device)
        
        # 预测
        with torch.no_grad():
            output = self.model(img_tensor)
            _, predicted = torch.max(output, 1)
            probabilities = torch.nn.functional.softmax(output, dim=1)[0]
            
        return predicted.item(), probabilities.cpu().numpy()
    
    def process_and_predict(self, image_path):
        """处理图像并预测"""
        preprocessed = self.preprocess_image(image_path)
        prediction, probabilities = self.predict_digit(preprocessed)
        return preprocessed, prediction, probabilities
    
    def visualize_prediction(self, image_path):
        """可视化预测结果"""
        orig_image = cv2.imread(image_path)
        orig_image = cv2.cvtColor(orig_image, cv2.COLOR_BGR2RGB)
        
        preprocessed, prediction, probabilities = self.process_and_predict(image_path)
        
        plt.figure(figsize=(12, 4))
        
        plt.subplot(1, 3, 1)
        plt.imshow(orig_image)
        plt.title("原始图像")
        plt.axis('off')
        
        plt.subplot(1, 3, 2)
        plt.imshow(preprocessed, cmap='gray')
        plt.title("预处理图像")
        plt.axis('off')
        
        plt.subplot(1, 3, 3)
        bars = plt.bar(range(10), probabilities)
        plt.xticks(range(10))
        plt.title(f"预测结果: {prediction}")
        plt.ylabel("概率")
        plt.xlabel("数字")
        
        # 高亮预测的数字
        bars[prediction].set_color('red')
        
        plt.tight_layout()
        plt.savefig('results/prediction_visualization.svg')
        plt.show()
        
        return prediction
    
    def predict_from_webcam(self):
        """从摄像头获取图像并预测"""
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("无法打开摄像头")
            return
            
        print("按下 's' 键截取图像并预测，按下 'q' 键退出")
        
        while True:
            ret, frame = cap.read()
            if not ret:
                print("无法获取图像")
                break
                
            # 显示摄像头图像
            cv2.imshow("摄像头", frame)
            
            # 等待按键
            key = cv2.waitKey(1)
            if key == ord('q'):
                break
            elif key == ord('s'):
                # 将图像转换为灰度图并预测
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                preprocessed, prediction, probabilities = self.process_and_predict(gray)
                
                # 显示结果
                print(f"预测结果: {prediction}")
                
                # 显示预处理后的图像
                cv2.imshow("预处理图像", np.array(preprocessed))
                
                # 显示概率条形图
                plt.figure()
                bars = plt.bar(range(10), probabilities)
                plt.xticks(range(10))
                plt.title(f"预测结果: {prediction}")
                bars[prediction].set_color('red')
                plt.show(block=False)
        
        cap.release()
        cv2.destroyAllWindows()
    
    def create_gui(self):
        """创建图形用户界面"""
        root = tk.Tk()
        root.title("手写数字识别")
        root.geometry("600x500")
        
        # 创建标签和按钮
        title_label = Label(root, text="手写数字识别演示", font=("Arial", 16))
        title_label.pack(pady=10)
        
        # 按钮框架
        button_frame = tk.Frame(root)
        button_frame.pack(pady=10)
        
        # 选择图像按钮
        select_button = Button(button_frame, text="选择图像", command=lambda: self.select_image(image_label, result_label))
        select_button.pack(side=tk.LEFT, padx=5)
        
        # 摄像头识别按钮
        webcam_button = Button(button_frame, text="摄像头识别", command=self.predict_from_webcam)
        webcam_button.pack(side=tk.LEFT, padx=5)
        
        # 图像显示标签
        image_label = Label(root)
        image_label.pack(pady=10)
        
        # 结果显示标签
        result_label = Label(root, text="", font=("Arial", 14))
        result_label.pack(pady=10)
        
        root.mainloop()
    
    def select_image(self, image_label, result_label):
        """选择图像并显示预测结果"""
        file_path = filedialog.askopenfilename(
            title="选择图像",
            filetypes=[("图像文件", "*.jpg *.jpeg *.png")]
        )
        
        if not file_path:
            return
            
        try:
            # 处理图像并预测
            preprocessed, prediction, probabilities = self.process_and_predict(file_path)
            
            # 显示原始图像
            orig_image = PILImage.open(file_path)
            orig_image = orig_image.resize((200, 200))
            photo = ImageTk.PhotoImage(orig_image)
            image_label.config(image=photo)
            image_label.image = photo
            
            # 显示预测结果
            result_label.config(text=f"预测结果: {prediction}")
            
            # 将结果保存为文件
            save_path = 'results'
            os.makedirs(save_path, exist_ok=True)
            
            plt.figure(figsize=(8, 4))
            plt.subplot(1, 2, 1)
            plt.imshow(preprocessed, cmap='gray')
            plt.title("预处理图像")
            plt.axis('off')
            
            plt.subplot(1, 2, 2)
            bars = plt.bar(range(10), probabilities)
            plt.xticks(range(10))
            plt.title(f"预测结果: {prediction}")
            bars[prediction].set_color('red')
            
            plt.tight_layout()
            plt.savefig(os.path.join(save_path, 'latest_prediction.svg'))
            plt.close()
            
        except Exception as e:
            result_label.config(text=f"错误: {str(e)}")
            print(f"图像处理错误: {e}")

if __name__ == "__main__":
    demo = RealWorldDemo()
    demo.create_gui()