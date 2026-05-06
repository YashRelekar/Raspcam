#!/usr/bin/env python3
"""
emotion_detection.py

Runs real-time emotion detection from an IMX219 camera attached to cam0
on a Raspberry Pi 5.

Each video frame is captured with picamera2, passed through the FER
(Facial Expression Recognition) detector, and the dominant emotion + its
confidence score are drawn on the frame before it is shown in an OpenCV
preview window.

Press 'q' or Ctrl+C to quit.

Dependencies
------------
    sudo apt install -y python3-picamera2 python3-opencv
    pip install fer tensorflow
"""

import signal
import sys

import cv2
from fer import FER
from picamera2 import Picamera2

# Preview window dimensions
FRAME_WIDTH = 640
FRAME_HEIGHT = 480


def draw_emotion_overlay(frame, emotion_results):
    """Draw bounding boxes and emotion labels on *frame* (in-place).

    Parameters
    ----------
    frame : numpy.ndarray
        BGR image array that will be annotated.
    emotion_results : list[dict]
        Output from ``FER.detect_emotions()``.  Each element contains a
        ``"box"`` (x, y, w, h) and an ``"emotions"`` dict mapping emotion
        names to confidence scores.
    """
    for result in emotion_results:
        x, y, w, h = result["box"]

        # Pick the dominant emotion
        emotions = result["emotions"]
        dominant_emotion = max(emotions, key=emotions.get)
        confidence = emotions[dominant_emotion]

        emotion_label = f"{dominant_emotion}: {confidence:.0%}"

        # Bounding box around the face
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Label background for readability
        label_y = y - 10 if y - 10 > 10 else y + h + 20
        (text_w, text_h), _ = cv2.getTextSize(emotion_label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)
        cv2.rectangle(frame, (x, label_y - text_h - 4), (x + text_w, label_y + 4), (0, 255, 0), cv2.FILLED)
        cv2.putText(frame, emotion_label, (x, label_y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)


def main():
    # Initialise picamera2
    picam2 = Picamera2(camera_num=0)

    # Request RGB888 output so OpenCV / FER can process it directly
    config = picam2.create_preview_configuration(
        main={"format": "RGB888", "size": (FRAME_WIDTH, FRAME_HEIGHT)}
    )
    picam2.configure(config)
    picam2.start()

    print("Emotion detection started.  Press 'q' or Ctrl+C to stop.")

    # Initialise FER detector (MTCNN gives better face detection accuracy)
    detector = FER(mtcnn=True)

    def _stop(signum, frame):
        print("\nStopping emotion detection...")
        picam2.stop()
        cv2.destroyAllWindows()
        sys.exit(0)

    signal.signal(signal.SIGINT, _stop)
    signal.signal(signal.SIGTERM, _stop)

    while True:
        # Capture a frame as a NumPy array (RGB)
        frame_rgb = picam2.capture_array()

        # FER works on RGB; OpenCV imshow expects BGR — keep one copy of each
        frame_bgr = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)

        # Detect emotions (runs face detection + expression classification)
        emotion_results = detector.detect_emotions(frame_rgb)

        # Annotate the BGR copy
        draw_emotion_overlay(frame_bgr, emotion_results)

        # Show the annotated frame
        cv2.imshow("Emotion Detection — Raspberry Pi 5", frame_bgr)

        # Exit on 'q' key
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    picam2.stop()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
