# 전문 엔지니어 배정

전문 역할은 구현 분야를, 기존 harness 역할은 탐색·설계·독립 리뷰·QA 절차를 구분한다.
이 목록은 역할 수만큼 에이전트를 항상 실행하라는 뜻이 아니다. 각 작업에 필요한 역할만 선택한다.
모델·추론 수준·권한은 부모 설정을 상속한다. 전문 이름이나 역할 TOML이 별도 장비 권한을 부여하지 않는다.

## 역할과 기본 영역

- `roport_system_architect`: UR/SR·시나리오·아키텍처·Tech Spec의 추적 관계와 상충하는 계약을 검토한다. 기본 읽기 전용이며 부모가 적용 범위·공통 계약·미결 결정을 확정할 수 있게 근거를 반환한다. 오케스트레이션이나 제품 코드 구현을 대신하지 않는다.
- `roport_pinky_navigation_engineer`: Pinky 주행·도킹·ROS 2·TF·센서·안전 정지. 기본 영역은 `services/roport-pinky/`. 관제의 작업 배정과 출발 허가는 관제 역할과 계약을 맞춘다.
- `roport_omx_control_engineer`: OMX 양팔 제어·관절/action·시리얼·캘리브레이션·LeRobot 정책 실행 경계. 기본 영역은 `services/roport-omx/`. AI 후보를 실행하는 현장 검사와 양팔 정지를 담당하며 관제의 출발 허가를 대신하지 않는다.
- `roport_robot_perception_engineer`: 고객 동행/사람 추적·QR/마커/라벨/라인 인식·관측 좌표/신뢰도. 기본 후보는 Pinky·AI의 배정된 인지 파일이다. 인식 성공을 서비스 인증·파지·주행 안전으로 바꾸지 않는다.
- `roport_imitation_learning_engineer`: 시연·episode·LeRobot 데이터셋·ACT 학습/평가·모델/feature/보정 버전 인계. 기본 후보는 OMX의 팀 학습 코드와 배정된 AI 변환 경계다. 데이터·GPU 학습·실물 rollout은 별도 허용 작업이다.
- `roport_control_integration_engineer`: WSS/MQTT·명령 수신·상태 저장/전달·중복·재시작·복구. 기본 영역은 `services/roport-control-server/`. 계획 정책과 네트워크 어댑터를 구분하며 로봇 내부 구동과 서비스 업무 DB 소유권을 넘겨받지 않는다.
- `roport_fleet_planning_engineer`: 작업/로봇/슬롯 배정·공유 작업대·맵/경로망·1차선 점유/대피·교착·스케줄 정책. 기본 영역은 관제의 배정된 계획 코드다. 명령 전송/상태 저장은 관제 연동, 로컬 추종/정지는 Pinky/OMX가 맡는다.
- `roport_ai_inference_engineer`: 영상·관측·전처리·모델 입출력·추론 deadline, P0 UDP/P1 MQTT 어댑터. 기본 영역은 `services/roport-ai-server/`. 모터/시리얼 제어나 실제 작업 완료를 담당하지 않는다.
- `roport_service_backend_engineer`: Java/Spring 기반 주문·예약·고객 검증·실제 수령과 관제 업무 계약. 기본 영역은 `services/roport-service-server/`. 현장 자원 배정·로봇 안전 판정을 대신하지 않는다.
- `roport_web_engineer`: 고객/직원/관리자 React·TypeScript UI, API 연결·권한별 상태 표시·접근성. 기본 영역은 `services/roport-web/`. UI의 버튼 숨김을 서버 권한 검사로 취급하거나 화면 진입 시 장비 명령을 발행하지 않는다.
- `roport_hmi_engineer`: 기체 LCD/LED/부저와 Qt 패드 GUI의 서비스 입력·탑승 알림·수령 확인·stale 표시. 실제 Qt 구현 위치/의존성은 부모가 먼저 확인한다. React 웹과 역할을 나누며 화면 이벤트는 장비 구동 권한이 아니다.
- `roport_hardware_integration_engineer`: 기체/포트/전원/CPU/드라이버·카메라·TF·설치/보정의 측정 근거와 현장 준비. Pinky/OMX의 배정된 설정/probe/검증 파일을 맡는다. 장비 connect·포트 open도 기본 검사가 아니다.
- `roport_robot_validation_engineer`: 시나리오·경계면 실패 주입·replay·시뮬레이션·실물 인수 기준의 전문 QA. 배정된 테스트/산출물만 쓰며 제품 구현은 고치지 않는다. 일반 테스트 실행은 `harness_qa`가 맡을 수 있다.
- `roport_platform_engineer`: CI·의존성/패키징·환경/배포 준비·로그/관측·LAN/WAN/TLS 비교 검증. 배정된 workflow/운영/설정 파일만 수정하며 배포·Cloud·sudo·운영 네트워크 변경은 자동 실행하지 않는다.
- `roport_security_reviewer`: QR/주문/역할별 인증·개인정보·TLS/ACL·명령 만료/재전송·안전 경계의 독립 읽기 전용 리뷰. 실제 결함의 근거를 반환하고 구현/외부 스캔/장비 연결을 하지 않는다.

기본 영역은 자동 쓰기 허용 범위가 아니다. 부모가 작업별로 명시한 소유 파일만 수정한다.
공용 schema·lockfile·설정은 부모가 소유자를 확정한다. 원본 오픈소스 수정은 별도 범위를 확인한다.

## 프로젝트 요구사항 범위와 근거

2026-10-27 조회한 [UR v29](https://fp-team1.atlassian.net/wiki/spaces/MFS/pages/2260995),
[SR v32](https://fp-team1.atlassian.net/wiki/spaces/MFS/pages/2293766)와 현재 제품 AGENTS/manifest/CI를 대조했다.
이 목록은 인력 배정과 검토 범위이며 해당 기능의 구현·안전 승인 완료를 뜻하지 않는다.

- UR-01/02/04/05/06·SR-07/09/10/13/14/18/19: 예약·슬롯·상하차·통행·인도 → 서비스/웹, fleet planning, 관제 연동, Pinky, OMX, 학습, 하드웨어, 검증.
- UR-03/07·SR-11/17/20/21/22: 탑승 알림·라인 주행·동행/고객 상실·Qt 패드 → Pinky, 인지, HMI, AI, 서비스/웹, 관제/fleet, 검증.
- UR-08/09/10·SR-23/24/25: 이력·통합 모니터링·정지/복구 → 관제, 서비스/웹, 플랫폼, 로봇 검증과 보안 리뷰.
- 모델/데이터 수집·ACT 평가 → [OMX 반출 명세 v6](https://fp-team1.atlassian.net/wiki/spaces/MFS/pages/10027126),
  [양팔 명세 v3](https://fp-team1.atlassian.net/wiki/spaces/MFS/pages/10518529),
  [창고 상차 명세 v2](https://fp-team1.atlassian.net/wiki/spaces/MFS/pages/10584065)를 적용 시나리오별로 확인한다.
- 전송·업무 경계 → [MQTT/AI 명세 v6](https://fp-team1.atlassian.net/wiki/spaces/MFS/pages/10125435),
  [서비스↔관제 명세 v6](https://fp-team1.atlassian.net/wiki/spaces/MFS/pages/10125388)를 대조한다.

SR에는 과거 OMX 대수/배치·DDS/TCP·터치 LCD와 다른 설계 문구가 함께 남아 있다.
새 OMX 명세의 AI 정책 실행/상태 보고 계층과 기존 Host 현장 실행 검사 책임도 단일 승인 계약으로 정리됐다고 가정하지 않는다.
시스템 아키텍트가 관련 소유자와 적용 범위를 확인하고 부모가 결정하기 전에는 장비/안전 소유권을 바꾸지 않는다.
이미지만 있는 System/SW Architecture는 Markdown 본문만 읽어 도식까지 검토했다고 보고하지 않는다.

## 배정 예

### Pinky 도킹 중 통신 단절

먼저 `harness_explorer`가 실제 호출 흐름과 안전 정지 경로를 확인한다.
부모가 정지·timeout·명령 소유권과 상태 계약을 확정한 뒤 Pinky 엔지니어와 관제 엔지니어에게 서로 겹치지 않는 파일을 배정한다.
센서/명령 replay와 연결 단절 mock으로 확인하고 `harness_reviewer`·`harness_qa`가 독립 검증한다.
bringup이나 cmd_vel 발행으로 연결을 확인하지 않는다.

### 양팔 반출 중 추론 timeout

OMX 엔지니어가 action 폐기·양팔 보류·현장 정지 경로, AI 엔지니어가 timeout·seq·결과 유효성,
관제 엔지니어가 실패/복구·출발 보류 상태를 맡는다. execution ID·deadline·오류 계약은 부모가 먼저 조율한다.
팔 토크·캘리브레이션·실행 속도 한계가 미정이면 값을 발명하지 않고 필요한 확인 항목으로 반환한다.

### 예약에서 픽업 상태까지

서비스 백엔드 엔지니어와 웹 엔지니어가 API·권한·상태 계약을 맞춘다.
현장 작업 생성이 포함되면 관제 엔지니어를 추가한다. 전송 성공·작업 접수·물품 도착·고객 수령을 각각 검증한다.

### 고객 추종·QR·패드와 탑승 알림

인지 엔지니어가 사람/QR 관측, HMI가 고객 입력/표시·알림, 서비스가 고객/주문/항공편 검증을 맡는다.
Pinky가 로컬 이동/정지, 관제/fleet이 미재발견·복귀/점유 조정을 맡는다. 얼굴을 다시 찾았다는 이유만으로 인증/재개하지 않는다.

### 데이터 수집에서 모델 인계까지

학습 엔지니어가 조건별 시연·episode 품질·분할·ACT 평가를, 하드웨어가 포트/카메라/보정 근거를 맡는다.
OMX와 AI가 feature·전처리·모델/보정 버전·chunk/deadline 계약을 소비한다. 실물 수집·훈련·rollout은 각각 허용 범위를 확인한다.

### 공용 통로와 운영 장애

fleet planning이 점유/통행/대기 정책, 관제 연동이 전송/상태 재조정, 플랫폼이 로그/시계/환경을 맡는다.
로봇 검증이 단절/재시작·교착을 주입하고 보안 리뷰어가 재전송/권한/비밀값 경계를 독립 검토한다.

## 탐색·리뷰와 실제 호출

작은 변경은 한 명 또는 부모가 처리하고 모든 역할을 거치는 절차를 강제하지 않는다.
구현은 해당 전문 엔지니어를 우선 선택하며 `harness_worker`와 같은 파일을 중복 배정하지 않는다.
분야를 가르는 탐색·설계에는 `harness_explorer`·`harness_architect`, 독립 검증에는 `harness_reviewer`·`harness_qa`를 재사용한다.
도메인 계약 충돌은 `roport_system_architect`, 로봇 통합 실패 검증은 `roport_robot_validation_engineer`, 보안/개인정보/명령 신뢰 경계는 `roport_security_reviewer`를 필요할 때 추가한다.
같은 역할의 독립 작업도 파일·장비 포트·빌드 캐시 소유권이 겹치면 순차화한다. 동시 실행 한도는 계속 자식 3개 또는 실제 런타임 한도 중 작은 값이다.

역할 TOML을 선택할 수 있는 현재 도구라면 `name`과 일치하는 역할로 호출한다.
새 정의가 현재 도구에 없으면 해당 TOML을 읽어 기본 worker/explorer에 지시를 전달한 대체 실행으로 기록한다.
이 경우 새 custom role의 직접 발견을 검증한 것으로 보고하지 않는다. 역할 추가 후 새 제품 프로젝트 채팅에서 다시 확인한다.
