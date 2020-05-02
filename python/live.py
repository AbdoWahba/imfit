import numpy as np
import cv2
import time
from matplotlib import pyplot as plt 
import math



cap=cv2.VideoCapture('https://www.videvo.net/videvo_files/converted/2018_05/preview/180419_Boxing_15_06.mp466556.webm')
#cap=cv2.VideoCapture(0)# live camera

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
        mean= np.nanmean(net)
        if(point[0]+meany-meanx+point[1] >= mean):
            if(len(testnet)>0 and testnet[-1]==0):
                print (x[-1]-lasttime)
                if(x[-1]-lasttime >= 30):# 30 if in live mode 100 if video
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
  

      
