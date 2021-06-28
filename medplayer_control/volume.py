import cv2
import time
import os
import numpy as np
import pyautogui
import hand_module as hm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

pTime = 0
cTime = 0
cap = cv2.VideoCapture(0)
detector = hm.handDetector(detectionCon=0.75)

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
vol=volume.GetVolumeRange()
minVol=vol[0]
maxVol=vol[1]

tipIds=[4,8,12,16,20]

while True:
    success, img = cap.read()
    img = detector.detect_hand(img, draw=True )
    lmList = detector.findPosition(img, draw=False)
    if len(lmList) != 0:
        #pause a video if no of fingers 0
        fingers = []

        # Thumb
        if lmList[tipIds[0]][2] < lmList[tipIds[0] + 1][2]:
            fingers.append(1)
        else:
            fingers.append(0)
        # 4 Fingers
        for id in range(1, 5):
            if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        #print the no of fingers
        totalFingers = fingers.count(1)
        #functionality-1 pause or resume
        if(totalFingers==1):
            cv2.putText(img, 'Play/Pause', (40, 450), cv2.FONT_HERSHEY_COMPLEX,1, (255, 0, 0), 3)
            pyautogui.press('space')
        
        #functionality-1 Volume up and down
        else:
            x1, y1 = lmList[4][1], lmList[4][2]
            x2, y2 = lmList[8][1], lmList[8][2]
            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

            cv2.circle(img, (x1, y1), 5, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 5, (255, 0, 255), cv2.FILLED)
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 1)
            cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)
            #distance between thumb tip and index tip
            length = math.hypot(x2 - x1, y2 - y1)
            #print(length)
            #convert length to volume (25-200) to (-96 - 0)
            set_vol=np.interp(length,[25,200],[minVol,maxVol])
            volume.SetMasterVolumeLevel(set_vol, None)
            #create a volume bar
            volBar = np.interp(length, [25,200], [400, 150])
            volPer = np.interp(length, [25,200], [0, 100])
            
            
            if length < 20:
                cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)
            
            cv2.rectangle(img, (50, 150), (85, 400), (255, 0, 0), 3)
            cv2.rectangle(img, (50, int(volBar)), (85, 400), (255, 0, 0), cv2.FILLED)
            cv2.putText(img, f'{int(volPer)} %', (40, 450), cv2.FONT_HERSHEY_COMPLEX,1, (255, 0, 0), 3)
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    
    #print fps
    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                (255, 0, 255), 3)

    if cv2.waitKey(1) == ord("q"):
        break
    cv2.imshow("Image", img)
    
cap.release()
cv2.destroyAllWindows()