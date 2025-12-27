import cv2 as cv
import numpy as np
from PIL import Image, ImageDraw, ImageFont

# 读取图片，并调整大小
img = cv.imread('img1.jpg')
img = cv.resize(img, (800, 600))

# 将图片转换为PIL格式
pil_img = Image.fromarray(cv.cvtColor(img, cv.COLOR_BGR2RGB))

# 在图片上添加文字
draw = ImageDraw.Draw(pil_img)
font = ImageFont.truetype('C:/Windows/Fonts/simsun.ttc', 40)
draw.text((10, 50), '22121630 汪江豪', font = font,  fill= (0, 245, 255))

# 将PIL格式图片转换为OpenCV格式
img = cv.cvtColor(np.asarray(pil_img), cv.COLOR_RGB2BGR)

# 保存图片并展示
cv.imwrite('out.jpg', img)
cv.imshow('Image', img)
cv.waitKey(0)
cv.destroyAllWindows()

