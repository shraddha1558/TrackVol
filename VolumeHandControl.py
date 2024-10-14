import cv2
import time
import numpy as np
import HandTrackModule as htm
import math
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

wCam, hCam = 640, 480

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0


detector = htm.handDetector(detectionCon=0.75)

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)

volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]
vol = 0
volBar = 400
volPer = 0

colors = {
    "low": (255, 69, 0),      # Red-Orange
    "medium": (255, 215, 0),  # Gold
    "high": (0, 128, 0),      # Green
    "bar_border": (211, 211, 211),  # Light Gray for border
}

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)

    volBar_color = colors["high"] 

    if len(lmList) != 0:  
        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
 
        if volPer < 30:
            dot_color = colors["low"]  # Red-Orange for low volume
            volBar_color = colors["low"]  # Red-Orange for low volume
        elif volPer < 70:
            dot_color = colors["medium"]  # Gold for medium volume
            volBar_color = colors["medium"]  # Gold for medium volume
        else:
            dot_color = colors["high"]  # Green for high volume
            volBar_color = colors["high"]  # Green for high volume

        # Draw hand landmarks
        cv2.circle(img, (x1, y1), 15, dot_color, cv2.FILLED)
        cv2.circle(img, (x2, y2), 15, dot_color, cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), dot_color, 3)
        cv2.circle(img, (cx, cy), 15, dot_color, cv2.FILLED)
        
        length = math.hypot(x2 - x1, y2 - y1)

        vol = np.interp(length, [20, 350], [minVol, maxVol])
        volBar = np.interp(length, [20, 350], [400, 150])
        volPer = np.interp(length, [30, 400], [0, 100])

        print(int(length), vol)
        volume.SetMasterVolumeLevel(vol, None)
        
        if length < 50:
            cv2.circle(img, (cx, cy), 15, colors["low"], cv2.FILLED)
            
    # Draw a volume bar
    cv2.rectangle(img, (50, 150), (85, 400), colors["bar_border"], 3)  # Border 
    cv2.rectangle(img, (50, int(volBar)), (85, 400), volBar_color, cv2.FILLED)  
    cv2.putText(img, f'{int(volPer)}%', (40, 450), cv2.FONT_HERSHEY_COMPLEX, 1, colors["bar_border"], 3)
    
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    
    cv2.putText(img, f'FPS: {int(fps)}', (40, 50), cv2.FONT_HERSHEY_COMPLEX, 1, colors["bar_border"], 3)
    
    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
