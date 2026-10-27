# 개인 Codex 하네스 작업 규칙

- 이 저장소는 RO:PORT에 선택적으로 설치하는 개인 Codex 하네스다. 제품 구현 저장소와 분리한다.
- 하네스 구축·수정은 `.agents/skills/harness/SKILL.md`, RO:PORT 작업 절차는 `.agents/skills/roport-orchestrator/SKILL.md`를 읽는다.
- 대상 프로젝트의 AGENTS.md·manifest·lockfile·CI가 팀 규칙과 실제 실행 명령의 원본이다. 하네스가 대상의 추적 파일을 바꾸거나 안전 기준을 완화하지 않는다.
- 에이전트 권한은 부모를 상속한다. 역할의 읽기 전용 지시와 강제 sandbox 격리를 구분한다. 사용자 요청으로 정한 역할별 모델·추론 기본값은 역할 TOML에서 관리한다. 메인 모델·개인 권한·전역 설정은 바꾸지 않는다.
- 설치는 `scripts/install.py --target PROJECT --dry-run`으로 먼저 확인한다. 충돌 파일은 보존하고 사용자 편집을 덮어쓰지 않는다.
- `python3 -m unittest discover -s tests -v`와 `python3 .agents/skills/harness/scripts/validate.py --project .`로 검증한다.
- 로봇 bringup·connect·토크·캘리브레이션 쓰기·모터 구동·Cloud 연결은 기본 검사에 넣지 않는다.
- 비밀값·개인 환경·원본 대화·장비 데이터·실행 로그를 커밋하지 않는다. upstream SHA·LICENSE·NOTICE를 보존한다.
- 이 개인 저장소의 커밋에 팀 Jira 번호를 임의로 붙이지 않는다. RO:PORT 제품 변경은 해당 저장소의 Jira/PR 규칙을 따른다.
- 한국어로 결론부터 간결하게 보고한다. rtk가 있으면 셸 명령 앞에 사용한다.
