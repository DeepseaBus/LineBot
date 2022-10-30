
import cv2 as cv
import numpy as np

img = cv.imread('apple2.jpg')
kernel = np.ones((3,3),dtype=np.uint8) # erosion 3 * 3
kernel = np.ones((10,10),dtype=np.uint8) # erosion 10 * 10
erosion = cv.erode(img,kernel)

cv.imwrite('./erosion.jpg',erosion)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
img = cv.imread('grape.jpg')
gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
ret,binary = cv.threshold(gray,200,255,cv.THRESH_BINARY_INV)

# create kernel
kernel = np.ones((8,8),dtype=np.uint8)

# MORPH_OPEN
opening = cv.morphologyEx(binary,cv.MORPH_OPEN,kernel)

# MORPH_CLOSE
closing = cv.morphologyEx(binary,cv.MORPH_CLOSE,kernel)

# MORPH_GRADIENT
gradient = cv.morphologyEx(binary,cv.MORPH_GRADIENT,kernel)

# MORPH_TOPHAT
tophat = cv.morphologyEx(binary,cv.MORPH_TOPHAT,kernel)

# MORPH_BLACKHAT
blackhat = cv.morphologyEx(binary,cv.MORPH_BLACKHAT,kernel)

# MORPH_TOPHAT + MORPH_BLACKHAT
twohat = cv.add(tophat,blackhat)

cv.imwrite('./binary.jpg',binary)
cv.imwrite('./opening.jpg',opening)
cv.imwrite('./closing.jpg',closing)
cv.imwrite('./gradient.jpg',gradient)
cv.imwrite('./tophat.jpg',tophat)
cv.imwrite('./blackhat.jpg',blackhat)
cv.imwrite('./twohat.jpg',twohat)
