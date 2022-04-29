import cv2
import numpy as np
import datetime
import time
import math
import os
from skimage.morphology import skeletonize
from utils import *

PATH = "/home/lab/Downloads/MECLO_C_M_26_83.avi.avi"

skeletons = []
frame_data = [np.array([[[0, 0]], [[0, 0]]])]

cap = cv2.VideoCapture(PATH)

ret, frame = cap.read()
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

cx, cy, cr = get_circles(gray)

cnt = 1

back_sub = cv2.createBackgroundSubtractorMOG2(history=700, 
        varThreshold=20, detectShadows=True)

kernel = np.ones((20,20),np.uint8)

while(cap.isOpened()):
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 3)
    
    ret, thresh = cv2.threshold(gray, 130, 255, cv2.THRESH_BINARY_INV)
    ret, img = cv2.threshold(thresh, 254, 1, cv2.THRESH_BINARY)
    skeleton = skeletonize(img)
    
    img = np.array(skeleton.astype(int) * 255, dtype = np.uint8)
    
    print(cnt)
    cnt += 1
    
    img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    
    h, w = img.shape[:2]
    mask = create_circular_mask(h, w, radius=int(h/2.1))
    masked_img = img.copy()
    masked_img[~mask] = 0
    masked_img = cv2.cvtColor(masked_img, cv2.COLOR_BGR2GRAY)
    
    contours, hierarchy = cv2.findContours(masked_img,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)[-2:]
    rects = [cv2.boundingRect(c) for c in contours]
    
    empty_img = np.zeros((h, w, 3), np.uint8)

    if len(rects) > 0:
        # Find the largest moving"""  """ object in the image
        max = 0
        max_list = []
        for rect in rects:
            s = rect[2] * rect[3]
            if s > max:
                max = s
                max_list = rect
        max_index = rects.index(max_list)

        # Draw the bounding box
        x,y,w,h = max_list
        contour = contours[max_index]
        # print(contour)
        # time.sleep(1)
        skeletons.append([item[0] for item in contour])
        # print(skeletons)
        if cnt > 3:
            frame_data.append(analyse_skeletons(skeletons[-1], frame_data[-1], cnt))
        """ contour = edit_contour(contour) """
        # cv2.drawContours(empty_img, contour, -1, (255, 128, 0), 1)
        if len(frame_data) != 0:
            cv2.drawContours(empty_img, frame_data[-1], -1, (255, 128, 0), 1)
            cv2.drawContours(frame, frame_data[-1], -1, (255, 128, 0), 3)
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()
