# origin-plot

논문 형식 그래프 작성

에이전트 설명(메인 세션이 위임 여부를 판단할 때 읽는 글): OriginLab Origin 그래프 생성·스타일링·export 전담 상담·실행 에이전트. Origin(win32com COM) 그래프를 논문 형식으로 그리거나 기존 .opju 스타일을 재현하는 요청, LabTalk/축/범례/심볼 스타일 질문을 처리한다. "오리진으로 그래프 그려줘", "이 논문 그래프 형식 따라해", "opju 스타일 재현", "LabTalk으로 축/범례 설정" 요청 시 사용. 데이터 계산·해석·물리 판단은 관할 외.

## 설치

```
/plugin marketplace add ohh000410/subagents
/plugin install origin-plot@ohh000410-subagents
```

설치 후 에이전트 이름은 `origin-plot:origin-plot` 이다. 이 에이전트가 시작될 때만 동작하는 훅(`hooks/hooks.json`)이 함께 설치되어
공통 규칙과 본문을 주입한다.

Codex·Antigravity 에서는 저장소를 내려받아 `codex/agents/origin-plot.toml`·`agy/agents/origin-plot/` 을 연결한다 — 저장소 [README](../../README.md#설치)·[AGENTS.md](../../AGENTS.md) 참조.

## 요구 사항

- Windows PowerShell(Windows 기본 포함) — 위 훅이 사용한다.
- Origin 2019. `originpro` 불가. win32com COM: `app = w32.Dispatch("Origin.ApplicationSI")`
- Python(`<python>`): 이 PC 환경 값(메모리)의 절대경로
- 원본 `.opju`: `app.Load`만. 산출물: 다른 경로, `app.Save(r"...")`, 백슬래시 경로
- 검증 도구: `origin-plot/tools/origin_verify.py` (사용법·`intended` 스키마 = docstring, 검사별 근거 = 보고의 `ref` 칸·각 검사 주석의 references 파일, 개요 `origin-plot/tools/README.md`). 세션 시작·LabTalk 전송·종료는 이 도구로만

도구·예제 코드가 사용하는 Python 패키지: `pywin32`

## 첫 사용

- 에이전트가 환경 값(앱 경로·venv)을 찾지 못하면 사용자에게 확인한다. 확인된 값은 에이전트 메모리 `~/.claude/agent-memory/origin-plot-origin-plot/` 에 기록된다.
- 도구 설명: `origin-plot/tools/README.md`

## 구성 파일

- `agents/origin-plot.md` — 에이전트 껍데기(이름·설명·도구·모델, 파일 위치·메모리 안내)
- `origin-plot/AGENT.md` — 본문. 에이전트 시작 시 훅이 공통 계약과 함께 주입
- `hooks/` — 시작 훅(`origin-plot:origin-plot` 시작 시에만 동작, Windows PowerShell)
- `origin-plot/references/` — 5개 파일
- `origin-plot/tools/` — 4개 파일
- `policies/` — 공통 계약(훅이 주입), 공통 정책(실패 처리, GUI 창 멈춤 대처)
- `LICENSE` — MIT

## 라이선스

이 저장소의 파일(에이전트 지시문·references·도구)은 MIT 라이선스를 따른다(`LICENSE`). 에이전트가 다루는 앱(Inventor, Ansys SpaceClaim·SPEOS·Lumerical, Origin, PowerPoint)과 도구가 사용하는 Python 패키지는 포함되어 있지 않으며, 각 라이선스에 따라 설치하고 해당 약관을 준수해야 한다.
