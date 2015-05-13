import numpy as np
import cv2
from math import *


def subtract(bg, img, seuil):
    if(bg.shape == img.shape):
        height, width, depth = img.shape
        

def main_task():
    cam = cv2.VideoCapture(0)

    waitTime = 100
    for i in range(waitTime):
        _, avg = cam.read()

    #avg = np.float32(avg)

    while(1):
        _, img_cur = cam.read()
        #   alpha = 0.01 #factor of forgetting
        #  cv2.accumulateWeighted(img_cur, avg, alpha)
        #avg_scaled = cv2.convertScaleAbs(avg)
        #img_diff = cv2.absdiff(img_cur, avg_scaled)
        img_diff = cv2.absdiff(img_cur, avg)

        cv2.imshow('img_cur', img_cur)
        cv2.imshow('img_diff', img_diff)
        #cv2.imshow('avg', avg_scaled)

       
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
        

    cam.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main_task()
