"""
    Documentation https://google.github.io/mediapipe/solutions/hands.html
"""

import cv2
import mediapipe as mp
import time

cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils


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
                print(id, cx, cy)
                if id == 4: #Index finger point
                    cv2.circle(img, (cx,cy), 20, (255,0,0), 3)

            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

    #FPS Calculation
    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime

    #Display FPS
    cv2.putText(img, str(int(fps)),(10,70), cv2.FONT_HERSHEY_PLAIN, 3, (0,255,0), 3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)