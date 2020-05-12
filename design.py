import cv2
import sys
# from PyQt5.QtWidgets import  QWidget, QLabel, QApplication
# from PyQt5.QtCore import QThread, Qt, pyqtSignal, pyqtSlot
# from PyQt5.QtGui import QImage, QPixmap

from functions import *
from posethread import *
import globals

class PageWindow(QtWidgets.QMainWindow):
    gotoSignal = QtCore.pyqtSignal(str)
    updatesignal=QtCore.pyqtSignal(str)

    def goto(self, name):
        self.gotoSignal.emit(name)
        self.updatesignal.emit(name)
    def reset(self):
        globals.x=[]
        globals.y=[]
        globals.xall=[]
        globals.xall2=[]
        globals.yall=[]
        globals.testnet=[]
        globals.t=0
        globals.lasttime=0
        
#------------main window widget for opencv------------------------
class MainWindow(PageWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        #print("in main")
        self.update()
        self.title = "main"
        self.left = 150
        self.top = 50
        self.width = 150
        self.height = 150
        self.initUI()   
    

    def updatelabels(self):
        self.pu_label.setText(f"{globals.pushupsCount}")
        self.sq_label.setText(f"{globals.squatscount}")


    def initUI(self):
        self.UiComponents()
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.resize(800, 600)
        self.label = QLabel(self)
        self.label.move(80, 80)


    def UiComponents(self):
        self.pushupcountb = QtWidgets.QPushButton('start Push-Ups',self)
        self.pushupcountb.move(550,150)
        self.pushupcountb.resize(150,60)
        self.pushupcountb.setFixedHeight(60)
        self.pushupcountb.setStyleSheet("""QPushButton{
            background-color: darkBlue;
            border-style: outset;
            border-width: 1px;
            border-radius: 10px;
            border-color: beige;
            font: bold 14px;
            min-width: 10em;
            padding: 6px;
            color: white
            }""")
        self.pushupcountb.clicked.connect(self.make_handleButton("pushupCount"))

        self.squatscountb = QtWidgets.QPushButton('start Squats',self)
        self.squatscountb.move(550,230)
        self.squatscountb.resize(150,60)
        self.squatscountb.setFixedHeight(60)
        self.squatscountb.setStyleSheet("""QPushButton{
            background-color: darkBlue;
            border-style: outset;
            border-width: 1px;
            border-radius: 10px;
            border-color: beige;
            font: bold 14px;
            min-width: 10em;
            padding: 6px;
            color: white
            }""")
        self.squatscountb.clicked.connect(self.make_handleButton("squatsCount"))
        

        self.empty= QtWidgets.QLabel(self)
        self.empty.setText(' ')

        self.pushupcount_label = QtWidgets.QLabel(self)
        self.pushupcount_label.setText('Push-up count')
        self.pushupcount_label.setStyleSheet("""QLabel{
            font: bold 14px;
            min-width: 10em;
            padding: 6px;
            }""")
        
        self.pu_label = QtWidgets.QLabel(self)
        self.pu_label.setText(f'{globals.pushupsCount}')
        self.pu_label.setStyleSheet("""QLabel{
            font: bold 14px;
            min-width: 10em;
            padding: 6px;
            }""")

        self.squatscount_label = QtWidgets.QLabel(self)
        self.squatscount_label.setText('squats count')
        self.squatscount_label.setStyleSheet("""QLabel{
            font: bold 14px;
            min-width: 10em;
            padding: 6px;
            }""")

        self.sq_label = QtWidgets.QLabel(self)
        self.sq_label.setText(str(globals.squatscount))
        self.sq_label.setStyleSheet("""QLabel{
            font: bold 14px;
            min-width: 10em;
            padding: 6px;
            }""")

        self.gotoPose= QtWidgets.QPushButton('openPose model',self)
        self.gotoPose.move(550,230)
        self.gotoPose.resize(150,60)
        self.gotoPose.setFixedHeight(60)
        self.gotoPose.setStyleSheet("""QPushButton{
            background-color: darkBlue;
            border-style: outset;
            border-width: 1px;
            border-radius: 10px;
            border-color: beige;
            font: bold 14px;
            min-width: 10em;
            padding: 6px;
            color: white
            }""")
        self.gotoPose.clicked.connect(self.make_handleButton("gotoPose"))

        self.horizontalGroupBox = QtWidgets.QGroupBox(" ")
        layout = QtWidgets.QGridLayout()
        # layout.setColumnStretch(0, 3)
        layout.setRowStretch(2,4)
        layout.setRowStretch(2, 6)
        layout.setVerticalSpacing(10)
        
        layout.addWidget(self.empty,0,1)
        layout.addWidget(self.empty,0,2)
        layout.addWidget(self.gotoPose,0,3)
        layout.addWidget(self.empty,1,1)
        layout.addWidget(self.empty,1,2)
        layout.addWidget(self.empty,1,3)
        layout.addWidget(self.pushupcount_label,2,1)
        layout.addWidget(self.pu_label,2,2)
        layout.addWidget(self.pushupcountb,2,3)
        layout.addWidget(self.squatscount_label,3,1)
        layout.addWidget(self.sq_label,3,2)
        layout.addWidget(self.squatscountb,3,3)
        layout.addWidget(self.empty,4,1)
        layout.addWidget(self.empty,4,2)
        layout.addWidget(self.empty,4,3)
        

        layout.addWidget(self.empty,0,0)
        layout.addWidget(self.empty,1,0)
        layout.addWidget(self.empty,2,0)

        layout.addWidget(self.empty,0,4)
        layout.addWidget(self.empty,1,4)
        layout.addWidget(self.empty,2,4)

        self.setCentralWidget(self.horizontalGroupBox)
        self.horizontalGroupBox.setLayout(layout)


    def make_handleButton(self, button):
        def handleButton():
            if button == "pushupCount":
                self.reset()
                globals.pushupsCount=0
                globals.recording=True
                globals.inpushup=True
                
                self.goto("count")
            if button == "squatsCount":
                self.reset()
                globals.squatscount=0
                globals.recording=True
                globals.insquats=True
                self.goto("count")
            if button == "gotoPose":
                self.goto("openPose")
        return handleButton


#----------------------main window for openpose------------------
class MainPoseWindow(PageWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        #print("in main")
        self.update()
        self.title = "main"
        self.left = 150
        self.top = 50
        self.width = 150
        self.height = 150
        self.initUI()   
    

    def updatelabels(self):
        self.pu_label.setText(f"{globals.pushupsCount}")
        self.posetest_answer.setText(f"{globals.poseState}")


    def initUI(self):
        self.UiComponents()
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.resize(800, 600)
        self.label = QLabel(self)
        self.label.move(80, 80)


    def UiComponents(self):
        self.pushupcountb = QtWidgets.QPushButton('start Push-Ups',self)
        self.pushupcountb.move(550,150)
        self.pushupcountb.resize(150,60)
        self.pushupcountb.setFixedHeight(60)
        self.pushupcountb.setStyleSheet("""QPushButton{
            background-color: darkBlue;
            border-style: outset;
            border-width: 1px;
            border-radius: 10px;
            border-color: beige;
            font: bold 14px;
            min-width: 10em;
            padding: 6px;
            color: white
            }""")
        self.pushupcountb.clicked.connect(self.make_handleButton("openPosecount"))
      
        self.testb = QtWidgets.QPushButton('test Pose',self)
        self.testb.move(550,310)
        self.testb.resize(150,60)
        self.testb.setFixedHeight(60)
        self.testb.setStyleSheet("""QPushButton{
            background-color: darkBlue;
            border-style: outset;
            border-width: 1px;
            border-radius: 10px;
            border-color: beige;
            font: bold 14px;
            min-width: 10em;
            padding: 6px;
            color: white
            }""")

        self.empty= QtWidgets.QLabel(self)
        self.empty.setText(' ')

        self.pushupcount_label = QtWidgets.QLabel(self)
        self.pushupcount_label.setText('Push-up count')
        self.pushupcount_label.setStyleSheet("""QLabel{
            font: bold 14px;
            min-width: 10em;
            padding: 6px;
            }""")
        
        self.pu_label = QtWidgets.QLabel(self)
        self.pu_label.setText(f'{globals.pushupsCount}')
        self.pu_label.setStyleSheet("""QLabel{
            font: bold 14px;
            min-width: 10em;
            padding: 6px;
            }""")

        self.posetest = QtWidgets.QLabel(self)
        self.posetest.setText('pose state')
        self.posetest.setStyleSheet("""QLabel{
            font: bold 14px;
            min-width: 10em;
            padding: 6px;
            }""")

        self.posetest_answer = QtWidgets.QLabel(self)
        self.posetest_answer.setText('correct')
        self.posetest_answer.setStyleSheet("""QLabel{
            font: bold 14px;
            min-width: 10em;
            padding: 6px;
            }""")

        self.gotomain= QtWidgets.QPushButton('openCV',self)
        self.gotomain.move(550,230)
        self.gotomain.resize(150,60)
        self.gotomain.setFixedHeight(60)
        self.gotomain.setStyleSheet("""QPushButton{
            background-color: darkBlue;
            border-style: outset;
            border-width: 1px;
            border-radius: 10px;
            border-color: beige;
            font: bold 14px;
            min-width: 10em;
            padding: 6px;
            color: white
            }""")
        self.gotomain.clicked.connect(self.make_handleButton("main"))

        self.horizontalGroupBox = QtWidgets.QGroupBox(" ")
        layout = QtWidgets.QGridLayout()
        # layout.setColumnStretch(0, 3)
        layout.setRowStretch(2,4)
        layout.setRowStretch(2, 6)
        layout.setVerticalSpacing(10)
        
        layout.addWidget(self.empty,0,1)
        layout.addWidget(self.empty,0,2)
        layout.addWidget(self.gotomain,0,3)
        layout.addWidget(self.empty,1,1)
        layout.addWidget(self.empty,1,2)
        layout.addWidget(self.empty,1,3)
        layout.addWidget(self.pushupcount_label,2,1)
        layout.addWidget(self.pu_label,2,2)
        layout.addWidget(self.pushupcountb,2,3)
        layout.addWidget(self.posetest,3,1)
        layout.addWidget(self.posetest_answer,3,2)
        layout.addWidget(self.testb,3,3)
        layout.addWidget(self.empty,4,1)
        layout.addWidget(self.empty,4,2)
        layout.addWidget(self.empty,4,3)

        layout.addWidget(self.empty,0,0)
        layout.addWidget(self.empty,1,0)
        layout.addWidget(self.empty,2,0)

        layout.addWidget(self.empty,0,4)
        layout.addWidget(self.empty,1,4)
        layout.addWidget(self.empty,2,4)

        self.setCentralWidget(self.horizontalGroupBox)
        self.horizontalGroupBox.setLayout(layout)


    def make_handleButton(self, button):
        def handleButton():
            if button == "openPosecount":
                self.goto("openPosecount")
            if button == "main":
                self.goto("main")
        return handleButton

#------------------recording window for opencv-----------------------
class countWindow(PageWindow):
    def __init__(self):
        super().__init__()
        self.title = "live"
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
        
        self.backb= QtWidgets.QPushButton('back',self)
        self.backb.move(570,570)
        self.backb.resize(150,60)
        self.backb.setFixedHeight(60)
        self.backb.setStyleSheet("""QPushButton{
            background-color: darkBlue;
            border-style: outset;
            border-width: 1px;
            border-radius: 10px;
            border-color: beige;
            font: bold 14px;
            min-width: 10em;
            padding: 6px;
            color: white
            }""")
        self.backb.clicked.connect(self.make_handleButton("back"))
        

        self.th = Thread(self)
        self.th.changePixmap.connect(self.setImage)
    def startth(self):
        self.th.start()
        #self.show()
    def killth(self):
        #print('inkill')
        self.th.quit()
    def make_handleButton(self, button):
        def handleButton():
            if button == "back":
                self.reset()
                #print(globals.pushupsCount)
                globals.recording=False
                if(globals.inpushup):
                    globals.inpushup=False
                elif(globals.insquats):
                    globals.insquats=False

                
                self.goto("main")
        return handleButton

#-------------------recording openPose---------------------------------
class countOpenPoseWindow(PageWindow):
    def __init__(self):
        super().__init__()
        self.title = "live"
        self.left = 150
        self.top = 50
        self.width = 150
        self.height = 150
        self.initUI()

    @pyqtSlot(QImage)
    def setImage(self, image):
        self.label.setPixmap(QPixmap.fromImage(image))
        if globals.show_msg['type'] == 'success':
            self.msg.setStyleSheet("""QLabel{
            font: bold 14px;
            color:green;
            min-width: 10em;
            padding: 6px;
            }""")
            self.msg.setText(f"{globals.show_msg['content']}")
        elif globals.show_msg['type'] == 'error':
            self.msg.setStyleSheet("""QLabel{
            font: bold 14px;
            color:red;
            min-width: 10em;
            padding: 6px;
            }""")
            self.msg.setText(f"{globals.show_msg['content']}")

        

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.resize(800, 700)
        # create a label
        self.label = QLabel(self)
        self.label.move(80, 80)
        self.label.resize(640, 480)

        self.msg= QtWidgets.QLabel(self)
        self.msg.setText(f"{globals.show_msg['content']}")
        self.label.move(100, 570)

        self.backb= QtWidgets.QPushButton('back',self)
        self.backb.move(570,570)
        self.backb.resize(150,60)
        self.backb.setFixedHeight(60)
        self.backb.setStyleSheet("""QPushButton{
            background-color: darkBlue;
            border-style: outset;
            border-width: 1px;
            border-radius: 10px;
            border-color: beige;
            font: bold 14px;
            min-width: 10em;
            padding: 6px;
            color: white
            }""")
        self.backb.clicked.connect(self.make_handleButton("back"))
        

        self.th = poseThread(self)
        self.th.changePixmap.connect(self.setImage)
    def startth(self):
        self.th.start()
        #self.show()
    def killth(self):
        #print('inkill')
        self.th.quit()
    def make_handleButton(self, button):
        def handleButton():
            if button == "back":
                globals.recording=False
                self.goto("openPose")
        return handleButton


class Window(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.left = 150
        self.top = 50
        self.width = 150
        self.height = 150
        globals.init()
        self.initUI()
        self.updatesignal1=QtCore.pyqtSignal(str)

        self.stacked_widget = QtWidgets.QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.m_pages = {}

        self.register(MainWindow(), "main")
        self.register(countWindow(), "count")
        self.register(MainPoseWindow(), "openPose")
        self.register(countOpenPoseWindow(), "openPosecount")
        #self.register(countWindow(), "testimage")

        self.goto("main")

    def initUI(self):
        #self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.resize(800, 700)
        # create a label
        self.label = QLabel(self)
        self.label.move(80, 80)
        self.label.resize(640, 480)

    def register(self, widget, name):
        self.m_pages[name] = widget
        self.stacked_widget.addWidget(widget)
        if isinstance(widget, PageWindow):
            widget.gotoSignal.connect(self.goto)  


    @QtCore.pyqtSlot(str)
    def goto(self, name):
        if name in self.m_pages:
            widget = self.m_pages[name]
            self.stacked_widget.setCurrentWidget(widget)
            self.setWindowTitle(widget.windowTitle())
            if name=="main":
                widget.updatelabels()
                w2=self.m_pages["count"]
                w2.killth()
            elif name =="count":
                globals.quitcap=False
                widget.startth()
            elif name=="openPose":
                widget.updatelabels()
                w2=self.m_pages["openPosecount"]
                w2.killth()
            elif name =="openPosecount":
                globals.quitcapPose=False
                widget.startth()

if __name__=="__main__":
    App = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(App.exec())