from lib2to3.pytree import convert
from re import L
import cv2 as cv
import numpy as np

def convert_rgb_to_hsv(arr):
    arr_dot = np.array(arr)/255
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

def DetectColor(orginal_image,):

if __name__ == "__main__":
    image = cv.imread("/home/sri/VirtualVision/data/sample/digestive_system.jpg",cv.IMREAD_COLOR)
    hsv_value = convert_rgb_to_hsv([241,102,35])
    print(convert_hsv_to_standard(hsv_value))
    while True:
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
    cv.destroyAllWindows()