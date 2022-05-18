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
    ret, frames[i] = cap.read()

height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
blank_image = np.zeros((height * 3, width * 2, 3), np.uint8)

#TODO: blank image creation
for i in range(len(frames)):
    blank_image[]
    

def getThrottle(event):
    thresh_value = Throttle.get()
    print(thresh_value)

Throttle = Scale(master, from_=0, to=254, orient=HORIZONTAL, command=getThrottle)
Throttle.set(0)
Throttle.pack()

master.mainloop()