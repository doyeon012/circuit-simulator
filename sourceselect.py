import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic
from dc_opt import DC_opt as DC




form_class= uic.loadUiType("sourceselect.ui")[0]

class Sourseselection(QMainWindow,form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.dcsource.clicked.connect(self.show_dc)
    def show_dc(self):
        self.w = DC()
        self.w.show()



    

if __name__ == "__main__" :
    app = QApplication(sys.argv)         #QApplication : 프로그램을 실행시켜주는 클래스
    myWindow = Sourseselection()             #WindowClass의 인스턴스 생성
    myWindow.show()                      #프로그램 화면을 보여주는 코드
    app.exec_()                          #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
