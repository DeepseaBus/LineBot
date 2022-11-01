import cv2 as cv
import numpy as np


def image_processing_1(image_name, image_path):
    # read origin image
    img = cv.imread(image_path)

    # convert to gray
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    # convert to binary
    ret, binary = cv.threshold(gray, 200, 255, cv.THRESH_BINARY)

    # save converted image in path
    gray_path = './static/gray_' + image_name
    binary_path = './static/binary_' + image_name
    contour_image_path = './static/contour_' + image_name
    cv.imwrite(gray_path, gray)
    cv.imwrite(binary_path, binary)

    # put binary image in contours
    contours, hierarchy = cv.findContours(binary, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
    # copy img
    copy = img.copy()
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
        if area / total_area > 0.15 and area / total_area < 0.50:  # if contour area > 15% total area <50%
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])
            center = tuple((cx, cy))
            if cx > img.shape[1] * 0.25 and cx < img.shape[1] * 0.75:
                # put text on empty img
                # cv.putText(empty, '. no.=' + str(i), center, font, 2, (0, 0, 255), 1)
                # print('輪廓編號%d，面積大小%d，中心點%s' % (i, area, str(center)))
                # draw contour on copy img
                # copy = cv.drawContours(empty, contours[i], -1, (255, 0, 0), 2)

                # draw contour on copy img
                # copy = cv.drawContours(img, contours[i], -1, (255, 0, 0), 2)

                # bulid single channel mask
                mask = np.zeros(gray.shape, dtype=np.uint8)
                cv.drawContours(mask, contours[i], -1, (255, 255, 255), -1)
                meanVal = cv.mean(img, mask=mask)  # mask is an area, so it has to be single channel
                if meanVal[2] > meanVal[1] and meanVal[2] > meanVal[1]:
                    print(meanVal)  # print contour's B、G、R average
                    if abs(meanVal[2] - meanVal[1]) > 10:  # if abs(green - red)>10
                        copy = cv.drawContours(img, contours[i], -1, (0, 0, 255), 2)

                        copy = img.copy()
                        copy = cv.drawContours(copy, contours[i], -1, (0, 0, 255), 2)
                        # save img
                        contour_image_path = './static/contour_' + image_name
                        cv.imwrite(contour_image_path, copy)

                        # bounding rectangle
                        copy = img.copy()
                        x, y, w, h = cv.boundingRect(contours[0])
                        brcnt = np.array([[[x,y]],[[x+w,y]],[[x+w,y+h]],[[x,y+h]]])
                        cv.drawContours(copy,[brcnt],-1,(255,0,0),2)
                        a = './static/a_' + image_name
                        cv.imwrite(a,copy)

                        # min bounding rectangle
                        copy = img.copy()
                        rect = cv.minAreaRect(contours[i])
                        points = cv.boxPoints(rect)
                        repoint = np.array(points).reshape((-1,1,2)).astype(np.int32)
                        cv.drawContours(copy,[repoint],0,(255,0,0),2)
                        b = './static/b_'+image_name
                        cv.imwrite(b,copy)

                        # min bounding circle
                        copy = img.copy()
                        (x, y), radius = cv.minEnclosingCircle(contours[i])
                        center = (int(x), int(y))
                        radius = int(radius)
                        cv.circle(copy, center, radius, (255, 0, 0), 2)
                        c = './static/c_' + image_name
                        cv.imwrite(c, copy)

                        # min bounding ellipse
                        copy = img.copy()
                        ellipse = cv.fitEllipse(contours[i])
                        cv.ellipse(copy, ellipse, (255, 0, 0), 3)
                        d = './static/d_' + image_name
                        cv.imwrite(d, copy)

                        # min fit line
                        copy = img.copy()
                        rows, cols = copy.shape[:2]
                        [vx, vy, x, y] = cv.fitLine(contours[i], cv.DIST_L2, 0, 0.01, 0.01)
                        lefty = int(((-x * vy / vx) + y))
                        righty = int(((cols - x) * vy / vx) + y)
                        cv.line(copy, (cols - 1, righty), (0, lefty), (255, 0, 0), 2)
                        e = './static/e_' + image_name
                        cv.imwrite(e, copy)

                        # min bounding triangle
                        # error -  Can't parse 'pt1'. Sequence item with index 0 has a wrong type 2022/10/30
                        # copy = img.copy()
                        # area, trgl = cv.minEnclosingTriangle(contours[i])
                        # print(trgl)
                        # for i in range(0, 3):
                        #     cv.line(copy, tuple(trgl[i][0]), tuple(trgl[(i + 1) % 3][0]), (255, 0, 0), 2)
                        # f = './static/f_' + image_name
                        # cv.imwrite(f, copy)

    # copy origin img
    # copy = img.copy()

    # sketch contour on img
    # copy = cv.drawContours(copy, contours, -1, (255, 0, 0), 2)
    # copy = cv.drawContours(empty, contours, -1, (255, 0, 0), 2)
    # save after contoured img
    # contour_image_path = './static/contour_' + image_name
    # cv.imwrite(contour_image_path, copy)
    return gray_path, binary_path, contour_image_path
