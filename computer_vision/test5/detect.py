import cv2
import os
import numpy as np
import matplotlib.pyplot as plt



# 测试图片路径
def load_images_from_folder(folder):
    images = []
    for filename in os.listdir(folder):
        img = cv2.imread(os.path.join(folder, filename))
        if img is not None:
            images.append(img)
    return images

# 使用Haar分类器检测人脸
def detect_faces(face_cascade, img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    return faces

# 绘制检测结果
def draw_faces(img, faces):
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
    return img

def face_detect(img):
    # 加载haar级联分类器
    facexml = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # 检测人脸，1.3是缩放比例，5是检测到的最小邻居数
    faces = facexml.detectMultiScale(gray_img, 1.1,3)
    
    print('face num:', len(faces))
    
    # x,y,w,h分别是人脸的左上角坐标和宽高
    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
        roi_face = gray_img[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]
    cv2.imshow('face', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# 测试检测器
def test_detector():
    # face_cascade = load_data()
    # test_images = load_images_from_folder('./2002/07/19/big/img_416.jpg')
    img_path = './2002/07/19/big/img_416.jpg'
    test_img = cv2.imread(img_path)
    face_detect(test_img)

    

# 主函数
if __name__ == "__main__":
    test_detector()