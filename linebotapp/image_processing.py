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

    # return gray_path, binary_path
    # put binary image in contours
    contours, hierarchy = cv.findContours(binary, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)

    # copy origin img
    copy = img.copy()

    # sketch contour on img
    copy = cv.drawContours(copy, contours, -1, (255, 0, 0), 2)

    # save after contoured img
    contour_image_path = './static/contour.png'
    cv.imwrite(contour_image_path, copy)
    return contour_image_path
