import cv2

PATH = "home/lab/Downloads/MECLO_C_M_26_83.avi.avi"

def init_capture(path):
    cap = cv2.VideoCapture(path)
    return cap

def read_thresh_frame(cap, thresh_value):
    ret, frame = cap.read()
    ret, thresh = cv2.threshold(frame, thresh_value, 255, cv2.THRESH_BINARY_INV)
    return thresh

while(cap.isOpened()):
    c = init_capture(PATH)
    while c.isOpened():
        frame = read_thresh_frame(c, 110)
        cv2.imshow(PATH, frame)
        
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break