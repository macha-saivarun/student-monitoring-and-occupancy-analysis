# utils.py
import cv2

def draw_boxes(frame, people):
    for (x, y, w, h) in people:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    return frame
