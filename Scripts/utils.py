import math
import datetime
import numpy as np
import cv2
import time

def get_distance(x, y, xc, yc):
    return math.floor((((xc - x )**2) + ((yc-y)**2) )**0.5)

def millis(start_time):
   return int((datetime.datetime.now() - start_time).total_seconds() * 1000)

def create_circular_mask(h, w, center=None, radius=None):
    if center is None: # use the middle of the image
        center = (int(w/2), int(h/2))
    if radius is None: # use the smallest distance between the center and image walls
        radius = min(center[0], center[1], w-center[0], h-center[1])

    Y, X = np.ogrid[:h, :w]
    dist_from_center = np.sqrt((X - center[0])**2 + (Y-center[1])**2)

    mask = dist_from_center <= radius
    return mask

def get_angle(a, b, c):
    ang = math.degrees(math.atan2(c[1]-b[1], c[0]-b[0]) - math.atan2(a[1]-b[1], a[0]-b[0]))
    return ang + 360 if ang < 0 else ang

def get_ref_values(points):
    ref_values = []
    threshold = 4 
    angle = get_angle(points[-2], points[-1], points[0])
    if angle < threshold or angle > 360 - threshold:
        ref_values.append(len(points)-1)
    angle = get_angle(points[-1], points[0], points[1])
    if angle < threshold or angle > 360 - threshold:
        ref_values.append(0)

    for i in range(len(points)-2):
        angle = get_angle(points[i], points[i+1], points[i+2])
        if angle < threshold or angle > 360 - threshold:
            ref_values.append(i)
    return ref_values

def get_circles(frame):
    circles = cv2.HoughCircles(frame, cv2.HOUGH_GRADIENT, 2, 1000,
              param1=30,
              param2=15,
              minRadius=80,
              maxRadius=240)

    circles = np.uint16(np.around(circles))

    cx = circles[0][0][0]
    cy = circles[0][0][1]
    cr = circles[0][0][2]
    
    return [cx, cy, cr]


def analyse_skeletons(data, last_points, cnt):
    ref_values = get_ref_values(data)
    print(ref_values)

    if len(ref_values) == 1:
        head = last_points[0][0]
        tail = last_points[1][0]
        point = data[ref_values[0]]
        head_proximity = get_distance(point[0], point[1], head[0], head[1])
        tail_proximity = get_distance(point[0], point[1], tail[0], tail[1]) 

    if cnt > 2 and len(ref_values) > 2:
        head = last_points[0][0]
        tail = last_points[1][0]
        head_proximity = {}
        tail_proximity = {}
        for value in ref_values:
            point = data[value]
            head_proximity[value] = get_distance(head[0], head[1], point[0], point[1]) 
            tail_proximity[value] = get_distance(tail[0], tail[1], point[0], point[1]) 
        temp = min(head_proximity.values())
        res_head = [key for key in head_proximity if head_proximity[key] == temp]
        temp = min(tail_proximity.values())
        res_tail = [key for key in tail_proximity if tail_proximity[key] == temp]
        ref_values = [res_head[0], res_tail[0]]
        print(ref_values)
        # time.sleep(4)
    # temporary code for testing the output points
    out_contour = []
    for value in ref_values:
        a = []
        a.append(data[value])
        out_contour.append(a)
    out_contour = np.array(out_contour)
    print(out_contour)
    return out_contour
