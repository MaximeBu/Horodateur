import cv2
from matplotlib.transforms import Bbox
import mediapipe as mp
import math


class HandDetector:
    
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, minTrackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.minTrackCon = minTrackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(static_image_mode=self.mode, max_num_hands=self.maxHands,
                                        min_detection_confidence=self.detectionCon,
                                        min_tracking_confidence=self.minTrackCon)
        self.mpDraw = mp.solutions.drawing_utils
        self.tipIds = [4, 8, 12, 16, 20]
        self.fingers = []
        self.lmList = []

    def findHands(self, img, draw=True, flipType=True):
        mp_draw=mp.solutions.drawing_utils
        mp_hand=mp.solutions.hands

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        allHands = []
        h, w, c = img.shape
        if self.results.multi_hand_landmarks:
            for handType, handLms in zip(self.results.multi_handedness, self.results.multi_hand_landmarks):
                myHand = {}
                ## lmList
                lmList = []
                mylmList = []
                xList = []
                yList = []
                for id, lm in enumerate(handLms.landmark):
                    px, py, pz = int(lm.x * w), int(lm.y * h), int(lm.z * w)
                    mylmList.append([px, py, pz])
                    xList.append(px)
                    yList.append(py)
                    h,w,c=img.shape
                    cx,cy= int(lm.x*w), int(lm.y*h)
                    lmList.append([id,cx,cy])

            
                mp_draw.draw_landmarks(img, handLms, mp_hand.HAND_CONNECTIONS)


                ## bbox
                xmin, xmax = min(xList), max(xList)
                ymin, ymax = min(yList), max(yList)
                boxW, boxH = xmax - xmin, ymax - ymin
                bbox = xmin, ymin, boxW, boxH
                cx, cy = bbox[0] + (bbox[2] // 2), \
                         bbox[1] + (bbox[3] // 2)

                myHand["lmList"] = lmList
                myHand["mylmList"] = mylmList
                myHand["bbox"] = bbox
                myHand["center"] = (cx, cy)

                if flipType:
                    if handType.classification[0].label == "Right":
                        myHand["type"] = "Left"
                    else:
                        myHand["type"] = "Right"
                else:
                    myHand["type"] = handType.classification[0].label
                allHands.append(myHand)

                ## draw
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms,
                                               self.mpHands.HAND_CONNECTIONS)
                    cv2.rectangle(img, (bbox[0] - 20, bbox[1] - 20),
                                  (bbox[0] + bbox[2] + 20, bbox[1] + bbox[3] + 20),
                                  (255, 0, 255), 2)
                    cv2.putText(img, myHand["type"], (bbox[0] - 30, bbox[1] - 30), cv2.FONT_HERSHEY_PLAIN,
                                2, (255, 0, 255), 2)
        if draw:
            return allHands, img
        else:
            return allHands
   


    def fingersUp(self, myHand):
        myHandType = myHand["type"]
        myLmList = myHand["lmList"]
        if self.results.multi_hand_landmarks:
            fingers = []

            # Thumb
            #NOTE La partie suivante vérifie la présence du pouce et si la main est inversé.
            if myHandType == "Right":
                reversedThumb = myLmList[self.tipIds[0]][1] < myLmList[self.tipIds[4]][1]
                if myLmList[self.tipIds[0]][1] > myLmList[self.tipIds[0]-1][1]:
                    fingers.append(0) if reversedThumb else fingers.append(1)
                else:
                    fingers.append(1) if reversedThumb else fingers.append(0)
            else:
                reversedThumb = myLmList[self.tipIds[0]][1] > myLmList[self.tipIds[4]][1]
                if myLmList[self.tipIds[0]][1] < myLmList[self.tipIds[0]-1][1]:
                    fingers.append(0) if reversedThumb else fingers.append(1)
                else:
                    fingers.append(1) if reversedThumb else fingers.append(0)

            
            for id in range(1,5):
                if myLmList[self.tipIds[id]][2] < myLmList[self.tipIds[id]-2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)

        fingerCount = fingers.count(1)
        #May need a list so I'll consider returning a list.
        return fingerCount


    def findDistance(self, p1, p2, img=None):
        x1, y1 = p1 #Point 1
        x2, y2 = p2 #Point 2
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
        length = math.hypot(x2 - x1, y2 - y1)
        info = (x1, y1, x2, y2, cx, cy)
        if img is not None:
            cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
            cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
            return round(length, 1), info, img
        else:
            return length, info
   

    def infoOnHand(self,
               img,
               hand,
               textToShow: list = None):

        x, y, w, h = hand["bbox"]
        brect = x, y, x + w, y + h
        handType = hand["type"]

        x1, x2 = brect[0], brect[2]
        font = (x2 - x1) * 0.00375

        if textToShow is not None:
            length = len(textToShow)
            cv2.rectangle(img, (brect[0], brect[1]), (brect[2], brect[1] - 26*(length+1)),
                    (0, 0, 0), -1)

            x, y = brect[0] + 5, (brect[1] - 8)

            cv2.putText(img, f"{handType}: ", (x, y - 26 * length),
                cv2.FONT_HERSHEY_SIMPLEX, font, (255, 255, 255), 1, cv2.LINE_AA)
            isFirst = True
            for text in textToShow:
                if not isFirst:
                    y -= 26

                cv2.putText(img, str(text), (x, y),
                    cv2.FONT_HERSHEY_SIMPLEX, font, (255, 255, 255), 1, cv2.LINE_AA)
                isFirst = False
        else:
            cv2.rectangle(img, (brect[0], brect[1]), (brect[2], brect[1] - 22),
            (0, 0, 0), -1)

            cv2.putText(img, handType, (brect[0] + 5, (brect[1] - 4)),
                cv2.FONT_HERSHEY_SIMPLEX, font, (255, 255, 255), 1, cv2.LINE_AA)
        return img