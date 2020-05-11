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
        self.pushupcount = QtWidgets.QPushButton('start Push-Ups',self)
        self.pushupcount.move(550,150)
        self.pushupcount.resize(150,60)
        self.pushupcount.clicked.connect(self.make_handleButton("pushupCount"))
        


    def make_handleButton(self, button):
        def handleButton():
            if button == "pushupCount":
                globals.recording=True
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