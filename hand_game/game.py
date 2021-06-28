import cv2
import time
import os
import hand_module as hm
import random

pTime = 0
cTime = 0
wCam, hCam = 640, 480

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
detector = hm.handDetector(detectionCon=0.6)

#computer moves images
folderPath = "com_move"
myList = os.listdir(folderPath)
overlayList = []
for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}')    #0-stone 1-paper 2-scissor
    # print(f'{folderPath}/{imPath}')
    overlayList.append(image)
#finger tip ids
tipIds = [4, 8, 12, 16, 20]

while True:
    success, img = cap.read()
    img = detector.detect_hand(img, draw=True )
    lmList = detector.findPosition(img, draw=False)
    if(len(lmList)!=0):
        compMoveid = random.randint(0, len(overlayList)-1)
        compMove = overlayList[compMoveid]
        h, w, c = compMove.shape
        #print(h,w)
        img[0:h,0:w]=compMove
        fingers=[]
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

        #print the computer moves depending upon no of fingers
        if(compMoveid==0):
            cv2.putText(img, "STONE", (10, 270), cv2.FONT_HERSHEY_PLAIN, 3,
                (0, 0, 255), 3)
        if(compMoveid==1):
            cv2.putText(img, "PAPER", (10, 270), cv2.FONT_HERSHEY_PLAIN, 3,
                (0, 0, 255), 3)
        if(compMoveid==2):
            cv2.putText(img, "SCISSOR", (10, 270), cv2.FONT_HERSHEY_PLAIN, 3,
                (0, 0, 255), 3)

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