---

# ⚙️ PyQt5 기반 회로 시뮬레이션 프로그램 (Circuit Simulator)

## 📌 프로젝트 소개

본 프로젝트는 **PyQt5와 Matplotlib을 활용**하여 **직관적이고 인터랙티브한 회로 시뮬레이션 프로그램**입니다.  
**마우스 기반의 회로 설계, 소자 설정, 와이어 연결, 자동 노드 판별, 시뮬레이션 분석까지** 모든 과정을 직접 개발한 **GUI 회로 시뮬레이터**입니다.  
**전자공학 입문자와 비전공자, 영어에 익숙하지 않은 학생들**도 쉽게 사용할 수 있도록 고안되었습니다.  
해당 프로젝트는 **김도연** 이름으로 **졸업 프로젝트 및 논문**으로 작성되었습니다.

---

## 💡 개발 동기

학부 과정에서 사용한 **TINA-TI, PSPICE, OCTAVE 등 복잡한 툴의 불편함**을 직접 개선하고자 시작되었습니다.  
**과도하게 복잡한 UI, 상이한 소자 규격, 복잡한 사용법**을 해결하기 위해,  
**마우스 인터페이스만으로 회로 설계부터 시뮬레이션까지 가능한 플랫폼**을 목표로 개발되었습니다.  

---

## 👨‍💻 팀 구성 및 역할

| 이름 | 역할 | 상세 기능 (이력서 기반) |
|:---|:---|:---|
| **김도연 (팀장)** | **UI 및 시뮬레이션 인터랙션 개발** | **PyQt 기반 UI (회로 소자, 전원, 접지 배치)**, **마우스 기반 배치**, **시간/주파수 도메인 그래프 (Matplotlib)**, **Undo/Redo, Auto Save** |
| **김승찬** | **회로 연결 및 소자 값 편집** | **와이어 연결 시스템 (마우스 클릭/드래그 기반)**, **더블 클릭 소자 값 실시간 수정** |
| **정하건** | **전압 측정 및 편집 기능** | **마커로 특정 지점 전압 측정**, **시뮬레이션 데이터 시각화**, **편집 및 단계 관리 (이전/다음)** |

---

## 🔑 주요 기능 (코드 기반)

### 🧩 **회로 소자 배치 및 설정 (QLabel 기반)**
- **저항, 커패시터, 인덕터, OP-AMP, DC/AC 전원, 접지** 배치 가능
- **마우스 클릭으로 간편 배치 및 회전 (우클릭)**
- **더블 클릭 시 소자 설정 팝업 (값 수정)**

### 🖱️ **와이어 연결 (자동 노드 인식)**
- **마우스 드래그로 선 연결 (QLabel 단자 자동 감지)**
- **내부적으로 노드 자동 저장 (`self.node_dict`, `self.wire_connection`)**

### 🔄 **소자 이동/편집 시스템**
- **마우스 드래그 이동 (QLabel 커스텀 이벤트)**
- **Undo/Redo 편집 이력 저장 (작업 복원)**

### 📈 **시간/주파수 도메인 분석 (Matplotlib)**
- **마커로 선택한 지점 전압 시뮬레이션**
- **시간/주파수 영역 자동 그래프 출력**

### 💾 **자동 저장 및 복원 (Auto Save)**
- **소자 배치/연결/설정 즉시 저장**

---

## 🛠️ 기술 스택 (코드 기반)

| 기술 | 설명 |
|:----|:----|
| **Python 3.12** | 전체 프로그램 로직, 데이터 저장 |
| **PyQt5** | 마우스 기반 회로 UI, 소자 이동/연결/편집 |
| **Matplotlib** | 시간/주파수 도메인 시뮬레이션 그래프 |
| **NumPy** | 데이터 계산 및 파형 생성 |

---

## 🚀 사용 방법 (코드 흐름 기반)

1. **프로그램 실행** (Python으로 실행)
2. **소자 선택 후 배치** (자동 마우스 아이콘 표시)
3. **우클릭 → 소자 회전 / 더블클릭 → 값 수정**
4. **와이어 모드 → 소자 단자 연결 (자동 노드 인식)**
5. **마커로 측정 지점 설정**
6. **실행 → 시간/프로젝트명 입력**
7. **자동 생성된 시뮬레이션 그래프 확인 (Matplotlib)**

---
## 📷 시뮬레이터 시연 이미지

| 실행 설정창 | 마커 배치 |
| :--: | :--: |
| <img src="./images/실행 설정창.png" width="400"/> | <img src="./images/마커 배치.png" width="400"/> |

| 마커 소자에 미연결된 그래프 | 마커 소자에 연결된 그래프 |
| :--: | :--: |
| <img src="./images/마커 소자에 미연결 그래프.png" width="400"/> | <img src="./images/마커 소자에 연결 그래프.png" width="400"/> |

---
