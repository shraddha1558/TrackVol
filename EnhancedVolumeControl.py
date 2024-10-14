import cv2
import time
import numpy as np
import HandTrackModule as htm
import math
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# Camera settings
wCam, hCam = 640, 480

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0

# Initialize hand detector
detector = htm.handDetector(detectionCon=0.75)

# Get audio volume settings
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]
vol = 0
volBar = 400
volPer = 0


loud = cv2.imread('loud.jpg')  # Add your loud icon image path
low = cv2.imread('low.png')  # Add your soft icon image path
loud = cv2.resize(loud, (100, 100))
low = cv2.resize(low, (100, 100))
# Cartoon icons for volume indication
loud_icon = cv2.imread('loud.jgp')  # Add your loud icon image path
soft_icon = cv2.imread('low.png')  # Add your soft icon image path

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)

    if len(lmList) != 0:
        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        # Draw hands
        cv2.circle(img, (x1, y1), 20, (255, 105, 180), cv2.FILLED)  # Light pink
        cv2.circle(img, (x2, y2), 20, (255, 105, 180), cv2.FILLED)  # Light pink
        cv2.line(img, (x1, y1), (x2, y2), (255, 105, 180), 4)  # Light pink
        cv2.circle(img, (cx, cy), 20, (255, 105, 180), cv2.FILLED)  # Light pink

        # Calculate length and volume
        length = math.hypot(x2 - x1, y2 - y1)
        vol = np.interp(length, [20, 400], [minVol, maxVol])
        volBar = np.interp(length, [20, 400], [400, 150])
        volPer = np.interp(length, [20, 400], [0, 100])

        # Set system volume
        volume.SetMasterVolumeLevel(vol, None)

        # Change color to red if close
        if length < 50:
            cv2.circle(img, (cx, cy), 20, (0, 0, 255), cv2.FILLED)  # Red for close

    # Draw volume bar
    cv2.rectangle(img, (50, 150), (85, 400), (255, 140, 0), 3)  # Orange border
    cv2.rectangle(img, (50, int(volBar)), (85, 400), (0, 255, 0), cv2.FILLED)  # Green fill
    cv2.putText(img, f'{int(volPer)}%', (40, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 3)

    # Display cartoon icon based on volume
    if volPer > 50:
        img[50:150, 400:500] = loud  # Position the loud icon
    else:
        img[50:150, 400:500] = low  # Position the soft icon

    # Frame rate calculation
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    # Display FPS
    cv2.putText(img, f'FPS: {int(fps)}', (40, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 3)

    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
