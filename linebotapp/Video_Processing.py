import numpy as np
import cv2 as cv

image_path = './static/video_canny.jpg'
video_path = './static/video_canny.mp4'


def video_processing(path):
    cap = cv.VideoCapture(path)

    # set capture img size
    # fourcc = 0x00000021
    fourcc = -1
    FPS = 24
    w = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))

    # create VideoWriter object, output video to  './static/video_canny2.mp4'
    # FPS = 24, fourcc = 0x00000021=>convert to mp4，w,h set to origin video size
    output = cv.VideoWriter(video_path, fourcc, FPS, (w, h))

    while cap.isOpened():
        ret, frame = cap.read()
        # use cv2.Canny()for edge detect, threshold1 and threshold2 can set to 0-255
        canny = cv.Canny(frame, 80, 220)
        if ret:
            # write in frame
            output.write(canny)

            cv.imshow('canny', canny)
            cv.imwrite(image_path, canny)
            # cv2.waitKey() parameter in braces is ms, means every img's stay time，default = 25
            if cv.waitKey(25) & 0xFF == ord('q'):
                break
        else:
            break
    return image_path, video_path
