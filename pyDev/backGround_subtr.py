import numpy as np
import cv2

camera = cv2.VideoCapture(0)

fgbg = cv2.createBackgroundSubtractorMOG()

while(1):
    ret, frame = camera.read()
    fgmask = fgbg.apply(frame)

    cv2.imshow('frame', fgmask)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()


    
