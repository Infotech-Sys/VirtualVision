import cv2 as cv
import numpy as np


def find_threshold_value(color_image):
    gray_scale = cv.cvtColor(color_image, cv.COLOR_BGR2GRAY)
    threshold_value, threshold_image = cv.threshold(gray_scale, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
    return threshold_value


def edge_detection(color_image, threshold1, threshold2):
    blured_image = cv.GaussianBlur(color_image, (3, 3), 1)
    canny_image = cv.Canny(blured_image, threshold1, threshold2, cv.LINE_8)  # Changed cv.LINE_AA -> cv.LINE_8
    return canny_image


def contour_edge(img):
    contours, hierarchy = cv.findContours(img, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
    result_image = img.copy()
    cv.drawContours(result_image, contours, -1, (0, 0, 0), 1, cv.LINE_AA)

    return result_image


def add_color(orginal_image, border_image):
    border_image = cv.cvtColor(border_image, cv.COLOR_GRAY2BGR)
    border_image = np.float64(border_image) / 255
    result = np.uint8(orginal_image * border_image)
    return result


def increase_edge_thickness(img):
    img = cv.bitwise_not(img)
    kernel = np.ones((3, 3), np.uint8)
    result_image = cv.dilate(img,  kernel, iterations=1)
    # result_image = cv.erode(img, kernel=kernel, iterations=1)
    result_image = cv.bitwise_not(result_image)
    return result_image
