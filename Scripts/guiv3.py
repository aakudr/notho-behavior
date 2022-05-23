import cv2
import time

title_window = 'window'
thresh_value = 0
slider_max = 255

def on_trackbar(val):
    global thresh_value
    thresh_value = val
    print(thresh_value)
#    beta = ( 1.0 - alpha )
#    dst = cv.addWeighted(src1, alpha, src2, beta, 0.0)
#    cv.imshow(title_window, dst)

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