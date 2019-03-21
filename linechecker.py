import os

txtdir = '/home/arthur/PycharmProjects/preprocess/3/'
imgdir = '/home/arthur/PycharmProjects/preprocess/processCutter/'
txtfiles = os.listdir(txtdir)
imgfiles = os.listdir(imgdir)
txtfiles.sort(key=lambda x : (int(x[:5])))
imgfiles.sort(key=lambda x : (int(x[:5]), (x[5]), int(x[7:-4])))
print(txtfiles)
print(imgfiles)
right = 0
allfileCount = 0
allfileCount = 3 * len(txtfiles)
for txtfile in txtfiles:
    txt = open(txtdir + txtfile)
    lines = len(txt.readlines()) + 1
    #print(lines)
    imgfile = [imgfile for imgfile in imgfiles if imgfile.startswith(txtfile[:5])]
    a = [a for a in imgfile if a[5] == 'a']
    b = [b for b in imgfile if b[5] == 'b']
    c = [c for c in imgfile if c[5] == 'c']
    if len(a) == lines:
        right += 1
    else:
        print(txtfile[:5] + 'a' + ' has ' + str(lines) +' but ' + str(len(a)) + ' lines')
    if len(b) == lines:
        right += 1
    else:
        print(txtfile[:5] + 'b' + ' has ' + str(lines) +' but ' + str(len(b)) + ' lines')
    if len(c) == lines:
        right += 1
    else:
        print(txtfile[:5] + 'c' + ' has ' + str(lines) +' but ' + str(len(c)) + ' lines')

print(float(right)/allfileCount)