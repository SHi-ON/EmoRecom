# EmoRecom
Real‑time facial emotion detection with a Flask UI plus location recommendations backed by Google Places.

## What it does
- Captures webcam frames, detects faces, and classifies emotions with a trained Xception mini model.
- Streams the camera feed and a scoreboard overlay through Flask endpoints (`/video_feed`, `/video_feed1`).
- Stores the dominant emotion so downstream logic can tailor recommendations.
- Finds nearby places (gym, cinema, bar, restaurant, etc.) using Google Places based on the detected emotion.

## Requirements
- Python 3.7+
- Access to a webcam and OpenCV video support.
- Pip packages: `flask`, `keras`, `tensorflow` (or `tensorflow-cpu`), `opencv-python`, `imutils`, `numpy`, `googlemaps`, `googleplaces`, `requests`.
- Model files present:
  - `models/face_hyperparams.xml` (face detector)
  - `models/Xception_mini106.hdf5` (emotion classifier for the Flask app)
  - `fer_engine/models/_mini_XCEPTION.106-0.65.hdf5` (emotion classifier for the standalone demo)
  Placeholders are already in the repo; replace them with the trained weights if needed.

## Setup
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install flask keras tensorflow opencv-python imutils numpy googlemaps googleplaces requests
```

## Run the Flask app
```bash
python server.py
```
Then open `http://127.0.0.1:5000/start` in a browser. Routes of note:
- `/video_feed` – camera stream with bounding box and label
- `/video_feed1` – emotion scoreboard stream
- `/map` – kicks off place recommendations based on the current emotion

## Standalone demo (no Flask)
```bash
python fer_engine/real_time_classifier.py
```
This opens a window with the webcam feed and emotion probabilities until you press `q`.

## Notes
- A Google Places API key is required for map suggestions; the code currently reads a hardcoded key in `server.py`. Replace it with your key before using in production.
- If the camera does not open, ensure another process is not using it and that `cv2.VideoCapture(0)` matches your device index.
