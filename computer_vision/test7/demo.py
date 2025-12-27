import cv2
import numpy as np
import matplotlib.pyplot as plt

img1 = cv2.imread('img1.png')
img2 = cv2.imread('img2.png')

# 转换为灰度图像
gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

# 创建SIFT对象
sift = cv2.SIFT_create()

# 检测关键点
kp1, des1 = sift.detectAndCompute(gray1, None)
kp2, des2 = sift.detectAndCompute(gray2, None)

# 绘制关键点
img1_kp = cv2.drawKeypoints(img1, kp1, None, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
img2_kp = cv2.drawKeypoints(img2, kp1, None, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

# 先显示两张原图片
plt.figure(figsize=(12, 6))
plt.subplot(121)
plt.imshow(cv2.cvtColor(img1, cv2.COLOR_BGR2RGB))
plt.title('Image 1')
plt.axis('off')
plt.subplot(122)
plt.imshow(cv2.cvtColor(img2, cv2.COLOR_BGR2RGB))
plt.title('Image 2')
plt.axis('off')
# plt.savefig('original_images.svg')
plt.show()

# 显示关键点
plt.figure(figsize=(12, 6))
plt.subplot(121)
plt.imshow(cv2.cvtColor(img1_kp, cv2.COLOR_BGR2RGB))
plt.title('Image 1 keypoints')
plt.axis('off')
plt.subplot(122)
plt.imshow(cv2.cvtColor(img2_kp, cv2.COLOR_BGR2RGB))
plt.title('Image 2 keypoints')
plt.axis('off')
# plt.savefig('keypoints.svg')
plt.show()

# 使用FLANN匹配器进行特征匹配
FLANN_INDEX_KDTREE = 1
index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
search_params = dict(checks=50)
flann = cv2.FlannBasedMatcher(index_params, search_params)
matches = flann.knnMatch(des1, des2, k=2) # 快速最近邻搜索匹配器，找到每个描述符的两个最近邻

# 应用比率测试来筛选好的匹配点，只有当第一个匹配点的距离小于第二个匹配点的距离的0.7倍时，才认为是好的匹配
good_matches = []
for m, n in matches:
    if m.distance < 0.7 * n.distance:
        good_matches.append(m)
        
# 绘制匹配结果
img_matches = cv2.drawMatches(img1, kp1, img2, kp2, good_matches, None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
plt.figure(figsize=(12, 6))
plt.imshow(cv2.cvtColor(img_matches, cv2.COLOR_BGR2RGB))
plt.title('Feature Matches')
plt.axis('off')
# plt.savefig('matches.svg')
plt.show()

# 提取匹配点的坐标
src_pts = np.float32([kp1[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
dst_pts = np.float32([kp2[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)

# 使用RANSAC算法进行匹配点的提纯
M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

#根据RANSAC筛选结果，绘制匹配点连线图，只显示内点匹配
matchesMask = mask.ravel().tolist()
draw_params = dict(matchColor=(0, 255, 0),singlePointColor=None, matchesMask=matchesMask,flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
img_ransac_matches = cv2.drawMatches(img1, kp1, img2, kp2, good_matches, None, **draw_params)

# 显示RANSAC匹配结果
plt.figure(figsize=(12, 6))
plt.imshow(cv2.cvtColor(img_ransac_matches, cv2.COLOR_BGR2RGB))
plt.title('RANSAC Matches')
plt.axis('off')
# plt.savefig('ransac_matches.svg')
plt.show()

# 根据单应性矩阵完成图片拼接
h1, w1 = img1.shape[:2]
h2, w2 = img2.shape[:2]

# 计算拼接后图像的大小
points_img1 = np.float32([[0, 0], [0, h1], [w1, h1], [w1, 0]]).reshape(-1, 1, 2)
points_img2 = np.float32([[0, 0], [0, h2], [w2, h2], [w2, 0]]).reshape(-1, 1, 2)
points_img2_transformed = cv2.perspectiveTransform(points_img2, M)
points_combined = np.concatenate((points_img1, points_img2_transformed), axis=0)

[x_min, y_min] = np.int32(points_combined.min(axis=0).ravel() - 0.5)
[x_max, y_max] = np.int32(points_combined.max(axis=0).ravel() + 0.5)

translation_dist = [-x_min, -y_min]
H_translation = np.array([[1, 0, translation_dist[0]], [0, 1, translation_dist[1]], [0, 0, 1]])

# 将 img1 和 img2 拼接到同一图像中
result = cv2.warpPerspective(img1, H_translation @ M, (x_max - x_min, y_max - y_min))
# 确保目标区域大小与img2一致
y1, y2 = translation_dist[1], translation_dist[1] + h2
x1, x2 = translation_dist[0], translation_dist[0] + w2
# 调整切片范围，确保不超出result的边界
y2 = min(y2, result.shape[0])
x2 = min(x2, result.shape[1])

result[y1:y2, x1:x2] = img2[:y2 - y1, :x2 - x1]

# 显示拼接结果
plt.figure(figsize=(12, 6))
plt.imshow(cv2.cvtColor(result, cv2.COLOR_BGR2RGB))
plt.title('Stitched Image')
plt.axis('off')
plt.savefig('stitched_image.svg')
plt.show()