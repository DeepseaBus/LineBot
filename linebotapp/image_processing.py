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

    # put binary image in contours
    contours, hierarchy = cv.findContours(binary, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)

    # create empty img
    empty = np.ones(img.shape, dtype=np.uint8) * 255
    # find ROI(region of interest)
    total_area = img.shape[0] * img.shape[1]
    font = cv.FONT_HERSHEY_COMPLEX
    print(total_area)
    n = len(contours)
    for i in range(n):
        M = cv.moments(contours[i])
        area = M['m00']
        if area / total_area > 0.15 and area / total_area < 0.50:  # if coutour area > 15% total area <50%
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])
            center = tuple((cx, cy))
            if cx > img.shape[1] * 0.25 and cx < img.shape[1] * 0.75:
                # put text on empty img
                cv.putText(empty, '. no.=' + str(i), center, font, 2, (0, 0, 255), 1)
                print('輪廓編號%d，面積大小%d，中心點%s' % (i, area, str(center)))
                # draw coutour on copy img
                copy = cv.drawContours(empty, contours[i], -1, (255, 0, 0), 2)
    # copy origin img
    # copy = img.copy()

    # sketch contour on img
    # copy = cv.drawContours(copy, contours, -1, (255, 0, 0), 2)
    copy = cv.drawContours(empty, contours, -1, (255, 0, 0), 2)
    # save after contoured img
    contour_image_path = './static/contour_'+ image_name
    cv.imwrite(contour_image_path, copy)
    return gray_path, binary_path, contour_image_path
