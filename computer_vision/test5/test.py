import cv2
import os, random
import numpy as np
import matplotlib.pyplot as plt

# 设置plt的中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置中文字体为黑体
plt.rcParams['axes.unicode_minus'] = False  # 显示负号

class HaarCascadeFaceDetector:
    """
    基于 Haar 特征和 AdaBoost 算法的人脸检测器
    """

    def __init__(self, cascade_path=None):
        """
        初始化人脸检测器
        :param cascade_path: Haar 级联分类器的 XML 文件路径，如果为 None 则使用 OpenCV 默认提供的分类器
        """
        if cascade_path is None:
            # 使用 OpenCV 自带的人脸检测级联分类器
            self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        else:
            self.face_cascade = cv2.CascadeClassifier(cascade_path)

        if self.face_cascade.empty():
            raise ValueError("无法加载级联分类器")

    def detect_faces(self, image, scale_factor=1.2, min_neighbors=8, min_size=(20, 20)):
        """
        检测图像中的人脸
        :param image: 输入图像
        :param scale_factor: 图像缩放因子
        :param min_neighbors: 最小邻居数
        :param min_size: 最小人脸大小
        :return: 检测到的人脸矩形框列表
        """
        # 转换为灰度图像
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image

        # 使用级联分类器检测人脸
        faces = self.face_cascade.detectMultiScale(
            gray,
            scaleFactor=scale_factor,
            minNeighbors=min_neighbors,
            minSize=min_size
        )        
        return faces # 返回一个ndarray，每个元素包括：(x, y, w, h)，分别表示人脸的左上角坐标和宽高

    def draw_faces(self, image, faces, color=(0, 255, 0), thickness=2):
        """
        在图像上绘制检测到的人脸
        :param image: 输入图像
        :param faces: 人脸矩形框列表
        :param color: 矩形框颜色
        :param thickness: 矩形框线条粗细
        :return: 绘制了人脸框的图像
        """
        img_copy = image.copy()
        for (x, y, w, h) in faces:
            cv2.rectangle(img_copy, (x, y), (x + w, y + h), color, thickness)
        return img_copy # 返回一个ndarray，绘制了人脸框的图像


def test_on_image(detector, image_path):
    """
    在单张图像上测试人脸检测器
    :param detector: 人脸检测器实例
    :param image_path: 图像路径
    :return: 原始图像, 检测结果图像, 检测到的人脸数量
    """
    # 读取图像
    image = cv2.imread(image_path)
    if image is None:
        print(f"无法读取图像: {image_path}")
        return None, None, 0

    # 检测人脸
    faces = detector.detect_faces(image)

    # 绘制结果
    result_image = detector.draw_faces(image, faces)

    return image, result_image, len(faces)


def test_on_dataset(detector, dataset_dir, output_dir=None, max_images=5):
    """
    在数据集上测试人脸检测器
    :param detector: 人脸检测器实例
    :param dataset_dir: 数据集目录
    :param output_dir: 输出目录，用于保存检测结果
    :param max_images: 最大测试图像数
    """
    if output_dir is not None and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    image_files = [] # 存储所有图片路径
    for root, _, files in os.walk(dataset_dir):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                image_files.append(os.path.join(root, file))
    
    # 随机抽取max_images张图片
    if len(image_files) > max_images:
        image_files = random.sample(image_files, max_images)
        
    # 限制测试图像数量
    # image_files = image_files[:max_images]

    results = []
    for image_path in image_files:
        print(f"处理图像: {image_path}")
        _, result_image, face_count = test_on_image(detector, image_path)

        if result_image is not None:
            results.append((image_path, result_image, face_count)) # 图片路径，检测结果，检测到的人脸数量

            if output_dir is not None:
                output_path = os.path.join(output_dir, os.path.basename(image_path)) # 输出路径为：输出目录+图片名称
                cv2.imwrite(output_path, result_image)
                print(f"结果已保存至: {output_path}")

    return results


def display_results(results):
    """
    显示检测结果
    :param results: 检测结果列表
    """
    n = len(results)
    fig, axes = plt.subplots(n, 1, figsize=(10, 5 * n))

    if n == 1:
        axes = [axes]

    for i, (image_path, result_image, face_count) in enumerate(results):
        axes[i].imshow(cv2.cvtColor(result_image, cv2.COLOR_BGR2RGB))
        axes[i].set_title(f"图像: {os.path.basename(image_path)}, 检测到 {face_count} 张人脸")
        axes[i].axis('off')

    plt.tight_layout()
    plt.show()


def main():
    # 初始化人脸检测器
    detector = HaarCascadeFaceDetector()

    # 设置 FDDB 数据集路径
    # 注意：请根据你的实际路径修改
    dataset_dir = "./2002/09/19/big"
    output_dir = "./detection_results"

    # 在数据集上测试
    results = test_on_dataset(detector, dataset_dir, output_dir, max_images=5)

    # 显示结果
    if results:
        display_results(results)
    else:
        print("没有检测到有效的结果")


if __name__ == "__main__":
    main()