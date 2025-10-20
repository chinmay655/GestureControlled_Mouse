# 🖱️ AI Virtual Mouse (Enhanced)

Control your computer using hand gestures with real-time webcam input.
This enhanced version includes:
- Move cursor with index finger
- Left click (index + thumb)
- Right click (middle + thumb)
- Drag & drop (index + middle)
- Volume control (pinch distance mapped to volume level; uses pycaw on Windows if available)
- Screenshot gesture (three fingers together)

## Features
- Uses OpenCV + Mediapipe for hand tracking
- Uses PyAutoGUI for controlling cursor and clicks
- Modular code with src/ modules for clarity
- Configurable thresholds in src/utils.py

## Requirements
See `requirements.txt` for Python packages. For full volume control on Windows, install `pycaw`:
```bash
pip install -r requirements.txt
# Optional (Windows only) for better volume control:
pip install pycaw
```

## Run
```bash
python src/main.py
```

## Notes
- Works best in good lighting with a simple background.
- If volume control doesn't work on your OS, the code falls back to printing volume changes.
- Press `ESC` to exit.

