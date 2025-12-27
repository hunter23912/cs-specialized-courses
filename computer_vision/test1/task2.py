import cv2 as cv

cap = cv.VideoCapture('video.mp4')

# 播放视频，按任意键退出
while True:
    ret, frame = cap.read()
    if not ret:
        break
    cv.imshow('the playing video', frame)
    if cv.waitKey(30) != -1:
        break

cap.release() 
cv.destroyAllWindows()