import cv2 as cv
import numpy as np

image = np.ones((1000,1000),np.uint8)
image = image*255
for i in range(0,1000,20):
    for j in range(0,1000,20):
        image = cv.circle(image,(i,j),5,(0,0,0),-1)
cv.imshow('image',image)
while True:
    if cv.waitKey(1) & 0xFF == ord('q'):
        break
cv.destroyAllWindows()