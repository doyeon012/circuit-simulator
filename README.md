# PyQt5 기반 간편 회로 시뮬레이션 프로그램

## 프로젝트 소개

이 프로젝트는 PyQt5를 활용하여 개발된 직관적이고 사용하기 쉬운 회로 시뮬레이션 프로그램입니다. 전자공학 입문자와 영어에 취약한 학생들을 위해 설계되었으며, 기존의 복잡한 시뮬레이션 도구들의 장점을 살리고 단점을 보완하여 만들어졌습니다. 이 프로젝트는 개인 졸업 프로젝트로 진행되었으며, 저의 이름(김도연)으로 관련 논문도 작성되었습니다.

## 개발 동기

정보통신공학과 학업 과정에서 TINA-TI, OCTIVE, PSPICE 등 다양한 회로 시뮬레이션 도구를 사용하면서 느낀 불편함을 해소하고자 시작되었습니다. 매 학기마다 다른 도구를 사용해야 하는 어려움과 복잡한 인터페이스, 그리고 다양한 부품 규격으로 인한 혼란을 줄이고자 했습니다. 1학년 때부터 느꼈던 불편함을 후배들은 겪지 않았으면 하는 마음에서 이 프로젝트를 시작하게 되었습니다.

## 팀 구성 및 역할

본 프로젝트는 3인 팀으로 진행된 졸업 프로젝트입니다.

1. 김도연(본인, 팀장)
   - UI(회로 소자, 전원 및 접지 배치) 설계 및 구현
   - 시간/주파수 도메인 그래프 생성 기능 구현
     
3. 김승찬(팀원1)
   - 회로 연결 구현
   - 각 소자 더블 클릭으로 값 수정 가능

4. 정하건(팀원2)
   - 마커를 통한 특정 지점 전압 측정 구현
   - 편집 기능 구현
     
## 주요 기능

1. **회로 소자 배치 및 설정**
   - 저항, 커패시터, 인덕터, OP-AMP 지원
   - 각 소자 더블 클릭으로 값 수정 가능

2. **전원 및 접지**
   - DC 및 AC 전원 소스 추가
   - 접지 연결 기능

3. **회로 연결**
   - 마우스로 와이어 연결 기능
   - 자동 노드 인식 및 연결 정보 저장

4. **측정 및 분석**
   - 마커를 통한 특정 지점 전압 측정
   - 시간 영역 및 주파수 영역 그래프 생성

5. **편집 기능**
   - 이전/다음 기능으로 작업 단계 관리
   - 전체 회로 지우기 기능

## 기술 스택

- Python
- PyQt5
- NumPy
- Matplotlib

## 사용 방법

1. 프로그램 실행
2. 원하는 소자를 드래그 앤 드롭으로 배치
3. 와이어 도구를 사용하여 소자 연결
4. 필요한 경우 소자를 더블 클릭하여 값 조정
5. 마커를 사용하여 측정 지점 설정
6. 실행 버튼 클릭 후 시간과 프로젝트 이름 입력
7. 생성된 그래프 확인

## 향후 개선 사항

1. 연결선 그리기 개선
2. 비선형 소자 계산 기능 추가
3. UI 디자인 개선
4. 다국어 지원 추가
5. 회로 저장 및 불러오기 기능 구현
