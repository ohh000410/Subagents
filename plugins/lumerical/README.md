# lumerical

FDTD·RCWA 시뮬레이션 수행

에이전트 설명(메인 세션이 위임 여부를 판단할 때 읽는 글): Lumerical 상담·실행 에이전트 (FDTD·RCWA·STACK). 설정·수렴·mesh·PML·source/monitor·lumapi 질문은 전문가로 진단하고, 실행 요청은 lumapi 시뮬 실행→결과 추출→xlsx 저장까지만 수행. Lumerical 라이선스로 도는 solver는 전부 관할 — 순수 python RCWA(meent/grcwa/torcwa)는 research-compute 담당. 상담 모드는 시뮬 실행·memory write 금지(코드·진단만), 실행 모드만 시뮬 수행 후 검증된 실측/API 함정 기록.

## 설치

```
/plugin marketplace add ohh000410/subagents
/plugin install lumerical@ohh000410-subagents
```

설치 후 에이전트 이름은 `lumerical:lumerical` 이다. 이 에이전트가 시작될 때만 동작하는 훅(`hooks/hooks.json`)이 함께 설치되어
공통 규칙과 본문을 주입한다.

Codex·Antigravity 에서는 저장소를 내려받아 `codex/agents/lumerical.toml`·`agy/agents/lumerical/` 을 연결한다 — 저장소 [README](../../README.md#설치)·[AGENTS.md](../../AGENTS.md) 참조.

## 요구 사항

- Windows PowerShell(Windows 기본 포함) — 위 훅이 사용한다.
- Python(`<python>`): 이 PC 환경 값(메모리)의 절대경로만. `python`/`py` 이름은 Store stub·다른 판으로 가 lumapi 미기동·hang.
- Lumerical 설치 경로·사용 판 = 이 PC 환경 값(메모리)
- 회전 convention: intrinsic/body-fixed

도구·예제 코드가 사용하는 Python 패키지: `numpy`, `openpyxl`

## 첫 사용

- 에이전트가 환경 값(앱 경로·venv)을 찾지 못하면 사용자에게 확인한다. 확인된 값은 에이전트 메모리 `~/.claude/agent-memory/lumerical-lumerical/` 에 기록된다.
- 도구 설명: `lumerical/tools/README.md`

## 구성 파일

- `agents/lumerical.md` — 에이전트 껍데기(이름·설명·도구·모델, 파일 위치·메모리 안내)
- `lumerical/AGENT.md` — 본문. 에이전트 시작 시 훅이 공통 계약과 함께 주입
- `hooks/` — 시작 훅(`lumerical:lumerical` 시작 시에만 동작, Windows PowerShell)
- `lumerical/references/` — 24개 파일
- `lumerical/tools/` — 5개 파일
- `policies/` — 공통 계약(훅이 주입), 공통 정책(실패 처리, GUI 창 멈춤 대처)
- `LICENSE` — MIT

## 라이선스

이 저장소의 파일(에이전트 지시문·references·도구)은 MIT 라이선스를 따른다(`LICENSE`). 에이전트가 다루는 앱(Inventor, Ansys SpaceClaim·SPEOS·Lumerical, Origin, PowerPoint)과 도구가 사용하는 Python 패키지는 포함되어 있지 않으며, 각 라이선스에 따라 설치하고 해당 약관을 준수해야 한다.
