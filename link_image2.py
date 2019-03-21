import cv2
import os
import sys
import numpy as np

basedir = '/home/arthur/PycharmProjects/preprocess/processCutter/'
outputdir = '/home/arthur/PycharmProjects/preprocess/processCutterOut3/'
filenames = os.listdir(basedir)
filenames.sort(key=lambda x : (int(x[:5]), (x[5]), int(x[7:-4])))
#filenames.sort(key=lambda x: (x[5]))
#filenames.sort()
#for file in filenames:
#    print(file)
#filenames.sort(key=lambda x: int(x[7:-4]))
processing = filenames[0][0: 6]
print(processing)
count = 0
necount = 0
tmcount = 0
allcount = 1
processingimg = cv2.imread(basedir+filenames[0], cv2.COLOR_BGR2GRAY)
processingimg = cv2.resize(processingimg,(568,32))
cv2.imshow('show', processingimg)
cv2.waitKey(0)
print(processing)
for file in filenames:
    #print(count)
    tmpname = file[0:6]
    if tmpname == processing:
        tmpimg = cv2.imread(basedir+file, cv2.COLOR_BGR2GRAY)

        tmpimg = cv2.resize(tmpimg, (568, 32))
        if count == 0:
            processingimg =tmpimg
            count += 1
        else:
            processingimg = np.vstack((processingimg, tmpimg))
            count += 1
        if count == 11:
            cv2.imwrite(outputdir+file[0:6] + '.png', processingimg)
            #cv2.imshow('show', processingimg)
            #cv2.waitKey(0)

    else:
        if count!= 11:
            if count < 11:
                print("error not enough, file: " +processing + 'count' + str(count))
                necount += 1
            else:
                print("error too much, file: " + processing + 'count' + str(count))
                tmcount += 1
            count = 0
        processingimg = cv2.imread(basedir+file, cv2.COLOR_BGR2GRAY)

        processingimg = cv2.resize(processingimg, (568, 32))
        processing = file[0: 6]
        count = 1
        allcount += 1

print('not enough rate:')
print(necount/allcount)
print('too much rate: ')
print(tmcount/allcount)