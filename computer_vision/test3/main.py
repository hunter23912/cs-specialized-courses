import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
# 读取一张图片，转换为HSV空间
# 分离原 图片的RGB通道及转换后的HSV通道
# 对RGB三个通道分别画出三维图（polt_sufface函数）
# 通过plt.show()显示三维图

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

def show_res(*img):
    plt.figure(figsize=(12, 8))
    
    # 设置2行2列的子图
    plt.subplot(2, 2, 1)
    plt.imshow(cv.cvtColor(img[0], cv.COLOR_BGR2RGB))
    plt.title('原图')
    plt.axis('off') # 关闭坐标轴
    
    plt.subplot(2, 2, 2)
    plt.imshow(img[1], cmap='gray')
    plt.title('B通道')
    plt.axis('off')

    plt.subplot(2, 2, 3)
    plt.imshow(img[2], cmap='gray')
    plt.title('G通道')
    plt.axis('off')
    
    plt.subplot(2, 2, 4)
    plt.imshow(img[3], cmap='gray')
    plt.title('R通道')
    plt.axis('off')
    
    plt.tight_layout()
    plt.savefig('BGR.png') # 保存图片
    plt.show()

# 绘制HSV空间的三个通道
def test1_1():
    img = cv.imread('img.jpg')
    img_hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    h, s, v = cv.split(img_hsv) # Hue色调, Saturation饱和度, Value亮度
    #分离RGB通道
    b, g, r = cv.split(img) # BGR通道
    
    # show_res(img, h, s, v) # 显示原图和HSV三个通道
    show_res(img, b, g, r) # 显示原图和RGB三个通道

# 绘制RGB三通道的三维图
def test1_2():
    '''调用channels_3D函数，绘制RGB三通道的三维图'''
    img = cv.imread('img.jpg')
    img = cv.resize(img, (0, 0), fx = 0.6, fy = 0.6) # 缩小图片

    # 将BGR图像转换为RGB图像
    img_rgb = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    # 分离RGB通道
    r, g, b = cv.split(img_rgb) 
    
    # 创建网格
    h, w = img.shape[:2]
    x = np.arange(0, w, 1) # x轴
    y = np.arange(0, h, 1) # y轴
    x_mesh, y_mesh = np.meshgrid(x, y) # 创建网格
    
    # 创建3D图形
    fig = plt.figure(figsize=(16, 12))
    
    ax0 = fig.add_subplot(2,2,1)
    ax0.imshow(img_rgb) # 显示原图
    ax0.set_title('原图')
    ax0.axis('off')
    
    # R通道
    ax1 = fig.add_subplot(2,2,2, projection='3d')
    surf1 = ax1.plot_surface(x_mesh, y_mesh, r, cmap='Reds')
    ax1.set_title('R通道三维图')
    ax1.set_xlabel('X轴')
    ax1.set_ylabel('Y轴')
    
    # G通道
    ax2 = fig.add_subplot(2,2,3, projection='3d')
    surf2 = ax2.plot_surface(x_mesh, y_mesh, g, cmap='Greens')
    ax2.set_title('G通道三维图')
    ax2.set_xlabel('X轴')
    ax2.set_ylabel('Y轴')
    
    # B通道
    ax3 = fig.add_subplot(2,2,4, projection='3d')
    surf3 = ax3.plot_surface(x_mesh, y_mesh, b, cmap='Blues')
    ax3.set_title('B通道三维图')
    ax3.set_xlabel('X轴')
    ax3.set_ylabel('Y轴')
    
    # 为曲面添加颜色条
    fig.colorbar(surf1, ax=ax1, shrink=0.5, aspect=5, label='R通道像素值')
    fig.colorbar(surf2, ax=ax2, shrink=0.5, aspect=5, label='G通道像素值')
    fig.colorbar(surf3, ax=ax3, shrink=0.5, aspect=5, label='B通道像素值')
    
    plt.tight_layout() # 自动调整子图参数
    plt.savefig('RGB_3D.png') # 保存图片
    plt.show() # 显示图形

# 画出灰度图像及其直方图
def test2_1():
    img = cv.imread('home_color.png')
    # 计算直方图
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    hist, bins = np.histogram(img.flatten(), 256, [0, 256]) # 计算直方图
    
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.imshow(gray, cmap='gray')
    plt.title('home_gray')
    plt.axis('off')
    
    plt.subplot(1, 2, 2)
    plt.plot(hist, color='gray')
    plt.xlim([0, 256])
    plt.title('Histogram')
    plt.xlabel('Pixel Value')
    plt.ylabel('Frequency')
    plt.grid()
    
    plt.tight_layout()
    plt.savefig('gray_histogram.png') # 保存图片
    plt.show()
    
# 计算RGB通道的直方图
def test2_2():
    img = cv.imread('home_color.png')
    # 计算RGB通道的直方图
    colors = ('b', 'g', 'r')
    plt.figure(figsize=(12, 6))
    
    # 左边显示彩色原图
    plt.subplot(1, 2, 1)
    plt.imshow(cv.cvtColor(img, cv.COLOR_BGR2RGB))
    plt.title('home_color')
    plt.axis('off')
    
    # 右边显示彩色直方图
    plt.subplot(1, 2, 2)
    for i, color in enumerate(colors):
        hist = cv.calcHist([img], [i], None, [256], [0, 256])
        plt.plot(hist, color=color, label = f'{color.upper()}通道')
    
    plt.xlim([0, 256])
    plt.title('彩色直方图')
    plt.xlabel('像素值')
    plt.ylabel('频数')
    plt.grid()
    
    plt.tight_layout()
    plt.savefig('color_histogram.png') # 保存图片
    plt.show()

# 将四个子图放在一起，原图，ROI的mask图，ROI提取后的图及其直方图
def test2_3():
    img = cv.imread('home_color.png')
    # 定义ROI区域
    x_start, x_end = 50, 100
    y_start, y_end = 100, 200
    roi = img[x_start:x_end, y_start:y_end] # 提取ROI区域
    
    # 创建mask
    mask = np.zeros(img.shape[:2], dtype=np.uint8) # 创建mask
    mask[x_start:x_end, y_start:y_end] = 255 # 设置ROI区域为255
    
    masked_img = cv.bitwise_and(img, img, mask=mask) # 应用mask
    
    # 计算ROI区域的直方图
    colors = ('b', 'g', 'r')
    plt.figure(figsize=(12, 8))
    
    plt.subplot(2, 2, 1)
    plt.imshow(cv.cvtColor(img, cv.COLOR_BGR2RGB))
    plt.title('home_color')
    plt.axis('off')
    
    plt.subplot(2, 2, 2)
    plt.imshow(mask, cmap='gray')
    plt.title('ROI Mask')
    plt.axis('off')
    
    plt.subplot(2, 2, 3)
    plt.imshow(cv.cvtColor(masked_img, cv.COLOR_BGR2RGB))
    plt.title('ROI 提取图')
    plt.axis('off')
    
    plt.subplot(2, 2, 4)
    for i, color in enumerate(colors):
        hist = cv.calcHist([roi], [i], None, [256], [0, 256])
        plt.plot(hist, color=color, label = f'{color.upper()}通道')
    plt.xlim([0, 256])
    plt.title('ROI直方图')
    plt.xlabel('像素值')
    plt.ylabel('频数')
    plt.grid()
    plt.legend() # 显示图例
    
    plt.tight_layout()
    plt.savefig('roi_histogram.png') # 保存图片
    plt.show()

# 自实现直方图均衡化
def histogram_equalization(img):

    # 将图像转为灰度图
    img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    # 计算灰度图像的直方图
    # hist纵坐标数值数组，bins是直方图的横坐标
    hist, bins = np.histogram(img_gray.flatten(), 256, [0, 256])

    # 计算累计分布函数
    cdf = hist.cumsum()  # 累积函数，表示每个灰度级的累计像素数量

    # 使用cdf对图像均衡化
    cdf_m = np.ma.masked_equal(cdf, 0)  # 掩盖cdf数组中的0值

    # 按权重映射到0-255之间
    cdf_m = (cdf_m - cdf_m.min()) / (cdf_m.max() - cdf_m.min()) * 255
    cdf = np.ma.filled(cdf_m, 0).astype("uint8") # 查找表
    
    # 将原图像的灰度级映射到均衡化后的灰度级
    img_res = cdf[img_gray]

    return img_res

# 绘制直方图及均衡化后的直方图
def plot_histograms(img, img_res, img_res_cv):

    plt.figure(figsize=(10, 10))

    # 原始图像及其直方图
    plt.subplot(3, 2, 1)
    plt.imshow(cv.cvtColor(img, cv.COLOR_BGR2RGB))
    plt.title("hill原图像")
    plt.axis("off")

    plt.subplot(3, 2, 2)
    plt.hist(img.ravel(), 256, [0, 256], color="black")
    plt.title("hill原图像直方图")
    # 关闭纵坐标
    # plt.gca().axes.get_yaxis().set_visible(False)

    # 均衡化后的图像及其直方图
    plt.subplot(3, 2, 3)
    plt.imshow(img_res, cmap="gray")
    plt.title("自实现均衡化后的hill图像")
    plt.axis("off")

    plt.subplot(3, 2, 4)
    plt.hist(img_res.ravel(), 256, [0, 256], color="black")
    plt.title("自实现均衡化后的hill图像直方图")

    # opencv直方图均衡化后的图像及其直方图
    plt.subplot(3, 2, 5)
    plt.imshow(img_res_cv, cmap="gray")
    plt.title("opencv均衡化后的hill图像")
    plt.axis("off")

    plt.subplot(3, 2, 6)
    plt.hist(img_res_cv.ravel(), 256, [0, 256], color="black")
    plt.title("opencv均衡化后的hill图像直方图")

    # 调整图像参数
    plt.tight_layout()
    plt.subplots_adjust(
        left=0.01, right=0.95, top=0.95, bottom=0.05, wspace=0.3, hspace=0.3
    )
    plt.savefig("hill_result.png")
    plt.show()

# 直方图均衡化
def test3():
    img = cv.imread("hill.jpg")
    img_res = histogram_equalization(img)
    # 使用opencv的直方图均衡化
    img_res_cv = cv.equalizeHist(cv.cvtColor(img, cv.COLOR_BGR2GRAY))

    plot_histograms(img, img_res, img_res_cv)

def main():
    # test1_1()
    # test1_2()
    # test2_1()
    # test2_2()
    # test2_3()
    test3()
 
if __name__ == '__main__':
    main()
