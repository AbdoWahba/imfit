
from __future__ import print_function
from __future__ import division
import argparse
from math import atan2, cos, sin, sqrt, pi

import numpy as np
import cv2
import time
from matplotlib import pyplot as plt 
import math

from test import *

def drawAxis(img, p_, q_, colour, scale):
    p = list(p_)
    q = list(q_)
    
    angle = atan2(p[1] - q[1], p[0] - q[0]) # angle in radians
    hypotenuse = sqrt((p[1] - q[1]) * (p[1] - q[1]) + (p[0] - q[0]) * (p[0] - q[0]))
    # Here we lengthen the arrow by a factor of scale
    q[0] = p[0] - scale * hypotenuse * cos(angle)
    q[1] = p[1] - scale * hypotenuse * sin(angle)
    cv2.line(img, (int(p[0]), int(p[1])), (int(q[0]), int(q[1])), colour, 1, cv2.LINE_AA)
    # create the arrow hooks
    p[0] = q[0] + 9 * cos(angle + pi / 4)
    p[1] = q[1] + 9 * sin(angle + pi / 4)
    cv2.line(img, (int(p[0]), int(p[1])), (int(q[0]), int(q[1])), colour, 1, cv2.LINE_AA)
    p[0] = q[0] + 9 * cos(angle - pi / 4)
    p[1] = q[1] + 9 * sin(angle - pi / 4)
    cv2.line(img, (int(p[0]), int(p[1])), (int(q[0]), int(q[1])), colour, 1, cv2.LINE_AA)
    
def getOrientation(pts, img):
    
    sz = len(pts)
    data_pts = np.empty((sz, 2), dtype=np.float64)
    for i in range(data_pts.shape[0]):
        data_pts[i,0] = pts[i,0,0]
        data_pts[i,1] = pts[i,0,1]
    # Perform PCA analysis
    mean = np.empty((0))
    mean, eigenvectors, eigenvalues = cv2.PCACompute2(data_pts, mean)
    # Store the center of the object
    cntr = (int(mean[0,0]), int(mean[0,1]))
    
    
    cv2.circle(img, cntr, 3, (255, 0, 255), 2)
    p1 = (cntr[0] + 0.02 * eigenvectors[0,0] * eigenvalues[0,0], cntr[1] + 0.02 * eigenvectors[0,1] * eigenvalues[0,0])
    p2 = (cntr[0] - 0.02 * eigenvectors[1,0] * eigenvalues[1,0], cntr[1] - 0.02 * eigenvectors[1,1] * eigenvalues[1,0])
    drawAxis(img, cntr, p1, (0, 255, 0), 1)
    drawAxis(img, cntr, p2, (255, 255, 0), 5)
    angle = atan2(eigenvectors[0,1], eigenvectors[0,0]) # orientation in radians
    
    return angle*180/pi



#cap=cv2.VideoCapture('https://www.videvo.net/videvo_files/converted/2018_05/preview/180419_Boxing_15_06.mp466556.webm')
#cap = cv2.VideoCapture('/home/asmaa/Downloads/20200501_194209.mp4')
cap=cv2.VideoCapture(0)# live camera
MODEL = DeepLabModel('model/deeplab_model.tar.gz')
fgbg = cv2.createBackgroundSubtractorMOG2()
x=[]
y=[]
xall=[]
xall2=[]
yall=[]
counter=0
testnet=[]
t=0
lasttime=0
while(1):
    
    ret, frame = cap.read()
    if not ret:
      break
    #--------model-------------------------
    im=preprocess(frame)
    resized_im, seg_map = MODEL.run(im)
    seg_image = label_to_color_image(seg_map).astype(np.uint8)
    #cv2.imshow('output', seg_image)
    gray = cv2.cvtColor(seg_image, cv2.COLOR_BGR2GRAY)
    _, bw = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    # print(type(seg_image))
    # print(type(bw))
    # print(seg_image.shape)
    # print(bw.shape)
    # print(seg_image.dtype)
    # print(bw.dtype)
    contours, _ = cv2.findContours(bw, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    pcas=[]
    for i, c in enumerate(contours):
        # Calculate the area of each contour
        area = cv2.contourArea(c)
        # Ignore contours that are too small or too large
        if area < 1e3 or 1e8 < area:
            continue
        # Draw each contour only for visualisation purposes
        cv2.drawContours(seg_image, contours, i, (0, 0, 255), 2)
        # Find the orientation of each shape
        angle=getOrientation(c, seg_image)
        pcas.append(angle)
    cv2.imshow('output', seg_image)
    print(np.average(pcas))
    if (np.average(pcas)>=80):print('up')
    else:print('down')

    #--------------------------------------
    fgmask = fgbg.apply(frame)
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(fgmask,str(counter),(0,130), font, 5, (255, 0, 0), 4, cv2.LINE_AA)
    cv2.imshow('frame', fgmask) 
    x.append(t)
    t=t+1
    point=np.average(np.where(fgmask==255), axis=1)
    y.append(point)
    xall.append(point[0])
    yall.append(point[1])

    #------------test------------------
    if(not np.isnan(point[0])):
        meanx= 0 if (len(xall)<=0)  else np.nanmean(xall)
        meany= 0 if (len(yall)<=0) else np.nanmean(yall)
        xall2=xall.copy()+meany-meanx 
        #print(min(yall))
        net=xall2+yall
        mean= 0 if (len(yall)<=1) else np.nanmean(net)
        if(point[0]+meany-meanx+point[1] >= mean):
            if(len(testnet)>0 and testnet[-1]==0):
                print (x[-1]-lasttime)
                if(lasttime==0):
                    #counter=counter+1
                    lasttime=x[-1]
                elif(x[-1]-lasttime >= 20):# 20/30 if in live mode 100 if video
                    counter=counter+1
                    lasttime=x[-1]
                    print(counter)
                print('--------------')
            testnet.append(1)
        else:
            testnet.append(0)
    
    if cv2.waitKey(1) & 0xFF == ord('q'): 
        break
    #-------------------


cap.release()
print(counter)
print(mean)
#print(xall)
#------------------------------------------------------------
# meanx=np.nanmean(xall)
# meany=np.nanmean(yall)
# xall=xall+meany-meanx 
# #print(min(yall))
# net=xall2+yall
# meannet=np.nanmean(net)
# print('--------------')
# print(meannet)
#-------------------------------------
# for i in range(len(net)):
#   if net[i] >= meannet:
#     net[i]=1
#   else:
#     net[i]=0
# plt.plot(x,xall)
# plt.plot(x,yall)
#.plot(x,y)
plt.subplot(3, 1, 1)
plt.plot(x,yall)
plt.plot(x,xall)
plt.subplot(3, 1, 2)
plt.plot(x,testnet)
plt.subplot(3, 1, 3)
plt.plot(x,net)

plt.show()

#print(y)
cv2.destroyAllWindows()




      
