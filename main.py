import random

import cvzone
import cv2
from cvzone.HandTrackingModule import HandDetector
import time

cap = cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)

detector = HandDetector(maxHands=1)

timer = 0
stateResult = False
startGame = False
scores = [0,0]  #[AI,player]

while True:
    imgBG = cv2.imread("Resources/Resources/BG.png") #have to update everytime

    success,img = cap.read()
    imgScaled = cv2.resize(img,(0,0),None,0.875,0.875)    #420/480=0.875 scale
    imgScaled = imgScaled[:, 80:480]

    #Find Hands
    hands, img = detector.findHands(imgScaled)
    if startGame:
        if stateResult is False:
            timer = time.time() - initialTime
            cv2.putText(imgBG,str(int(timer)),(605,435),cv2.FONT_HERSHEY_SIMPLEX,3,(0,0,255),4)

            if timer >3:
               stateResult = True
               timer =0

               if hands:
                    playerMove =None
                    hand = hands[0]
                    fingers = detector.fingersUp(hand)
                    if fingers == [0,0,0,0,0]:
                        playerMove = 1
                    if fingers == [1,1,1,1,1]:
                        playerMove = 2
                    if fingers == [0,1,1,0,0]:
                        playerMove = 3
                    # print(playerMove)
                    randomNumber = random.randint(1,3)

                    imgAI = cv2.imread(f'Resources/Resources/{randomNumber}.png',cv2.IMREAD_UNCHANGED)
                    imgBG = cvzone.overlayPNG(imgBG, imgAI, (149, 310))

                    #player wins
                    if (playerMove ==1 and randomNumber==3) or \
                            (playerMove==2 and randomNumber==1) or \
                            (playerMove==3 and randomNumber==2):
                        print("You Win")
                        scores[1] +=1

                        # cv2.putText(imgBG, str(Text), (900, 435), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 2)

                    # AI wins
                    if (playerMove == 3 and randomNumber == 1) or \
                            (playerMove == 1 and randomNumber == 2) or \
                            (playerMove == 2 and randomNumber ==3 ):
                        print("AI Wins")
                        scores[0] += 1

                        # Text = "AI Wins"
                        # cv2.putText(imgBG, str(Text), (350, 435), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 2)

                    # print(fingers)

    imgBG[234:654,795:1195] = imgScaled
    if stateResult:
        imgBG = cvzone.overlayPNG(imgBG, imgAI, (149, 310))

    cv2.putText(imgBG,str(scores[0]),(410,215),cv2.FONT_HERSHEY_PLAIN,4,(255,255,255),6)
    cv2.putText(imgBG,str(scores[1]),(1112,215),cv2.FONT_HERSHEY_PLAIN,4,(255,255,255),6)
    # cv2.imshow("Image",img)
    cv2.imshow("BG",imgBG)
    # cv2.imshow("Scaled",imgScaled)


    key = cv2.waitKey(1)
    if key == ord('s'):
        startGame = True
        initialTime = time.time()  #when s is presses and the actual game started time
        stateResult = False #each time pressed 's' key the game resets
    if  0xFF == ord('q'):
        break






















