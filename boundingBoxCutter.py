import numpy as np
import os
import pandas as pd
import cv2

basedir = '/home/arthur/PycharmProjects/preprocess/Tamil_3_rows/'
outputdir = '/home/arthur/PycharmProjects/preprocess/processCutter/'
filenames = os.listdir(basedir)
filenames.sort(key=lambda x : (x[0: 8], int(x[9:-4])))
print(filenames)
count = 0
processing = filenames[0][0: 8]
processing2 = filenames[0][0: 6]
processingimg = cv2.imread(basedir+filenames[0], cv2.COLOR_BGR2GRAY)
# df1 = pd.DataFrame()
for file in filenames[1: ]:
    img = cv2.imread(basedir + file, cv2.COLOR_BGR2GRAY)

    df1 = pd.DataFrame(img)
    df1 = df1[~df1.isin([0])].dropna(axis=1)
    img = df1.values
    #cv2.imshow('a', img)
    #cv2.waitKey(0)
    #print(processing + ':' + file[0:8])
    if file[0:8] == processing:
        img = cv2.resize(img, (img.shape[1], processingimg.shape[0]))
        padding = np.ones((processingimg.shape[0], 10)) * processingimg[2][2]
        processingimg = np.hstack((processingimg, padding))
        processingimg = np.hstack((processingimg, img))
    else:
        cv2.imwrite(outputdir + processing[0: 7] + str(count) + '.png', processingimg)
        processingimg = img
        processing = file[0: 8]
        count += 1
        if (file[0: 6] != processing2):
            count = 0
            processing2 = file[0: 6]

cv2.imwrite(outputdir + processing[0: 7] + str(count) + '.png', processingimg)