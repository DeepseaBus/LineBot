# image_calculator.py
import cv2 as cv
import numpy as np

# image_path = './test2.png'

# img = cv.imread(image_path, 0)
img = cv.imread('./coca_cola.png')
# print(img)
# img2 = np.ones(img.shape, dtype=np.uint8) * 30
img2 = cv.imread('./google.png')
# print(img2)
# img3 = cv.add(img, img2)
img3 = cv.addWeighted(img, 2, img2, 0.4, 0)  # img weighted
# print(img3)

cv.imwrite('./img.png', img)
cv.imwrite('./img2.png', img2)
cv.imwrite('./img3.png', img3)
