# Raspcam

Real-time **emotion detection** and **camera preview** scripts for the
Raspberry Pi 5, using an IMX219 camera module connected to **cam0**.

---

## Scripts

### `camera_preview.py`

Displays a live Qt-based preview window from the camera.  Ported from
[YashRelekar/Cam5Raspi](https://github.com/YashRelekar/Cam5Raspi).

### `emotion_detection.py`

Captures frames via `picamera2`, detects facial expressions with the
[FER](https://github.com/justinshenk/fer) library, and shows an annotated
OpenCV preview window with bounding boxes and dominant emotion labels in
real time.

---

## Requirements

| Requirement | Notes |
|---|---|
| Raspberry Pi 5 | Any memory variant |
| IMX219 camera module | Connected to the **cam0** ribbon-cable connector |
| Raspberry Pi OS (Bookworm or later) | 64-bit recommended |
| `picamera2` | `sudo apt install -y python3-picamera2` |
| OpenCV | `sudo apt install -y python3-opencv` |
| Qt display libraries | `sudo apt install -y python3-pyqt5` (needed for `camera_preview.py`) |
| `fer` + `tensorflow` | `pip install fer tensorflow` |

### Install all dependencies

```bash
# System packages
sudo apt install -y python3-picamera2 python3-opencv python3-pyqt5

# Python packages
pip install fer tensorflow
# or using the requirements file:
pip install -r requirements.txt
```

---

## Usage

### Camera preview (Qt window)

```bash
python3 camera_preview.py
```

Press **Ctrl+C** in the terminal to close the window.

### Emotion detection (OpenCV window)

```bash
python3 emotion_detection.py
```

Press **`q`** in the preview window, or **Ctrl+C** in the terminal, to stop.