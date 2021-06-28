import cv2
import time
import os
import hand_module as hm


pTime = 0
cTime = 0
cap = cv2.VideoCapture(0)
detector = hm.handDetector()

#finger tip ids
tipIds = [4, 8, 12, 16, 20]
while True:
    success, img = cap.read()
    img = detector.detect_hand(img, draw=True )
    lmList = detector.findPosition(img, draw=False)
    if len(lmList) != 0:
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
        cv2.rectangle(img, (20, 225), (170, 425), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, str(totalFingers), (45, 375), cv2.FONT_HERSHEY_PLAIN,
                    10, (255, 0, 0), 25)
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