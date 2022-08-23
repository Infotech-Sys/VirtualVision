import cv2 as cv
import numpy as np


def TactileGenerator(image):
    orginal_image = image.copy()
    gray_scale_image = cv.cvtColor(image,cv.COLOR_BGR2GRAY)
    otsu_threshold_value, threshold_image = cv.threshold(gray_scale_image,0,255,cv.THRESH_BINARY+cv.THRESH_OTSU)

    blured_image = cv.GaussianBlur(image,(3,3),1)

    threshold1 = otsu_threshold_value - 40
    threshold2 = otsu_threshold_value + 40

    canny_edge_detected_image = cv.Canny(blured_image,threshold1,threshold2)
    white_bg_edge_image = cv.bitwise_not(canny_edge_detected_image)

    contours, hierarchy = cv.findContours(white_bg_edge_image,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)

    contours_edge_image = np.ones_like(image) * 255
    cv.drawContours(contours_edge_image,contours,-1,(0,0,0),2,cv.LINE_8)

    kernel_mat = np.ones((3,3),np.int8)
    
    # result_image = cv.GaussianBlur(contours_edge_image,(3,3),1)
    # result_image = cv.erode(result_image,kernel_mat,iterations=1)
    # result_image = cv.dilate(contours_edge_image,kernel_mat,iterations=1)

    border_gray_image = np.float64(contours_edge_image) / 255
    border_color_image = np.uint8(orginal_image * border_gray_image)


    return border_color_image