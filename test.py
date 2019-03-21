import cv2
import pandas as pd

a = cv2.imread('test_rows/10100a_c_1.jpg', cv2.COLOR_BGR2GRAY)
cv2.imshow('a', a)

cv2.waitKey(0)
df1 = pd.DataFrame(a)
df1 = df1[~df1.isin([0])].dropna(axis=1)
print(df1)
#print(a)
a = df1.values
print(a.shape[0])

cv2.imshow('a', a)
cv2.waitKey(0)