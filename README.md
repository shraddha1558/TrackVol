# TrackVol

**TrackVol** is a Python-based application that enables system volume control using hand gestures. By utilizing OpenCV for hand tracking and Pycaw for audio interface control, the project allows you to adjust the volume dynamically based on finger positions. It also includes enhanced visual feedback through images for a polished user experience.

## Project Structure

- **VolumeHandControl.py**: This script provides the basic implementation of volume control using hand gestures. It uses OpenCV to detect hand landmarks and adjusts the system volume based on the distance between the thumb and index finger.

- **HandTrackModule.py**: A helper module that simplifies the implementation of hand tracking using the Mediapipe library. It facilitates easy detection and tracking of hand landmarks.

- **EnhancedVolumeControl.py**: An enhanced version of the volume control, which includes images to indicate high (loud) and low volume, along with smoother visual elements.

- **loud.jpg**: An image file used to visually represent high volume.

- **low.png**: An image file used to represent low volume.

## How It Works

- **Hand Gesture Control**: The application detects the position of the thumb and index finger using OpenCV. The distance between the fingers determines the volume: 
  - The closer the fingers, the lower the volume.
  - The further the fingers, the higher the volume.
  
- **Volume Bar**: A real-time dynamic volume bar is displayed on the screen, which changes its color and size based on the current volume level.

- **Visual Feedback**: For better clarity, images for "Loud" and "Low" volume levels are displayed, giving immediate feedback about the sound intensity.

## Requirements

- Python 3.x
- OpenCV
- Mediapipe
- Pycaw
- Numpy
- Comtypes

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/TrackVol.git
   cd TrackVol
