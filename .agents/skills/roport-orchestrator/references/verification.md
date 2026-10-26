# 검증 실행

명령은 RO:PORT 제품 프로젝트 루트를 `--project`로 명시한다. 개인 하네스 checkout 경로와 제품 경로를 구분한다. Python 3.11+와 Node.js 24가 필요하며 CI는 Python 3.12를 사용한다.
`rtk`가 있으면 셸 명령 앞에 `rtk` 또는 `rtk proxy`를 붙인다.

## 기본 검사

```bash
python3 /path/to/roport-codex-harness/scripts/harness.py --project /path/to/ROPORT check
```

설치된 하네스 TOML·스킬 참조·실행 장부 구조, 제품 커밋 규칙, Pinky·OMX의 기존 표준 라이브러리 source/mock 테스트를 실행한다. 의존성 설치·ROS 노드·모터·시리얼 연결·GPU·Cloud 연결은 실행하지 않는다.
이 검사는 실제 native 역할 발견·권한 강제·동시 실행의 성공을 증명하지 않는다.

## 변경 모듈 CI

실행할 명령과 디렉토리를 먼저 확인할 수 있다.

```bash
python3 /path/to/roport-codex-harness/scripts/harness.py --project /path/to/ROPORT ci --module omx --dry-run
python3 /path/to/roport-codex-harness/scripts/harness.py --project /path/to/ROPORT ci --module omx
```

`--module`은 `pinky`, `omx`, `control-server`, `ai-server`, `service-server`, `web` 중 하나를 명시한다. 생략하면 실패한다.
명령은 개인 하네스의 `scripts/harness.py`와 제품의 `.github/workflows/*-ci.yml`을 대조한다. 실제 모듈 CI가 원본이다. runner 동작·설치기 자체 테스트는 개인 하네스의 `tests/`에서 실행한다.

- Pinky: ROS 2 Jazzy 환경에서 기존 `bash ci/test.sh`로 source 검사·선택 패키지 빌드·메시지/URDF 검사를 한다. ARM64 드라이버·센서·주행이나 Gazebo 실행 검증은 별도다.
- OMX: `uv sync --locked`, `ruff check src`, `ruff format --check src`, 코어 import, `bash ci/test.sh`, `uv build`. LeRobot 학습 환경 설치·하드웨어 connect는 포함하지 않는다.
- 관제·AI: locked uv 환경, Ruff, pytest, wheel build. health 성공을 연결·모델 준비로 확대하지 않는다.
- 서비스: Java 21/Maven으로 `mvn --batch-mode --no-transfer-progress verify`.
- Web: Node.js 24로 `npm ci`, `npm run typecheck`, `npm run build`.

모듈 CI는 locked 의존성 설치와 빌드 캐시 생성을 수행할 수 있다. 로봇 bringup이나 네트워크 배포를 추가하지 않는다. 실행 전 변경된 CI·테스트 코드에 장비/실서비스 접근이 생겼는지 확인한다.
실패하면 뒤 명령을 중단한다. 미설치 도구·네트워크 차단은 통과로 숨기지 않고 실제 실패와 미실행 후속 검사를 기록한다.

## 연동 변경의 검증 근거

생산자·소비자에 동일 schema/단위/ID/시간 기준과 오류 표현을 적용했는지 확인한다. mock 또는 replay로 정상 처리, 중복·유실·순서 역전·만료·timeout·재접속·중도 재시작을 변경 범위에 맞게 검증한다. 테스트를 위해 실제 topic에 publish하거나 장비 connect를 호출하지 않는다.

시뮬레이션과 실장비 검사는 별도 절차다. 장비 지시와 현장 안전 조건이 확인되기 전에는 모터·토크·캘리브레이션 쓰기를 실행하지 않는다. 실물 검증에는 기체·포트 소유자·설정·단위/좌표·제한값·캘리브레이션·정지/복구 방법과 로그/영상 근거를 기록한다.

최종 보고에는 대상 commit 또는 로컬 diff, 환경, 실제 명령·결과, 실패·미실행 사유를 남긴다. 원격 push/CI는 직접 조회한 결과만 보고한다.
