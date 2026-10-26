# Codex Harness 출처

- 원본: https://github.com/revfactory/codex-harness
- 확인일: 2026-10-27
- 소스: `main`, commit `80f8217b5b6d3f220a31f05f9c0adaf09dac40f4`
- plugin manifest 표시 버전: `0.1.0` (릴리스 태그로 고정한 버전이 아니다)
- 설치: 원본 `scripts/install.py --target PROJECT --dry-run` 검토 후 동일 설치기 실행
- 복사 범위: `skills/harness/` → `.agents/skills/harness/`, 5개 `.codex/agents/harness-*.toml`, 기본 project config, 루트 AGENTS 포인터
- 라이선스: Apache-2.0. 원본 [LICENSE](LICENSE)와 [NOTICE](NOTICE)를 함께 보존한다.
- 원 프로젝트: https://github.com/revfactory/harness, upstream 기반 SHA `cceac68ea1d0ad198ef4b7b906cd238375836387`

원본 스킬/스크립트/seed 역할은 수정하지 않았다. 이 출처 기록과 원본 LICENSE·NOTICE만 설치 사본에 추가했다.
RO:PORT 전용 절차는 인접 `roport-orchestrator` 스킬, 공통 검사 진입점은 루트 `scripts/harness.py`에 둔다.
갱신할 때는 새 원본 SHA·설치 충돌·라이선스·원본 자동 테스트·로컬 검사를 확인하고 이 기록을 함께 갱신한다. 충돌을 덮어쓰지 않는다.

## Codex 버전 차이

원본은 seed 역할에 `sandbox_mode`를 기록한다. 현재 [공식 subagents 문서](https://learn.chatgpt.com/docs/agent-configuration/subagents)는 자식의 권한·provider·MCP가 부모를 상속하고 custom agent의 `sandbox_mode`가 부모 설정을 재정의하지 않는다고 설명한다.
따라서 읽기 전용 역할은 쓰기 금지 지시이며 별도 강제 격리를 보장하지 않는다. 적용되는 실제 세션 권한을 확인한다.
구조 검사 통과는 native custom-role 발견·동시 실행·sandbox 강제나 로봇/Cloud 검증을 의미하지 않는다.
