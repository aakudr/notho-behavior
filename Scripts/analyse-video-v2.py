import cv2
import numpy as np

PATH = "/home/lab/Downloads/MECLO_C_M_26_83.avi.avi"

def init_capture(path):
    cap = cv2.VideoCapture(path)
    return cap

def read_thresh_frame(cap, thresh_value):
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, thresh_value, 255, cv2.THRESH_BINARY_INV)
    return thresh

def create_circular_mask(h, w, center=None, radius=None):
    if center is None: # use the middle of the image
        center = (int(w/2), int(h/2))
    if radius is None: # use the smallest distance between the center and image walls
        radius = min(center[0], center[1], w-center[0], h-center[1])

    Y, X = np.ogrid[:h, :w]
    dist_from_center = np.sqrt((X - center[0])**2 + (Y-center[1])**2)

    mask = dist_from_center <= radius
    return mask

def cut_circle(frame, mask_radius):
    h, w = frame.shape[:2]
    mask = create_circular_mask(h, w, radius=int(h / mask_radius))
    masked_frame = frame.copy()
    masked_frame[~mask] = 0
    return masked_frame

c = init_capture(PATH)

while c.isOpened():

    frame = read_thresh_frame(c, 110)
    frame = cut_circle(frame, 2.3)

    cv2.imshow(PATH, frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break