# RO:PORT Codex Harness

RO:PORT 로봇 시스템 개발을 지원하는 개인 Codex 하네스입니다.
Codex 에이전트·스킬·오케스트레이션·검증 실행기와 설치기를 제품 저장소에서 분리해 관리합니다.
Claude Code 하네스는 이 저장소의 범위에 포함하지 않습니다.

## 구성

- `.codex/agents/`: 탐색·설계·구현·리뷰·QA 기본 역할 5개
- `.agents/skills/harness/`: 실행 장부·협업 기록·입력 변경 감지·부분 재실행 도구
- `.agents/skills/roport-orchestrator/`: RO:PORT 모듈·계약·안전·검증 절차
- `scripts/install.py`: 제품의 추적 파일을 바꾸지 않는 개인 설치기
- `scripts/harness.py`: 대상 프로젝트를 명시하는 기본 검사·모듈별 CI 실행기
- `tests/`: 설치 보존·충돌·멱등성과 실행 경계 검사

## 설치

Python 3.11+와 Git을 사용합니다. Node.js 24 등 제품 검사 환경은 대상 프로젝트의 manifest·CI를 따릅니다.
`rtk`가 있으면 아래 셸 명령 앞에 `rtk` 또는 `rtk proxy`를 붙입니다.

```bash
git clone https://github.com/jsh0116/roport-codex-harness.git
cd roport-codex-harness
python3 scripts/install.py --target /absolute/path/to/kernel-robot-repo-1 --dry-run
python3 scripts/install.py --target /absolute/path/to/kernel-robot-repo-1
```

설치기는 두 스킬·5개 역할과 필요한 프로젝트 Codex 기본 설정을 설치합니다.
개인 파일과 실행 로그는 대상의 `.git/info/exclude`로 로컬에서만 제외합니다.
팀의 `AGENTS.md`, README, package.json, `.gitignore`, 서비스 코드와 CI는 수정하지 않습니다.
기존 모델·권한 설정을 보존하며 충돌 파일이나 수정이 필요한 추적 설정은 덮어쓰지 않고 실패합니다.

대상 프로젝트에서 새 Codex 채팅을 열고 요청합니다.

```text
$roport-orchestrator 관련 Tech Spec과 기존 코드를 확인하고 P0 기능을 구현해줘.
독립 작업은 나누고 변경 모듈 CI와 mock 검증 결과를 남겨줘.
```

RO:PORT 코드 작업은 **제품 프로젝트에서 시작한 채팅**에서 수행합니다. 이 하네스 checkout에서 시작한 자식은 제품 프로젝트로 자동 이동하지 않습니다.
하네스 자체를 수정·점검할 때는 `$harness`를 사용합니다. 역할 파일 생성은 현재 채팅의 custom role 발견·권한 격리·실행 성공을 보장하지 않습니다.

## 제품 검사

```bash
python3 scripts/harness.py --project /absolute/path/to/kernel-robot-repo-1 check
python3 scripts/harness.py --project /absolute/path/to/kernel-robot-repo-1 ci --module omx --dry-run
python3 scripts/harness.py --project /absolute/path/to/kernel-robot-repo-1 ci --module omx
```

`check`는 설치 구조, 기존 커밋 규칙과 Pinky/OMX source·mock 검사를 실행합니다. 루트 Husky 의존성은 제품 README대로 미리 설치합니다.
모듈은 `pinky`, `omx`, `control-server`, `ai-server`, `service-server`, `web` 중 하나를 명시합니다.
모듈 CI는 잠긴 의존성 설치·빌드를 수행할 수 있고 서비스의 Spring 테스트는 localhost 서버를 엽니다.
로봇 구동·GPU 학습·Cloud 연결은 기본 검사에 포함하지 않습니다.
실제 명령의 원본은 제품의 `.github/workflows/`입니다. 변경 시 실행기와 대조합니다.

## 하네스 개발·갱신

```bash
python3 -m unittest discover -s tests -v
python3 .agents/skills/harness/scripts/validate.py --project .
```

사용한 source commit은 `git rev-parse HEAD`로 확인하고 고정합니다. 갱신은 원하는 새 commit을 검토한 뒤 설치기를 다시 실행합니다.
동일한 파일의 재설치는 변경이 없고, 버전이 다른 기존 파일은 충돌로 보고하므로 백업·비교 후 명시적으로 교체합니다.
설치한 개인 파일을 제거하면 팀 파일은 남습니다. 제외 규칙은 `.git/info/exclude`의 관리 블록에 있습니다.
실행 기록·장비 데이터와 이동 전 백업은 원격에 올리지 않습니다.

프로젝트 사실과 안전 기준은 [RO:PORT 저장소](https://github.com/kernel-robot-8th/kernel-robot-repo-1)와 최신 Confluence 명세를 원본으로 사용합니다.
하네스 검증과 실제 장비·Cloud 검증을 구분합니다. 출처·변경 범위·라이선스는 [UPSTREAM](UPSTREAM.md)을 확인합니다.
