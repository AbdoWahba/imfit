import numpy as np
import time
from matplotlib import pyplot as plt 
import math
#from PIL import Image

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
        t0 = time.time()
        font = cv2.FONT_HERSHEY_SIMPLEX
        
        while globals.quitcap==False :

            if(globals.recording ):
                ret, frame = cap.read()
                if ret and time.time()-t0>6:
                    fgmask = fgbg.apply(frame)
                    t= globals.t
                    globals.x.append(t)
                    t=t+1
                    point=np.average(np.where(fgmask==255), axis=1)
                    globals.y.append(point)
                    globals.xall.append(point[0])
                    globals.yall.append(point[1])
                    if(not np.isnan(point[0])):
                        meanx= np.nanmean(globals.xall)
                        meany= np.nanmean(globals.yall)
                        globals.xall2=globals.xall.copy()+meany-meanx 
                        #print(min(yall))
                        net=globals.xall2+globals.yall
                        if(t<20 or t%20==0 ):
                            mean= np.nanmean(net)
                        if(point[0]+meany-meanx+point[1] >= mean):
                            if(len(globals.testnet)>0 and globals.testnet[-1]==0):
                                #print (x[-1]-lasttime)
                                if(globals.lasttime==0):
                                    if(globals.inpushup):
                                        globals.pushupsCount=globals.pushupsCount+1
                                        globals.lasttime=globals.x[-1]
                                    elif(globals.insquats):
                                        globals.squatscount=globals.squatscount+1
                                        globals.lasttime=globals.x[-1]
                                elif(globals.x[-1]-globals.lasttime >= 20):# 20/30 if in live mode 100 if video
                                    if(globals.inpushup):
                                        globals.pushupsCount=globals.pushupsCount+1
                                        globals.lasttime=globals.x[-1]
                                    elif(globals.insquats):
                                        globals.squatscount=globals.squatscount+1
                                        globals.lasttime=globals.x[-1]
                                    #print(counter)
                                #print('--------------')
                            globals.testnet.append(1)
                        else:
                            globals.testnet.append(0)

                    # if(globals.pushupsCount > 3 and net[-1]>=max(net)+50):
                    #     print('out?')
                #---------------------------
                else :
                    cv2.putText(frame,str(5-int(time.time()-t0)),(int(frame.shape[0]/2+10),int(frame.shape[1]/2-10)), font, 5, (255, 0, 0), 4, cv2.LINE_AA)
                    frame= cv2.circle(frame, (int(frame.shape[0]/2+55),int(frame.shape[1]/2-55)), 80, (255, 0, 0), 4)
                    cv2.putText(frame,"get ready",(int(frame.shape[0]/2-90),int(frame.shape[1]/2+70)), font, 2, (255, 0, 0), 4, cv2.LINE_AA)

                #-----------------------
                
                if(globals.inpushup):
                    cv2.putText(frame,str(globals.pushupsCount),(0,130), font, 5, (255, 0, 0), 4, cv2.LINE_AA)
                if(globals.insquats):
                    cv2.putText(frame,str(globals.squatscount),(0,130), font, 5, (255, 0, 0), 4, cv2.LINE_AA)
                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgbImage.shape
                bytesPerLine = ch * w
                convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
                p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
                self.changePixmap.emit(p)

        cap.release()

    def quit(self):
        globals.quitcap=True  


# def preprocess(image):
#   #print(type(image))
#   img = np.array(image)
#   mean = 0
#   gauss = np.random.normal(mean, 1, img.shape)

#   noisy = img + gauss
#   minv = np.amin(noisy)
#   maxv = np.amax(noisy)
#   noisy = (255 * (noisy - minv) / (maxv - minv)).astype(np.uint8)

#   im = Image.fromarray(noisy)
#   return(im)