from tkinter import *
import cv2
import multiprocessing

from guiLoop import guiLoop

master = Tk()

thresh_value = 0

PATH = "/home/lab/Downloads/MECLO_C_M_26_83.avi.avi"
cap = cv2.VideoCapture(PATH)

@guiLoop
def thread_function():
    while(cap.isOpened()):
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.medianBlur(gray, 3)
        
        ret, thresh = cv2.threshold(gray, thresh_value, 255, cv2.THRESH_BINARY_INV)
        print(thresh_value)

        cv2.imshow('frame', thresh)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

thread_function(master)

def getThrottle(event):
    thresh_value.value = Throttle.get()
    print(thresh_value)

Throttle = Scale(master, from_=0, to=254, orient=HORIZONTAL, command=getThrottle)
Throttle.set(0)
Throttle.pack()

master.mainloop()