import time

import numpy as np
import cv2
import serial
from imutils import resize
from keras.models import load_model
from keras.preprocessing.image import img_to_array
from keras.applications.mobilenet_v2 import preprocess_input


def gstreamer_pipeline(
    capture_width=1920,
    capture_height=1080,
    display_width=960,
    display_height=540,
    framerate=30,
    flip_method=0,
):
    return (
        "nvarguscamerasrc ! "
        "video/x-raw(memory:NVMM), "
        "width=(int)%d, height=(int)%d, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink drop=True"
        % (
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
    )

serial_port = serial.Serial(
    port="/dev/ttyUSB0",
    baudrate=115200,
    timeout=0.5
)

model = load_model('fire_detector.model')

flagFire = 0
flagNofire = 1

vs = cv2.VideoCapture(gstreamer_pipeline(), cv2.CAP_GSTREAMER)

flagNofire = 0
flagFire = 0
while True:
    success, im = vs.read()
    imgray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY) # chuyển ảnh xám thành ảnh grayscale
    #thresh = cv2.Canny(imgray, 127, 255) # nhị phân hóa ảnh
    ret, binImg = cv2.threshold(imgray, 127, 255, cv2.THRESH_BINARY)

    (contours, _) = cv2.findContours(binImg,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    #cv2.drawContours(im, contours, -1, (0, 255, 0), 2) # vẽ lại ảnh contour vào ảnh gốc
    fire_imgs = []
    locs = []
    preds = []
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        if 20000 < w * h:
            #cv2.putText(im, str(w*h), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0))
            crop_img = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
            crop_img = cv2.resize(crop_img, (224, 224))
            crop_img = img_to_array(crop_img)
            crop_img = preprocess_input(crop_img)

            fire_imgs.append(crop_img)
            locs.append((x, y, w, h))
    if len(fire_imgs)>0:
        fire_imgs = np.array(fire_imgs, dtype='float32')
        preds = model.predict(fire_imgs, batch_size=32)
    else:
        print("No Fire")
        cv2.putText(im, "No Fire Detected!!!", (10, 10), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 255), thickness=4)
    for (loc, pred) in zip(locs, preds):
        (x, y, w, h) = loc
        (fire, nofire) = pred
        text = 'Fire' if fire > nofire else 'No Fire'
        if text == "Fire":
            if(flagFire==0):
                print("Fire detected")
                serial_port.write("1")
                cv2.rectangle(im, (x, y), (x+w, y+h), (0, 255, 0), thickness=3)
                cv2.rectangle(im, (x - 3, y - 20), (x + w + 2, y), (0, 255, 0), thickness= -1)
                cv2.putText(im, "Fire detected !", (x, y - 7), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 255), thickness=2)
                flagFire=1
                flagNofire=0
        else:
            if(flagNofire==0):
                print("No Fire")
                serial_port.write("0")
                cv2.putText(im, "No Fire Detected!!!", (10,10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), thickness=4)
                flagFire = 0
                flagNofire = 1
    im = resize(im, width=1200)
    cv2.imshow('FireDec', im)
    key = cv2.waitKey(10) & 0xFF
    if key == 27 or key == ord('q'):
        break
    time.sleep(5)
cv2.destroyAllWindows()
vs.stop()