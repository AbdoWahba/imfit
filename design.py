import cv2
import sys
# from PyQt5.QtWidgets import  QWidget, QLabel, QApplication
# from PyQt5.QtCore import QThread, Qt, pyqtSignal, pyqtSlot
# from PyQt5.QtGui import QImage, QPixmap

from functions import *

# class Thread(QThread):
#     changePixmap = pyqtSignal(QImage)

#     def run(self):
#         cap = cv2.VideoCapture(0)
#         fgbg = cv2.createBackgroundSubtractorMOG2()
#         x=[]
#         y=[]
#         xall=[]
#         xall2=[]
#         yall=[]
#         counter=0
#         testnet=[]
#         t=0
#         lasttime=0
#         while True:
#             ret, frame = cap.read()
#             if ret:
#                 rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#                 h, w, ch = rgbImage.shape
#                 bytesPerLine = ch * w
#                 convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
#                 p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
#                 self.changePixmap.emit(p)


class window(QWidget):
    def __init__(self):
        super().__init__()
        self.title = "Scheduler"
        self.left = 150
        self.top = 50
        self.width = 150
        self.height = 150
        self.initUI()

    @pyqtSlot(QImage)
    def setImage(self, image):
        self.label.setPixmap(QPixmap.fromImage(image))

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.resize(800, 700)
        # create a label
        self.label = QLabel(self)
        self.label.move(80, 80)
        self.label.resize(640, 480)
        th = Thread(self)
        th.changePixmap.connect(self.setImage)
        th.start()
        self.show()

if __name__=="__main__":
    App = QApplication(sys.argv)
    window = window()
    sys.exit(App.exec())