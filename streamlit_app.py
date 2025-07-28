import streamlit as st
import cv2
import numpy as np
from ultralytics import YOLO
from PIL import Image

# Constants
FRAME_WIDTH = 1920
FRAME_HEIGHT = 1080
ZONE_CAPACITY = 10
NUM_ZONES = 4
ZONE_WIDTH = FRAME_WIDTH // 2
ZONE_HEIGHT = FRAME_HEIGHT // 2

# Define 4 zones (1-indexed)
ZONES = {
    1: {"x": 0, "y": 0, "w": ZONE_WIDTH, "h": ZONE_HEIGHT},
    2: {"x": ZONE_WIDTH, "y": 0, "w": ZONE_WIDTH, "h": ZONE_HEIGHT},
    3: {"x": 0, "y": ZONE_HEIGHT, "w": ZONE_WIDTH, "h": ZONE_HEIGHT},
    4: {"x": ZONE_WIDTH, "y": ZONE_HEIGHT, "w": ZONE_WIDTH, "h": ZONE_HEIGHT},
}

# Load YOLOv8
model = YOLO("yolov8n.pt")  # Replace with your trained model if needed

# Streamlit UI
st.set_page_config(layout="wide")
st.title("🎥 Person Detection & Zone Occupancy Dashboard")

source_type = st.radio("Select Input Source:", ("Webcam", "Offline Video"))

video_path = None
if source_type == "Offline Video":
    uploaded_file = st.file_uploader("Upload Video", type=["mp4", "avi", "mov"])
    if uploaded_file:
        video_path = uploaded_file.name
        with open(video_path, "wb") as f:
            f.write(uploaded_file.read())

frame_display = st.empty()
zone_metrics = st.empty()
alert_area = st.empty()

# Helper: point inside zone
def point_in_zone(x, y, zone):
    return zone["x"] <= x <= zone["x"] + zone["w"] and zone["y"] <= y <= zone["y"] + zone["h"]

# Frame processing
def process_frame(frame):
    results = model(frame)[0]
    detections = []

    for box in results.boxes:
        cls = int(box.cls[0])
        if model.names[cls] == 'person':
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            bbox_w = x2 - x1
            bbox_h = y2 - y1
            cx = x1 + bbox_w // 2
            cy = y1 + bbox_h // 2
            area = bbox_w * bbox_h
            detections.append({"bbox": (x1, y1, x2, y2), "center": (cx, cy), "area": area})

    # Zone metrics
    zone_counts = {i: 0 for i in ZONES}
    zone_areas = {i: 0 for i in ZONES}

    for det in detections:
        cx, cy = det["center"]
        for i, zone in ZONES.items():
            if point_in_zone(cx, cy, zone):
                zone_counts[i] += 1
                zone_areas[i] += det["area"]
                break

    # Draw zones
    for i, zone in ZONES.items():
        cv2.rectangle(frame, (zone["x"], zone["y"]),
                      (zone["x"] + zone["w"], zone["y"] + zone["h"]), (0, 255, 0), 2)
        cv2.putText(frame, f"Zone {i}", (zone["x"] + 10, zone["y"] + 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Draw person boxes
    for det in detections:
        x1, y1, x2, y2 = det["bbox"]
        cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)

    return frame, zone_counts, zone_areas

# Start video
if (source_type == "Webcam") or (source_type == "Offline Video" and video_path):
    cap = cv2.VideoCapture(0 if source_type == "Webcam" else video_path)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            st.warning("End of video stream." if source_type == "Offline Video" else "Failed to grab frame.")
            break

        frame = cv2.resize(frame, (FRAME_WIDTH, FRAME_HEIGHT))
        processed_frame, counts, areas = process_frame(frame)

        # Compute metrics
                # Compute metrics
        table_data = []
        alerts = []

        for i in range(1, NUM_ZONES + 1):
            headcount = counts[i]
            occupancy = (headcount / ZONE_CAPACITY) * 100
            zone_area = ZONE_WIDTH * ZONE_HEIGHT
            area_pct = (areas[i] / zone_area) * 100

            # Determine status
            if headcount > ZONE_CAPACITY:
                status = "Overcrowded"
                alerts.append(f"⚠️ Overcrowding in Zone {i} ({headcount} people)")
            elif occupancy >= 90:
                status = "Nearly full"
            elif occupancy <= 30:
                status = "Underutilized"
            else:
                status = "Available space"

            if headcount < 2:
                alerts.append(f"⚠️ Low activity in Zone {i}")

            table_data.append({
                "Zone": f"Zone {i}",
                "Capacity": ZONE_CAPACITY,
                "Headcount": headcount,
                "Occupancy %": f"{occupancy:.0f}%",
                "Area Occupied %": f"{area_pct:.0f}%",
                "Status": status
            })

        # Update dashboard
               # Layout for video + table side-by-side
        col1, col2 = st.columns([2, 1])

        with col1:
            frame_rgb = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)
            frame_display.image(frame_rgb, channels="RGB", use_container_width=True)

        with col2:
            zone_metrics.dataframe(table_data, use_container_width=True)
            alert_area.warning("  \n".join(alerts) if alerts else "✅ All zones are within safe limits.")

