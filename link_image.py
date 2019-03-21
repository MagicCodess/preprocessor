import cv2
import numpy as np
pic = cv2.imread('1.jpg')

gray1 = cv2.cvtColor(pic, cv2.COLOR_BGR2GRAY)
image = gray1
count = 5
while(count):


    pic2 = cv2.imread('2.jpg')
    #des = cv2.hconcat(pic, pic)

    gray2 = cv2.cvtColor(pic2, cv2.COLOR_BGR2GRAY)
    image = np.vstack((image, gray2))
    cv2.imshow('image', image)
    cv2.waitKey(0)
    count-=1
