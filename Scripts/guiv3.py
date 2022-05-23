import cv2
import time
import os

title_window = 'window'
thresh_value = 0
slider_max = 255
file_extension = 'tvalue'

def on_trackbar(val):
    global thresh_value
    thresh_value = val
    print(thresh_value)

def save_file(path, val, ext):
    #dir = os.path.split(path)
    f = open(path + '.' + ext, 'w')
    f.write(str(val))
    f.close()

PATH = "/home/lab/Downloads/MECLO_C_M_26_83.avi.avi"
cap = cv2.VideoCapture(PATH)

cv2.namedWindow(title_window)
trackbar_name = 'threshold'
cv2.createTrackbar(trackbar_name, title_window , 0, slider_max, on_trackbar)

while(cap.isOpened()):
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 3)
    
    ret, thresh = cv2.threshold(gray, thresh_value, 255, cv2.THRESH_BINARY_INV)
    print(thresh_value)

    cv2.imshow('title_window', thresh)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    time.sleep(0.015)

save_file(PATH, thresh_value, file_extension)