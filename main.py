from ultralytics import YOLO
import cv2

model = YOLO("yolov8n.pt")  # Replace with your model path if needed

def process_frame(frame):
    results = model(frame)[0]
    boxes = []
    zones = [0, 0, 0, 0]  # Zone 1 (Top-Left), 2 (Top-Right), 3 (Bottom-Left), 4 (Bottom-Right)

    height, width, _ = frame.shape

    for box in results.boxes.xyxy:
        x1, y1, x2, y2 = map(int, box[:4])
        x_center = (x1 + x2) // 2
        y_center = (y1 + y2) // 2
        boxes.append((x1, y1, x2, y2))

        # Determine zone based on center point
        if x_center < width // 2 and y_center < height // 2:
            zones[0] += 1  # Zone 1
        elif x_center >= width // 2 and y_center < height // 2:
            zones[1] += 1  # Zone 2
        elif x_center < width // 2 and y_center >= height // 2:
            zones[2] += 1  # Zone 3
        else:
            zones[3] += 1  # Zone 4

    return zones, boxes
