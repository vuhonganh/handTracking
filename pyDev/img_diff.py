import numpy as np
import cv2

img1 = cv2.imread("bg.jpg")
img2 = cv2.imread("bg_with_hand.jpg")

img3 = cv2.absdiff(img1, img2)
#cv2.imshow('test minus images RGB', img3)

img3_gray = cv2.cvtColor(img3, cv2.COLOR_BGR2GRAY)
#cv2.imshow('test minus images gray', img3_gray)

img3_blur = cv2.GaussianBlur(img3_gray, (3,3), 0)
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (10,10))
#img3_blur = cv2.erode(img3_blur, kernel, 1)
#img3_blur = cv2.dilate(img3_blur, kernel, 2)
#img3_blur = cv2.erode(img3_blur, kernel)
img3_blur = cv2.GaussianBlur(img3_blur, (5,5), 255)
ret, img3_bin = cv2.threshold(img3_blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

img3_bin = cv2.erode(img3_bin, kernel)
img3_bin = cv2.dilate(img3_bin, kernel, 2)

cv2.imshow('test minus images binary', img3_bin)
cv2.waitKey(0)
