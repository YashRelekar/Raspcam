#!/usr/bin/env python3
"""
camera_preview.py

Displays a live camera feed from an IMX219 camera attached to cam0
on a Raspberry Pi 5.  Run this script and press Ctrl+C to stop.

Ported from https://github.com/YashRelekar/Cam5Raspi
"""

import signal
import sys

from picamera2 import Picamera2
from picamera2.previews import QtPreview


def main():
    # Open the camera on index 0 (cam0 / IMX219)
    picam2 = Picamera2(camera_num=0)

    # Build a preview configuration (full-colour, default resolution)
    config = picam2.create_preview_configuration()
    picam2.configure(config)

    # Start the Qt-based preview window
    picam2.start_preview(QtPreview())
    picam2.start()

    print("Camera preview started.  Press Ctrl+C to stop.")

    # Signal handler – defined here so it can close the picam2 instance
    # that was opened above.
    def _stop(signum, frame):
        print("\nStopping camera preview...")
        picam2.stop_preview()
        picam2.stop()
        sys.exit(0)

    signal.signal(signal.SIGINT, _stop)
    signal.signal(signal.SIGTERM, _stop)

    # Block the main thread, waiting for SIGINT (Ctrl+C) or SIGTERM.
    signal.pause()


if __name__ == "__main__":
    main()
