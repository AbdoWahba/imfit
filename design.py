import cv2
import sys
# from PyQt5.QtWidgets import  QWidget, QLabel, QApplication
# from PyQt5.QtCore import QThread, Qt, pyqtSignal, pyqtSlot
# from PyQt5.QtGui import QImage, QPixmap

from functions import *
import globals

class PageWindow(QtWidgets.QMainWindow):
    gotoSignal = QtCore.pyqtSignal(str)

    def goto(self, name):
        self.gotoSignal.emit(name)
    def reset(self):
        globals.x=[]
        globals.y=[]
        globals.xall=[]
        globals.xall2=[]
        globals.yall=[]
        globals.testnet=[]
        globals.t=0
        globals.lasttime=0
        

class MainWindow(PageWindow):
    def __init__(self):
        super().__init__()
        self.title = "main"
        self.left = 150
        self.top = 50
        self.width = 150
        self.height = 150
        self.initUI()

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
        self.pu_label.setText(str(globals.pushupsCount))
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

        self.horizontalGroupBox = QtWidgets.QGroupBox(" ")
        layout = QtWidgets.QGridLayout()
        # layout.setColumnStretch(0, 3)
        layout.setRowStretch(2,4)
        layout.setRowStretch(2, 6)
        layout.setVerticalSpacing(10)
        
        layout.addWidget(self.pushupcount_label,0,1)
        layout.addWidget(self.pu_label,0,2)
        layout.addWidget(self.pushupcountb,0,3)
        layout.addWidget(self.squatscount_label,1,1)
        layout.addWidget(self.sq_label,1,2)
        layout.addWidget(self.squatscountb,1,3)
        layout.addWidget(self.posetest,2,1)
        layout.addWidget(self.posetest_answer,2,2)
        layout.addWidget(self.testb,2,3)

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
                globals.pushupCount=0
                globals.recording=True
                globals.inpushup=True
                
                self.goto("count")
            if button == "squatsCount":
                self.reset()
                globals.squatsCount=0
                globals.recording=True
                globals.insquats=True
                self.goto("count")
        return handleButton

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
        th = Thread(self)
        th.changePixmap.connect(self.setImage)
        th.start()
        #self.show()

class Window(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.left = 150
        self.top = 50
        self.width = 150
        self.height = 150
        globals.init()
        self.initUI()

        self.stacked_widget = QtWidgets.QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.m_pages = {}

        self.register(MainWindow(), "main")
        self.register(countWindow(), "count")

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

if __name__=="__main__":
    App = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(App.exec())