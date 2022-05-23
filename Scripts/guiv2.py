from tkinter import *
import cv2
import random
import numpy as np

master = Tk()

thresh_value = 0

PATH = "/home/lab/Downloads/MECLO_C_M_26_83.avi.avi"
cap = cv2.VideoCapture(PATH)
totalFrames = cap.get(cv2.CAP_PROP_FRAME_COUNT)

sample_frames = [int(random.random() * (totalFrames - 200) + 200) for i in range(6)]
frame_placement = [[0, 0], [0, 1], [1, 0], [1, 1], [2, 0], [2, 1]]

frames = []
for i in range(len(sample_frames)):
    cap.set(cv2.CAP_PROP_POS_FRAMES, sample_frames[i])
    ret, frame = cap.read()
    frames.append(frame)

height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))

#blank_image[frame_placement[1][0]:frame_placement[1][0] + height, frame_placement[1][1]:frame_placement[1][1] + width,:] = frames[1]    

def getImage(h, w):
    global frame_placement
    global frames
    blank_image = np.zeros((h * 3, w * 2, 3), np.uint8)

    blank_image[frame_placement[1][0]:frame_placement[1][0] + h, frame_placement[1][1]:frame_placement[1][1] + w, :] = frames[1]
    ret, thresh = cv2.threshold(blank_image, thresh_value, 255, cv2.THRESH_BINARY_INV)
    cv2.imshow('blank', thresh)
    return thresh

test_img = getImage(height, width)

def getThrottle(event):
    global height
    global width
    global thresh_value
    thresh_value = Throttle.get()
    img_combo = getImage(height, width)
    print(thresh_value)

Throttle = Scale(master, from_=0, to=254, orient=HORIZONTAL, command=getThrottle)
Throttle.set(0)
Throttle.pack()

master.mainloop()