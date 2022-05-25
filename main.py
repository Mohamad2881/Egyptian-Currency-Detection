import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from currency_detector import siftDetector
import pyttsx3


path = './Resources/reference'


class CurDet(QWidget):
    def __init__(self, parent=None):
        ###################################################
        self.sft = siftDetector(path)
        self.deslist, self.imgNames = self.sft.findDes()
        print(self.imgNames)
        ###################################################
        super(CurDet, self).__init__(parent)

        layout = QFormLayout()

        browseBTN = QPushButton('Browse', self)
        browseBTN.move(115, 350)
        browseBTN.setFixedSize(120, 70)
        browseBTN.setFont(QFont('Times', 15))
        browseBTN.clicked.connect(self.getfile)
        browseBTN.setToolTip('Browse an image ...')
        browseBTN.setStyleSheet('background-color:#CACFD6;')

        self.img = QLabel("")
        self.img.setPixmap(QPixmap('currency.jpg').scaled(480, 240))
        layout.addWidget(self.img)

        self.detimgLBL = QLabel('', self)
        self.detimgLBL.setGeometry(350, 260, 100, 50)
        self.detimgLBL.setFont(QFont('Times', 22))
        self.detimgLBL.setStyleSheet("background-color:#DCD6F7;")
        self.detimgLBL.setToolTip("Currency name appears here ...")
        layout.addWidget(self.detimgLBL)

        detectBTN = QPushButton('Detect', self)
        # detectBTN.move(390, 300)
        detectBTN.move(370, 350)
        detectBTN.setFixedSize(120, 70)
        detectBTN.setFont(QFont('Times', 15))
        detectBTN.clicked.connect(self.detect)
        detectBTN.setToolTip('Currency Detection ...')
        detectBTN.setStyleSheet('background-color:#CACFD6;')

        self.setLayout(layout)
        # self.setFixedSize(500, 360)
        self.setFixedSize(640, 480)
        self.setStyleSheet("background-color: #A6B1E1;")
        self.setWindowIcon(QIcon('cd.png'))
        self.setWindowTitle("Currency Detector")

    def getfile(self):
        # fname = QFileDialog.getOpenFileName(self, 'Open file', 'c:\\', "Image files (*.jpg *.gif)")
        fname = QFileDialog.getOpenFileName(self, "Choose Pic", ".\Resources\\Test",
                                                        "images ( *.png *.jpg )")
        self.fname = fname[0]
        # self.ui.label_pic.setPixmap(QPixmap(self.fname))

        if fname[0] == '':
            self.img.setPixmap(QPixmap('currency.jpg').scaled(480, 240))
        else:
            self.img.setPixmap(QPixmap(fname[0]).scaled(480, 240))

    def detect(self):
        # self.detimgLBL.setText("It is a photo of: ")
        # playsound('80.mp3')
        try:
            print("_____________")
            # print(self.id)
            self.id = self.sft.findID(self.deslist, self.fname, 50)
            # print(self.id)
            if self.id != -1:
                self.res = self.imgNames[self.id][:-1]
                self.saytext = self.res + " egyptian pound"
            else:
                self.res = "Detection failed"
                self.saytext = self.res

            self.detimgLBL.setText(self.res+" EGP")
            # self.ui.label.setText(self.res)
            engine = pyttsx3.init()
            engine.say(self.saytext)
            engine.runAndWait()

        except:
            pass


def main():
    app = QApplication(sys.argv)
    ex = CurDet()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
