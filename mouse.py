# import cv2
# import autopy
# import time
# import numpy as np
# import pyHandler as htm
#
# ############################
# wCam, hCam = 640, 480
# frameR = 60 # Frame Reduction
# smoothening = 7
# ############################
#
# pTime = 0
# plocX, plocY = 0, 0
# clocX, clocY = 0, 0
#
# cap = cv2.VideoCapture(0)
# cap.set(3, wCam)
# cap.set(4, hCam)
# detector = htm.handDetector(maxHands=1)
# wScr, hScr = autopy.screen.size()
# #print(wScr, hScr)
#
# while True:
#     success, img = cap.read()
#     img = detector.findHands(img)
#     lmList, bbox = detector.findPosition(img)
#
#     if len(lmList)!=0:
#         x1, y1 = lmList[8][1:]
#         x2, y2 = lmList[4][1:]
#
#         #print(x1, y1, x2, y2)
#
#         fingers = detector.fingersUp()
#         #print(fingers)
#         cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR),
#                       (255, 0, 255), 2)
#         # 4. Only index Finger :Moving Mode
#         if fingers[1] == 1 and fingers[2] == 0:
#             # 5. convert coordinates
#
#             x3 = np.interp(x1, (frameR, wCam-frameR), (0, wScr))
#             y3 = np.interp(y1, (frameR, hCam-frameR), (0, hScr))
#             # 6. Smoothen Values
#             clocX = plocX +(x3 -plocX) /smoothening
#             clocY = plocY + (y3 - plocY) / smoothening
#
#             # 7. Move Mouse
#             autopy.mouse.move(wScr-clocX, clocY)
#             cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
#             plocX, plocY = clocX, clocY
#
#         # 8. Both Index and Middle Finger are up : Clicking Mode
#         if fingers[1] == 1 and fingers[2] == 1:
#             length, img, lineInfo = detector.findDistance(8, 4, img)
#             print(length)
#             if length < 39:
#                 cv2.circle(img, (lineInfo[8], lineInfo[5]),
#                            15, (0, 255, 0), cv2.FILLED)
#                 autopy.mouse.click()
#         # 9. Find Distance between Fingers
#
#     cTime = time.time()
#     fps = 1 / (cTime - pTime)
#     pTime = cTime
#     cv2.putText(img, str(int(fps)), (40, 50), cv2.FONT_HERSHEY_PLAIN, 3,
#                 (255, 0, 0), 3)
#
#     cv2.imshow("Img", img)
#     cv2.waitKey(1)

import cv2
import autopy
import time
import numpy as np
import pyHandler as htm

############################
wCam, hCam = 640, 480
frameR = 130  # Frame Reduction
smoothening = 10
click_threshold = 55  # Distance threshold for click event
############################

pTime = 0
plocX, plocY = 0, 0
clocX, clocY = 0, 0

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
detector = htm.handDetector(maxHands=1)
wScr, hScr = autopy.screen.size()

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)

    if len(lmList) != 0:
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[4][1:]
        fingers = detector.fingersUp()
        cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR), (255, 0, 255), 2)

        # Moving Mode
        if fingers[1] == 1 and fingers[2] == 0:
            x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
            y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))
            clocX = plocX + (x3 - plocX) / smoothening
            clocY = plocY + (y3 - plocY) / smoothening

            autopy.mouse.move(wScr - clocX, clocY)
            cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
            plocX, plocY = clocX, clocY

        # Clicking Mode
        if fingers[0] == 1 and fingers[1] == 1:
            length, img, lineInfo = detector.findDistance(8, 4, img)
            if len(lineInfo) >= 6:  # Check if lineInfo has enough elements
                if length < click_threshold:
                    cv2.circle(img, (lineInfo[0], lineInfo[1]), 15, (0, 255, 0), cv2.FILLED)
                    autopy.mouse.click()

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (40, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

    cv2.imshow("Img", img)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
