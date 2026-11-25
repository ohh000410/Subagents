# inventor

부품 3D 모델·2D 도면 작성

에이전트 설명(메인 세션이 위임 여부를 판단할 때 읽는 글): Inventor 2027 COM 에이전트. 기계 부품·조립품을 3D 모델(.ipt/.iam)로 만들거나 STEP/IPT/IAM을 2D 도면(.idw/.pdf)으로 만들 때, 또는 COM API·모델링·도면 오류를 진단할 때 사용. 상담 모드는 진단(코드·근거만, memory write 금지), 실행 모드는 .ipt/.iam 또는 .idw/.pdf 생성→체적 되읽기· 충돌검사·시각검증까지 수행 후 검증된 함정만 기록. SPEOS·ANSYS용 형상과 광학 곡면은 spaceclaim 담당.

## 설치

```
/plugin marketplace add ohh000410/subagents
/plugin install inventor@ohh000410-subagents
```

설치 후 에이전트 이름은 `inventor:inventor` 이다. 이 에이전트가 시작될 때만 동작하는 훅(`hooks/hooks.json`)이 함께 설치되어
공통 규칙과 본문을 주입한다.

Codex·Antigravity 에서는 저장소를 내려받아 `codex/agents/inventor.toml`·`agy/agents/inventor/` 을 연결한다 — 저장소 [README](../../README.md#설치)·[AGENTS.md](../../AGENTS.md) 참조.

## 요구 사항

- Windows PowerShell(Windows 기본 포함) — 위 훅이 사용한다.
| 항목 | 값 |
|---|---|
| Inventor 2027 | `C:\Program Files\Autodesk\Inventor 2027\Bin\Inventor.exe` |
| COM ProgID | `Inventor.Application` |
| venv | Inventor COM 스크립트 = 환경 값(PC 마다 다름). build123d·가져오기 = `inventor/tools/.venv` |
| IDW Template | `C:\Users\Public\Documents\Autodesk\Inventor 2027\Templates\en-US\Metric\ANSI (mm).idw` |
| IPT Template | `C:\Users\Public\Documents\Autodesk\Inventor 2027\Templates\en-US\Metric\Standard (mm).ipt` |
| API 문서 | 로컬 CHM `C:\Users\Public\Documents\Autodesk\Inventor 2027\Local Help\admapi_31_0.chm` 우선 → `https://help.autodesk.com/view/INVNTOR/2025/ENU/` |

`app.Visible = True` 필수. `False` → `Profiles.AddForSolid` 실패, 모달 정지 감지 불가.

도구·예제 코드가 사용하는 Python 패키지: `build123d==0.13.0`, `optuna==5.0.0`, `pywin32==312`

## 첫 사용

- 에이전트가 환경 값(앱 경로·venv)을 찾지 못하면 사용자에게 확인한다. 확인된 값은 에이전트 메모리 `~/.claude/agent-memory/inventor-inventor/` 에 기록된다.
- 도구 설명: `inventor/tools/README.md`

## 구성 파일

- `agents/inventor.md` — 에이전트 껍데기(이름·설명·도구·모델, 파일 위치·메모리 안내)
- `inventor/AGENT.md` — 본문. 에이전트 시작 시 훅이 공통 계약과 함께 주입
- `hooks/` — 시작 훅(`inventor:inventor` 시작 시에만 동작, Windows PowerShell)
- `inventor/references/` — 7개 파일
- `inventor/tools/` — 11개 파일
- `policies/` — 공통 계약(훅이 주입), 공통 정책(실패 처리, GUI 창 멈춤 대처)
- `LICENSE` — MIT

## 라이선스

이 저장소의 파일(에이전트 지시문·references·도구)은 MIT 라이선스를 따른다(`LICENSE`). 에이전트가 다루는 앱(Inventor, Ansys SpaceClaim·SPEOS·Lumerical, Origin, PowerPoint)과 도구가 사용하는 Python 패키지는 포함되어 있지 않으며, 각 라이선스에 따라 설치하고 해당 약관을 준수해야 한다.
