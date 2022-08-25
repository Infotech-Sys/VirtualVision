from unittest import result
import cv2 as cv
import numpy as np


def edge_detection(img, th1, th2):
    img = cv.GaussianBlur(img,(3,3),1)
    canny_image = cv.Canny(img, th1, th2, cv.LINE_AA)
    return canny_image


def find_threshold_value(img):
    gray_scale = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    ret, threshold_image = cv.threshold(gray_scale, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
    return ret


def contour_edge(img):
    # thresh_val = find_threshold_value(img)
    # gray_image = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
    # threshold_image = cv.threshold(img,thresh_val-10,thresh_val+10)
    contours, hierarchy = cv.findContours(img,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)
    result_image = img.copy()
    # print(len(contours))
    cv.drawContours(result_image,contours,-1,(0,0,0),1,cv.LINE_8)
    return result_image


def increase_edge_thickness(img):
    # kernel = cv.getStructuringElement(cv.MORPH_RECT, (5, 5))
    img = cv.bitwise_not(img)
    kernel = np.ones((3,3),np.uint8)
    result_image = cv.dilate(img, kernel,iterations=1)
    # result_image = cv.erode(img,kernel=kernel,iterations=1)
    result_image = cv.bitwise_not(result_image)
    return result_image


def add_color(orginal_image,border_image):
    # for i in range(border_image.shape[0]):
    #     for j in range(border_image.shape[1]):
    #         if border_image[i][j] != 255:
    #             orginal_image[i][j] = [border_image[i][j],border_image[i][j],border_image[i][j]]

    # border_image = np.float64(border_image)
    # border_image = (border_image/255)
    # for i in range(border_image.shape[0]):
    #     for j in range(border_image.shape[1]):
    #         orginal_image[i][j] = orginal_image[i,j,:] * border_image[i][j]

    border_image = cv.cvtColor(border_image,cv.COLOR_GRAY2BGR)
    border_image = np.float64(border_image) / 255
    result = np.uint8(orginal_image * border_image)
    return result


def convert_rgb_to_hsv(arr):
    arr_dot = arr/255
    cmax = arr_dot.max()
    cmin = arr_dot.min()
    del_value = cmax - cmin

    h_value=0
    s_value=0
    v_value=cmax

    if del_value == 0:
        h_value = 0
    elif cmax == arr_dot[0]:
        h_value = 60 * (((arr_dot[1]-arr_dot[2])/del_value)%6)
    elif cmax == arr_dot[1]:
        h_value = 60 * (((arr_dot[2]-arr_dot[0])/del_value)+2)
    else :
        h_value = 60 * (((arr_dot[0]-arr_dot[1])/del_value)+4)

    if cmax == 0:
        s_value=0
    else:
        s_value = del_value/cmax

    return np.array([h_value,s_value*100,v_value*100])

def convert_hsv_to_standard(hsv_value):
    return np.array([hsv_value[0]/360*255,hsv_value[1]/100*255,hsv_value[2]/100*255],np.uint8)

def DrawPattern(image,pattern,pattern_size,pattern_sep):
    if pattern == 'dot':
        for i in range(0,image.shape[1],pattern_sep):
            for j in range(0,image.shape[0],pattern_sep):
                image = cv.circle(image,(i,j),pattern_size,(0,0,0),-1)
        return image

def DetectColor(orginal_image,x,y,value,pattern,pattern_size,pattern_sep):
    bgr_value = orginal_image[x,y]
    rgb_value = bgr_value[::-1]
    print(type(rgb_value))
    hsv_value = convert_rgb_to_hsv(rgb_value)
    hsv_value = convert_hsv_to_standard(hsv_value)
    l_b = hsv_value - value
    l_b[l_b > 255-value] = 0
    u_b = hsv_value + value
    u_b[u_b < value] = 255
    print(l_b)
    print(u_b)
    orginal_image = cv.cvtColor(orginal_image,cv.COLOR_BGR2HSV)
    mask = cv.inRange(orginal_image,l_b,u_b)
    result_image = cv.bitwise_and(orginal_image,orginal_image,mask=mask)
    result_image = cv.cvtColor(result_image,cv.COLOR_HSV2BGR)
    pattern_image = DrawPattern(result_image,pattern,pattern_size,pattern_sep)
    return pattern_image


if __name__ == '__main__':
    image = cv.imread('/home/sri/VirtualVision/data/sample/digestive_system.jpg', cv.IMREAD_COLOR)

    threshold_value = find_threshold_value(image)
    
    edge_image = edge_detection(image, threshold_value-25, threshold_value+25)
    
    edge_image_inv = cv.bitwise_not(edge_image)
    
    contour_edge = contour_edge(edge_image_inv)
    
    color_result = add_color(image,contour_edge)
    
    increase_edge_thickness_image = increase_edge_thickness(color_result)
    
    result_image = DetectColor(image,174,410,10,'dot',1,5)
    cv.imwrite('yellow.jpg',result_image)
    cv.imshow('result', result_image)
    while True:
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
    cv.destroyAllWindows()
    