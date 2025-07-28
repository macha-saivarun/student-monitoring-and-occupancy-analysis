🧠 Zone-wise Real-Time People Detection & Occupancy Dashboard
A real-time computer vision dashboard built with YOLOv8, OpenCV, and Streamlit to detect people in live video streams or offline videos, divide the frame into four zones, and calculate zone-specific headcount, occupancy %, area occupied %, and status. Ideal for monitoring crowd density, social distancing, or managing room capacities.

📸 Features
✅ YOLOv8-powered Person Detection

✅ Real-time or offline video feed support (webcam or uploaded file)

✅ Automatic zone detection (frame divided into 4 equal quadrants)

✅ Zone-wise:

🔢 Headcount

📊 Occupancy %

🟫 Area Occupied %

🟢 Status (Underutilized, Nearly Full, Overcrowded, etc.)

✅ Live analytics table

✅ Custom alerts for:

🚨 Overcrowding (when people > 10)

⚠️ Low activity (people < 2)

📐 Zone Calculations
Each frame is split into 4 equal zones:

Metric	Formula Description
Headcount	Count of detected persons per zone
Occupancy %	(Headcount / Zone Capacity) * 100
Area Occupied	(Sum of bounding box areas for people / Zone area) * 100
Status	Logic based on thresholds for occupancy and area (%): e.g., Underutilized, Full

🛠 Tech Stack
Tech	Purpose
YOLOv8	Object detection (person)
OpenCV	Video processing
Streamlit	Interactive dashboard
NumPy	Mathematical computations
Pillow	Image rendering

▶️ How to Run
1. Install dependencies
bash
Copy
Edit
pip install -r requirements.txt
or individually:

bash
Copy
Edit
pip install streamlit opencv-python ultralytics pillow
2. Run the app
bash
Copy
Edit
streamlit run streamlit_app.py
⚠️ If streamlit is not recognized, try:

bash
Copy
Edit
python -m streamlit run streamlit_app.py
3. Choose Video Source
📷 Webcam

📁 Upload a local video file (MP4, AVI, etc.)

📊 Example Analytics Table
Zone	Capacity	Headcount	Occupancy %	Area Occupied %	Status
Zone 1	10	9	90%	72%	Nearly full
Zone 2	10	2	20%	12%	Underutilized
Zone 3	10	11	110%	95%	Overcrowded
Zone 4	10	4	40%	38%	Moderate

📁 Project Structure
bash
Copy
Edit
📦 person-detection-dashboard
├── streamlit_app.py         # Main Streamlit app
├── requirements.txt         # Python dependencies
├── yolov8n.pt               # YOLOv8 model weights (optional or download at runtime)
└── README.md                # Project documentation
🚀 Use Cases
Crowd control in public areas

Smart surveillance systems

Event or conference room monitoring

Workspace utilization analytics

📌 Future Improvements
Custom zone drawing (manual ROI)

Heatmap visualization

Export reports (CSV/Excel)

Multi-camera support

🧑‍💻 Author
SAI VARUN MACHA
