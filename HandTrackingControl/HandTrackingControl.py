"""
    Documentation https://google.github.io/mediapipe/solutions/hands.html
"""

import cv2
import mediapipe as mp
import time
import math

cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

#Variables
ix = 0
iy = 0
tx = 0
ty = 0
volBar = 0

#FPS variables
pTime = 0
cTime = 0

while True:
    res, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) #convert to rgb for mphands function
    results = hands.process(imgRGB)
    #print(results.multi_hand_landmarks)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks: #For each hand found
            for id, lm in enumerate(handLms.landmark): #For all landmark positions
                #print(id, lm)
                h,w,c = img.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                #print(id, cx, cy)
                if id == 4: #Index finger point
                    cv2.circle(img, (cx,cy), 15, (255,0,0), 3)
                    tx = cx #thumb x
                    ty = cy #thumb y

                if id == 8: #Index finger point
                    cv2.circle(img, (cx,cy), 15, (255,0,0), 3)
                    ix = cx #index x
                    iy = cy #index y

                if ix != 0 and iy != 0 and tx != 0 and ty != 0:
                    cv2.line(img, (ix, iy), (tx, ty), (255,0,0), 3)
                    distance = math.sqrt(abs(ty-iy)**2 + abs(tx-ix)**2)
                    cv2.putText(img, str(int(distance)), (500, 70), cv2.FONT_HERSHEY_PLAIN, 3, (0,255,0), 3)
                    if(distance < 30):
                        cv2.circle(img, (int((ix + tx) / 2), int((iy + ty) / 2)), 10, (0, 0, 255), cv2.FILLED)
                        volBar = 400
                    else:
                        cv2.circle(img, (int((ix + tx) / 2), int((iy + ty) / 2)), 10, (255, 0, 0), cv2.FILLED)
                        if distance > 230:
                            volBar = 150
                        else:
                            volBar = 400 - distance

                    cv2.rectangle(img, (50, 150), (85, 400), (0, 255, 0), 3)
                    # 150 - 400
                    cv2.rectangle(img, (50, int(volBar)), (85,400), (0,255,0), cv2.FILLED)
                    #cv2.rectangle(img, (50, 150), (85, 400), (0, 255, 0), cv2.FILLED)

                    print(distance)
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

    #FPS Calculation
    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime

    #Display FPS
    cv2.putText(img, str(int(fps)),(10,70), cv2.FONT_HERSHEY_PLAIN, 3, (0,255,0), 3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)

    """
    TODO:
        * Link to computer volume using pycaw
        * Functionize remove DRY code
    """