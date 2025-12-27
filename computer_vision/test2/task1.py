import numpy as np
import cv2 as cv
'''
任务：读取图片
1. 平移:x轴平移100像素，y轴平移150像素
2. 缩放：缩放到1024*768，按比例缩小60%
3. 翻转：水平翻转，垂直反转，水平+垂直翻转
4. 旋转：给出旋转中心，旋转角度
5. 缩略：将图片缩小，放到原图的左上角
'''
# 平移函数
def shift(img):
    rows, cols = img.shape[:2]
    M = np.float32([[1, 0, 100], [0, 1, 150]])
    img_shift = cv.warpAffine(img, M, (cols, rows))
    cv.imwrite('img_shift.jpg', img_shift)
    cv.imshow('img_shift', img_shift)
    cv.waitKey(0)
    cv.destroyAllWindows()
    
# 缩放函数
def scale(img):
    rows, cols = img.shape[:2]
    img_scale1 = cv.resize(img, (1024, 768), interpolation=cv.INTER_LINEAR)
    cv.imwrite('img_scale1.jpg', img_scale1)
    cv.imshow('img_scale1', img_scale1)
    cv.waitKey(0)
    cv.destroyAllWindows()
    
    img_scale2 = cv.resize(img, None, fx=0.6, fy=0.6, interpolation=cv.INTER_LINEAR)
    cv.imwrite('img_scale2.jpg', img_scale2)
    cv.imshow('img_scale2', img_scale2)
    cv.waitKey(0)
    cv.destroyAllWindows()
    
# 翻转函数
def flip(img):
    img_flip1 = cv.flip(img, 1) # >0 水平翻转
    cv.imwrite('img_flip_h.jpg', img_flip1)
    cv.imshow('img_flip_h', img_flip1)
    cv.waitKey(0)
    cv.destroyAllWindows()
    
    img_flip2 = cv.flip(img, 0) # =0 垂直翻转
    cv.imwrite('img_flip_v.jpg', img_flip2)
    cv.imshow('img_flip_v', img_flip2)
    cv.waitKey(0)
    cv.destroyAllWindows()
    
    img_flip3 = cv.flip(img, -1) # <0 水平+垂直翻转
    cv.imwrite('img_flip_hv.jpg', img_flip3)
    cv.imshow('img_flip3_hv', img_flip3)
    cv.waitKey(0)
    cv.destroyAllWindows()
    
# 旋转函数
def rotate(img):
    rows, cols = img.shape[:2]
    M = cv.getRotationMatrix2D((cols/2, rows/2), 45, 1) # 旋转中心，旋转角度，缩放比例
    img_rotate = cv.warpAffine(img, M, (cols, rows))
    cv.imwrite('img_rotate.jpg', img_rotate)
    cv.imshow('img_rotate', img_rotate)
    cv.waitKey(0)
    cv.destroyAllWindows()
    
# 缩略函数,将图片缩小，放到原图的左上角
def thumbnail(img):
    rows, cols = img.shape[:2]
    img_thumbnail = cv.resize(img, (cols//2, rows//2), interpolation=cv.INTER_LINEAR)
    # 放到原图左上角
    img[0:rows//2, 0:cols//2] = img_thumbnail
    cv.imwrite('img_thumbnail.jpg', img)
    cv.imshow('img_thumbnail', img)
    cv.waitKey(0)
    cv.destroyAllWindows()


def main():
    # 读取图片
    img = cv.imread('img.jpg')
    if img is None:
        print('图片读取失败')
        return
    # shift(img)
    scale(img)
    # flip(img)
    # rotate(img)
    # thumbnail(img)
    

if __name__ == '__main__':
    main()
    

