from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from sklearn.datasets import load_sample_image

# 设置plt中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置中文字体为黑体
plt.rcParams['axes.unicode_minus'] = False  # 显示负号

# 加载示例图片
china = load_sample_image("china.jpg")
img = china[50:200, 50:200, 0] / 255  # 截取部分区域并转为灰度

# PCA降维重建
pca = PCA(5)  # 保留10个主成分
img_reduced = pca.fit_transform(img)
print(len(img))
print(len(img_reduced))
print(img.shape)
print(img_reduced.shape)
img_reconstructed = pca.inverse_transform(img_reduced)
print(img_reconstructed.shape)


# 显示结果
plt.figure(figsize=(10, 5))
plt.subplot(121), plt.imshow(img, cmap='gray'), plt.title('原始图片')
plt.subplot(122), plt.imshow(img_reconstructed, cmap='gray'), 
plt.title(f'PCA降维重建 (保留10个成分)\n解释方差:{sum(pca.explained_variance_ratio_):.1%}')
plt.show()

image_path = ''  # 替换为你的图片路径
