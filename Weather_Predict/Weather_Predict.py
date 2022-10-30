import requests
import datetime
import time

import cv2 as cv
import numpy as np
import urllib.request

# set detected center x,y
center = [2051, 883]

# URL to image
def url_to_image(url):
    resp = urllib.request.urlopen(url)
    # bytearray => convert(return) data to a new array
    # asarray => copy array and turn it into ndarray
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    # cv2.imdecode() => decode data to OPENCV image
    image = cv.imdecode(image, cv.IMREAD_COLOR)
    # return the image
    return image


while True:
    now = datetime.datetime.now()
    url = 'https://opendata.cwb.gov.tw/fileapi/v1/opendataapi/O-A0058-003?Authorization=rdec-key-123-45678-011121314&format=JSON'
    res_get = requests.get(url)

    # convert request data to dict
    radar_echo = res_get.json()

    # get img url form dict
    image_url = radar_echo['cwbopendata']['dataset']['resource']['uri']
    image = url_to_image(image_url)

    # according the center point, cut down the img from the center point, size = 100 * 100
    image = image[center[1] - 100:center[1] + 100, center[0] - 100:center[0] + 100]
    # split B G R from the cut down img
    B, G, R = cv.split(image)

    # caculate the img ，exR= especially red index
    exR = 2 * np.max(R) - np.max(G) - np.max(B)
    print('exR=', exR, '日期時間=', now)
    print('雷達回波圖的網址=', image_url)
    # if there is yellow/red in cut down img, report a warning
    if np.max(exR) >= 150:  # exR>=150 then report
        print('快要下雨啦!!!')
        print(image_url)
        time.sleep(60 * 120)  # if report a warning sleep 2 hours
    else:
        time.sleep(60 * 10)  # if there is no raining sign, detect every 10 minutes
