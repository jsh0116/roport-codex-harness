# RO:PORT Codex Harness

RO:PORT 로봇 시스템을 개발할 때 쓰는 개인 Codex 하네스입니다.
분야별 서브에이전트, 작업 절차, 설치기와 검사 도구를 관리합니다.
제품 코드는 [RO:PORT 저장소](https://github.com/kernel-robot-8th/kernel-robot-repo-1)에서 개발하고, 이 저장소에는 Codex용 개발 도구를 둡니다.

## 작업 방식

**제품 프로젝트에서 연 메인 Codex 채팅이 오케스트레이터를 맡습니다.**
`$roport-orchestrator`를 호출하면 메인 채팅이 해당 스킬을 읽고 다음 순서로 작업합니다.

1. 최신 요구사항과 기존 코드를 확인하고, 필요한 전문 에이전트를 선택합니다.
2. 각 에이전트가 수정할 파일과 주고받을 API·메시지 형식을 정합니다.
3. 서로 독립적인 작업은 나눠 진행하고, 앞선 결과가 필요한 작업은 순서대로 진행합니다.
4. 변경 내용을 합친 뒤 리뷰와 검사를 거쳐 결과·실패·미검증 항목을 보고합니다.

에이전트 정의는 **전문 역할 15개와 공통 작업 역할 5개, 총 20개**입니다.
요청마다 필요한 역할만 호출합니다. 새로 설치할 때 동시 실행 한도는 자식 3개로 설정하며, 기존 프로젝트 설정이 있으면 그 설정을 보존합니다. 실제 실행 환경에서 허용하는 한도도 따릅니다.
작은 수정에 모든 역할을 거치는 절차를 강제하지 않습니다.

## 폴더 구조

```text
roport-codex-harness/
├── .codex/
│   ├── config.toml                   # 프로젝트 에이전트 기본 설정
│   └── agents/
│       ├── harness-*.toml            # 공통 작업 역할 5개
│       └── roport_*.toml             # 전문 역할 15개
├── .agents/skills/
│   ├── harness/
│   │   ├── SKILL.md                  # 하네스 구축·점검 절차
│   │   ├── scripts/                  # 실행 기록·통신·재개·구조 검사
│   │   └── agents/openai.yaml        # harness 스킬의 표시·호출 설정
│   └── roport-orchestrator/
│       ├── SKILL.md                  # RO:PORT 작업 조율 절차
│       └── references/engineering-roles.md
├── scripts/
│   ├── install.py                    # 제품 프로젝트에 개인 하네스 설치
│   └── harness.py                    # 제품 검사·모듈별 CI 실행
├── tests/                            # 설치기·실행기 테스트
└── .github/workflows/harness-ci.yml   # 이 하네스 자체의 CI
```

**실제 서브에이전트 정의는 `.codex/agents/*.toml`에 있습니다.**
스킬은 에이전트가 따를 절차와 도구를 묶은 것입니다. `harness/agents/openai.yaml`은 `harness` 스킬의 이름·기본 요청문·호출 정책을 정하며, Pinky나 OMX 전문 에이전트를 정의하는 파일은 아닙니다.

## 설치

Python 3.11 이상과 Git이 필요합니다. 이 저장소는 비공개이므로 clone할 수 있는 GitHub 계정 권한도 필요합니다.
아래 명령은 **하네스 저장소에서** 실행합니다. `/absolute/path/to/kernel-robot-repo-1`은 실제 제품 프로젝트 경로로 바꿉니다.
`rtk`가 설치돼 있으면 셸 명령 앞에 `rtk` 또는 `rtk proxy`를 붙입니다.

```bash
git clone https://github.com/jsh0116/roport-codex-harness.git
cd roport-codex-harness
python3 scripts/install.py --target /absolute/path/to/kernel-robot-repo-1 --dry-run
python3 scripts/install.py --target /absolute/path/to/kernel-robot-repo-1
```

설치기는 제품 프로젝트에 두 스킬, 20개 역할과 필요한 Codex 기본 설정을 복사합니다.
같은 파일이 이미 있으면 그대로 두고, 내용이 다르면 덮어쓰지 않고 충돌을 알립니다. 기존 모델·권한 설정도 보존합니다.
팀의 `AGENTS.md`, README, `package.json`, `.gitignore`, 서비스 코드와 CI는 수정하지 않습니다.

하네스 원본은 이 개인 저장소에서 버전 관리합니다. 제품에 설치한 개인 파일과 실행 기록은 제품의 `.git/info/exclude`에 등록해 로컬에서만 Git 추적 대상에서 제외합니다.

## 사용

설치 후 **RO:PORT 제품 프로젝트에서 새 Codex 채팅을 열고** 요청합니다.
하네스 자체를 수정할 때는 이 하네스 저장소를 열고 `$harness`를 사용합니다.
하네스 저장소에서 시작한 자식 에이전트가 제품 디렉터리로 자동 이동하지는 않습니다.

### 여러 분야에 걸친 기능 구현

```text
$roport-orchestrator Pinky 도킹 중 연결이 끊겼을 때 정지 처리와 관제 상태 전달을 구현해줘.
Pinky 주행 엔지니어와 관제 연동 엔지니어로 나누고 mock으로 검증해줘.
```

### 명세와 구현 검토

```text
$roport-orchestrator 양팔 반출의 추론 timeout 처리를 검토해줘.
OMX 제어·AI 추론·시스템 아키텍처 관점에서 확인하되, 이번에는 코드를 수정하지 마.
```

역할을 직접 고르지 않아도 요청에 맞춰 메인 채팅이 선택합니다.
역할별 담당 범위와 분야 간 인계 예시는 [전문 역할 배정 안내](.agents/skills/roport-orchestrator/references/engineering-roles.md)에 있습니다.

## 에이전트 역할

### 전문 역할 15개

- `roport_system_architect`: 요구사항·시나리오·시스템 구조와 모듈 간 계약
- `roport_pinky_navigation_engineer`: Pinky 주행·도킹·ROS 2·안전 정지
- `roport_omx_control_engineer`: OMX 양팔 제어·관절/action·LeRobot 정책 실행
- `roport_robot_perception_engineer`: 고객 추적·QR/마커·영상 좌표·관측 유효성
- `roport_imitation_learning_engineer`: 시연·데이터셋·ACT 학습/평가·모델 인계
- `roport_control_integration_engineer`: 상태 전달·WSS/MQTT·중복 명령·실패/복구
- `roport_fleet_planning_engineer`: 작업/슬롯 배정·공유 자원·공용 통로·대피·스케줄
- `roport_ai_inference_engineer`: 모델 입출력·전처리·추론 유효성·UDP/MQTT
- `roport_service_backend_engineer`: Java/Spring 주문·예약·고객 검증·수령 처리
- `roport_web_engineer`: 고객/직원/관리자 웹·API 상태·권한별 표시·접근성
- `roport_hmi_engineer`: Qt 패드·LCD/LED/부저·고객 입력·탑승 알림
- `roport_hardware_integration_engineer`: 장비·포트·전원·설치 좌표·캘리브레이션 근거
- `roport_robot_validation_engineer`: 데이터 재생·시뮬레이션·로봇 통합 실패 검증
- `roport_platform_engineer`: CI·환경/배포 준비·운영 로그·네트워크 검증
- `roport_security_reviewer`: 인증·개인정보·명령 신뢰/안전 경계의 독립 리뷰

### 공통 작업 역할 5개

- `harness_explorer`: 관련 코드와 실제 호출 흐름을 읽고 근거를 찾습니다.
- `harness_architect`: 작업 범위·파일 소유권·의존성과 완료 기준을 정리합니다.
- `harness_worker`: 전문 분야를 따로 나눌 필요가 없는 구현을 맡습니다.
- `harness_reviewer`: 변경 내용을 독립적으로 검토하고 결함을 보고합니다.
- `harness_qa`: 허용된 검사를 실행하고 실패를 재현합니다.

메인 채팅이 최종 계약과 통합을 결정합니다. 구현 담당자와 독립 리뷰·QA 담당자의 책임을 구분하고, 같은 파일을 여러 작성자에게 동시에 맡기지 않습니다.

## 제품 검사

아래 명령도 **하네스 저장소에서** 실행합니다. `--project`에는 RO:PORT 제품 프로젝트 루트를 지정합니다.
Node.js 24 등 검사 환경과 루트 Husky 설치는 제품 README·manifest·CI를 따릅니다.

```bash
python3 scripts/harness.py --project /absolute/path/to/kernel-robot-repo-1 check
python3 scripts/harness.py --project /absolute/path/to/kernel-robot-repo-1 ci --module omx --dry-run
python3 scripts/harness.py --project /absolute/path/to/kernel-robot-repo-1 ci --module omx
```

- `check`: 설치된 하네스 구조, 제품의 커밋 규칙과 Pinky/OMX 소스·mock 검사를 실행합니다.
- `ci --module ...`: 지정한 모듈의 기존 CI 명령을 실행합니다. `--dry-run`으로 실행할 명령과 디렉터리를 먼저 확인할 수 있습니다.

모듈은 `pinky`, `omx`, `control-server`, `ai-server`, `service-server`, `web` 중 하나를 지정합니다.
모듈 CI는 lockfile에 맞춰 의존성을 설치하고 빌드할 수 있습니다. 서비스의 Spring 테스트는 localhost 테스트 서버를 엽니다.
실제 명령은 제품의 `.github/workflows/`를 기준으로 확인합니다.

기본 검사에는 로봇 구동·GPU 학습·Cloud 연결을 넣지 않습니다.
장비 연결 확인만을 위해 bringup·connect를 실행하지 않으며, 실장비 작업은 사용자 지시와 현장 안전 조건을 확인한 뒤 진행합니다.

## 하네스 검사와 갱신

하네스 자체의 설치기·실행기 테스트와 구조 검사는 이 저장소에서 실행합니다.

```bash
python3 -m unittest discover -s tests -v
python3 .agents/skills/harness/scripts/validate.py --project .
```

사용 중인 하네스 버전은 `git rev-parse HEAD`로 기록합니다. 갱신할 때는 원하는 커밋을 검토하고 설치기의 `--dry-run`부터 실행합니다.
기존 설치 파일과 내용이 다르면 충돌로 중단합니다. 충돌 파일은 백업하고 차이를 확인한 뒤 필요한 파일만 명시적으로 교체합니다.
설치할 스킬·역할 파일을 제품 Git에서 이미 추적 중이거나, 추적 중인 Codex 설정을 바꿔야 하는 경우도 설치기가 중단합니다.

## 검증 범위와 프로젝트 기준

설치·구조 검사와 원격 CI 통과는 역할 파일과 도구를 확인한 결과입니다.
Pinky·OMX 시나리오는 역할 정의를 기본 에이전트에 전달하는 방식으로 평가했습니다. 새 custom role을 이름으로 직접 선택하는 검증은 별도로 남아 있습니다.
역할이 보이지 않으면 설치 대상과 제품 프로젝트 경로를 확인하고 새 채팅에서 다시 확인합니다. 현재 도구가 해당 역할을 직접 제공하지 않으면 정의를 읽어 기본 역할에 전달하는 대체 실행임을 보고합니다.

프로젝트 사실과 안전 기준은 제품 저장소와 최신 Confluence 명세를 먼저 확인합니다. 역할이 정의돼 있다는 이유만으로 해당 업무 기능이나 장비 동작을 구현·검증했다고 판단하지 않습니다.
읽기 전용 역할의 지시와 실제 권한 격리도 구분합니다. 에이전트는 부모의 권한을 상속합니다.
실행 기록·장비 데이터·비밀값·이동 전 백업은 원격에 올리지 않습니다. 출처·변경 범위·라이선스는 [UPSTREAM](UPSTREAM.md)에 정리했습니다.
