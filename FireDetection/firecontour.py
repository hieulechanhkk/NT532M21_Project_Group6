
import numpy as np
import cv2
from keras.models import load_model
from keras.preprocessing.image import img_to_array
from keras.applications.mobilenet_v2 import preprocess_input
model = load_model('fire_detector.model')

vs = cv2.VideoCapture('FireVid.mp4')
while True:
    success, im = vs.read()
    imgray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY) # chuyển ảnh xám thành ảnh grayscale
    #thresh = cv2.Canny(imgray, 127, 255) # nhị phân hóa ảnh
    blur = cv2.GaussianBlur(im, (21, 21), 0)

    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
    imgray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
    ret, binImg = cv2.threshold(imgray, 127, 255, cv2.THRESH_BINARY)

    (contours, _) = cv2.findContours(binImg,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    cv2.drawContours(im, contours, -1, (0, 255, 0), 2) # vẽ lại ảnh contour vào ảnh gốc
    cv2.imshow('Show', im)
    cv2.waitKey(200)