# Real-Time Object Detection & Tracing

A Streamlit web app that uses YOLOv8 to detect and track objects from a live webcam feed in real time. The app lets you choose a target object, adjust the detection confidence threshold, and optionally save alert snapshots when the selected object appears.

## Features

- Live webcam object detection in the browser
- YOLOv8 object tracking with bounding boxes
- Selectable target object alerts
- Adjustable confidence threshold
- Optional auto-save for detected target snapshots
- Saved detections are stored in the `detections/` folder

## Project Files

```text
.
+-- app.py              # Main Streamlit application
+-- requirements.txt    # Python dependencies
+-- packages.txt        # System packages for deployment
+-- yolov8n.pt          # YOLOv8 nano model weights
+-- detections/         # Auto-saved alert images
```

## Requirements

- Python 3.10 or newer recommended
- Webcam access
- A modern browser

## Installation

1. Create and activate a virtual environment:

```bash
python -m venv .venv
```

On Windows PowerShell:

```bash
.venv\Scripts\Activate.ps1
```

2. Install the dependencies:

```bash
pip install -r requirements.txt
```

## Running the App

Start the Streamlit server:

```bash
streamlit run app.py
```

Then open the local URL shown in the terminal, usually:

```text
http://localhost:8501
```

Allow camera access when your browser asks for permission.

## How to Use

1. Choose a target object from the dropdown.
2. Adjust the confidence slider if needed.
3. Enable **Auto-Save** if you want snapshots saved when the target object is detected.
4. Start the webcam stream and point your camera at objects.

When the selected object appears, the app displays an alert on the video feed. If auto-save is enabled, snapshots are saved inside `detections/`.

## Notes

- The app uses `yolov8n.pt`, the lightweight YOLOv8 nano model.
- Detection performance depends on your camera, lighting, hardware, and confidence threshold.
- For deployment platforms such as Streamlit Community Cloud, `packages.txt` provides required Linux system packages.

## Troubleshooting

If the webcam does not start:

- Make sure the browser has camera permission.
- Close other apps that may be using the webcam.
- Try refreshing the page.

If dependencies fail to install:

- Upgrade pip:

```bash
python -m pip install --upgrade pip
```

- Then run:

```bash
pip install -r requirements.txt
```
