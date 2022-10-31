import cv2
import numpy as np

domain = 'https://2b79-2001-b011-3819-ddb7-3dd0-5d99-6cbb-8eed.jp.ngrok.io'  # ngrok domain


# SLIC
def SLIC(image_name, image_path):
    img = cv2.imread(image_path)
    # SLIC initial setting, default size = 10, set to 20, smoothing parameter = 20
    slic = cv2.ximgproc.createSuperpixelSLIC(img, region_size=20, ruler=20.0)
    slic.iterate(10)  # iterate(迭代) time, iterate more time => effective better
    mask_slic = slic.getLabelContourMask()  # create superpix mask, mask_slic = 1
    label_slic = slic.getLabels()  # get label
    number_slic = slic.getNumberOfSuperpixels()  # get number of pixels
    mask_inv_slic = cv2.bitwise_not(mask_slic)
    img_slic = cv2.bitwise_and(img, img, mask=mask_inv_slic)  # draw superpix edge on img
    cv2.imwrite('./static/SLIC.png', img_slic)  # save img
    return domain + '/static/SLIC.png'


# SEEDS
def SEEDS(image_name, image_path):
    img = cv2.imread(image_path)
    # SEEDS initial setting
    seeds = cv2.ximgproc.createSuperpixelSEEDS(img.shape[1], img.shape[0], img.shape[2], 2000, 15, 3, 5, True)
    seeds.iterate(img, 10)  # iterate time = 10
    mask_seeds = seeds.getLabelContourMask()
    label_seeds = seeds.getLabels()
    number_seeds = seeds.getNumberOfSuperpixels()
    mask_inv_seeds = cv2.bitwise_not(mask_seeds)
    img_seeds = cv2.bitwise_and(img, img, mask=mask_inv_seeds)
    cv2.imwrite('./static/SEED.png', img_seeds)
    return domain + '/static/SEED.png'


# LSC
def LSC(image_name, image_path):
    img = cv2.imread(image_path)
    # LSC initial setting
    lsc = cv2.ximgproc.createSuperpixelLSC(img)
    lsc.iterate(10)  # iterate time = 10
    mask_lsc = lsc.getLabelContourMask()
    label_lsc = lsc.getLabels()
    number_lsc = lsc.getNumberOfSuperpixels()
    mask_inv_lsc = cv2.bitwise_not(mask_lsc)
    img_lsc = cv2.bitwise_and(img, img, mask=mask_inv_lsc)
    cv2.imwrite('./static/LSC.png', img_lsc)
    return domain + '/static/LSC.png'
