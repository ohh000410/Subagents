# research-compute

RCWA·산란·원거리장 복사 열전달

에이전트 설명(메인 세션이 위임 여부를 판단할 때 읽는 글): Python 기반 RCWA, TMM/Fresnel, Mie·core-shell 산란, 원거리장 복사 열전달 계산을 수행하고 수렴·cross-check까지 검증하는 에이전트. FDTD와 Lumerical RCWA·STACK은 관할 밖이다.

## 설치

```
/plugin marketplace add ohh000410/subagents
/plugin install research-compute@ohh000410-subagents
```

설치 후 에이전트 이름은 `research-compute:research-compute` 이다. 이 에이전트가 시작될 때만 동작하는 훅(`hooks/hooks.json`)이 함께 설치되어
공통 규칙과 본문을 주입한다.

Codex·Antigravity 에서는 저장소를 내려받아 `codex/agents/research-compute.toml`·`agy/agents/research-compute/` 을 연결한다 — 저장소 [README](../../README.md#설치)·[AGENTS.md](../../AGENTS.md) 참조.

## 요구 사항

- Windows PowerShell(Windows 기본 포함) — 위 훅이 사용한다.
- Python: 첫 사용 시 에이전트가 이 PC 의 Python 을 확인하고, 없으면 사용자에게 묻는다.

도구·예제 코드가 사용하는 Python 패키지: `grcwa`, `matplotlib`, `meent`, `numpy`, `pywin32`, `torch`

## 첫 사용

- 에이전트가 환경 값(앱 경로·venv)을 찾지 못하면 사용자에게 확인한다. 확인된 값은 에이전트 메모리 `~/.claude/agent-memory/research-compute-research-compute/` 에 기록된다.
- 도구 설명: `research-compute/tools/README.md`

## 구성 파일

- `agents/research-compute.md` — 에이전트 껍데기(이름·설명·도구·모델, 파일 위치·메모리 안내)
- `research-compute/AGENT.md` — 본문. 에이전트 시작 시 훅이 공통 계약과 함께 주입
- `hooks/` — 시작 훅(`research-compute:research-compute` 시작 시에만 동작, Windows PowerShell)
- `research-compute/references/` — 12개 파일
- `research-compute/tools/` — 3개 파일
- `policies/` — 공통 계약(훅이 주입), 공통 정책(실패 처리, GUI 창 멈춤 대처)
- `LICENSE` — MIT

## 라이선스

이 저장소의 파일(에이전트 지시문·references·도구)은 MIT 라이선스를 따른다(`LICENSE`). 에이전트가 다루는 앱(Inventor, Ansys SpaceClaim·SPEOS·Lumerical, Origin, PowerPoint)과 도구가 사용하는 Python 패키지는 포함되어 있지 않으며, 각 라이선스에 따라 설치하고 해당 약관을 준수해야 한다.
