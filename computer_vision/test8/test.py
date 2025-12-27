# ukbench
import os
import cv2
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt
from tqdm import tqdm
import pickle

plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文
plt.rcParams['axes.unicode_minus'] = False  # 显示负号

'''
Bag of Visual Words (BoVW) 模型
该模型使用SIFT特征和K-means聚类来创建视觉词汇
然后为每张图像创建一个直方图表示
该模型可以用于图像检索任务
'''
class BagOfVisualWords:
    def __init__(self, vocab_size=1000):
        self.vocab_size = vocab_size
        self.kmeans = None
        self.features_dict = {}
        self.histograms = {}
        self.image_paths = []
        self.hog_features = {}
    
    def extract_sift_features(self, image_path):
        """从图像中提取SIFT特征"""
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            return np.array([])
        
        # 调整图像大小，保持特征一致性
        img = cv2.resize(img, (0,0), fx=0.8, fy=0.8)
        # 使用CLAHE进行对比度增强，改善特征提取
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        img = clahe.apply(img)
        # 初始化SIFT检测器
        sift = cv2.SIFT_create(nfeatures=500)
        # 检测关键点和计算描述符
        keypoints, descriptors = sift.detectAndCompute(img, None)
        if descriptors is None:
            return np.array([])
        return descriptors
    
    def extract_hog_features(self, image_path):
        """从图像中提取HOG特征"""
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            return np.array([])
        # 调整图像大小，保持特征一致性
        img = cv2.resize(img, (128, 128))
        
        # 计算HOG特征
        hog = cv2.HOGDescriptor()
        descriptors = hog.compute(img)
        
        return descriptors.flatten()
    
    def build_vocabulary(self, dataset_path):
        """构建视觉词典"""
        all_features = []
        
        # 获取所有图像路径
        for root, _, files in os.walk(dataset_path):
            for file in files:
                if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                    image_path = os.path.join(root, file)
                    self.image_paths.append(image_path)
        
        # 从每个图像中提取特征
        print('正在提取SIFT和HOG特征...')
        for image_path in tqdm(self.image_paths):
            descriptors = self.extract_sift_features(image_path)
            if descriptors.shape[0] > 0:
                self.features_dict[image_path] = descriptors
                all_features.append(descriptors)
        
            # 提取并存储HOG特征
            hog_descriptor = self.extract_hog_features(image_path)
            if hog_descriptor.shape[0] > 0:
                self.hog_features[image_path] = hog_descriptor
        
        # 将所有特征连接成一个大矩阵
        all_features = np.vstack(all_features)
        
        print(f"总共从{len(self.features_dict)}张图像中提取了{all_features.shape[0]}个特征点")
        
        # 使用K-means聚类来创建视觉词汇
        print(f"正在构建包含{self.vocab_size}个视觉词汇的词袋模型...")
        self.kmeans = KMeans(n_clusters=self.vocab_size, init='k-means++', random_state=42, n_init=1, verbose=1)
        
        # 强制采样，加快KMeans收敛速度
        max_samples = 50000
        # 如果特征数量过多，可以随机抽样减少计算量
        if all_features.shape[0] > max_samples:
            idx = np.random.choice(all_features.shape[0], max_samples, replace=False)
            sampled_features = all_features[idx]
            print(f'强制采样后特征点数：{sampled_features.shape[0]}')
        else:
            sampled_features = all_features
            
        # 始终使用采样后的特征点进行聚类
        self.kmeans.fit(sampled_features)
        
        print("词典构建完成！")
    
    def create_histogram(self, descriptors):
        """创建视觉词汇直方图"""
        if descriptors.shape[0] == 0:
            return np.zeros(self.vocab_size)
        
        # 预测每个特征点属于哪个聚类（视觉词）
        predictions = self.kmeans.predict(descriptors)
        histogram = np.zeros(self.vocab_size)
        
        # 计算Term Frequency(TF)
        for prediction in predictions:
            histogram[prediction] += 1
        
        # 归一化TF
        if np.sum(histogram) > 0:
            histogram = histogram / np.sum(histogram)
            
        # 应用IDF权重（只有在所有直方图都已生成后才有意义）
        if len(self.histograms) > 0:
            all_hist = np.array(list(self.histograms.values()))
            df = np.sum(all_hist > 0, axis=0)
            idf_weights = np.log((len(self.image_paths) + 1) / (df + 1))
            histogram = histogram * idf_weights
        # 否则不加IDF
        
        # L2归一化
        norm = np.linalg.norm(histogram)
        if norm > 0:
            histogram = histogram / norm
        
        return histogram
    
    def create_image_histograms(self):
        """为所有图像创建直方图"""
        print("正在为数据集中的每张图像创建直方图...")
        for image_path in tqdm(self.features_dict.keys()):
            descriptors = self.features_dict[image_path]
            self.histograms[image_path] = self.create_histogram(descriptors)
        
        print(f"成功为{len(self.histograms)}张图像创建了直方图")
    
    def save_model(self, filename="bow_model.pkl"):
        """保存模型到文件"""
        model_data = {
            "kmeans": self.kmeans,
            "histograms": self.histograms,
            "image_paths": self.image_paths,
            "vocab_size": self.vocab_size,
            "hog_features": self.hog_features
        }
        with open(filename, 'wb') as f:
            pickle.dump(model_data, f)
        print(f"模型已保存至 {filename}")
    
    def load_model(self, filename="bow_model.pkl"):
        """从文件加载模型"""
        with open(filename, 'rb') as f:
            model_data = pickle.load(f)
        
        self.kmeans = model_data["kmeans"]
        self.histograms = model_data["histograms"]
        self.image_paths = model_data["image_paths"]
        self.vocab_size = model_data["vocab_size"]
        self.hog_features = model_data.get("hog_features", {})
        print(f"模型已从 {filename} 加载")
    
    def search_image(self, query_image_path, top_n=5):
        """根据查询图像检索相似图像"""
        # 提取查询图像的SIFT和HOG特征
        query_sift_descriptor = self.extract_sift_features(query_image_path)
        query_hog_descriptor = self.extract_hog_features(query_image_path)
        
        if query_sift_descriptor.shape[0] == 0 or query_hog_descriptor.shape[0] == 0:
            print("无法从查询图像中提取特征")
            return []
        
        # 为查询图像创建直方图(SIFT)
        query_histogram = self.create_histogram(query_sift_descriptor)
        
        # HOG直接作为特征向量
        query_hog_vector = query_hog_descriptor.reshape(1, -1)
        
        # 计算查询直方图与所有图像直方图之间的相似度
        similarities = {}
        query_image_path_normalized = os.path.normpath(os.path.abspath(query_image_path))
        for image_path, histogram in self.histograms.items():
            # 规范化图像路径
            image_path_normalized = os.path.normpath(os.path.abspath(image_path))
            # 跳过原图本身
            if query_image_path_normalized == image_path_normalized:
                continue
            # SIFT相似度
            cosine_sim = cosine_similarity([query_histogram], [histogram])[0][0]
            euclidean_dist = 1- np.linalg.norm(query_histogram - histogram) / np.sqrt(self.vocab_size)
            chi2_dist = 1 - sum([(a - b) ** 2 / (a + b + 1e-10) for a, b in zip(query_histogram, histogram)]) / 2
            
            # HOG相似度
            hog_vector = self.hog_features[image_path].reshape(1, -1)
            hog_sim = cosine_similarity(query_hog_vector, hog_vector)[0][0]
            
            # 综合相似度 (可根据效果调整权重)
            similarity = 0.6*cosine_sim + 0.4*hog_sim
            # similarity = 0.7*cosine_sim + 0.2*euclidean_dist + 0.1*chi2_dist
            similarities[image_path] = similarity
        
        # 按相似度降序排序
        sorted_results = sorted(similarities.items(), key=lambda x: x[1], reverse=True)
        
        return sorted_results[:top_n]
    
def show_results(query_image_path, results):
    """显示检索结果"""
    plt.figure(figsize=(15, 10))
    
    # 查询图像位于左上角
    plt.subplot(2, 3, 1)
    query_img = cv2.imread(query_image_path)
    query_img = cv2.cvtColor(query_img, cv2.COLOR_BGR2RGB)
    plt.imshow(query_img)
    plt.title("查询图像", fontsize=14)
    plt.axis('off')
    
    # 结果图像放在2-6
    for i, (image_path, similarity) in enumerate(results[:5]):
        plt.subplot(2, 3, i + 2)
        result_img = cv2.imread(image_path)
        result_img = cv2.cvtColor(result_img, cv2.COLOR_BGR2RGB)
        plt.imshow(result_img)
        # 只显示文件名和相似度信息，不显示路径
        plt.title(f"相似度: {similarity:.4f}\n{os.path.basename(image_path)}", fontsize=10)
        plt.axis('off')
    plt.tight_layout()
    plt.show()

def main():
    # 设置数据集路径
    dataset_path = "./caltech-101"  # 请修改为实际的数据集路径
    
    # 1. 初始化BoVW模型
    bow = BagOfVisualWords(vocab_size=800)
    
    # 2. 模型加载或训练
    # 尝试加载现有模型，如果不存在则创建新模型
    if input("是否训练新模型？(y/n): ").strip().lower() == 'n':
        bow.load_model()
        print("已加载现有模型")
    else:
        print("构建新模型...")
        # 2.1 测试特征提取功能
        test_img_path = os.path.join(dataset_path, 'airplanes', 'image_0001.jpg')
        descriptors = bow.extract_sift_features(test_img_path)
        print(f'测试图片提取到{len(descriptors)}个特征点')
        
        # 2.2 构建词汇表
        bow.build_vocabulary(dataset_path)
        # 2.3 创建直方图
        test_hist = bow.create_histogram(descriptors)
        print(f'测试直方图形状: {test_hist}，总和：{np.sum(test_hist)}')
        
        # 2.4为所有图像创建直方图
        bow.create_image_histograms()
        
        # 2.5 保存模型
        bow.save_model()
    
    # 3. 检索功能测试
    while True:
        # 3.1 用户输入查询
        query_image_path = input("请输入查询图像路径（或输入'q'退出）: ").strip()
        if query_image_path.lower() == 'q':
            break
        parts = query_image_path.replace('\\', '/').split('/')
        category = parts[0]
        num = parts[1].zfill(4) # 补零到4位
        query_image_path = f'caltech-101/{category}/image_{num}.jpg'
   
        if not os.path.exists(query_image_path):
            print("图像路径不存在，请重新输入")
            continue
    
        # 3.2 执行检索
        results = bow.search_image(query_image_path, top_n=5)
        
        # 3.3 显示检索结果
        print("\n检索结果:")
        for i, (image_path, similarity) in enumerate(results):
            print(f"{i+1}. {os.path.basename(image_path)} - 相似度: {similarity:.4f}")
        
        # 3.4 可视化检索结果
        show_results(query_image_path, results)

if __name__ == "__main__":
    main()