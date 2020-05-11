import numpy as np
import time
from matplotlib import pyplot as plt 
import math

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import  QWidget, QLabel, QApplication
from PyQt5.QtCore import QThread, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QImage, QPixmap
 
from design import *

class Thread(QThread):
    changePixmap = pyqtSignal(QImage)

    def run(self):
        cap = cv2.VideoCapture(0)
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
        while True:
            if(globals.recording):
                ret, frame = cap.read()
                if ret:
                    # rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    # h, w, ch = rgbImage.shape
                    # bytesPerLine = ch * w
                    # convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
                    # p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
                    #--------------------------
                    fgmask = fgbg.apply(frame)
                    # font = cv2.FONT_HERSHEY_SIMPLEX
                    # cv2.putText(fgmask,str(counter),(0,130), font, 5, (255, 0, 0), 4, cv2.LINE_AA)
                    x.append(t)
                    t=t+1
                    point=np.average(np.where(fgmask==255), axis=1)
                    y.append(point)
                    xall.append(point[0])
                    yall.append(point[1])
                    if(not np.isnan(point[0])):
                        meanx= 0 if (len(xall)<=0)  else np.nanmean(xall)
                        meany= 0 if (len(yall)<=0) else np.nanmean(yall)
                        xall2=xall.copy()+meany-meanx 
                        #print(min(yall))
                        net=xall2+yall
                        mean= 0 if (len(yall)<=1) else np.nanmean(net)
                        if(point[0]+meany-meanx+point[1] >= mean):
                            if(len(testnet)>0 and testnet[-1]==0):
                                #print (x[-1]-lasttime)
                                if(lasttime==0):
                                    counter=counter+1
                                    lasttime=x[-1]
                                elif(x[-1]-lasttime >= 20):# 20/30 if in live mode 100 if video
                                    counter=counter+1
                                    lasttime=x[-1]
                                    #print(counter)
                                #print('--------------')
                            testnet.append(1)
                        else:
                            testnet.append(0)
                #---------------------------
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(frame,str(counter),(0,130), font, 5, (255, 0, 0), 4, cv2.LINE_AA)
                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgbImage.shape
                bytesPerLine = ch * w
                convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
                p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
                self.changePixmap.emit(p)