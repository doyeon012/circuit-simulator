
# 필요한 라리브러리 및 모듈 임포트
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic
from qrc_file import icon_rc, device_icon, finish_btn
import time, traceback
import numpy as np
import matplotlib.pyplot as plt
import pdb
import math

# 유틸리티 함수들
def sin_wave(dc,amp,freq,time):
    return amp*np.sin(2*np.pi*freq*time)+dc

#노드정렬.
def node_sort(wires):
    node_list = [k[1] for k in wires]
    print('node 리스트:',node_list)
    connect = []
    called_node = []
    calling_node = []
    connect_node = []
    for node in node_list:
        for wire in wires:
            if wire[0] == node:
                if node in called_node:
                    pass
                else:
                    called_node.append(node)
            elif wire[2] == node:
                if node in called_node:
                    pass
                else:
                    called_node.append(node)
            elif wire[1] == node:  #본인 노드에 본인 노드빼고 다연결한 친구.
                if node in connect:
                    pass
                else:
                    connect.append(node)
            #본인의 노드가 아니면서 다른애들의 노드가 있는 놈 탐색.
            my_node = wire[1]
            if my_node in calling_node:
                pass
            else:
                if wire[0] != my_node and 'node' in wire[0]:
                    temp = wire[0] + '-' + my_node
                    calling_node.append(my_node)
                    connect_node.append(temp)
                elif wire[2] != my_node and 'node' in wire[2]:
                    temp = wire[2] + '-' + my_node
                    calling_node.append(my_node)
                    connect_node.append(temp)
                    
    print("다른녀석(연결선)한테 불린녀석..(called_node):",called_node)
    print('전부 다른 놈들한테 연결한놈.(connect):',connect)
    print("다른 녀석(연결선) 부른 놈들.(calling_node):",calling_node)
    print('불린녀석 - 부른녀석(connect_node):',connect_node)
    return called_node,connect,calling_node,connect_node

# 주어진 리스트 'register'을 순회하면서 각 요소에서 특정 패턴에 따라 값을 처리하여 새로운 리스트 'result'에 저장
def temp_to_register(register):
    
    # 최종 결과를 저장할 리스트 초기화
    result = []
    
    # 주어진 리스트 'register'의 각 요소를 순회
    for k in register:
        
        # 임시 리스트 초기화 (각 k의 처리 결과를 임시로 저장)
        tmp =[]
        
        # 만약 k가 리스트인 경우
        if type(k) is list:
            
            # k의 각 요소를 순회
            for i in k:
                # 요소가 'V'를 포함하고 있다면 (특정 패턴을 찾는 작업)
                if 'V' in i:
                    tmp.append(i) # 그대로 임시 리스트에 추가
                else:
                    # '_'를 기준으로 문자열을 나누고, 첫 번째 부분(접두사)만 취함
                    name = i.split('_')[0]
                    tmp.append(name) # 접두사만 임시 리스트에 추가
        
        # k가 리스트가 아닌 경우
        elif k is not list:
            
            # 요소가 'V'를 포함하고 있다면
            try:
                
                if 'V' in k:
                    tmp.append(k) # 그대로 임시 리스트에 추가
                    
                else:
                    # '_'를 기준으로 문자열을 나누고, 첫 번째 부분만 취함
                    name = k.split('_')[0]
                    tmp.append(name) # 접두사만 임시 리스트에 추가
                    
            except:
                # 예외가 발생할 경우 (예: k가 문자열이 아닌 경우) 아무 작업도 하지 않음
                pass
            
        # 각 k에 대한 처리가 완료된 후, tmp를 최종 결과 리스트에 추가    
        result.append(tmp)
    
     # 최종 결과 리스트 반환
    return result

#재귀함수 순서구분없이 실행
def sum_one(sum_dict,register,name_cnt,wires,connect_node):
    if len(connect_node):#시작조건.
        temp = []
        sentence = connect_node.pop()  #'node1-node2' 형식. 재사용 막기.
        wire_merge = sentence.split('-')
        
        for node in wire_merge:   #node == 'node1' 형식.
            for wire in wires:
                if node == wire[1]: #찾음.
                    delete = wire
                    if 'node' in wire[0]:
                        if 'node' in wire[2]:
                            pass
                        else:
                            if wire[2] in temp:
                                pass
                            else:
                                temp.append(wire[2])
                                
                        pass
                    elif 'node' in wire[2]:  #wire[0]은 확정적으로 node가 아님.
                        if wire[0] in temp:
                            pass
                        else:
                            temp.append(wire[0])
                        pass
                    else: #wire[0] 과 wire[2] 모두 node 가아님.
                        if wire[0] in temp:
                            pass
                        else:
                            temp.append(wire[0])
                        if wire[2] in temp:
                            pass
                        else:
                            temp.append(wire[2])
                    wires.remove(delete) #사용된 node는 삭제.
        name_cnt+=1
        name = 'connect'+str(name_cnt)
        sum_dict[name] = temp
        aa= temp_to_register(temp)
        register.append(aa)
        #register.append(temp)
        temp = []
        sum_dict,register,name_cnt,wires,connect_node = sum_one(sum_dict,register,name_cnt,wires,connect_node)
        return sum_dict,register,name_cnt,wires,connect_node
        pass
    
    elif len(wires):#시작조건2 #이단계에서는 병렬 연결없음. 직렬연결밖에안남음.(device, node , device) 형식.
        name_cnt+=1
        name = 'connect'+str(name_cnt)
        wire = wires.pop() #재사용 막기.
        temp = []
        temp.append(wire[0])
        temp.append(wire[2])
        sum_dict[name] = temp
        aa= temp_to_register(temp)
        register.append(aa)
        #register.append(temp)
        sum_dict,register,name_cnt,wires,connect_node = sum_one(sum_dict,register,name_cnt,wires,connect_node)
        return sum_dict,register,name_cnt,wires,connect_node
        pass
    else:#w종료조건.
        return sum_dict,register,name_cnt,wires,connect_node


# 주어진 'register' 리스트를 순회하면서 병렬 및 직렬 연결된 요소들을 구분하여 최종적으로 직렬과 병렬 요소들을 분류하는 작업 수행
def serial_pararelle(register):
    
    # 'register' 리스트의 구조를 평탄화(flatten)하여 'n_reg' 리스트에 저장 
    n_reg= [] # 평탄화된 리스트를 저장할 변수
    
    # 'register' 리스트를 순회하며 각 요소를 처리
    for reg in register:#[['R2'], ['gnd1'], ['R3']]
        
        temp = []# 각 'reg'의 요소들을 임시로 저장할 리스트
        
        for k in reg:# 예: ['R2']
            for a in k: # 예: 'R2'
                temp.append(a) # 각 문자들을 'temp' 리스트에 추가
        n_reg.append(temp) # 완성된 'temp' 리스트를 'n_reg'에 추가
    
    # 평탄화된 결과 출력 (디버깅 목적)    
    print(n_reg)
    
    temp_pararelle = [] # 병렬 연결된 요소들을 저장할 리스트
    temp_serial = [] # 직렬 연결된 요소들을 저장할 리스트
    
    # 길이가 2보다 큰 경우 (병렬 연결)
    for reg in n_reg:
        
        # 길이가 2보다 큰 경우 (병렬 연결)
        if len(reg)>2:
            temp_pararelle.append(reg)
        
        # 길이가 2 이하인 경우 (직렬 연결)    
        else:
            temp_serial.append(reg)
    
    # 병렬 및 직렬 분류 결과 출력 (디버깅 목적)        
    print(temp_pararelle)
    print(temp_serial)

    # 직렬 연결된 요소들을 병렬 리스트에 반영하여 업데이트
    for serial in temp_serial:
        
        # 첫 번째 요소의 이름을 가져옴    
        name = serial[0]
        
        # 병렬 리스트에서 직렬 연결된 요소와 같은 이름을 가진 요소를 찾아 대체
        for pararelle in temp_pararelle:
            for k in range(len(pararelle)):
                
                if name == pararelle[k]:
                    pararelle[k] = [serial[0],serial[1]]
        
        # 두 번째 요소의 이름을 가져옴            
        name = serial[1]
        
        for pararelle in temp_pararelle:
            for k in range(len(pararelle)):
                
                if name == pararelle[k]:
                    pararelle[k] = [serial[0],serial[1]]
    
    # 업데이트된 병렬 리스트 출력 (디버깅 목적)                
    print('temp_pararelle: ',temp_pararelle)
    print('temp_serial:',temp_serial)
    
    #위에서 이제 길이가 3인 리스트만 모여있음. 저기서 두번이상 등장하는 요소들 전부빼면됨.
    align = []
    
    for entities in temp_pararelle: #[['R1', 'R2'], 'gnd1', 'R3']
        for entity in entities:
            
            if entity in align:
                pass # 이미 존재하면 추가하지 않음
            else:
                align.append(entity)
    
    # 병렬 리스트의 모든 요소를 담은 'align' 출력 (디버깅 목적)             
    print('align:',align)
    
    pararelle = [] # 최종 병렬 연결된 요소들을 저장할 리스트
    serial = [] # 최종 직렬 연결된 요소들을 저장할 리스트
    
    for device in align: #[['R1', 'R2'], 'gnd1', 'R3', 'V1']
        cnt = 0 # 특정 요소가 두 번 이상 등장하면 병렬로 처리
        
        for temp in temp_pararelle:
            if device in temp:
                cnt+=1
                
        if cnt==2:
            pararelle.append(device)
        else:
            serial.append(device)
            
    if len(serial):
        pass
    
    elif len(pararelle):
        pass
    
    else: #전부 직렬연결임.
        
        for temp in temp_serial:
            for device in temp:
                
                if device in serial:
                    pass
                else:
                    serial.append(device)
        pass

    # 최종 병렬 및 직렬 리스트 출력 (디버깅 목적)    
    print('리스트 안의 요소끼리 병렬 구조, 리스트안의 리스트는 직렬연결임 : ',pararelle)
    print("최종 직렬 계산 : ",serial)
    
    # 최종 결과 반환: 직렬 요소와 병렬 요소
    return serial, pararelle

# 커스텀 이벤트 핸들러
#QLabel 클릭 커스텀 이벤트.
def QDblclick(widget):
    '''
    사용예시
    QDblclick(self.widget).connect(self.function)
    '''
    class Filter(QObject):
        clicked = pyqtSignal()   #사용자정의 시그널

        def eventFilter(self, object, event):
            
            if object == widget and event.type() == QEvent.MouseButtonDblClick:
                self.clicked.emit()
                return True
            
            return False

    filter = Filter(widget)
    widget.installEventFilter(filter)

    pass
    return filter.clicked

#라벨 이동 함수
def QPress(widget):
    
    # 마우스 누르기 이벤트 핸들러
    class Filter(QObject):
        press = pyqtSignal()

        def eventFilter(self, object, event):
            
            if object == widget and event.type() == QEvent.MouseButtonPress:
                self.press.emit()
                return True
            
            return False

    filter = Filter(widget)
    widget.installEventFilter(filter)
    
    pass
    return filter.press

def QMove(widget):
    
    class Filter(QObject):
        move = pyqtSignal()

        def eventFilter(self, object, event):
            if object == widget and event.type() == QEvent.MouseMove:
                self.move.emit()
                return True
            return False

    filter = Filter(widget)
    widget.installEventFilter(filter)
    
    pass
    return filter.move

def QRelease(widget):
    
    class Filter(QObject):
        release = pyqtSignal()

        def eventFilter(self, object, event):
            if object == widget and event.type() == QEvent.MouseButtonRelease:
                self.release.emit()
                return True
            return False

    filter = Filter(widget)
    widget.installEventFilter(filter)
    
    pass
    return filter.release

# 다양한 다이얼로그 클래스들
#전원옵션창 Ui
class DC_opt(QDialog):
    
    # DC 전원 옵션 다이얼로그
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("dc_opt.ui",self)
        self.finishbotton.clicked.connect(self.finish_evt)
        self.value = ""
        
    def finish_evt(self):
        value = self.voltage_input.text()
        
        try:
            self.value = (float(value))
            self.close()
        except:
            print("숫자가 아닙니다")  #나중에 경고창 형식으로 뜨게함.

    pass

class Ac_opt(QDialog):
    
    def __init__(self):
        
        super().__init__()
        self.ui = uic.loadUi("ac_opt.ui",self)
        self.finishbotton.clicked.connect(self.finish_evt)
        self.dc_level = ""
        self.ac_volt_value = ""
        self.freq_value = ""
        
    def finish_evt(self):
        
        dc_value = self.dc_voltage.text()
        ac_value = self.ac_voltage.text()
        frequency = self.frequency.text()
        
        try:
            self.dc_level = float(dc_value)
            self.ac_volt_value = float(ac_value)
            self.freq_value = float(frequency)
            self.close()
            
        except:
            print("값을 입력해 주세요.")  #나중에 경고창 형식으로 뜨게함.
            
    pass
class Reg_opt(QDialog):
    
    def __init__(self):
        
        super().__init__()
        self.ui = uic.loadUi("reg_opt.ui",self)
        self.finishbotton.clicked.connect(self.finish_evt)
        self.value = ""
        
    def finish_evt(self):
        value = self.reg_input.text()
        
        try:
            self.value = float(value)
            self.close()
            
        except:
            print("값을 입력해 주세요.")  #나중에 경고창 형식으로 뜨게함.
class Ind_opt(QDialog):
    
    def __init__(self):
        
        super().__init__()
        self.ui = uic.loadUi("ind_opt.ui",self)
        self.finishbotton.clicked.connect(self.finish_evt)
        self.value = ""
        
    def finish_evt(self):
        value = self.ind_input.text()
        
        try:
            self.value = float(value)
            self.close()
            
        except:
            print("값을 입력해 주세요.")  #나중에 경고창 형식으로 뜨게함.

class Cap_opt(QDialog):
    
    def __init__(self):
        super().__init__()
        
        self.ui = uic.loadUi("cap_opt.ui",self)
        self.finishbotton.clicked.connect(self.finish_evt)
        self.value = ""
        
    def finish_evt(self):
        value = self.cap_input.text()
        
        try:
            self.value = float(value)
            self.close()
        except:
            print("값을 입력해 주세요.")  #나중에 경고창 형식으로 뜨게함.


#전원 선택창 Ui
class Sourceselection(QDialog):
    
    def __init__(self):
        super().__init__()
        
        self.ui = uic.loadUi("sourceselect.ui",self)
        self.dcsource.clicked.connect(self.dc_cursor_evt)
        self.acsource.clicked.connect(self.ac_cursor_evt)
        self.show()

        #기본상태(아무것도 안눌렀을 때)
        Sourceselection.sel_evt = "none"

    #버튼이벤트   
    def dc_cursor_evt(self):
        
        Sourceselection.sel_evt = "dc"
        self.close()
        
    def ac_cursor_evt(self):
        
        Sourceselection.sel_evt = "ac"
        self.close()


#소자 선택창 Ui
class Deviceselection(QDialog):
    
    def __init__(self):
        
        super().__init__()
        self.ui = uic.loadUi("deviceselect.ui",self)

        self.reg_btn.clicked.connect(self.reg_cursor_evt)
        self.ind_btn.clicked.connect(self.ind_cursor_evt)
        self.cap_btn.clicked.connect(self.cap_cursor_evt)
        self.amp_btn.clicked.connect(self.amp_cursor_evt)

        self.show()
        #기본상태(아무것도 안눌렀을 때)
        Deviceselection.sel_evt = "none"
    
    #버튼이벤트(눌렀을때)
    def reg_cursor_evt(self):
        
        Deviceselection.sel_evt = "reg"
        self.close()
        pass
    
    def ind_cursor_evt(self):
        
        Deviceselection.sel_evt = "ind"
        self.close()
        pass
    
    def cap_cursor_evt(self):
        
        Deviceselection.sel_evt = "cap"
        self.close()
        pass
    
    def amp_cursor_evt(self):
        
        Deviceselection.sel_evt = "amp"
        self.close()
        pass
    
#실행 설정창 Ui
class Act_opt(QDialog):
    
    def __init__(self):
        
        super().__init__()
        self.ui = uic.loadUi("act_opt.ui",self)
        self.show()
        self.finishbotton.clicked.connect(self.finish_evt)
        self.sec_value = ""
        self.name_value = ""
    
    def finish_evt(self):
        
        self.sec_value = self.sec_input.text()
        
        try:
            self.sec_value = float(self.sec_value)
            self.name_value = self.name_input.text()
            self.close()
            
        except:
            print('숫자입력하세요')
    
    pass

# 메인 윈도우 클래스
#메인창 Ui  
class mainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()
        
        self.ui=uic.loadUi("circuit_simul.ui",self)             #ui 불러오기
        
        #기본 버튼들 연결
        self.source.clicked.connect(self.show_source)
        self.device.clicked.connect(self.show_device)
        self.ground.clicked.connect(self.gnd_cursor_evt)
        self.wire.clicked.connect(self.wire_cursor_evt)
        self.marker.clicked.connect(self.marker_cursor_evt)
        self.act.clicked.connect(self.show_act)
        self.prev.clicked.connect(self.prev_evt)
        self.next.clicked.connect(self.next_evt)
        self.clear.clicked.connect(self.clear_evt)
        self.show()
        
        #사용 변수
        self.rotate = False
        self.redo = []
        self.redo_wire = []
        self.wire_save = []
        self.save_list = []
        self.draw_wire = []
        self.node_cnt = 0
        self.node_dict = {'node_sample':['wire_list']}
        self.act_time = 0.001
        self.project_name = "noname"
        self.wire_connection = []
        self.tmp_draw_wire = []
        self.object_draw = self
        self.mouse_state = "none"
        self.name = ""
        self.dc_cnt = 0
        self.dc_dict ={"Vsample" : ["QLabel_entity","Voltage_value","position_list","dc"]}
        self.ac_cnt = 0
        self.ac_dict = {"Vsample" : ["QLabel_entity","DC_level ","Voltage_value","Frequency_value","postion_list","ac"]}
        self.reg_cnt =0
        self.reg_dict ={"Rsample" : ["QLabel_entity","ohm_value", "position_list","reg"]}
        self.ind_cnt = 0
        self.ind_dict={"Lsample" : ["QLabel_entity","ind_value","postion_list","ind"]}
        self.cap_cnt = 0
        self.cap_dict = {"Csample" : ["QLabel_entity","cap_value","postion_list","cap"]}
        self.amp_cnt =0
        self.amp_dict = {"IOP_sample" : ["QLabel_entity","postion_list",'amp']}
        self.gnd_cnt =0
        self.gnd_dict = {"gnd_sample" : ["QLabel_entity","postion_list",'gnd']}
        self.mkr_cnt = 0
        self.mkr_dict = {"mkr_sample" : ["QLabel_entity","postion_list",'mkr']}
        self.auto_save()
        

    # 사용자가 회로 설계 과정에서 전원 소스를 선택하고 추가하는 작업을 직관적이고 효율적으로 수행할 수 있도록 돕는 중요한 역할
    def show_source(self):
        
        sourcewindow = Sourceselection()
        sourcewindow.exec_()                                    # 모달 다이얼로그로 실행 (사용자 입력을 기다림)
        
        # 사용자가 선택한 전원 타입을 mouse_state에 저장
        self.mouse_state = sourcewindow.sel_evt                 # 전원선택창에서 받은 event값 저장
        
        # 선택된 전원 타입에 따라 마우스 커서 변경
        if self.mouse_state == "dc":
            
            # DC 전원이 선택된 경우
            dc_pixmap = QPixmap("dc_source_rbg.png") # DC 전원 이미지 로드
            dc_pixmap =dc_pixmap.scaled(90,90) # 이미지 크기 조정
            temp_cursor = QCursor(dc_pixmap) # 커스텀 커서 생성
            
            QApplication.setOverrideCursor(temp_cursor) # 애플리케이션의 커서를 변경
            
            pass
        
        elif self.mouse_state == "ac":
            
            # AC 전원이 선택된 경우
            ac_pixmap = QPixmap("ac sourse_rgb.png") # AC 전원 이미지 로드
            ac_pixmap = ac_pixmap.scaled(70,90) # 이미지 크기 조정
            temp_cursor = QCursor(ac_pixmap) # 커스텀 커서 생성
            QApplication.setOverrideCursor(temp_cursor) # 애플리케이션의 커서를 변경

            pass
        
        elif self.mouse_state == "none":
            
            # 아무것도 선택되지 않은 경우
            pass # 아무 동작도 하지 않음


    def show_device(self):
        
        # Deviceselection 클래스의 인스턴스를 생성하여 장치 선택 창을 표시.
        devicewindow = Deviceselection()
        devicewindow.exec_()
        
        # 사용자가 선택한 장치 유형을 mouse_state에 저장
        self.mouse_state = devicewindow.sel_evt
        
        # 선택된 소자 유형에 따라 마우스 커서 변경
        if self.mouse_state == "reg":
            
            # 저항 선택 시
            reg_pixmap = QPixmap("reg.png")
            reg_pixmap = reg_pixmap.scaled(QSize(90,70))
            
            # 저항 아이콘을 커서로 설정하고, 커서의 핫스팟(커서의 클릭 포인트)을 (20,20)으로 설정
            temp_cursor = QCursor(reg_pixmap,20,20)   #리사이즈 필요 너무큼
            
            # 애플리케이션의 커서를 새로 설정
            QApplication.setOverrideCursor(temp_cursor)
            pass
        
        elif self.mouse_state == "ind":
            
            # 지시기 아이콘을 로드하고, 크기를 (110x80)으로 조정
            ind_pixmap = QPixmap("ind.png")
            ind_pixmap = ind_pixmap.scaled(QSize(110,80))
            
            # 지시기 아이콘을 커서로 설정하고, 커서의 핫스팟을 (20,20)으로 설정
            temp_cursor = QCursor(ind_pixmap,20,20)
            
            # 애플리케이션의 커서를 새로 설정
            QApplication.setOverrideCursor(temp_cursor)
            pass
        
        elif self.mouse_state == "cap":
            
             # 캐패시터 아이콘을 로드하고, 크기를 (90x70)으로 조정
            cap_pixmap = QPixmap("cap.png")
            cap_pixmap = cap_pixmap.scaled(QSize(90,70))
            
            # 캐패시터 아이콘을 커서로 설정하고, 커서의 핫스팟을 (20,20)으로 설정
            temp_cursor = QCursor(cap_pixmap,20,20)
            
            # 애플리케이션의 커서를 새로 설정
            QApplication.setOverrideCursor(temp_cursor)
            pass
        
        elif self.mouse_state == "amp":
            
            # 연산 증폭기 아이콘을 로드하고, 크기를 (210x180)으로 조정
            amp_pixmap = QPixmap("op_amp.png")
            amp_pixmap = amp_pixmap.scaled(QSize(210,180))
            
            # 연산 증폭기 아이콘을 커서로 설정하고, 커서의 핫스팟을 (20,20)으로 설정
            temp_cursor = QCursor(amp_pixmap,20,20)
            
            # 애플리케이션의 커서를 새로 설정
            QApplication.setOverrideCursor(temp_cursor)
            pass
        
    # GND 커서 설정 메서드
    def gnd_cursor_evt(self):
        # 현재 마우스 상태를 "gnd"로 설정하여 GND 모드로 전환
        self.mouse_state = "gnd"
        
        # "gnd.png" 파일에서 이미지 로드
        gnd_pixmap = QPixmap("gnd.png")
        
        # 로드된 이미지를 크기 (60x70)으로 조정
        gnd_pixmap = gnd_pixmap.scaled(QSize(60,70))
        
        # 이미지로 커서를 설정합니다. 커서의 핫스팟은 (20,20)으로 설정
        temp_cursor = QCursor(gnd_pixmap,20,20)
        QApplication.setOverrideCursor(temp_cursor)
        pass
    
    def wire_cursor_evt(self):
        self.mouse_state = "wire"
        pass
    
    def marker_cursor_evt(self):
        
        self.mouse_state = "marker"
        marker_pixmap = QPixmap("marker.png")
        marker_pixmap = marker_pixmap.scaled(QSize(20,60))
        temp_cursor = QCursor(marker_pixmap,20,20)
        
        QApplication.setOverrideCursor(temp_cursor)
        pass
    
    #실행창으로 이동.
    def show_act(self):
        
        actwindow = Act_opt()
        actwindow.sec_input.setText(str(self.act_time))
        actwindow.name_input.setText(self.project_name)
        actwindow.exec_()
        self.act_time = actwindow.sec_value
        self.project_name = actwindow.name_value
        serial = []
        pararelle = []
        register = []
        sum_dict={}
        name_cnt = 0
        target = 'none'
        called_node = []  #[node1]
        calling_node = []   # [node2]
        connect_node = []  #[node1 - node2]
        temp = []
        temp.append(self.wire_connection)
        called_node,connect,calling_node,connect_node=node_sort(self.wire_connection)
        sum_dict,register,name_cnt,wires,connect_node = sum_one(sum_dict,register,name_cnt,self.wire_connection,connect_node)
        serial, pararelle = serial_pararelle(register)
        self.ploting_board(serial,pararelle)
        self.wire_connection = temp.pop()

        pass
    
    #커서안바뀌고 실행되는 부분
    def prev_evt(self):
        
        if len(self.save_list):
            self.write_value()
            self.recreate_label()
        else:
            print('이전단계 없음')
        self.update()
        
        pass
    
    def next_evt(self):
        
        if len(self.redo):
            self.redo_write()
            self.recreate_label()
        else:
            print("다음단계없음.")
        self.update()
        
        pass
    
    def clear_evt(self):
        
        for i in range(1,self.dc_cnt+1):
            name = "V"+str(i)
            self.dc_dict[name][0].setHidden(True)       #라벨 감추기 먼저해야지 감추는게 가능
            
        self.dc_dict = {"Vsample" : ["QLabel_entity","Voltage_value","position_list","dc"]}             
        self.dc_cnt = 0
        
        for i in range(1,self.ac_cnt+1):
            name = "V"+str(i)
            self.ac_dict[name][0].setHidden(True)
            
        self.ac_dict = {"Vsample" : ["QLabel_entity","DC_level ","Voltage_value","Frequency_value","postion_list","ac"]}
        self.ac_cnt = 0
        
        for i in range(1,self.reg_cnt+1):
            name = "R"+str(i)
            self.reg_dict[name][0].setHidden(True)
            
        self.reg_dict ={"Rsample" : ["QLabel_entity","ohm_value", "position_list","reg"]}
        self.reg_cnt = 0
        
        for i in range(1,self.ind_cnt+1):
            
            name = "L"+str(i)
            self.ind_dict[name][0].setHidden(True)
            
        self.ind_dict={"Lsample" : ["QLabel_entity","ind_value","postion_list","ind"]}
        self.ind_cnt = 0
        
        for i in range(1,self.cap_cnt+1):
            
            name = "C"+str(i)
            self.cap_dict[name][0].setHidden(True)
            
        self.cap_dict = {"Csample" : ["QLabel_entity","cap_value","postion_list","cap"]}
        self.cap_cnt = 0
        
        for i in range(1,self.amp_cnt+1):
            
            name = "IOP"+str(i)
            self.amp_dict[name][0].setHidden(True)
            
        self.amp_dict = {"IOP_sample" : ["QLabel_entity","postion_list",'amp']}
        self.amp_cnt = 0
        
        for i in range(1,self.gnd_cnt+1):
            
            name = 'gnd'+str(i)
            self.gnd_dict[name][0].setHidden(True)
            
        self.gnd_dict = {"gnd_sample" : ["QLabel_entity","postion_list",'gnd']}
        self.gnd_cnt = 0
        
        for i in range(1,self.mkr_cnt+1):
            
            name = 'mkr'+str(i)
            self.mkr_dict[name][0].setHidden(True)
            
        self.mkr_dict = {"mkr_sample" : ["QLabel_entity","postion_list",'mkr']}
        self.mkr_cnt = 0
        self.tmp_draw_wire = []
        self.wire_connection = []
        self.node_cnt = 0
        self.node_dict = {}
        self.draw_wire = []
        self.update()
        pass
  
    #행동시마다 저장하는 친구. 
    def auto_save(self):
        
        print('저장됨')
        tmp = [self.dc_cnt, self.dc_dict, self.ac_cnt, self.ac_dict, self.reg_cnt, self.reg_dict,
        self.ind_cnt, self.ind_dict, self.cap_cnt, self.cap_dict, self.amp_cnt, self.amp_dict,
        self.gnd_cnt, self.gnd_dict, self.mkr_cnt, self.mkr_dict, self.node_cnt,
        self.node_dict, self.wire_connection]
        self.save_list.append(tmp)
        
        #와이어이벤트 저장안되는 현상 있어서 따로저장.
        wire = [wire for wire in self.draw_wire]   
        self.wire_save.append(wire)
        self.redo = []
        self.redo_wire = []
        
    def redo_write(self):
        self.clear_evt()
        tmp = self.redo.pop()
        self.dc_cnt = tmp[0]
        self.dc_dict = tmp[1]
        self.ac_cnt = tmp[2]
        self.ac_dict = tmp[3]
        self.reg_cnt = tmp[4]
        self.reg_dict = tmp[5]
        self.ind_cnt = tmp[6]
        self.ind_dict = tmp[7]
        self.cap_cnt = tmp[8]
        self.cap_dict = tmp[9]
        self.amp_cnt = tmp[10]
        self.amp_dict = tmp[11]
        self.gnd_cnt = tmp[12]
        self.gnd_dict = tmp[13]
        self.mkr_cnt =  tmp[14]
        self.mkr_dict = tmp[15]
        self.node_cnt = tmp[16]
        self.node_dict = tmp[17]
        self.wire_connection = tmp[18]
        
        try:
            tmp_wire = self.redo_wire.pop()
        except:
            tim_wire = []
            pass
        
        self.draw_wire = tmp_wire
        self.save_list.append(tmp)
        self.wire_save.append(tmp_wire)
        self.update()
        pass
    
    def write_value(self):
        
        self.clear_evt()
        tmp = self.save_list.pop()
        self.dc_cnt = tmp[0]
        self.dc_dict = tmp[1]
        self.ac_cnt = tmp[2]
        self.ac_dict = tmp[3]
        self.reg_cnt = tmp[4]
        self.reg_dict = tmp[5]
        self.ind_cnt = tmp[6]
        self.ind_dict = tmp[7]
        self.cap_cnt = tmp[8]
        self.cap_dict = tmp[9]
        self.amp_cnt = tmp[10]
        self.amp_dict = tmp[11]
        self.gnd_cnt = tmp[12]
        self.gnd_dict = tmp[13]
        self.mkr_cnt =  tmp[14]
        self.mkr_dict = tmp[15]
        self.node_cnt = tmp[16]
        self.node_dict = tmp[17]
        self.wire_connection = tmp[18]
        
        try:
            tmp_wire = self.wire_save.pop()
        except:
            tim_wire = []
            pass
        
        self.draw_wire = tmp_wire
        self.redo.append(tmp)
        self.redo_wire.append(tmp_wire)
        self.update()
        
        pass
    
    def recreate_label(self):
        # DC 컴포넌트가 존재하는지 확인
        
        if self.dc_cnt>0:
            for i in range(1,self.dc_cnt+1):
                name = 'V'+str(i) # DC 컴포넌트의 이름 생성, ex) 'V1', 'V2' 등
                
                print(name)
                
                position = self.dc_dict[name][2] # 컴포넌트의 위치 정보 추출
                state = self.dc_dict[name][3] # 컴포넌트의 상태 정보 추출
                
                if self.dc_dict[name][-1]: # 컴포넌트가 회전된 상태인지 확인
                    self.self.dc_dict[name][0].setGeometry(position[0],position[1],90,80)
                    self.dc_pixmap = QPixmap("dc_source_rbg_rotate.png")
                    self.dc_pixmap = self.dc_pixmap.scaled(QSize(90,80))
                    
                else: # 컴포넌트가 회전되지 않은 상태
                    # 컴포넌트의 위치 및 크기를 설정하고 기본 이미지를 불러옴
                    self.dc_dict[name][0].setGeometry(position[0],position[1],80,90)  
                    self.dc_pixmap = QPixmap("dc_source_rbg.png")
                    self.dc_pixmap = self.dc_pixmap.scaled(QSize(80,90))
                
                # 이미지 적용 및 컴포넌트 표시
                self.dc_dict[name][0].setPixmap(self.dc_pixmap)
                self.dc_dict[name][0].show()
                
                # 컴포넌트 더블클릭 이벤트 설정 (설정창 열기)
                self.update()
                QDblclick(self.dc_dict[name][0]).connect(lambda : self.QLabel_dbl_event(name,state))   #설정창 여는 이벤트
                
                try:
                    # 이동 이벤트 설정 (컴포넌트를 꾹 눌러서 이동)
                    self.moving_event = self.press_event   #moving event가 pressing 중 움직일때만 호출되기 때문에 그전에 생성 안됨. 따라서 따로 생성.
                    QPress(self.dc_dict[name][0]).connect(lambda : self.QLabel_move_event_press(self.press_event))     #꾹 눌러서 옮기기/
                    QMove(self.dc_dict[name][0]).connect(lambda : self.QLabel_move_event_move(self.moving_event, name, state))
                    QRelease(self.dc_dict[name][0]).connect(lambda : self.QLabel_move_event_release(self.release_event))
                except:
                    # 예외 발생 시 에러 출력
                    print(traceback.format_exc())
                pass
        
        # AC 컴포넌트가 존재하는지 확인
        if self.ac_cnt>0:
            
            for i in range(1,self.ac_cnt+1):
                name = 'V'+str(i) # AC 컴포넌트의 이름 생성
                position = self.ac_dict[name][4] # 컴포넌트의 위치 정보 추출
                state = self.ac_dict[name][5] # 컴포넌트의 상태 정보 추출
                
                if self.ac_dict[name][-1]: # 컴포넌트가 회전된 상태인지 확인
                    
                    # 컴포넌트의 위치 및 크기를 설정하고 회전된 이미지를 불러옴
                    self.ac_dict[name][0].setGeometry(position[0], position[1], 90, 60)
                    self.ac_pixmap = QPixmap("ac sourse_rgb_rotate")
                    self.ac_pixmap = self.ac_pixmap.scaled(QSize(90,60))
                
                else: # 컴포넌트가 회전되지 않은 상태
                    # 컴포넌트의 위치 및 크기를 설정하고 기본 이미지를 불러옴
                    self.ac_dict[name][0].setGeometry(position[0], position[1], 60, 90)
                    self.ac_pixmap = QPixmap("ac sourse_rgb")
                    self.ac_pixmap = self.ac_pixmap.scaled(QSize(60,90))
                
                # 이미지 적용 및 컴포넌트 표시   
                self.ac_dict[name][0].setPixmap(self.ac_pixmap)
                self.ac_dict[name][0].show()
                
                # 컴포넌트 더블클릭 이벤트 설정
                QDblclick(self.ac_dict[name][0]).connect(lambda : self.QLabel_dbl_event(name,state))
                
                try:
                    # 이동 이벤트 설정 (컴포넌트를 꾹 눌러서 이동)
                    self.moving_event = self.press_event
                    QPress(self.ac_dict[name][0]).connect(lambda : self.QLabel_move_event_press(self.press_event))     
                    QMove(self.ac_dict[name][0]).connect(lambda : self.QLabel_move_event_move(self.moving_event, name, state))
                    QRelease(self.ac_dict[name][0]).connect(lambda : self.QLabel_move_event_release(self.release_event))
                
                except:
                    # 예외 발생 시 에러 출력
                    print(traceback.format_exc())
                    pass
        
         # REG 컴포넌트가 존재하는지 확인
        if self.reg_cnt>0:
            
            for i in range(1,self.reg_cnt+1):
                name = 'R'+str(i) # REG 컴포넌트의 이름 생성
                position = self.reg_dict[name][2] # 컴포넌트의 위치 정보 추출
                state = self.reg_dict[name][3]
                
                if self.reg_dict[name][-1]: # 컴포넌트가 회전된 상태인지 확인
                    
                    # 컴포넌트의 위치 및 크기를 설정하고 회전된 이미지를 불러옴
                    self.reg_dict[name][0].setGeometry(position[0], position[1], 70, 100)
                    self.reg_pixmap = QPixmap("reg_rotate.png")
                    self.reg_pixmap = self.reg_pixmap.scaled(QSize(70,100))
                
                else: # 컴포넌트가 회전되지 않은 상태
                    # 컴포넌트의 위치 및 크기를 설정하고 기본 이미지를 불러옴
                    self.reg_dict[name][0].setGeometry(position[0], position[1], 100, 70)
                    self.reg_pixmap = QPixmap("reg.png")
                    self.reg_pixmap = self.reg_pixmap.scaled(QSize(100,70))
                    
                # 이미지 적용 및 컴포넌트 표시
                self.reg_dict[name][0].setPixmap(self.reg_pixmap)
                self.reg_dict[name][0].show()
                
                # 컴포넌트 더블클릭 이벤트 설정
                QDblclick(self.reg_dict[name][0]).connect(lambda : self.QLabel_dbl_event(name,state))
                
                try:
                    # 이동 이벤트 설정 (컴포넌트를 꾹 눌러서 이동)
                    self.moving_event = self.press_event
                    QPress(self.reg_dict[name][0]).connect(lambda : self.QLabel_move_event_press(self.press_event))     
                    QMove(self.reg_dict[name][0]).connect(lambda : self.QLabel_move_event_move(self.moving_event, name, state))
                    QRelease(self.reg_dict[name][0]).connect(lambda : self.QLabel_move_event_release(self.release_event))
                
                except:
                    # 예외 발생 시 에러 출력
                    print(traceback.format_exc())
                    pass
                
                pass
            
        # IND 컴포넌트가 존재하는지 확인
        if self.ind_cnt>0:
            
            for i in range(1,self.ind_cnt+1):
                name = 'L'+str(i) # IND 컴포넌트의 이름 생성
                position_list = self.ind_dict[name][2] # 컴포넌트의 위치 정보 추출
                state = self.ind_dict[name][3] # 컴포넌트의 상태 정보 추출
                
                if self.ind_dict[name][-1]: # 컴포넌트가 회전된 상태인지 확인
                    
                    # 컴포넌트의 위치 및 크기를 설정하고 회전된 이미지를 불러옴
                    self.ind_dict[name][0].setGeometry(position_list[0], position_list[1], 70, 100)
                    self.ind_pixmap = QPixmap("ind_rotate.png")
                    self.ind_pixmap = self.ind_pixmap.scaled(QSize(70,100))
                
                else: # 컴포넌트가 회전되지 않은 상태
                    # 컴포넌트의 위치 및 크기를 설정하고 기본 이미지를 불러옴
                    self.ind_dict[name][0].setGeometry(position_list[0], position_list[1], 100, 70)
                    self.ind_pixmap = QPixmap("ind.png")
                    self.ind_pixmap = self.ind_pixmap.scaled(QSize(100,70))
                    
                # 이미지 적용 및 컴포넌트 표시
                self.ind_dict[name][0].setPixmap(self.ind_pixmap)
                self.ind_dict[name][0].show()
                
                # 컴포넌트 더블클릭 이벤트 설정
                QDblclick(self.ind_dict[name][0]).connect(lambda : self.QLabel_dbl_event(name,state))
                
                try:
                    # 이동 이벤트 설정 (컴포넌트를 꾹 눌러서 이동)
                    self.moving_event = self.press_event
                    QPress(self.ind_dict[name][0]).connect(lambda : self.QLabel_move_event_press(self.press_event))     
                    QMove(self.ind_dict[name][0]).connect(lambda : self.QLabel_move_event_move(self.moving_event, name, state))
                    QRelease(self.ind_dict[name][0]).connect(lambda : self.QLabel_move_event_release(self.release_event))
                
                except:
                    # 예외 발생 시 에러 출력
                    print(traceback.format_exc())
                    pass
                
        if self.cap_cnt>0:
            
            for i in range(1,self.cap_cnt+1):
                name = 'C'+str(i)
                position_list = self.cap_dict[name][2]
                state = self.cap_dict[name][3]
                
                if self.cap_dict[name][-1]:
                    self.cap_dict[name][0].setGeometry(position_list[0], position_list[1], 70, 100)
                    self.cap_pixmap = QPixmap("cap_rotate.png")
                    self.cap_pixmap = self.cap_pixmap.scaled(QSize(70,100))
                    
                else:
                    self.cap_dict[name][0].setGeometry(position_list[0], position_list[1], 100, 70)
                    self.cap_pixmap = QPixmap("cap.png")
                    self.cap_pixmap = self.cap_pixmap.scaled(QSize(100,70))
                self.cap_dict[name][0].setPixmap(self.cap_pixmap)
                self.cap_dict[name][0].show()
                QDblclick(self.cap_dict[name][0]).connect(lambda : self.QLabel_dbl_event(name,state))
                
                try:
                    self.moving_event = self.press_event
                    QPress(self.cap_dict[name][0]).connect(lambda : self.QLabel_move_event_press(self.press_event))     
                    QMove(self.cap_dict[name][0]).connect(lambda : self.QLabel_move_event_move(self.moving_event, name, state))
                    QRelease(self.cap_dict[name][0]).connect(lambda : self.QLabel_move_event_release(self.release_event))
                
                except:
                    print(traceback.format_exc())
                    pass
                
        if self.amp_cnt>0:
            
            for i in range(1,self.amp_cnt+1):
                name = 'IOP'+str(i)
                position_list = self.amp_dict[name][1]
                state = self.amp_dict[name][2]
                self.amp_dict[name][0].setGeometry(position_list[0], position_list[1], 210, 180)
                self.amp_pixmap = QPixmap("op_amp.png")
                self.amp_pixmap = self.amp_pixmap.scaled(QSize(210,180))
                self.amp_dict[name][0].setPixmap(self.amp_pixmap)
                self.amp_dict[name][0].show()
                
                try:
                    self.moving_event = self.press_event
                    QPress(self.amp_dict[name][0]).connect(lambda : self.QLabel_move_event_press(self.press_event))     
                    QMove(self.amp_dict[name][0]).connect(lambda : self.QLabel_move_event_move(self.moving_event, name, state))
                    QRelease(self.amp_dict[name][0]).connect(lambda : self.QLabel_move_event_release(self.release_event))
                
                except:
                    print(traceback.format_exc())
                    pass
                
        if self.gnd_cnt>0:
            
            for i in range(1,self.gnd_cnt+1):
                name = 'gnd'+str(i)
                position_list= self.gnd_dict[name][1]
                state = self.gnd_dict[name][2]
                
                if self.gnd_dict[name][-1]:
                    self.gnd_dict[name][0].setGeometry(position_list[0],position_list[1],60,70)
                    self.gnd_pixmap = QPixmap("gnd_rotate.png")
                    self.gnd_pixmap = self.gnd_pixmap.scaled(QSize(60,70))
                
                else:
                    self.gnd_dict[name][0].setGeometry(position_list[0],position_list[1],60,70)
                    self.gnd_pixmap = QPixmap("gnd.png")
                    self.gnd_pixmap = self.gnd_pixmap.scaled(QSize(60,70))
                self.gnd_dict[name][0].setPixmap(self.gnd_pixmap)
                self.gnd_dict[name][0].show()
                
                try:
                    self.moving_event = self.press_event
                    QPress(self.gnd_dict[name][0]).connect(lambda : self.QLabel_move_event_press(self.press_event))     
                    QMove(self.gnd_dict[name][0]).connect(lambda : self.QLabel_move_event_move(self.moving_event, name, state))
                    QRelease(self.gnd_dict[name][0]).connect(lambda : self.QLabel_move_event_release(self.release_event))
                
                except:
                    print(traceback.format_exc())
                    pass
        
        if self.mkr_cnt>0:
            name = 'mkr1'
            position_list = self.mkr_dict[name][1]
            state = self.mkr_dict[name][2]
            self.mkr_dict[name][0].setGeometry(position_list[0],position_list[1],20,60)
            self.mkr_pixmap = QPixmap("marker.png")
            self.mkr_pixmap = self.mkr_pixmap.scaled(QSize(30,90))
            self.mkr_dict[name][0].setPixmap(self.mkr_pixmap)
            self.mkr_dict[name][0].show()
            state = "mkr"
            self.update()
            
            try:
                self.moving_event = self.press_event
                QPress(self.mkr_dict[name][0]).connect(lambda : self.QLabel_move_event_press(self.press_event))  
                QMove(self.mkr_dict[name][0]).connect(lambda : self.QLabel_move_event_move(self.moving_event, name, state))
                QRelease(self.mkr_dict[name][0]).connect(lambda : self.QLabel_move_event_release(self.release_event))
            except:
                print(traceback.format_exc())
                self.moving_event = self.press_event
            pass
        pass
    
    # device_connect_wire 참고
    # 주어진 마커 위치하여 회로 내의 다양한 컴포넌트(V, R, L, C, IOP, gnd 등)을 검색하여, 마커가 특정 컴포넌트의 단자에 가까운지 확인하고,
    # 가까운 컴포넌트를 'target'으로 반환하는 역할을 한다. 
    def marker_searching(self):
        
        name = 'mkr1' # 찾으려는 마커의 이름 (기본적으로 'mkr1'으로 설정)
        position = self.mkr_dict[name][1]  #마커사이즈 20,60
        point = [position[0]+10,position[1]+60]
        target = 'none'
        dif = 5
        #"Vsample" : ["QLabel_entity","Voltage_value","position_list","dc"] size 80,90
        
        # DC 전원 소자 검색
        for k in range(1,self.dc_cnt+1):
            name = "V"+ str(k) # DC 소자의 이름 생성 (예: V1, V2, ...)
            tmp = self.dc_dict[name] # DC 소자의 정보를 가져옴
            
            # DC 소자가 회전된 상태인지 확인
            if self.dc_dict[name][-1]:
                
                plus_port_x = tmp[2][0]+95   # 플러스 단자 위치 (회전된 경우)
                plus_port_y = tmp[2][1]+39
                minus_port_x = plus_port_x - 100 # 마이너스 단자 위치 (회전된 경우)
                minus_port_y = plus_port_y
            
            # DC 소자가 회전되지 않은 상태
            else:
                plus_port_x = tmp[2][0] + 40   # 플러스 단자 위치
                plus_port_y = tmp[2][1] - 5
                minus_port_x = plus_port_x # 마이너스 단자 위치
                minus_port_y = plus_port_y+100
            
            # 마커가 플러스 단자에 가까운지 확인
            if abs(point[0]-plus_port_x)<dif and abs(point[1]-plus_port_y)<dif:
                target = name # 가까운 경우 해당 소자를 타겟으로 설정
            
            # 마커가 마이너스 단자에 가까운지 확인
            if abs(point[0]-minus_port_x)<dif and abs(point[1]-minus_port_y)<dif:
                target = name # 가까운 경우 해당 소자를 타겟으로 설정

        # AC 전원 소자 검색
        for k in range(1,self.ac_cnt+1):
            #"Vsample" : ["QLabel_entity","DC_level ","Voltage_value","Frequency_value","postion_list","ac"] size 60,90
            name = "V"+ str(k) # AC 소자의 이름 생성
            tmp = self.ac_dict[name] # AC 소자의 정보를 가져옴

            # AC 소자가 회전된 상태인지 확인
            if self.ac_dict[name][-1]:
                plus_port_x = tmp[4][0]+95 # 플러스 단자 위치 (회전된 경우)
                plus_port_y = tmp[4][1]+30
                minus_port_x = plus_port_x-100 # 마이너스 단자 위치 (회전된 경우)
                minus_port_y = plus_port_y
            
            # AC 소자가 회전되지 않은 상태
            else:
                plus_port_x = tmp[4][0]+30 # 플러스 단자 위치
                plus_port_y = tmp[4][1]-5
                minus_port_x = plus_port_x # 마이너스 단자 위치
                minus_port_y = plus_port_y+100

            # 마커가 플러스 단자에 가까운지 확인
            if abs(point[0]-plus_port_x)<dif and abs(point[1]-plus_port_y)<dif:
                target = name # 가까운 경우 해당 소자를 타겟으로 설정
            
            # 마커가 마이너스 단자에 가까운지 확인
            elif abs(point[0]-minus_port_x)<dif and abs(point[1]-minus_port_y)<dif:
                target = name # 가까운 경우 해당 소자를 타겟으로 설정
            else:
                continue # 조건에 맞지 않으면 다음으로 넘어감
        
        # 저항 소자 검색
        for k in range(1,self.reg_cnt+1):
            #"Rsample" : ["QLabel_entity","ohm_value", "position_list","reg"] size 100,70
            name = "R"+ str(k)  # 저항 소자의 이름 생성
            tmp = self.reg_dict[name] # 저항 소자의 정보를 가져옴
            
            if self.reg_dict[name][-1]: # 저항 소자가 회전된 상태인지 확인
                a_port_x = tmp[2][0]+35 # A 단자 위치 (회전된 경우)
                a_port_y = tmp[2][1] - 5
                b_port_x = a_port_x # B 단자 위치 (회전된 경우)
                b_port_y = a_port_y + 110
                
            # 저항 소자가 회전되지 않은 상태
            else:
                a_port_x = tmp[2][0]-5 # A 단자 위치
                a_port_y = tmp[2][1] + 35
                b_port_x = a_port_x + 110 # B 단자 위치
                b_port_y = a_port_y

            # 마커가 A 단자에 가까운지 확인
            if abs(point[0]-a_port_x)<dif and abs(point[1]-a_port_y)<dif:
                target = name # 가까운 경우 해당 소자를 타겟으로 설정
                
            # 마커가 B 단자에 가까운지 확인
            elif abs(point[0]-b_port_x)<dif and abs(point[1]-b_port_y)<dif:
                target = name # 가까운 경우 해당 소자를 타겟으로 설정
            else:
                continue # 조건에 맞지 않으면 다음으로 넘어감
        
        # 인덕터 소자 검색
        for k in range(1,self.ind_cnt+1):
            #""Lsample" : ["QLabel_entity","ind_value","postion_list","ind"] size 100,70
            name = "L"+ str(k)  # 인덕터 소자의 이름 생성
            tmp = self.ind_dict[name] # 인덕터 소자의 정보를 가져옴
            
            # 인덕터 소자가 회전된 상태인지 확인
            if self.ind_dict[name][-1]:
                a_port_x = tmp[2][0] +27 # A 단자 위치 (회전된 경우)
                a_port_y = tmp[2][1] -5
                b_port_x = a_port_x # B 단자 위치 (회전된 경우)
                b_port_y = a_port_y +110
                
            # 인덕터 소자가 회전되지 않은 상태
            else:
                a_port_x = tmp[2][0] -5   #단자부분의 위치
                a_port_y = tmp[2][1] + 41
                b_port_x = a_port_x + 110
                b_port_y = a_port_y
            
            # 마커가 A 단자에 가까운지 확인
            if abs(point[0]-a_port_x)<dif and abs(point[1]-a_port_y)<dif:
                target = name # 가까운 경우 해당 소자를 타겟으로 설정   
            
            # 마커가 B 단자에 가까운지 확인
            elif abs(point[0]-b_port_x)<dif and abs(point[1]-b_port_y)<dif:
                target = name # 가까운 경우 해당 소자를 타겟으로 설정
            else:
                continue # 조건에 맞지 않으면 다음으로 넘어감
        
        # 커패시터 소자 검색
        for k in range(1,self.cap_cnt+1):
            #""Csample" : ["QLabel_entity","cap_value","postion_list","ind"] size 100,70
            name = "C"+ str(k) # 커패시터 소자의 이름 생성
            tmp = self.cap_dict[name] # 커패시터 소자의 정보를 가져옴
            
            # 커패시터 소자가 회전된 상태인지 확인
            if self.cap_dict[name][-1]:
                a_port_x = tmp[2][0] +35 # A 단자 위치 (회전된 경우)
                a_port_y = tmp[2][1] - 5
                b_port_x = a_port_x # B 단자 위치 (회전된 경우)
                b_port_y = a_port_y +110
            
            # 커패시터 소자가 회전되지 않은 상태
            else:
                a_port_x = tmp[2][0] - 5 # A 단자 위치
                a_port_y = tmp[2][1] + 35
                b_port_x = a_port_x + 110 # B 단자 위치
                b_port_y = a_port_y

            if abs(point[0]-a_port_x)<dif and abs(point[1]-a_port_y)<dif:
                target = name    #.
            elif abs(point[0]-b_port_x)<dif and abs(point[1]-b_port_y)<dif:
                target = name
            else:
                continue
        
        for k in range(1,self.amp_cnt+1):
            #""IOPsample" : ["QLabel_entity","postion_list","amp"] size 210,180
            name = "IOP"+ str(k) 
            tmp = self.amp_dict[name]   
            pos_input_x = tmp[1][0] - 5
            pos_input_y = tmp[1][1] + 37
            neg_input_x = pos_input_x
            neg_input_y = tmp[1][1] + 144
            output_x = pos_input_x +220
            output_y = tmp[1][1] + 90

            if abs(point[0]-pos_input_x)<dif or abs(point[1]-pos_input_y)<dif:
                target = name + '_pos'
            elif abs(point[0] - neg_input_x)<dif or abs(point[1] - neg_input_y)<dif:
                target = name + '_neg'
            elif abs(point[0] - output_x)<dif or abs(point[1] - output_x)<dif:
                target = name + '_out'
        
        # 접지(GND) 소자 검색
        for k in range(1,self.gnd_cnt+1):
            #""gnd_sample" : ["QLabel_entity","postion_list",'gnd'] size 60,70
            name = "gnd"+ str(k) # GND 소자의 이름 생성
            tmp = self.gnd_dict[name] # GND 소자의 정보를 가져옴
            
            # GND 소자가 회전된 상태인지 확인
            if self.gnd_dict[name][-1]:
                port_x = tmp[1][0] +30 # 단자 위치 (회전된 경우)
                port_y = tmp[1][1] +75
                
            # GND 소자가 회전되지 않은 상태
            else:
                port_x = tmp[1][0] +30 # 단자 위치
                port_y = tmp[1][1] - 5
            
            # 마커가 단자에 가까운지 확인
            if abs(point[0]-port_x)<dif and abs(point[1]-port_y)<dif:
                target = name # 가까운 경우 해당 소자를 타겟으로 설정
            else:
                
                continue # 조건에 맞지 않으면 다음으로 넘어감
            pass 
        return target
        pass
    
    #계산 시작
    def ploting_board(self,serial,pararelle):
        
        timescale = self.act_time
        timescale = np.arange(0,1,timescale*0.001)
        timelen = len(timescale)
        ac_max_freq = 0
        plot_list = []
        plot_name_list = []
        
        #전원은 기본출력
        for i in range(1,self.dc_cnt+1):
            name = 'V'+str(i)
            dc_value = self.dc_dict[name][1] #dc,amp,freq,time
            result = sin_wave(dc_value,0,0.00000001,timescale)
            plot_list.append(result)
            plot_name = 'Vdc'+str(i)
            plot_name_list.append(plot_name)
        
        for i in range(1,self.ac_cnt+1):
            name = 'V'+str(i)
            dc_value = self.ac_dict[name][1]
            ac_value = self.ac_dict[name][2]
            frequency = self.ac_dict[name][3]
            result = sin_wave(dc_value,ac_value,frequency,timescale)
            plot_list.append(result)
            plot_name = 'Vac'+str(i)
            plot_name_list.append(plot_name)
            
            if frequency >ac_max_freq:
                ac_max_freq = frequency
        #여기서부터 계산
        #impedence_cal
        try:
            target = self.marker_searching()
            print('target :',target)
            
            total_impedence =np.zeros(timelen)
            part_impedence = np.ones(timelen)
            reverse_part_impedence = np.zeros(timelen)
            marker_impedence = np.zeros(timelen)
            freq_scale = (ac_max_freq*2)/timelen
            freq = np.arange(0,ac_max_freq*2,freq_scale)
            marker_where = ''
            #target값 서칭
            
            for k in range(len(pararelle)): # [[r1,r2],r3] 형식 #리스트안 리스트는 직렬연결임.
                
                if type(pararelle[k]) is list:
                    
                    if target in pararelle[k]: #병렬속 직렬연결일때. 안에 마커연결된 소자 있음.
                        marker_where = 'para'
                        
                        for pa in pararelle[k]:
                            
                            if 'R' in pa:
                                part_impedence += self.reg_dict[pa][1]
                            elif 'L' in pa:
                                part_impedence += freq*self.ind_dict[pa][1]
                            elif 'C' in pa:
                                part_impedence += 1/(freq*self.cap_dict[pa][1])
                            else: #V일경우 무시. op_amp 나중에 구현.
                                pass
                        pararelle[k] = part_impedence-1 #값대체
                        
                        #토탈 임피던스에서 전압강하 구한뒤. 전압강하에서 marker_impedence 곱하면 값나옴.
                        if 'R' in target:
                            marker_impedence = self.reg_dict[target][1]/part_impedence
                        elif 'L' in target:
                            marker_impedence = (freq*self.ind_dict[target][1])/part_impedence
                        elif 'C' in target:
                            marker_impedence = (1/freq*self.cap_dict[target][1])*(1/part_impedence)
                        part_impedence = np.ones(timelen) #값초기화
                        
                    else: #병렬안 직렬연결일때 안에 마커연결된 소자 없음.
                        
                        for pa in pararelle[k]:
                            if 'R' in pa:
                                part_impedence += self.reg_dict[pa][1]
                            elif 'L' in pa:
                                part_impedence += freq*self.ind_dict[pa][1]
                            elif 'C' in pa:
                                part_impedence += 1/(freq*self.cap_dict[pa][1])
                            else: #V일경우 무시. op_amp 나중에 구현.
                                pass
                        pararelle[k] = part_impedence #값대체
                        part_impedence = np.ones(timelen)
                        pass
                    
                else: #그냥 병렬 연결된 단일 소자.
                    pass
            temp_para = False
            
            for k in range(len(pararelle)): # 2번째 위에서 모든 병렬연결속 직렬 연결값 연결해놓음
                
                if type(pararelle[k]) is np.ndarray: #위에서 리스트화 된개체들 전부 계산되어 담겨있음.
                    pass
                else:#나머지 소규모 개체들.이곳에 마커 있을시 그냥 병렬 연결로 계산하면 됨.
                    
                    if target == pararelle[k]: #단읽개체이므로 in 과 == 같음
                        temp_para= True
                        marker_where = 'para'
                        if 'R' in target:
                            pararelle[k] = part_impedence -1 + self.reg_dict[target][1]
                        elif 'L' in target:
                            pararelle[k] = freq*self.ind_dict[target][1]
                        elif 'C' in target:
                            pararelle[k] = 1/(freq*self.cap_dict[target][1])
                    else:
                        
                        if 'R' in target:
                            pararelle[k] = part_impedence -1 + self.reg_dict[target][1]
                        elif 'L' in target:
                            pararelle[k] = freq*self.ind_dict[target][1]
                        elif 'C' in target:
                            pararelle[k] = 1/(freq*self.cap_dict[target][1])
                        pass
            if marker_where =='para':
                
                if temp_para: #True일시 병렬 개별 임피던스. #병렬임피던스의 전압강하가 곧 marker_impedence
                    print('병렬')
                    
                    for para in pararelle:
                        reverse_part_impedence +=1/para
                    part_impedence = 1/reverse_part_impedence #병렬저항의 총저항.
                    total_impedence +=part_impedence
                    
                    for seri in serial:
                        if 'R' in seri:
                            total_impedence += self.reg_dict[seri][1]
                        elif 'L' in seri:
                            total_impedence += freq*self.ind_dict[1]
                        elif 'C' in seri:
                            total_impedence += 1/(freq*self.cap_dict[1])
                    marker_impedence = part_impedence/total_impedence
                    print('marker_impedence:',marker_impedence[-1])
                    result_impedence = []
                    
                    for wave in plot_list:#v신호임.
                        result_impedence.append(wave*marker_impedence)

                    #plot_list.append(result_impedence)
                    #plot_name_list.append('marker')
                else:#병렬안 직렬일때. 병렬 임피던스의 전압강하 구한뒤 marker_impedence를 따로 곱해줘야함.
                    print('병렬안 직렬일때')
                    
                    for para in pararelle:
                        reverse_part_impedence +=1/para
                        
                    part_impedence = 1/reverse_part_impedence #병렬저항의 총저항.
                    total_impedence +=part_impedence
                    
                    for seri in serial:
                        
                        if 'R' in seri:
                            total_impedence += self.reg_dict[seri][1]
                        elif 'L' in seri:
                            total_impedence += freq*self.ind_dict[1]
                        elif 'C' in seri:
                            total_impedence += 1/(freq*self.cap_dict[1])
                    temp_impedence = part_impedence/total_impedence
                    result_impedence = []
                    print('marker_impedence:',marker_impedence[-1])
                    for wave in plot_list:#v신호임.
                        result_impedence.append(wave*temp_impedence*marker_impedence)
                    
                    #plot_list.append(result_impedence)
                    #plot_name_list('marker')
                pass
            
            else: #직렬 연결안에 마커있음.
                print('직렬연결에 마커')
                
                for para in pararelle:
                    reverse_part_impedence +=1/para
                    
                part_impedence = 1/reverse_part_impedence #병렬저항의 총저항.
                total_impedence +=part_impedence
                
                if math.isinf(total_impedence[0]):
                    total_impedence = np.zeros(timelen)
                    
                print('total_impedence',total_impedence)
                print('serial:',serial)
                
                for seri in serial:
                    print(seri)
                    
                    if 'R' in seri:
                        total_impedence += self.reg_dict[seri][1]
                    elif 'L' in seri:
                        total_impedence += freq*self.ind_dict[1]
                    elif 'C' in seri:
                        total_impedence += 1/(freq*self.cap_dict[1])
                        
                print('real_total',total_impedence)
                
                if 'R' in target:
                    marker_impedence = self.reg_dict[target][1]/total_impedence
                elif 'L' in target:
                    marker_impedence = (freq*self.ind_dict[target][1])/total_impedence
                elif 'C' in target:
                    marker_impedence = (1/(freq*self.cap_dict[target][1]))*(1/total_impedence)
                    
                result_impedence = []
                print('marker_impedence:',marker_impedence[-1])
                
                for wave in plot_list:#v신호임.
                    result_impedence.append(wave*marker_impedence)
                    
                print(result_impedence)
                #plot_list.append(result_impedence)
                #plot_name_list.append('marker')
                pass
            
        except:
            print(traceback.format_exc())
            pass


        
        #그리기
        plot_len = len(plot_list)
        result = plt.figure(figsize = (10,5))
        axe_1 = result.add_subplot(2,1,1)  #시간영역.
        axe_2 = result.add_subplot(2,1,2) #주파수영역.
        
        axe_1.set_xlabel('time')
        axe_1.set_ylabel('amplitude')
        axe_2.set_xlabel('frequency')
        axe_2.set_ylabel('amplitude')
        
        for result in plot_list:
            axe_1.plot(timescale,result,label = 'source')
            fft_signal = np.fft.fft(result)/len(result)
            fft_signal_amp = abs(fft_signal)
            axe_2.plot(fft_signal_amp)
            plt.show()
            
        try:
            axe_1.plot(timescale,result_impedence[0],label = 'marker')
            axe_1.legend()
            fft_signal = np.fft.fft(result_impedence[0])/len(result_impedence[0])
            fft_signal_amp = abs(fft_signal)
            axe_2.plot(fft_signal_amp)
            
        except:
            pass
        
        axe_1.set_xlim([0,self.act_time])
        axe_2.set_xlim([0,ac_max_freq*2])
        
        plt.show()
        pass
    #생성된 개체 더블클릭 이벤트
    def QLabel_dbl_event(self,name,state):
        
        #옵션창을 부른뒤 딕셔너리에 해당 값 입력
        if state == "dc":
            self.name = name
            dc_windo = DC_opt()
            dc_windo.voltage_input.setText(str(self.dc_dict[name][1]))  #옵션창에 호출된 소자의 값 표시
            dc_windo.exec_()

            self.dc_dict[name][1] = dc_windo.value
            self.name = ""
            pass
        
        elif state == "ac":
            self.name = name
            ac_windo = Ac_opt()
            ac_windo.dc_voltage.setText(str(self.ac_dict[name][1]))
            ac_windo.ac_voltage.setText(str(self.ac_dict[name][2]))
            ac_windo.frequency.setText(str(self.ac_dict[name][3]))
            ac_windo.exec_()

            self.ac_dict[name][1] = ac_windo.dc_level
            self.ac_dict[name][2] = ac_windo.ac_volt_value
            self.ac_dict[name][3] = ac_windo.freq_value
            self.name = ""
            pass
        
        elif state == "reg":
            self.name = name
            reg_windo = Reg_opt()
            reg_windo.reg_input.setText(str(self.reg_dict[name][1]))
            reg_windo.exec_()

            self.reg_dict[name][1] = reg_windo.value
            self.name = ""
            pass
        
        elif state == "ind":
            self.name = name
            ind_windo = Ind_opt()
            ind_windo.ind_input.setText(str(self.ind_dict[name][1]))
            ind_windo.exec_()

            self.ind_dict[name][1] = ind_windo.value
            self.name = ""
            pass
        
        elif state == "cap":
            self.name = name
            cap_windo = Cap_opt()
            cap_windo.cap_input.setText(str(self.cap_dict[name][1]))
            cap_windo.exec_()

            self.cap_dict[name][1] = cap_windo.value
            self.name = ""
            pass
        self.auto_save()
        
    #개체 옮기는 이벤트
    def QLabel_move_event_press(self,event):
        print("눌럿음.")
        
        self.grab_label = event.pos()
        self.auto_save()
        pass

    def QLabel_move_event_move(self,event,name,state):
        
        try:
            
            if self.mouse_state !='wire':
                
                if state =="dc":
                    print('움직이는 중')
                    self.dc_dict[name][0].move(self.dc_dict[name][0].pos()+event.pos()-self.grab_label) 
                    self.dc_dict[name][2] = [self.dc_dict[name][0].pos().x(), self.dc_dict[name][0].pos().y()] #포지션 저장(QPaint 갱신)
                
                elif state == "ac":
                    #"Vsample" : ["QLabel_entity","DC_level ","Voltage_value","Frequency_value","postion_list"]
                    self.ac_dict[name][0].move(self.ac_dict[name][0].pos()+event.pos()-self.grab_label)
                    self.ac_dict[name][4] = [self.ac_dict[name][0].pos().x(), self.ac_dict[name][0].pos().y()]
                
                elif state == "reg":
                    #"Rsample" : ["QLabel_entity","ohm_value", "position_list"]
                    self.reg_dict[name][0].move(self.reg_dict[name][0].pos()+event.pos()-self.grab_label)
                    self.reg_dict[name][2] = [self.reg_dict[name][0].pos().x(), self.reg_dict[name][0].pos().y()]
                
                elif state == "ind":
                    #"Lsample" : ["QLabel_entity","ind_value","postion_list"]
                    self.ind_dict[name][0].move(self.ind_dict[name][0].pos()+event.pos()-self.grab_label)
                    self.ind_dict[name][2] = [self.ind_dict[name][0].pos().x(), self.ind_dict[name][0].pos().y()]
                
                elif state == "cap":
                    #"Csample" : ["QLabel_entity","cap_value","postion_list"]
                    self.cap_dict[name][0].move(self.cap_dict[name][0].pos()+event.pos()-self.grab_label)
                    self.cap_dict[name][2] = [self.cap_dict[name][0].pos().x(), self.cap_dict[name][0].pos().y()]
                
                elif state == "amp":
                    #"IOP_sample" : ["QLabel_entity","postion_list"]
                    self.amp_dict[name][0].move(self.amp_dict[name][0].pos()+event.pos()-self.grab_label)
                    self.amp_dict[name][1] = [self.amp_dict[name][0].pos().x(), self.amp_dict[name][0].pos().y()]
                
                elif state == "gnd":
                    #"gnd_sample" : ["QLabel_entity","postion_list"]
                    self.gnd_dict[name][0].move(self.gnd_dict[name][0].pos()+event.pos()-self.grab_label)
                    self.gnd_dict[name][1] = [self.gnd_dict[name][0].pos().x(), self.gnd_dict[name][0].pos().y()]
                
                elif state == "mkr":
                    #"mkr_sample" : ["QLabel_entity","postion_list"]
                    self.mkr_dict[name][0].move(self.mkr_dict[name][0].pos()+event.pos()-self.grab_label)
                    self.mkr_dict[name][1] = [self.mkr_dict[name][0].pos().x(), self.mkr_dict[name][0].pos().y()]
        except:
            print(traceback.format_exc())
            

        self.update()
        pass

    def QLabel_move_event_release(self,event):
        
        print("놓앗음.")
        self.grab_label = None
        
    #개체생성이벤트 
    def create_label(self,position_list):
        
        if self.rotate: #돌아간 상태
            
            if self.mouse_state == "dc" :
                print("함수 작동확인 ")
                #개체생성
                self.dc_cnt = self.dc_cnt+1
                name = "V"+str(self.dc_cnt)
                
                self.dc_dict[name] = [QLabel(self),1] #기본 설정 전압 : 1볼트
                position_list = [position_list[i] - 20 for i in range(len(position_list))]
                self.dc_dict[name].append(position_list)   #위치값 저장
                self.dc_dict[name].append(self.mouse_state) #종류저장
                self.dc_dict[name][0].setGeometry(position_list[0],position_list[1],90,80)  
                self.dc_pixmap = QPixmap("dc_source_rbg_rotate.png")
                self.dc_pixmap = self.dc_pixmap.scaled(QSize(90,80))
                self.dc_dict[name][0].setPixmap(self.dc_pixmap)
                self.dc_dict[name][0].show()
                self.dc_dict[name].append(self.rotate)
                state="dc"
                self.update()

                #self.dc_dict[name][0].mouseDoubleClickEvent = self.QLabel_dbi_event(name,state)   #생성한 개체 클릭시 이벤트발생
                #더블클릭해야 발동하는 이벤트여야하는데 그냥 생성과 동시에 발동되는 문제 발생
                #다른방법.
                #connect에 함수에 인자를 전달해줄려면 lambda 사용 필수.

                QDblclick(self.dc_dict[name][0]).connect(lambda : self.QLabel_dbl_event(name,state))   #설정창 여는 이벤트
                
                try:
                    self.moving_event = self.press_event   #moving event가 pressing 중 움직일때만 호출되기 때문에 그전에 생성 안됨. 따라서 따로 생성.
                    QPress(self.dc_dict[name][0]).connect(lambda : self.QLabel_move_event_press(self.press_event))     #꾹 눌러서 옮기기/
                    QMove(self.dc_dict[name][0]).connect(lambda : self.QLabel_move_event_move(self.moving_event, name, state))
                    QRelease(self.dc_dict[name][0]).connect(lambda : self.QLabel_move_event_release(self.release_event))
                
                except:
                    print(traceback.format_exc())
                pass

            elif self.mouse_state == "ac":
                self.ac_cnt = self.ac_cnt +1
                name = "V"+str(self.ac_cnt)
                self.ac_dict[name] = [QLabel(self),0,1,50]  #기본설정 0V 1V ,50Hz
                position_list = [position_list[i] - 20 for i in range(len(position_list))]
                self.ac_dict[name].append(position_list)    #위치값 추가
                self.ac_dict[name].append(self.mouse_state)

                self.ac_dict[name][0].setGeometry(position_list[0], position_list[1], 90, 60)
                self.ac_pixmap = QPixmap("ac sourse_rgb_rotate.png")
                self.ac_pixmap = self.ac_pixmap.scaled(QSize(90,60))
                self.ac_dict[name][0].setPixmap(self.ac_pixmap)
                self.ac_dict[name][0].show()
                self.ac_dict[name].append(self.rotate)
                state="ac"
                self.update()
                QDblclick(self.ac_dict[name][0]).connect(lambda : self.QLabel_dbl_event(name,state))
                
                try:
                    self.moving_event = self.press_event
                    QPress(self.ac_dict[name][0]).connect(lambda : self.QLabel_move_event_press(self.press_event))     
                    QMove(self.ac_dict[name][0]).connect(lambda : self.QLabel_move_event_move(self.moving_event, name, state))
                    QRelease(self.ac_dict[name][0]).connect(lambda : self.QLabel_move_event_release(self.release_event))
                
                except:
                    print(traceback.format_exc())
                    pass

            elif self.mouse_state == "reg":
                self.reg_cnt = self.reg_cnt+1
                name = "R"+str(self.reg_cnt)
                self.reg_dict[name] = [QLabel(self),1000] #기본 저항 1k
                position_list = [position_list[i] - 20 for i in range(len(position_list))]
                self.reg_dict[name].append(position_list)
                self.reg_dict[name].append(self.mouse_state)

                self.reg_dict[name][0].setGeometry(position_list[0], position_list[1], 70, 100)
                self.reg_pixmap = QPixmap("reg_rotate.png")
                self.reg_pixmap = self.reg_pixmap.scaled(QSize(70,100))
                self.reg_dict[name][0].setPixmap(self.reg_pixmap)
                self.reg_dict[name][0].show()
                self.reg_dict[name].append(self.rotate)
                
                state="reg"
                self.update()

                QDblclick(self.reg_dict[name][0]).connect(lambda : self.QLabel_dbl_event(name,state))
                
                try:
                    self.moving_event = self.press_event
                    QPress(self.reg_dict[name][0]).connect(lambda : self.QLabel_move_event_press(self.press_event))     
                    QMove(self.reg_dict[name][0]).connect(lambda : self.QLabel_move_event_move(self.moving_event, name, state))
                    QRelease(self.reg_dict[name][0]).connect(lambda : self.QLabel_move_event_release(self.release_event))
                except:
                    print(traceback.format_exc())
                    pass
                pass
            
            elif self.mouse_state == "ind":
                self.ind_cnt = self.ind_cnt+1
                name = "L"+str(self.ind_cnt)
                self.ind_dict[name] = [QLabel(self),0.001] #기본 인덕턴스 1mH
                position_list = [position_list[i] - 20 for i in range(len(position_list))]
                self.ind_dict[name].append(position_list)
                self.ind_dict[name].append(self.mouse_state)

                self.ind_dict[name][0].setGeometry(position_list[0], position_list[1], 70, 100)
                self.ind_pixmap = QPixmap("ind_rotate.png")
                self.ind_pixmap = self.ind_pixmap.scaled(QSize(70,100))
                self.ind_dict[name][0].setPixmap(self.ind_pixmap)
                self.ind_dict[name][0].show()
                self.ind_dict[name].append(self.rotate)
                
                state="ind"
                self.update()

                QDblclick(self.ind_dict[name][0]).connect(lambda : self.QLabel_dbl_event(name,state))
                
                try:
                    self.moving_event = self.press_event
                    
                    QPress(self.ind_dict[name][0]).connect(lambda : self.QLabel_move_event_press(self.press_event))     
                    QMove(self.ind_dict[name][0]).connect(lambda : self.QLabel_move_event_move(self.moving_event, name, state))
                    QRelease(self.ind_dict[name][0]).connect(lambda : self.QLabel_move_event_release(self.release_event))
                
                except:
                    print(traceback.format_exc())
                    pass
                
                pass
            
            elif self.mouse_state == "cap":
                self.cap_cnt = self.cap_cnt+1
                name = "C"+str(self.cap_cnt)
                self.cap_dict[name] =[QLabel(self),0.000001] #기본 축전량 1uF
                position_list = [position_list[i] - 20 for i in range(len(position_list))]
                self.cap_dict[name].append(position_list)
                self.cap_dict[name].append(self.mouse_state)

                self.cap_dict[name][0].setGeometry(position_list[0], position_list[1], 70, 100)
                self.cap_pixmap = QPixmap("cap_rotate.png")
                self.cap_pixmap = self.cap_pixmap.scaled(QSize(70,100))
                self.cap_dict[name][0].setPixmap(self.cap_pixmap)
                self.cap_dict[name][0].show()
                self.cap_dict[name].append(self.rotate)
                state = "cap"
                self.update()
                
                QDblclick(self.cap_dict[name][0]).connect(lambda : self.QLabel_dbl_event(name,state))
                
                try:
                    self.moving_event = self.press_event
                    QPress(self.cap_dict[name][0]).connect(lambda : self.QLabel_move_event_press(self.press_event))     
                    QMove(self.cap_dict[name][0]).connect(lambda : self.QLabel_move_event_move(self.moving_event, name, state))
                    QRelease(self.cap_dict[name][0]).connect(lambda : self.QLabel_move_event_release(self.release_event))
                
                except:
                    print(traceback.format_exc())
                    pass
                
                pass
            
            #이 밑으로 개체 설정 이벤트 없음. #amp나 그외 rotate 미구현.
            elif self.mouse_state == "amp":
                self.amp_cnt = self.amp_cnt+1
                name = "IOP"+str(self.amp_cnt)
                self.amp_dict[name] = [QLabel(self)]
                position_list = [position_list[i] - 20 for i in range(len(position_list))]
                self.amp_dict[name].append(position_list)
                self.amp_dict[name].append(self.mouse_state)

                self.amp_dict[name][0].setGeometry(position_list[0], position_list[1], 210, 180)
                self.amp_pixmap = QPixmap("op_amp.png")
                self.amp_pixmap = self.amp_pixmap.scaled(QSize(210,180))
                self.amp_dict[name][0].setPixmap(self.amp_pixmap)
                self.amp_dict[name][0].show()
                state = "amp"
                self.update()
                
                try:
                    self.moving_event = self.press_event
                    QPress(self.amp_dict[name][0]).connect(lambda : self.QLabel_move_event_press(self.press_event))     
                    QMove(self.amp_dict[name][0]).connect(lambda : self.QLabel_move_event_move(self.moving_event, name, state))
                    QRelease(self.amp_dict[name][0]).connect(lambda : self.QLabel_move_event_release(self.release_event))
                except:
                    print(traceback.format_exc())
                    
                    pass 
                pass
            
            elif self.mouse_state == "gnd":
                self.gnd_cnt = self.gnd_cnt+1
                name = "gnd"+str(self.gnd_cnt)
                self.gnd_dict[name] = [QLabel(self)]
                position_list = [position_list[i] - 20 for i in range(len(position_list))]
                
                self.gnd_dict[name].append(position_list)
                self.gnd_dict[name].append(self.mouse_state)

                self.gnd_dict[name][0].setGeometry(position_list[0],position_list[1],60,70)
                self.gnd_pixmap = QPixmap("gnd_rotate.png")
                self.gnd_pixmap = self.gnd_pixmap.scaled(QSize(60,70))
                
                self.gnd_dict[name][0].setPixmap(self.gnd_pixmap)
                self.gnd_dict[name][0].show()
                self.gnd_dict[name].append(self.rotate)
                state = "gnd"
                self.update()
                
                try:
                    self.moving_event = self.press_event
                    QPress(self.gnd_dict[name][0]).connect(lambda : self.QLabel_move_event_press(self.press_event))     
                    QMove(self.gnd_dict[name][0]).connect(lambda : self.QLabel_move_event_move(self.moving_event, name, state))
                    QRelease(self.gnd_dict[name][0]).connect(lambda : self.QLabel_move_event_release(self.release_event))
                except:
                    print(traceback.format_exc())
                    self.moving_event = self.press_event
                    pass
                
                

            elif self.mouse_state == "wire":
                #그리기 이벤트인데 만들어 뒀던 각 라벨과 연동시킬수 있도록 짜야됨.
                pass
            
            elif self.mouse_state =="marker":
                
                if self.mkr_cnt >= 1:
                    pass
                else:
                    self.mkr_cnt+=1
                    name = "mkr"+str(self.mkr_cnt)
                    self.mkr_dict[name] = [QLabel(self)]
                    position_list = [position_list[i] - 20 for i in range(len(position_list))]
                    self.mkr_dict[name].append(position_list)
                    self.mkr_dict[name].append(self.mouse_state)

                    self.mkr_dict[name][0].setGeometry(position_list[0],position_list[1],20,60)
                    self.mkr_pixmap = QPixmap("marker.png")
                    self.mkr_pixmap = self.mkr_pixmap.scaled(QSize(20,60))
                    self.mkr_dict[name][0].setPixmap(self.mkr_pixmap)
                    self.mkr_dict[name][0].show()
                    
                    state = "mkr"
                    self.update()
                    
                    try:
                        self.moving_event = self.press_event
                        QPress(self.mkr_dict[name][0]).connect(lambda : self.QLabel_move_event_press(self.press_event))     
                        QMove(self.mkr_dict[name][0]).connect(lambda : self.QLabel_move_event_move(self.moving_event, name, state))
                        QRelease(self.mkr_dict[name][0]).connect(lambda : self.QLabel_move_event_release(self.release_event))
                    
                    except:
                        print(traceback.format_exc())
                        self.moving_event = self.press_event
                        pass
                    #self.
                    pass
            pass
        else: #안돌아간 상태
            if self.mouse_state == "dc" :
                print("함수 작동확인 ")
                #개체생성
                self.dc_cnt = self.dc_cnt+1
                name = "V"+str(self.dc_cnt)
                
                self.dc_dict[name] = [QLabel(self),1] #기본 설정 전압 : 1볼트
                position_list = [position_list[i] - 20 for i in range(len(position_list))]
                self.dc_dict[name].append(position_list)   #위치값 저장
                self.dc_dict[name].append(self.mouse_state) #종류저장
                self.dc_dict[name][0].setGeometry(position_list[0],position_list[1],80,90)  
                self.dc_pixmap = QPixmap("dc_source_rbg.png")
                self.dc_pixmap = self.dc_pixmap.scaled(QSize(80,90))
                self.dc_dict[name][0].setPixmap(self.dc_pixmap)
                self.dc_dict[name][0].show()
                self.dc_dict[name].append(self.rotate)
                state="dc"
                self.update()

                #self.dc_dict[name][0].mouseDoubleClickEvent = self.QLabel_dbi_event(name,state)   #생성한 개체 클릭시 이벤트발생
                #더블클릭해야 발동하는 이벤트여야하는데 그냥 생성과 동시에 발동되는 문제 발생
                #다른방법.
                #connect에 함수에 인자를 전달해줄려면 lambda 사용 필수.

                QDblclick(self.dc_dict[name][0]).connect(lambda : self.QLabel_dbl_event(name,state))   #설정창 여는 이벤트
                
                try:
                    self.moving_event = self.press_event   #moving event가 pressing 중 움직일때만 호출되기 때문에 그전에 생성 안됨. 따라서 따로 생성.
                    QPress(self.dc_dict[name][0]).connect(lambda : self.QLabel_move_event_press(self.press_event))     #꾹 눌러서 옮기기/
                    QMove(self.dc_dict[name][0]).connect(lambda : self.QLabel_move_event_move(self.moving_event, name, state))
                    QRelease(self.dc_dict[name][0]).connect(lambda : self.QLabel_move_event_release(self.release_event))
                
                except:
                    print(traceback.format_exc())
                pass

            elif self.mouse_state == "ac":
                self.ac_cnt = self.ac_cnt +1
                name = "V"+str(self.ac_cnt)
                self.ac_dict[name] = [QLabel(self),0,1,50]  #기본설정 0V 1V ,50Hz
                position_list = [position_list[i] - 20 for i in range(len(position_list))]
                self.ac_dict[name].append(position_list)    #위치값 추가
                self.ac_dict[name].append(self.mouse_state)

                self.ac_dict[name][0].setGeometry(position_list[0], position_list[1], 60, 90)
                self.ac_pixmap = QPixmap("ac sourse_rgb")
                self.ac_pixmap = self.ac_pixmap.scaled(QSize(60,90))
                self.ac_dict[name][0].setPixmap(self.ac_pixmap)
                self.ac_dict[name][0].show()
                self.ac_dict[name].append(self.rotate)
                state="ac"
                self.update()
                QDblclick(self.ac_dict[name][0]).connect(lambda : self.QLabel_dbl_event(name,state))
                
                try:
                    self.moving_event = self.press_event
                    QPress(self.ac_dict[name][0]).connect(lambda : self.QLabel_move_event_press(self.press_event))     
                    QMove(self.ac_dict[name][0]).connect(lambda : self.QLabel_move_event_move(self.moving_event, name, state))
                    QRelease(self.ac_dict[name][0]).connect(lambda : self.QLabel_move_event_release(self.release_event))
                
                except:
                    print(traceback.format_exc())
                    pass

            elif self.mouse_state == "reg":
                
                self.reg_cnt = self.reg_cnt+1
                name = "R"+str(self.reg_cnt)
                self.reg_dict[name] = [QLabel(self),1000] #기본 저항 1k
                position_list = [position_list[i] - 20 for i in range(len(position_list))]
                self.reg_dict[name].append(position_list)
                self.reg_dict[name].append(self.mouse_state)

                self.reg_dict[name][0].setGeometry(position_list[0], position_list[1], 100, 70)
                self.reg_pixmap = QPixmap("reg.png")
                self.reg_pixmap = self.reg_pixmap.scaled(QSize(100,70))
                self.reg_dict[name][0].setPixmap(self.reg_pixmap)
                self.reg_dict[name][0].show()
                self.reg_dict[name].append(self.rotate)
                state="reg"
                self.update()

                QDblclick(self.reg_dict[name][0]).connect(lambda : self.QLabel_dbl_event(name,state))
                
                try:
                    self.moving_event = self.press_event
                    QPress(self.reg_dict[name][0]).connect(lambda : self.QLabel_move_event_press(self.press_event))     
                    QMove(self.reg_dict[name][0]).connect(lambda : self.QLabel_move_event_move(self.moving_event, name, state))
                    QRelease(self.reg_dict[name][0]).connect(lambda : self.QLabel_move_event_release(self.release_event))
                
                except:
                    print(traceback.format_exc())
                    pass
                pass
            
            elif self.mouse_state == "ind":
                self.ind_cnt = self.ind_cnt+1
                name = "L"+str(self.ind_cnt)
                self.ind_dict[name] = [QLabel(self),0.001] #기본 인덕턴스 1mH
                position_list = [position_list[i] - 20 for i in range(len(position_list))]
                self.ind_dict[name].append(position_list)
                self.ind_dict[name].append(self.mouse_state)

                self.ind_dict[name][0].setGeometry(position_list[0], position_list[1], 100, 70)
                self.ind_pixmap = QPixmap("ind.png")
                self.ind_pixmap = self.ind_pixmap.scaled(QSize(100,70))
                self.ind_dict[name][0].setPixmap(self.ind_pixmap)
                self.ind_dict[name][0].show()
                self.ind_dict[name].append(self.rotate)
                state="ind"
                self.update()

                QDblclick(self.ind_dict[name][0]).connect(lambda : self.QLabel_dbl_event(name,state))
                
                try:
                    self.moving_event = self.press_event
                    QPress(self.ind_dict[name][0]).connect(lambda : self.QLabel_move_event_press(self.press_event))     
                    QMove(self.ind_dict[name][0]).connect(lambda : self.QLabel_move_event_move(self.moving_event, name, state))
                    QRelease(self.ind_dict[name][0]).connect(lambda : self.QLabel_move_event_release(self.release_event))
                except:
                    print(traceback.format_exc())
                    pass
                
                pass
            
            elif self.mouse_state == "cap":
                self.cap_cnt = self.cap_cnt+1
                name = "C"+str(self.cap_cnt)
                self.cap_dict[name] =[QLabel(self),0.000001] #기본 축전량 1uF
                position_list = [position_list[i] - 20 for i in range(len(position_list))]
                
                self.cap_dict[name].append(position_list)
                self.cap_dict[name].append(self.mouse_state)

                self.cap_dict[name][0].setGeometry(position_list[0], position_list[1], 100, 70)
                self.cap_pixmap = QPixmap("cap.png")
                self.cap_pixmap = self.cap_pixmap.scaled(QSize(100,70))
                
                self.cap_dict[name][0].setPixmap(self.cap_pixmap)
                self.cap_dict[name][0].show()
                self.cap_dict[name].append(self.rotate)
                state = "cap"
                self.update()
                
                QDblclick(self.cap_dict[name][0]).connect(lambda : self.QLabel_dbl_event(name,state))
                
                try:
                    self.moving_event = self.press_event
                    QPress(self.cap_dict[name][0]).connect(lambda : self.QLabel_move_event_press(self.press_event))     
                    QMove(self.cap_dict[name][0]).connect(lambda : self.QLabel_move_event_move(self.moving_event, name, state))
                    QRelease(self.cap_dict[name][0]).connect(lambda : self.QLabel_move_event_release(self.release_event))
                except:
                    print(traceback.format_exc())
                    pass
                
                pass
            
            #이 밑으로 개체 설정 이벤트 없음. 
            elif self.mouse_state == "amp":
                self.amp_cnt = self.amp_cnt+1
                name = "IOP"+str(self.amp_cnt)
                self.amp_dict[name] = [QLabel(self)]
                position_list = [position_list[i] - 20 for i in range(len(position_list))]
                self.amp_dict[name].append(position_list)
                self.amp_dict[name].append(self.mouse_state)

                self.amp_dict[name][0].setGeometry(position_list[0], position_list[1], 210, 180)
                self.amp_pixmap = QPixmap("op_amp.png")
                self.amp_pixmap = self.amp_pixmap.scaled(QSize(210,180))
                self.amp_dict[name][0].setPixmap(self.amp_pixmap)
                self.amp_dict[name][0].show()
                self.amp_dict[name].append(self.rotate)
                state = "amp"
                self.update()
                
                try:
                    self.moving_event = self.press_event
                    QPress(self.amp_dict[name][0]).connect(lambda : self.QLabel_move_event_press(self.press_event))     
                    QMove(self.amp_dict[name][0]).connect(lambda : self.QLabel_move_event_move(self.moving_event, name, state))
                    QRelease(self.amp_dict[name][0]).connect(lambda : self.QLabel_move_event_release(self.release_event))
                except:
                    print(traceback.format_exc())
                    pass 
                pass
            
            elif self.mouse_state == "gnd":
                self.gnd_cnt = self.gnd_cnt+1
                name = "gnd"+str(self.gnd_cnt)
                self.gnd_dict[name] = [QLabel(self)]
                position_list = [position_list[i] - 20 for i in range(len(position_list))]
                self.gnd_dict[name].append(position_list)
                self.gnd_dict[name].append(self.mouse_state)

                self.gnd_dict[name][0].setGeometry(position_list[0],position_list[1],60,70)
                self.gnd_pixmap = QPixmap("gnd.png")
                self.gnd_pixmap = self.gnd_pixmap.scaled(QSize(60,70))
                self.gnd_dict[name][0].setPixmap(self.gnd_pixmap)
                self.gnd_dict[name][0].show()
                self.gnd_dict[name].append(self.rotate)
                state = "gnd"
                self.update()
                
                try:
                    self.moving_event = self.press_event
                    QPress(self.gnd_dict[name][0]).connect(lambda : self.QLabel_move_event_press(self.press_event))     
                    QMove(self.gnd_dict[name][0]).connect(lambda : self.QLabel_move_event_move(self.moving_event, name, state))
                    QRelease(self.gnd_dict[name][0]).connect(lambda : self.QLabel_move_event_release(self.release_event))
                except:
                    print(traceback.format_exc())
                    self.moving_event = self.press_event
                    pass
                
                

            elif self.mouse_state == "wire":
                #그리기 이벤트인데 만들어 뒀던 각 라벨과 연동시킬수 있도록 짜야됨.
                pass
            
            elif self.mouse_state =="marker":
                if self.mkr_cnt >= 1:
                    pass
                else:
                    self.mkr_cnt+=1
                    name = "mkr"+str(self.mkr_cnt)
                    self.mkr_dict[name] = [QLabel(self)]
                    position_list = [position_list[i] - 20 for i in range(len(position_list))]
                    
                    self.mkr_dict[name].append(position_list)
                    self.mkr_dict[name].append(self.mouse_state)

                    self.mkr_dict[name][0].setGeometry(position_list[0],position_list[1],20,60)
                    self.mkr_pixmap = QPixmap("marker.png")
                    self.mkr_pixmap = self.mkr_pixmap.scaled(QSize(20,60))
                    
                    self.mkr_dict[name][0].setPixmap(self.mkr_pixmap)
                    self.mkr_dict[name][0].show()
                    state = "mkr"
                    self.update()
                    
                    try:
                        self.moving_event = self.press_event
                        QPress(self.mkr_dict[name][0]).connect(lambda : self.QLabel_move_event_press(self.press_event))     
                        QMove(self.mkr_dict[name][0]).connect(lambda : self.QLabel_move_event_move(self.moving_event, name, state))
                        QRelease(self.mkr_dict[name][0]).connect(lambda : self.QLabel_move_event_release(self.release_event))
                    except:
                        print(traceback.format_exc())
                        self.moving_event = self.press_event
                        pass
                    #self.
                    pass
        self.auto_save()
    pass


    #와이어로 연결한 디바이스들 판단하고 데이터로 남기는 함수.
    def device_connect_wire(self,connection):
        
        point_a = connection[0]
        point_b = connection[1]
        node_name = 'node'+str(self.node_cnt)     #self.node_dict[node_name] 에 연결선 좌표들이 저장되어있음.
        dif = 5
        device_a = node_name
        device_b = node_name

        #연결선이 끼어있을 경우.
        for node in self.node_dict:# == node_name {'node_name' : [ [ [시작좌표],[끝좌표] ], [ [시작좌표],[끝좌표] ], [ [시작좌표],[끝좌표] ] ]}
            
            a_state = False
            b_state = False
            node_diff = 3
            
            if node == node_name:  #현재 상태는 따로 계산(맨마지막에 계산하므로 덮어써버림.).
                continue
            elif node == 'node_sample': #샘플제외.
                continue
            else:
                
                for tmp in self.node_dict[node]:  # [ [시작좌표],[끝좌표] ]
                    for point in tmp: #2번반복. [시작좌표], [끝좌표]
                        
                        if abs(point_a[0]-point[0])<node_diff and abs(point_a[1] - point[1])<node_diff:
                            device_a = node
                            a_state = True
                        elif abs(point_b[0]-point[0])<node_diff and abs(point_b[1] - point[1])<node_diff:
                            device_b = node
                            b_state = True
                        else:
                            continue
            pass
        #"Vsample" : ["QLabel_entity","Voltage_value","position_list","dc"] size 80,90
        for k in range(1,self.dc_cnt+1):
            name = "V"+ str(k)
            tmp = self.dc_dict[name]
            
            if self.dc_dict[name][-1]: #회전된 상태
                plus_port_x = tmp[2][0]+95   #단자부분의 위치
                plus_port_y = tmp[2][1]+39
                minus_port_x = plus_port_x - 100
                minus_port_y = plus_port_y
            
            else:#회전안된상태
                plus_port_x = tmp[2][0]+40   #단자부분의 위치
                plus_port_y = tmp[2][1]-5
                minus_port_x = plus_port_x
                minus_port_y = plus_port_y+100
                
            if abs(point_a[0]-plus_port_x)<dif and abs(point_a[1]-plus_port_y)<dif:
                device_a = name+'_dc_plus'  #개체 이름 저장[name , 극성, dc or ac] dc일시 0 ac일시 1
                
            if abs(point_a[0]-minus_port_x)<dif and abs(point_a[1]-minus_port_y)<dif:
                device_a = name+'_dc_minus'
                
            if abs(point_b[0]-plus_port_x)<dif and abs(point_b[1]-plus_port_y)<dif:
                device_b = name+'_dc_plus'
                
            if abs(point_b[0]-minus_port_x)<dif and abs(point_b[1]-minus_port_y)<dif:
                device_b = name+'_dc_minus'
                    
        for k in range(1,self.ac_cnt+1):
            #"Vsample" : ["QLabel_entity","DC_level ","Voltage_value","Frequency_value","postion_list","ac"] size 60,90
            name = "V"+ str(k) 
            tmp = self.ac_dict[name]
            
            if self.ac_dict[name][-1]:
                plus_port_x = tmp[4][0]+95   #단자부분의 위치
                plus_port_y = tmp[4][1]+30
                
                minus_port_x = plus_port_x-100
                minus_port_y = plus_port_y
            else:
                plus_port_x = tmp[4][0]+30   #단자부분의 위치
                plus_port_y = tmp[4][1]-5
                
                minus_port_x = plus_port_x
                minus_port_y = plus_port_y+100

            if abs(point_a[0]-plus_port_x)<dif and abs(point_a[1]-plus_port_y)<dif:
                device_a = name+'_ac_plus'   #개체 저장.
                
            elif abs(point_a[0]-minus_port_x)<dif and abs(point_a[1]-minus_port_y)<dif:
                device_a = name+'_ac_minus'
                
            elif abs(point_b[0]-plus_port_x)<dif and abs(point_b[1]-plus_port_y)<dif:
                device_b = name+'_ac_plus'   #개체 저장.
                
            elif abs(point_b[0]-minus_port_x)<dif and abs(point_b[1]-minus_port_y)<dif:
                device_a = name+'_ac_minus'
                
            else:
                continue
            
        for k in range(1,self.reg_cnt+1):
            #"Rsample" : ["QLabel_entity","ohm_value", "position_list","reg"] size 100,70
            name = "R"+ str(k) 
            tmp = self.reg_dict[name]
            
            if self.reg_dict[name][-1]:
                a_port_x = tmp[2][0]+35   #단자부분의 위치
                a_port_y = tmp[2][1] - 5
                b_port_x = a_port_x
                b_port_y = a_port_y + 110
            else:
                a_port_x = tmp[2][0]-5   #단자부분의 위치
                a_port_y = tmp[2][1] + 35
                b_port_x = a_port_x + 110
                b_port_y = a_port_y

            if abs(point_a[0]-a_port_x)<dif and abs(point_a[1]-a_port_y)<dif:
                device_a = name+'_a'  #단자부분 왼쪽단자일경우 0 오른쪽일경우 1
            elif abs(point_a[0]-b_port_x)<dif and abs(point_a[1]-b_port_y)<dif:
                device_a = name+'_b'
            elif abs(point_b[0]-a_port_x)<dif and abs(point_b[1]-a_port_y)<dif:
                device_b = name+'_a'
            elif abs(point_b[0]-b_port_x)<dif and abs(point_b[1]-b_port_y)<dif:
                device_b = name+'_b'
            else:
                continue
        for k in range(1,self.ind_cnt+1):
            #""Lsample" : ["QLabel_entity","ind_value","postion_list","ind"] size 100,70
            name = "L"+ str(k) 
            tmp = self.ind_dict[name]
            
            if self.ind_dict[name][-1]:
                a_port_x = tmp[2][0] +27   #단자부분의 위치
                a_port_y = tmp[2][1] -5
                b_port_x = a_port_x
                b_port_y = a_port_y +110
                
            else:
                a_port_x = tmp[2][0] -5   #단자부분의 위치
                a_port_y = tmp[2][1] + 41
                b_port_x = a_port_x + 110
                b_port_y = a_port_y

            if abs(point_a[0]-a_port_x)<dif and abs(point_a[1]-a_port_y)<dif:
                device_a = name+'_a'   
                
            elif abs(point_a[0]-b_port_x)<dif and abs(point_a[1]-b_port_y)<dif:
                device_a = name+'_b'
                
            elif abs(point_b[0]-a_port_x)<dif and abs(point_b[1]-a_port_y)<dif:
                device_b = name+'_a'
                
            elif abs(point_b[0]-b_port_x)<dif and abs(point_b[1]-b_port_y)<dif:
                device_b = name+'_b'
            else:
                continue
        
        for k in range(1,self.cap_cnt+1):
            #""Csample" : ["QLabel_entity","cap_value","postion_list","ind"] size 100,70
            name = "C"+ str(k) 
            tmp = self.cap_dict[name]
            
            if self.cap_dict[name][-1]:
                a_port_x = tmp[2][0] +35   #단자부분의 위치
                a_port_y = tmp[2][1] - 5
                b_port_x = a_port_x 
                b_port_y = a_port_y +110
            else:
                a_port_x = tmp[2][0] - 5   #단자부분의 위치
                a_port_y = tmp[2][1] + 35
                b_port_x = a_port_x + 110
                b_port_y = a_port_y

            if abs(point_a[0]-a_port_x)<dif and abs(point_a[1]-a_port_y)<dif:
                device_a = name+'_a'    
            elif abs(point_a[0]-b_port_x)<dif and abs(point_a[1]-b_port_y)<dif:
                device_a = name+'_b'
            elif abs(point_b[0]-a_port_x)<dif and abs(point_b[1]-a_port_y)<dif:
                device_b = name+'_a'
            elif abs(point_b[0]-b_port_x)<dif and abs(point_b[1]-b_port_y)<dif:
                device_b = name+'_b'
            else:
                continue
        
        for k in range(1,self.amp_cnt+1):
            #""IOPsample" : ["QLabel_entity","postion_list","amp"] size 210,180
            name = "IOP"+ str(k) 
            tmp = self.amp_dict[name]   
            pos_input_x = tmp[1][0] - 5
            pos_input_y = tmp[1][1] + 37
            neg_input_x = pos_input_x
            neg_input_y = tmp[1][1] + 144
            output_x = pos_input_x +220
            output_y = tmp[1][1] + 90

            if abs(point_a[0]-pos_input_x)<dif or abs(point_a[1]-pos_input_y)<dif:
                device_a = name + '_pos'
            elif abs(point_a[0] - neg_input_x)<dif or abs(point_a[1] - neg_input_y)<dif:
                device_a = name + '_neg'
            elif abs(point_a[0] - output_x)<dif or abs(point_a[1] - output_x)<dif:
                device_a = name + '_out'
            elif abs(point_b[0] - pos_input_x)<dif or abs(point_b[1] - pos_input_y)<dif:
                device_b = name + '_pos'
            elif abs(point_b[0] - neg_input_x)<dif or abs(point_b[1] - neg_input_y)<dif:
                device_b = name + '_neg'
            elif abs(point_b[0] - output_x)<dif or abs(point_b[1] - output_y)<dif:
                device_b = name + '_out'
                
        for k in range(1,self.gnd_cnt+1):
            #""gnd_sample" : ["QLabel_entity","postion_list",'gnd'] size 60,70
            name = "gnd"+ str(k) 
            tmp = self.gnd_dict[name]
            
            if self.gnd_dict[name][-1]:
                port_x = tmp[1][0] +30
                port_y = tmp[1][1] +75
            else:
                port_x = tmp[1][0] +30
                port_y = tmp[1][1] - 5
                
            if abs(point_a[0]-port_x)<dif and abs(point_a[1]-port_y)<dif:
                device_a = name  
            elif abs(point_b[0]- port_x)<dif and abs(point_b[1]- port_y)<dif:
                device_b = name   
            else:
                continue
            pass
        
        try:
            print(device_a , node_name ,device_b, sep='\n')
            return [device_a, node_name , device_b]
        except:  #와이어끼리 엮을 방법 필요   해결
            pass
        
    #페인팅 이벤트
    def paintEvent(self, event):
        
        qp = QPainter(self)
        qp.setFont(QFont('나눔고딕',10))
        
        #전부다 일일이 지정(업뎃마다 하므로 개체 이동시에도 텍스트 따라감.)
        try:
            
            #dc_name표시
            for i in range(1,self.dc_cnt+1):
                name = "V"+str(i)
                #name:["QLabel_entity","Voltage_value","position_list"]  size 80,90
                position = self.dc_dict[name][2]
                
                if self.dc_dict[name][-1]: #돌아간 상태
                    qp.drawText(position[0]+40,position[1],name)
                    qp.drawRect(position[0]-10,position[1]+35,10,10)
                    qp.drawRect(position[0]+87,position[1]+35,10,10)
                    
                else:#정상
                    qp.drawText(position[0]+70,position[1]+50,name)
                    qp.drawRect(position[0]+35,position[1]-10,10,10)
                    qp.drawRect(position[0]+35,position[1]+90,10,10)
            #ac
            
            for i in range(1,self.ac_cnt+1):
                
                name = "V"+str(i)
                #name: ["QLabel_entity","DC_level ","Voltage_value","Frequency_value","postion_list"] size 60,90
                position = self.ac_dict[name][4]
                
                if self.ac_dict[name][-1]:
                    qp.drawText(position[0]+55,position[1],name)
                    qp.drawRect(position[0]-10,position[1]+25,10,10)
                    qp.drawRect(position[0]+90,position[1]+25,10,10)
                    
                else:
                    qp.drawText(position[0]+60,position[1]+45,name)
                    qp.drawRect(position[0]+25,position[1]-10,10,10)
                    qp.drawRect(position[0]+25,position[1]+90,10,10)
            
            #reg
            for i in range(1,self.reg_cnt+1):
                
                name = "R"+str(i)
                #name: ["QLabel_entity","ohm_value", "position_list"] size 100,70
                position = self.reg_dict[name][2]
                
                if self.reg_dict[name][-1]:
                    qp.drawText(position[0]+70,position[1]+50,name)
                    qp.drawRect(position[0]+30,position[1]-10,10,10)
                    qp.drawRect(position[0]+30,position[1]+100,10,10)
                    
                else:
                    qp.drawText(position[0]+35,position[1],name)
                    qp.drawRect(position[0]-10,position[1]+30,10,10)
                    qp.drawRect(position[0]+100,position[1]+30,10,10)
            
            for i in range(1,self.ind_cnt+1):
                name = "L"+str(i)
                #name :  ["QLabel_entity","ind_value","postion_list"] size 100,70
                position = self.ind_dict[name][2]
                
                if self.ind_dict[name][-1]:
                    qp.drawText(position[0]+65, position[1]+50, name)
                    qp.drawRect(position[0]+23,position[1]-10,10,10)    
                    qp.drawRect(position[0]+23,position[1]+100,10,10)
                    
                else:
                    qp.drawText(position[0]+35, position[1], name)
                    qp.drawRect(position[0]-10,position[1]+36,10,10)    
                    qp.drawRect(position[0]+100,position[1]+36,10,10)

            for i in range(1,self.cap_cnt+1):
                name = "C"+str(i)
                #name : ["QLabel_entity","cap_value","postion_list"] size 100,70
                position = self.cap_dict[name][2]
                
                if self.cap_dict[name][-1]:
                    qp.drawText(position[0]+65, position[1]+50, name)
                    qp.drawRect(position[0]+30,position[1]-10,10,10)
                    qp.drawRect(position[0]+30,position[1]+100,10,10)
                    
                else:
                    qp.drawText(position[0]+35, position[1], name)
                    qp.drawRect(position[0]-10,position[1]+30,10,10)
                    qp.drawRect(position[0]+100,position[1]+30,10,10)
            
            for i in range(1,self.amp_cnt+1):
                name = "IOP"+str(i)
                #name : ["QLabel_entity","postion_list"] size 210, 180
                position = self.amp_dict[name][1]
                qp.drawText(position[0]+130, position[1]+50, name)  #y : 37,144,90   ,x 210
                qp.drawRect(position[0]-10,position[1]+32,10,10)
                qp.drawRect(position[0]-10,position[1]+139,10,10)
                qp.drawRect(position[0]+210,position[1]+85,10,10)
            pass
        
            for i in range(1,self.gnd_cnt+1):
                name = 'gnd'+str(i)
                position = self.gnd_dict[name][1]
                
                if self.gnd_dict[name][-1]:
                    qp.drawRect(position[0]+25,position[1]+67,10,10)
                else:
                    qp.drawRect(position[0]+25,position[1]-10,10,10)
                    
            #임시로 그리는 친구.
            for k in self.tmp_draw_wire: #구조 [ [[start],[moving_point]] , [[start],[moving_point]] ]
                start_x = k[0][0]
                start_y = k[0][1]
                move_x = k[1][0]
                move_y = k[1][1]
                qp.drawLine(start_x,start_y,move_x,move_y)
                
            #영구적으로 그리는 친구.
            for wire in self.draw_wire:
                
                if len(wire) == 0:
                    pass
                else:
                    
                    for k in wire:
                        start_x = k[0][0]
                        start_y = k[0][1]
                        move_x = k[1][0]
                        move_y = k[1][1]
                        qp.drawLine(start_x,start_y,move_x,move_y)
                    pass
                pass
        
        except:
            print("실패")
            print(traceback.format_exc())
            pass
        
        qp.end()
        pass
    
    # 마우스 커서를 설정하는 함수
    def set_mouse(self):
        
        # self.rotate가 True일 때, 회전된 이미지를 사용하여 마우스 커서를 설정
        if self.rotate: #돌아간 상태
            
            # 마우스 상태가 "dc"인 경우
            if self.mouse_state == "dc":
                dc_pixmap = QPixmap("dc_source_rbg_rotate.png") # 회전된 DC 소스 이미지 로드
                dc_pixmap =dc_pixmap.scaled(90,90) # 이미지 크기 조정
                temp_cursor = QCursor(dc_pixmap) # 이미지로 커서 생성
                QApplication.setOverrideCursor(temp_cursor) # 현재 커서를 새 커서로 설정
                pass
            
            # 마우스 상태가 "ac"인 경우
            elif self.mouse_state == "ac":
                
                ac_pixmap = QPixmap("ac sourse_rgb_rotate.png") # 회전된 AC 소스 이미지 로드
                ac_pixmap = ac_pixmap.scaled(90,70) # 이미지 크기 조정
                temp_cursor = QCursor(ac_pixmap) # 이미지로 커서 생성
                
                QApplication.setOverrideCursor(temp_cursor) # 현재 커서를 새 커서로 설정
                pass
            
            # 마우스 상태가 "reg"인 경우
            elif self.mouse_state == "reg":
                reg_pixmap = QPixmap("reg_rotate.png") # 회전된 Reg 이미지 로드
                reg_pixmap = reg_pixmap.scaled(QSize(70,90)) # 이미지 크기 조정
                temp_cursor = QCursor(reg_pixmap,20,20)   #리사이즈 필요 너무큼
                
                QApplication.setOverrideCursor(temp_cursor) # 현재 커서를 새 커서로 설정
                pass
            
            # 마우스 상태가 "ind"인 경우
            elif self.mouse_state == "ind":
                ind_pixmap = QPixmap("ind_rotate.png") # 회전된 Ind 이미지 로드
                ind_pixmap = ind_pixmap.scaled(QSize(80,110)) # 이미지 크기 조정
                temp_cursor = QCursor(ind_pixmap,20,20) # 이미지로 커서 생성 (커서 핫스팟 지정)
                
                QApplication.setOverrideCursor(temp_cursor) # 현재 커서를 새 커서로 설정
                pass
            
            # 마우스 상태가 "cap"인 경우
            elif self.mouse_state == "cap":
                cap_pixmap = QPixmap("cap_rotate.png") # 회전된 Cap 이미지 로드
                cap_pixmap = cap_pixmap.scaled(QSize(70,90)) # 이미지 크기 조정
                temp_cursor = QCursor(cap_pixmap,20,20) # 이미지로 커서 생성 (커서 핫스팟 지정)
                
                QApplication.setOverrideCursor(temp_cursor) # 현재 커서를 새 커서로 설정
                pass
            pass
        
        # self.rotate가 False일 때, 기본 이미지를 사용하여 마우스 커서를 설정
        else: #그대로인 상태.
            
            # 마우스 상태가 "dc"인 경우
            if self.mouse_state == "dc":
                dc_pixmap = QPixmap("dc_source_rbg.png") # 기본 DC 소스 이미지 로드
                dc_pixmap =dc_pixmap.scaled(90,90) # 이미지 크기 조정
                temp_cursor = QCursor(dc_pixmap) # 이미지로 커서 생성
                
                QApplication.setOverrideCursor(temp_cursor) # 현재 커서를 새 커서로 설정
                pass
            
            # 마우스 상태가 "ac"인 경우
            elif self.mouse_state == "ac":
                ac_pixmap = QPixmap("ac sourse_rgb.png") # 기본 AC 소스 이미지 로드
                ac_pixmap = ac_pixmap.scaled(70,90) # 이미지 크기 조정
                temp_cursor = QCursor(ac_pixmap) # 이미지로 커서 생성
                
                QApplication.setOverrideCursor(temp_cursor) # 현재 커서를 새 커서로 설정
                pass
            
            # 마우스 상태가 "reg"인 경우
            elif self.mouse_state == "reg":
                reg_pixmap = QPixmap("reg.png") # 기본 Reg 이미지 로드
                reg_pixmap = reg_pixmap.scaled(QSize(90,70)) # 이미지 크기 조정
                temp_cursor = QCursor(reg_pixmap,20,20)   #리사이즈 필요 너무큼
                
                QApplication.setOverrideCursor(temp_cursor) # 현재 커서를 새 커서로 설정
                pass
            
            # 마우스 상태가 "ind"인 경우
            elif self.mouse_state == "ind":
                ind_pixmap = QPixmap("ind.png") # 기본 Ind 이미지 로드
                ind_pixmap = ind_pixmap.scaled(QSize(110,80)) # 이미지 크기 조정
                temp_cursor = QCursor(ind_pixmap,20,20)
                
                QApplication.setOverrideCursor(temp_cursor) # 현재 커서를 새 커서로 설정
                pass
            
            # 마우스 상태가 "cap"인 경우
            elif self.mouse_state == "cap":
                cap_pixmap = QPixmap("cap.png") # 기본 Cap 이미지 로드
                cap_pixmap = cap_pixmap.scaled(QSize(90,70)) # 이미지 크기 조정
                temp_cursor = QCursor(cap_pixmap,20,20)
                
                QApplication.setOverrideCursor(temp_cursor) # 현재 커서를 새 커서로 설정
                pass
        pass
            
    # 메인 윈도우 마우스 클릭 이벤트 발생시 작동하는 함수.(좌클릭 우클릭 구분 없음)
    def mousePressEvent(self,event):
        self.press_event = event # 이벤트 객체를 저장
        self.position = [event.x(), event.y()] # 마우스 클릭 위치를 (x, y) 좌표로 저장
        
        # 좌클릭인지 확인
        if event.buttons() & Qt.LeftButton:
            
            if self.mouse_state == "none": # 마우스 상태가 'none'인 경우
                QApplication.restoreOverrideCursor() # 커서를 기본 상태로 복구
                self.rotate = False # 회전 상태를 False로 설정
            
            elif self.mouse_state == 'wire': # 마우스 상태가 'wire'인 경우
                self.wire_start = [event.x(),event.y()] # 와이어 시작 지점의 좌표를 저장
                self.rotate = False # 회전 상태를 False로 설정
                
                pass # 추가 작업이 필요할 수 있으므로 pass로 처리
            
            else: # 그 외의 마우스 상태인 경우
                self.create_label(self.position) # 새로운 라벨(컴포넌트)을 생성
                
                QApplication.restoreOverrideCursor() # 커서를 기본 상태로 복구
                self.mouse_state = "none" # 마우스 상태를 'none'으로 리셋
                self.rotate = False # 회전 상태를 False로 설정
                pass
            
        # 우클릭인지 확인     
        elif event.buttons() & Qt.RightButton:
            
            if self.mouse_state == "none": # 마우스 상태가 'none'인 경우
                QApplication.restoreOverrideCursor() # 커서를 기본 상태로 복구

            # 마우스 상태가 'none'이 아닌 경우
            else:
                if self.rotate: # 이미 회전 상태인 경우
                    self.rotate = False # 회전 상태를 False로 설정
                    
                    QApplication.restoreOverrideCursor() # 커서를 기본 상태로 복구
                    self.set_mouse() # 마우스 상태를 업데이트
                
                # 회전 상태가 아닌 경우    
                else:
                    self.rotate = True # 회전 상태를 True로 설정
                    QApplication.restoreOverrideCursor() # 커서를 기본 상태로 복구
                    self.set_mouse() # 마우스 상태를 업데이트

        super().mousePressEvent(event) # 부모 클래스의 기본 마우스 이벤트를 호출
        pass # 함수 종료
    
    # 마우스가 움직일 때 호출되는 이벤트 핸들러
    def mouseMoveEvent(self, event):
        self.moving_event = event # 현재 발생한 마우스 이동 이벤트를 저장
        
        # 마우스 상태가 'wire'인 경우(즉, 와이어(선)을 그리는 중인 경우)
        if self.mouse_state == 'wire':
            delta_x = abs(self.wire_start[0] - event.x()) # 시작 지점과 현재 지점 간의 x축 거리 계산
            delta_y = abs(self.wire_start[1] - event.y()) # 시작 지점과 현재 지점 간의 y축 거리 계산
            
            # x축 또는 y축의 이동 거리가 10 픽셀 이상인 경우에만 선을 그리기 시작
            if delta_x>10 or delta_y>10:
                
                # x축 이동이 더 큰 경우 (수평 방향으로 선을 그림)
                if delta_x>delta_y:
                    
                    if self.wire_start[0]>event.x(): # 왼쪽으로 이동 중인 경우
                        
                        # 시작 지점부터 현재 위치까지 왼쪽으로 선을 그리며 저장
                        for x in range(self.wire_start[0],event.x()-1,-1):
                            tmp = [self.wire_start, [x, self.wire_start[1]]] # 수평 선의 시작점과 끝점
                            self.tmp_draw_wire.append(tmp) # 임시 선 목록에 추가
                            self.wire_start = [x,self.wire_start[1]] # 새로운 시작 지점 설정
                    
                    # 오른쪽으로 이동 중인 경우
                    else:
                        
                        # 시작 지점부터 현재 위치까지 오른쪽으로 선을 그리며 저장
                        for x in range(self.wire_start[0],event.x()+1,1):
                            tmp = [self.wire_start, [x, self.wire_start[1]]] # 수평 선의 시작점과 끝점
                            self.tmp_draw_wire.append(tmp)  # 임시 선 목록에 추가
                            self.wire_start = [x,self.wire_start[1]] # 새로운 시작 지점 설정
                
                # y축 이동이 더 큰 경우 (수직 방향으로 선을 그림)
                else:
                    
                    if self.wire_start[1]>event.y(): # 위쪽으로 이동 중인 경우
                        
                        # 시작 지점부터 현재 위치까지 위쪽으로 선을 그리며 저장
                        for y in range(self.wire_start[1],event.y()-1,-1):
                            tmp = [self.wire_start, [self.wire_start[0],y]] # 수직 선의 시작점과 끝점
                            self.tmp_draw_wire.append(tmp) # 임시 선 목록에 추가
                            self.wire_start = [self.wire_start[0],y] # 새로운 시작 지점 설정
                    
                    # 아래쪽으로 이동 중인 경우
                    else:
                        
                        # 시작 지점부터 현재 위치까지 아래쪽으로 선을 그리며 저장
                        for y in range(self.wire_start[1],event.y()+1,1):
                            tmp = [self.wire_start, [self.wire_start[0],y]] # 수직 선의 시작점과 끝점
                            self.tmp_draw_wire.append(tmp)  # 임시 선 목록에 추가
                            self.wire_start = [self.wire_start[0],y] # 새로운 시작 지점 설정
                            
            pass # 추가적인 동작을 위한 공간 (필요 시 구현 가능)
        
        self.update() # UI를 갱신하여 선이 그려진 상태를 화면에 반영
        super().mouseMoveEvent(event) # 부모 클래스의 기본 마우스 이동 이벤트를 호출하여 기본 동작 유지
        
        pass
    
    # 마우스 버튼이 릴리즈(떨어졌을) 때 호출되는 이벤트 핸들러
    def mouseReleaseEvent(self,event):
        
        self.release_event = event # 현재 발생한 마우스 릴리즈 이벤트를 저장
        self.wire_start = None # 와이어(선) 그리기를 종료하기 위해 시작점을 초기화
        
        # 마우스 상태가 'wire'인 경우 (와이어 그리기를 마친 경우)
        if self.mouse_state =='wire':
            
            #print('연결선 좌표 : ',self.tmp_draw_wire,'-'*20)
            
            # 노드 카운트를 증가시키고 새로운 노드 이름을 생성
            self.node_cnt = self.node_cnt+1
            node_name = 'node'+str(self.node_cnt) # 노드 이름 생성
            self.node_dict[node_name] = self.tmp_draw_wire # 현재 그린 임시 선을 노드 사전에 저장
            self.draw_wire.append(self.tmp_draw_wire) # 그린 선을 전체 선 리스트에 추가
            self.auto_save() # 현재 상태를 자동 저장
            self.tmp_draw_wire = [] # 임시 선 리스트 초기화
            self.update() # UI를 갱신하여 그려진 선이 화면에 반영되도록 함
            
            # 선 연결의 시작 지점과 끝 지점을 저장
            connection = [self.position , [event.x(),event.y()]]#맨처음 클릭한 지점에서 끝지점의 위치정보.
            
            # 기기 간의 연결 정보를 처리 (연결된 기기 정보 반환)
            data =self.device_connect_wire(connection)
            
            # 연결 정보가 존재하는 경우(연결이 성공적으로 이루어진 경우)
            if data is None:
                pass # 아무 동작도 하지 않음
            else:
                self.wire_connection.append(data) # 연결 정보를 wire_connection 리스트에 추가
            
            print(self.wire_connection) # 현재까지의 연결 정보를 출력
            self.mouse_state = "none" # 마우스 상태를 기본 상태로 초기화
        
        # 부모 클래스의 기본 마우스 릴리즈 이벤트를 호출하여 기본 동작 유지
        super().mouseReleaseEvent(event)

import os
import sys
from PyQt5.QtWidgets import QApplication

os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = r'C:\Users\김도연\AppData\Local\Programs\Python\Python312\Lib\site-packages\PyQt5\Qt5\plugins'

if __name__ == "__main__" :
    app = QApplication(sys.argv)         #QApplication : 프로그램을 실행시켜주는 클래스
    myWindow = mainWindow()             #WindowClass의 인스턴스 생성
    myWindow.show()                      #프로그램 화면을 보여주는 코드
    sys.exit(app.exec_())