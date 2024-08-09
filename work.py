import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic
from sourceselect import Sourseselection
import icon_rc
import dc_opt_rc

#ui 파일 연결시 코드파일과 같은 디렉토리에 있어야함
form_class= uic.loadUiType("circuit_simul.ui")[0]


#화면을 띄우는데 사용되는 Class 선언
class WindowClass(QMainWindow, form_class):
    def __init__(self) :
        super().__init__()
        self.setupUi(self)
        self.source.clicked.connect(self.show_source)

    def show_source(self):
        self.w = Sourseselection()
        self.w.show()
        


if __name__ == "__main__" :
    app = QApplication(sys.argv)         #QApplication : 프로그램을 실행시켜주는 클래스
    myWindow = WindowClass()             #WindowClass의 인스턴스 생성
    myWindow.show()                      #프로그램 화면을 보여주는 코드
    app.exec_()                          #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
