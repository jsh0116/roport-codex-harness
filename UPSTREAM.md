# 출처와 이관 범위

- upstream: [revfactory/codex-harness](https://github.com/revfactory/codex-harness)
- 고정 commit: `80f8217b5b6d3f220a31f05f9c0adaf09dac40f4` (`main`에서 확인, manifest 버전 0.1.0)
- 기반 원본: [revfactory/harness](https://github.com/revfactory/harness), `cceac68ea1d0ad198ef4b7b906cd238375836387`
- 라이선스: [Apache-2.0](LICENSE), 원본 고지 [NOTICE](NOTICE)
- 2026-10-27: RO:PORT에서 작성한 개인 Codex 하네스 자산을 이 저장소로 분리했다. 제품 코드·전체 팀 Git 이력·실행 로그·비밀값은 이관하지 않았다.

`harness` 스킬의 원본 18개 파일과 seed agent 5개는 upstream 내용을 보존한다.
스킬 안의 UPSTREAM.md는 초기 설치 출처 기록이며 이 개인 저장소의 현재 배치는 이 문서와 README를 따른다.
별도 root AGENTS, RO:PORT 전용 스킬, 외부 프로젝트 실행기, 개인 설치기와 테스트·CI를 추가했다.
후속 보완으로 시스템 설계·Pinky·OMX·인지·모방학습·관제·fleet·AI·서비스·웹·HMI·하드웨어·로봇 검증·플랫폼·보안 전문 역할 15개와 배정 절차를 추가했다. upstream 기본 역할 5개는 수정하지 않았다.
설치기의 `merge_config`와 파일 트랜잭션 도구는 upstream을 바탕으로 하며, 제품 AGENTS를 수정하는 설치 단계는 개인 설치기에서 사용하지 않는다.

현재 Codex는 자식 권한을 부모에게서 상속한다. seed TOML의 `sandbox_mode`는 강제 권한 분리의 근거가 아니다.
최신 [공식 subagents 문서](https://learn.chatgpt.com/docs/agent-configuration/subagents)와 실제 도구를 확인한다.
upstream의 과거 테스트 수치와 이 개인 저장소의 실제 CI 결과, custom role 발견·실장비 검증을 각각 구분한다.
