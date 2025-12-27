import cv2, os, random
import numpy as np
from sklearn.svm import LinearSVC
from sklearn.metrics import roc_curve, auc
import matplotlib.pyplot as plt
from tqdm import tqdm



# HOG参数（方向梯度直方图）
winSize = (64, 128)  # HOG窗口大小
blockSize = (16, 16)  # HOG块大小
blockStride = (8, 8)  # HOG块步长
cellSize = (8, 8)  # HOG单元格大小
nbins = 9  # HOG方向数

hog = cv2.HOGDescriptor(winSize, blockSize, blockStride, cellSize, nbins)

# 提取HOG特征
def extract_hog(img_path):
    img = cv2.imread(img_path,cv2.IMREAD_COLOR) # 读取图片
    if img is None:
        raise ValueError(f'无法读取图片：{img_path}')
    img = cv2.resize(img, winSize)  # 调整图片大小
    features = hog.compute(img)  # 计算HOG特征
    return features.flatten()  # 返回展平特征向量

# 加载数据集
def load_data(pos_dir, neg_dir, max_samples=None):
    X, y = [], []
    pos_imgs = [os.path.join(pos_dir, f) for f in os.listdir(pos_dir) if f.endswith('.png') or f.endswith('.jpg')]
    neg_imgs = [os.path.join(neg_dir, f) for f in os.listdir(neg_dir) if f.endswith('.png') or f.endswith('.jpg')]
    
    # 只提取前max_samples个样本
    if max_samples:
        pos_imgs = pos_imgs[:max_samples]
        neg_imgs = neg_imgs[:max_samples]
        
    for img_path in tqdm(pos_imgs, desc='加载正样本'):
        X.append(extract_hog(img_path))
        y.append(1)
    for img_path in tqdm(neg_imgs, desc='加载负样本'):
        X.append(extract_hog(img_path))
        y.append(0)
    return np.array(X), np.array(y)

# 路径设置
train_pos_dir = os.path.join('original_images', 'train', 'pos')
train_neg_dir = os.path.join('original_images', 'train', 'neg')
test_pos_dir = os.path.join('original_images', 'test', 'pos')
test_neg_dir = os.path.join('original_images', 'test', 'neg')

# 加载训练数据
X_train, y_train = load_data(train_pos_dir, train_neg_dir, max_samples=500)
# 加载测试数据
X_test, y_test = load_data(test_pos_dir, test_neg_dir, max_samples=200)

# SVM参数调优
best_auc = 0 # 初始AUC
best_C = 1.0 # 初始C参数 
Cs = [0.01, 0.1, 1, 10, 100] # C参数范围,值越大，拟合程度越高
for C in Cs:
    clf = LinearSVC(C=C, max_iter=10000) # 创建SVM分类器
    clf.fit(X_train, y_train) # 训练模型
    y_score = clf.decision_function(X_test) # 决策函数值
    fpr, tpr, thresholds = roc_curve(y_test, y_score) # 计算ROC曲线
    roc_auc = auc(fpr, tpr) # 计算AUC
    print(f'C={C}, AUC={roc_auc:.4f}')
    if roc_auc > best_auc:
        best_auc = roc_auc
        best_C = C
print(f'最佳参数：C={best_C}, 最优AUC={best_auc:.4f}')

# 用最优参数训练最终模型、
clf = LinearSVC(C=best_C, max_iter=10000)
clf.fit(X_train, y_train)
y_score = clf.decision_function(X_test)
# 绘制ROC曲线
fpr, tpr, thresholds = roc_curve(y_test, y_score)
roc_auc = auc(fpr, tpr)
plt.figure(figsize=(8, 6), dpi=120)
plt.style.use('seaborn-v0_8-darkgrid')  # 使用seaborn风格
plt.plot(fpr, tpr, color='darkorange', lw=3, label=f'ROC curve (AUC = {roc_auc:.2f})')
plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--', label='Random')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate', fontsize=14)
plt.ylabel('True Positive Rate', fontsize=14)
plt.title('ROC Curve for Pedestrian Detection', fontsize=16)
plt.legend(loc='lower right', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig('roc_curve.svg')
plt.show()

# 随机输出部分测试集结果
test_imgs = []
test_imgs += [os.path.join(test_pos_dir, f) for f in os.listdir(test_pos_dir) if f.endswith('.png') or f.endswith('.jpg')]
test_imgs += [os.path.join(test_neg_dir, f) for f in os.listdir(test_neg_dir) if f.endswith('.png') or f.endswith('.jpg')]


# 设置字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False

num_samples = 10
cols = 5
rows = num_samples // cols
sample_indices = random.sample(range(len(test_imgs)), num_samples)
plt.figure(figsize=(cols * 3, rows * 4))
for i, idx in enumerate(sample_indices):
    img_path = test_imgs[idx]
    feat = extract_hog(img_path).reshape(1, -1)
    pred = clf.predict(feat)[0]
    img = cv2.imread(img_path)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    plt.subplot(rows, cols, i + 1)
    plt.imshow(img_rgb)
    plt.axis('off')
    plt.title(f"预测: {'True' if pred==1 else 'False'}", fontsize=12)
plt.suptitle("随机抽取10张测试图片的预测结果", fontsize=16)
plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig('sample_predictions.svg')
plt.show()