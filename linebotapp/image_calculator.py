# image_calculator.py
import cv2 as cv
import numpy as np

# image_path = './test2.png'

# img = cv.imread(image_path, 0)
# img = cv.imread('./coca_cola.png')
img = cv.imread('./apple.png')
# print(img)
# img2 = np.ones(img.shape, dtype=np.uint8) * 30
# img2 = cv.imread('./google.png')
img2 = cv.imread('./twitter.png')
# print(img2)
# img3 = cv.add(img, img2)
# img3 = cv.addWeighted(img, 2, img2, 0.4, 0)  # img add with weighted
# img3 = cv.bitwise_and(img, img2)  # bitwise and
# img3 = cv.bitwise_or(img, img2)  # bitwise or
# img3 = cv.bitwise_not(img)  # bitwise not img
# img4 = cv.bitwise_not(img2)  # bitwise not img2
# img3 = cv.bitwise_xor(img,img2)  # bitwise xor
mask = np.zeros((img.shape[0], img.shape[1]), dtype=np.uint8)
print(mask.shape)
mask[300:500, 300:500] = 255
img3 = cv.bitwise_and(img, img2, mask=mask)  # bitwise and add mask
# print(img3)

cv.imwrite('./img.png', img)
cv.imwrite('./img2.png', img2)
cv.imwrite('./img3.png', img3)
# cv.imwrite('./img4.png', img4)
