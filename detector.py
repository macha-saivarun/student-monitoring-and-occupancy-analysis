# detector.py
from ultralytics import YOLO

# Load pre-trained model
model = YOLO("yolov8n.pt")  # Or yolov8s.pt, yolov8m.pt depending on performance needs

def detect_people(frame):
    results = model(frame, verbose=False)
    people = []

    for r in results:
        for box in r.boxes:
            cls = int(box.cls[0])
            if cls == 0:  # Class 0 = person
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                people.append((x1, y1, x2 - x1, y2 - y1))

    return people
