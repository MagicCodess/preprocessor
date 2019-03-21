import cv2
import numpy as np
import os

rightCount = 0
allCount = 0
basedir = '/home/arthur/PycharmProjects/preprocess/Tamil_3/'
filenames = os.listdir(basedir)
for file in filenames:
    a = cv2.imread(basedir + file, cv2.COLOR_BGR2GRAY)
    a = cv2.cvtColor(a, cv2.COLOR_BGR2GRAY)
    img = a
    cv2.imshow('a', a)
    #cv2.waitKey(0)

    a = cv2.Sobel(a, cv2.CV_8UC1, 1, 1)
    allCount += 1
    cv2.imshow('a', a)
    #cv2.waitKey(0)
    #print(a.shape)
    #ret, a = cv2.threshold(a, 0, 255, cv2.THRESH_OTSU)
    ret, a = cv2.threshold(a, 0, 255, cv2.THRESH_OTSU + cv2.THRESH_BINARY)
    #print(a.shape)
    cv2.imshow('a', a)
    #cv2.waitKey(0)

    k1 = cv2.getStructuringElement(cv2.MORPH_RECT, (30, 9))
    k2 = cv2.getStructuringElement(cv2.MORPH_RECT, (30, 3))

    a = cv2.dilate(a, k2)
    a = cv2.erode(a, k1)
    cv2.imshow('a', a)
    #cv2.waitKey(0)

    a = cv2.dilate(a, k2)
    a = cv2.dilate(a, k2)
    a = cv2.dilate(a, k2)
    #a = cv2.dilate(a, k2)
    cv2.imshow('a', a)
    #cv2.waitKey(0)

    contours,hierarchy = cv2.findContours(a, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    #print(contours)
    #print(hierarchy)
    contourCount = 0
    for c in contours:
        #x,y,w,h = cv2.boundingRect(c)
       # a = cv2.rectangle(a, (x, y), (x+w, y+h), (255, 0, 0), 2)
        rect = cv2.minAreaRect(c)
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        #print(box)
        if(max(max(max(box[0][1], box[1][1]), box[2][1]),box[3][1]) - min(min(min(box[0][1], box[1][1]), box[2][1]),box[3][1]) <8):
            #print('x')
            continue
        if(max(max(max(box[0][0], box[1][0]), box[2][0]),box[3][0]) - min(min(min(box[0][0], box[1][0]), box[2][0]),box[3][0]) <80):
            #print('y')
            continue
        a = cv2.drawContours(img, [box], 0, (0, 255, 0), 3)
        contourCount += 1
        #print(box[0][0])
    if(contourCount == 11):
        rightCount += 1

    #cv2.drawContours(a, contours, -1, (255, 0, 0), 10)

    cv2.imshow('a', a)
    print(float(rightCount)/allCount)
    #cv2.waitKey(0)
