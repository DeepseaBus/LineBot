import cv2 as cv
import numpy as np


def image_processing_1(image_name, image_path):
    # read origin image
    img = cv.imread(image_path)

    # convert to gray
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    # convert to binary
    ret, binary = cv.threshold(gray, 127, 255, cv.THRESH_BINARY)

    # save converted image in path
    gray_path = './static/gray_' + image_name
    binary_path = './static/binary_' + image_name
    cv.imwrite(gray_path, gray)
    cv.imwrite(binary_path, binary)

    return gray_path, binary_path
