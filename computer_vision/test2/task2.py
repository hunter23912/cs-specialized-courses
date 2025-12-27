import numpy as np
import cv2 as cv
'''
读取一张新的图片，将其转换为灰度图片；
缩放灰度图片为正方形（边长不小于500像素）；
用圆形掩膜对图片进行切片，并保存切片后的图像
'''

def main():
    img = cv.imread('img.jpg')
    if img is None:
        print('图片读取失败')
        return
    # 转换为灰度图片
    img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    # 调整为正方形
    suqare_size = 500
    img_square = cv.resize(img_gray, (suqare_size, suqare_size), interpolation=cv.INTER_LINEAR)
    # 画圆形掩膜,创建一个正方形黑幕，再画一个圆形掩膜
    mask = np.zeros((suqare_size, suqare_size), np.uint8)    
    # 圆心，半径，颜色，-1表示填充，返回值是一个圆形掩膜
    cv.circle(mask, (suqare_size//2, suqare_size//2), suqare_size//2, 255, -1) 
    # 与操作
    img_new = cv.bitwise_and(img_square, img_square, mask=mask)
    
    cv.imwrite('img_new.jpg', img_new)
    cv.imshow('img_new', img_new)
    cv.waitKey(0)
    cv.destroyAllWindows()
    
    
    
if __name__ == '__main__':
    main()