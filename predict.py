#!/usr/bin/python  
#-*- coding:utf-8 -*-  
############################  
#File Name: getHandWritten_result.py
#Author: dengbf 
#Mail: dengbf@rd.netease.com  
#Created Time: 2018-09-12 17:11:01
############################  

import argparse
import youdao_ocr 
import base64
import json
import os
import codecs
import hashlib
import sys
import importlib
importlib.reload(sys)


def txt_wrap_by(start_str, end, html):
        start = html.find(start_str)
        if start >= 0:
            start += len(start_str)
            end = html.find(end, start)
            if end >= 0:
                return html[start:end].strip()
def one_line(region, ypre0, ypre1, ypre2, ypre3 , xpre0, xpre1, x_second):
    y0 = int(region['boundingBox'].split(',')[1])
    y1 = int(region['boundingBox'].split(',')[3])
    y2 = int(region['boundingBox'].split(',')[5])
    y3 = int(region['boundingBox'].split(',')[7])
   # ymin = max(y0, y1)
   # ymax = min(y2, y3)
   # crossmin = max(ymin, ypremin)
   # crossmax = min(ymax, ypremax)
    passed = 0
    x0 = int(region['boundingBox'].split(',')[0])
    x1 = int(region['boundingBox'].split(',')[2])
    x2 = int(region['boundingBox'].split(',')[4])
    x3 = int(region['boundingBox'].split(',')[6])
    if (xpre0 == -1):
        xpre0 = x0
        xpre1 = x1
    x = min(x0, x3)
    width = x1 - x0
    height = y3 - y0
    print(y0)
    if(width < 1.3*height):
        passed = 1
        return (False, ypre0, ypre1, ypre2, ypre3, xpre0, xpre1, passed)
   # if x0 == 275:
#	print(crossmax)
#	print(crossmin)
#	print(ypremax)
#	print(ypremin)
#	print(ymax)
#	print(ymin)
#	print(height)
    xedge = 0
    if (x0<xpre0):
        crossmin = max(ypre0, y1)
        crossmax = min(ypre3, y2)
        xpre = xpre0
        xedge = x1
    else:
        crossmin = max(ypre1, y0)
        crossmax = min(ypre2, y3)
        xpre = xpre1
        xedge = x0
    height = ypre3- ypre0

    if abs(xedge - xpre) >=250:
        if(x0 - x_second)>150:
            passed = 1
            xpre0 = 0
            xpre1 = 0
            return (False, ypre0, ypre1, ypre2, ypre3, xpre0, xpre1, passed)
        return (False, y0, y1, y2, y3, x0,x1, passed)
    if crossmax - crossmin >=0.3*(y3-y0) :
        return (True, y0, y1, y2, y3, x0,  x1, passed)
    if crossmax-crossmin < 0.3*height:
        return (False,y0, y1, y2, y3, x0, x1, passed)
    if (x0 - x_second) <=50:
        return (False, y0, y1, y2, y3, x0, x1, passed)
    return (True, y0, y1, y2, y3, x0, x1, passed)

def parse_img_cont(cont):
    rec_results = list()
    print(cont)
    try:
        result = cont["Result"]
    except:
        return rec_results
    result_json = json.loads(result)
#    r = sorted(result_json.items(), key=lambda x:(int(x['regions']['boundingBox'].split(',')[1]),int(x['regions']['boundingBox'].split(',')[1])))
 #   print(r)
    newregion = list()
    for region in result_json["regions"]:
        for line in region["lines"]:
            region['x'] = int(line["boundingBox"].split(',')[0])
            region['y'] = int(line['boundingBox'].split(',')[1])
   # newregion = dict(newregion)
   # sorted(result_json["regions"].items(), key = lambda x:(x['y'],x['x']))
    result_json["regions"].sort(key = lambda x:(x['y'],x['x']))
    imgCnt = 0
#    print(newregion)
    ypre0 = -1
    ypre1 = -1
    ypre2 = 10000
    ypre3 = 10000
    xpre0= 0
    xpre1 = 0
    whichline = 'a'
    x_second = 10000
    x_first = 10000
    for region in result_json['regions']:
        x0 = int(region['boundingBox'].split(',')[0])
        if(x0 < x_first):
            x_second = x_first
            x_first = x0
        elif(x0 < x_second):
            x_second = x0
 #   print(x_second)
    for region in result_json["regions"]:
        for line in region["lines"]:
            x = region['boundingBox'].split(',')[0]
            (one, ypre0, ypre1, ypre2, ypre3, xpre0, xpre1, passed) = one_line(line, ypre0, ypre1, ypre2, ypre3, xpre0, xpre1, x_second)
            if passed:
                continue
            if 1-one:
                whichline = chr(ord(whichline) + 1)
		
#            for part in line:
               # print part.keys()
	#	print(line.keys())
            img = line["textimg"].strip()
            rec_results.append((img,line["text"],whichline,x))
    return rec_results


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process data generation.')
    parser.add_argument('-i', '--input_file', default='image/img_path.txt')
    parser.add_argument('-o', '--output_file', default='image/res.txt')
    parser.add_argument('-d', '--desDir', default='image/des')
    args = parser.parse_args()
    with codecs.open(args.input_file, encoding='utf-8') as f, codecs.open(args.output_file,'a',encoding='utf-8') as w:
        for i , line in enumerate(f.readlines()):
            if i % 100 == 0:
                print (i)
            imgPath = line.strip().split(" ")[0]
            desDir = os.path.dirname(imgPath) + "_rows" if args.desDir is None else args.desDir
            if not os.path.isdir(desDir):
                os.makedirs(desDir)
            img_name_prefix,img_name_posfix = os.path.splitext(os.path.basename(imgPath))
            new_path = os.path.join(desDir,img_name_prefix + "_" + str(0) + ".jpg")
            if os.path.isfile(new_path):
                continue
            jsonPath = imgPath + ".json"
            cont = youdao_ocr.predict(imgPath)
            #with open(jsonPath,"w") as w_json:
            #    w_json.writelines("{}\n".format(json.dumps(cont)))
            rec_results = parse_img_cont(cont)
            for imgCnt,rec_result in enumerate(rec_results):
                img = rec_result[0]
                txt = rec_result[1]
                line = rec_result[2]
                x = rec_result[3]
                new_path = os.path.join(desDir,img_name_prefix + "_" + line + "_" + x + ".jpg")
                fh = open(new_path , "wb+")
                img = base64.b64decode(img)
                fh.write(img)
                fh.close()
                w.writelines("{} {}\n".format(new_path,txt))
