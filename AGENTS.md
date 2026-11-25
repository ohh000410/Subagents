# AGENTS.md

AI 에이전트용 설치·사용 안내. 사람용 소개는 `README.md`.
이 저장소는 연구용 서브에이전트 묶음이다 — Claude Code 에는 플러그인 마켓플레이스 `ohh000410-subagents`(플러그인 하나 = 서브에이전트 하나), Codex·Antigravity(agy) 에는 같은 에이전트의 껍데기(`codex/agents/`, `agy/agents/`)와 공용 시작 훅(`hooks/subagent-start.ps1`).
그 에이전트가 뜰 때만 도는 훅(Windows PowerShell)이 공통 규칙과 본문을 넣는다 — Windows 전용. 에이전트 메모리는 세 하네스가 같은 폴더 `~/.claude/agent-memory/<이름>-<이름>/` 를 쓴다.

## 고르기

| 사용자가 하려는 일 | 에이전트 | 필요한 앱 |
|---|---|---|
| 문서 사진 → 스캔본·PDF | `doc-scan` | 없음 |
| 그래프 이미지 → 수치 | `plot-digitizer` | 웹 브라우저 |
| PowerPoint 도형 그림 | `pptx-figure` | PowerPoint |
| Origin 그래프 | `origin-plot` | Origin 2019 |
| 부품 3D 모델·2D 도면 | `inventor` | Inventor 2027 |
| SPEOS·ANSYS 용 형상 | `spaceclaim` | SpaceClaim v261 |
| SPEOS 광학 시뮬레이션 | `speos` | SPEOS v261 |
| Lumerical FDTD·RCWA·STACK | `lumerical` | Lumerical v242 |
| Python RCWA·산란·원거리장 복사 열전달 계산 | `research-compute` | 없음 |

모두 Python 을 쓴다(SpaceClaim·SPEOS 의 실행 스크립트는 CPython — 3.12·3.14 에서 시험). 앱의 검증한 판·설치 경로와 Python 패키지는 `plugins/<이름>/README.md` 의 "필요한 것".

설치할 에이전트와 하네스(Claude Code·Codex·agy)를 사용자에게 확인한다. 설정 파일을 바꾸는 단계마다 무엇을 바꿀지 보여 주고 먼저 묻고, 백업한다.

## 설치 — Claude Code

1. 범위(모든 프로젝트 = `user`, 이 프로젝트만 = `project`)를 사용자에게 확인한다.
2. `claude plugin marketplace add ohh000410/subagents` (Claude Code 대화 안에서는 `/plugin marketplace add ohh000410/subagents`)
3. 에이전트마다 `claude plugin install <이름>@ohh000410-subagents` — 이 프로젝트만이면 `--scope project`
4. `claude plugin details <이름>@ohh000410-subagents` 로 에이전트 1개가 잡혔는지 확인한다.
5. 에이전트는 새 세션부터 보인다. 이름은 `<이름>:<이름>` (예: `inventor:inventor`).

## 설치 — Codex

Codex 홈 = `CODEX_HOME`, 없으면 `%USERPROFILE%\.codex`. 아래 2·3번 모두 이 폴더 아래.

1. 저장소를 임시 폴더가 아닌 고정된 곳에 받는다: `git clone https://github.com/ohh000410/Subagents <저장소>`
2. 에이전트마다 `<저장소>\codex\agents\<이름>.toml` 을 `<Codex 홈>\agents\` 에 복사한다. 같은 이름이 이미 있으면 멈추고 묻는다.
3. `<Codex 홈>\hooks.json` 의 최상위 `hooks` 객체에 `SubagentStart` 항목 하나를 합친다(기존 항목은 모두 유지). `matcher` 에는 2번에서 설치한 이름만 `^(이름1|이름2)$` 로 — 다른 서브에이전트에는 훅이 돌지 않는다. `additionalContextLimit` 8000 은 빼지 않는다 — 기본값(약 2,500 토큰)이면 그보다 긴 본문이 파일로 빠지고 앞뒤만 보인다. doc-scan·inventor 를 설치한 예:

```json
{
  "hooks": {
    "SubagentStart": [
      {
        "matcher": "^(doc-scan|inventor)$",
        "hooks": [
          {
            "type": "command",
            "command": "powershell -NoProfile -ExecutionPolicy Bypass -File \"<저장소>\\hooks\\subagent-start.ps1\" -Harness codex",
            "timeout": 10,
            "additionalContextLimit": 8000
          }
        ]
      }
    ]
  }
}
```

4. 사용자가 Codex 에서 `/hooks` 로 이 훅을 승인해야 돈다.
5. 새 세션부터 그 에이전트(이름 = `<이름>`)에게 맡길 수 있다.

## 설치 — Antigravity (agy 1.5.16)

1. 저장소를 받는다(위 Codex 1번).
2. `%USERPROFILE%\.gemini\config\agents.json` 의 `entries` 에 `{"path": "<저장소>/agy/agents"}` 를 넣는다 — 없으면 `{"entries": [...]}` 로 새로 만들고, 경로는 `/` 와 드라이브 문자로. 그 폴더의 에이전트가 모두 목록에 보인다(부를 때만 뜬다).
3. 에이전트별 훅(`agy/agents/<이름>/hooks.json`)은 저장소 안 상대 경로(`..\..\..\hooks\`)라 고칠 것이 없다 — 에이전트 폴더를 저장소 밖으로 옮기면 훅을 못 찾는다. 그 서브에이전트 대화가 시작될 때(`SessionStart`) 한 번 본문을 넣는다.

## 설치 뒤 (공통)

- `plugins/<이름>/README.md` 의 "필요한 것"에 적힌 앱과 경로가 이 PC 에 있는지 확인하고, 없거나 다르면 사용자에게 알린다.

## 쓰기

- 할 일을 그 에이전트에게 맡긴다. 실행을 명시하지 않으면 상담 모드(읽기·진단만)다.
- 첫 실행 때 에이전트가 환경 값(앱 경로·venv)을 확인해 자기 메모리에 남긴다. 확인할 수 없으면 사용자에게 묻는다.
- 앱 라이선스와 약관은 사용자 몫이다(`README.md` 의 라이선스 절).

## 지우기

- Claude Code: `claude plugin uninstall <이름>@ohh000410-subagents` — 모두 지웠으면 `claude plugin marketplace remove ohh000410-subagents`.
- Codex: `<Codex 홈>\agents\` 의 그 `.toml` 을 지우고 `hooks.json` 의 `matcher` 에서 그 이름을 뺀다. 모두 지웠으면 그 `SubagentStart` 항목을 뺀다.
- agy: `agents.json` 의 그 항목을 뺀다(이 저장소의 에이전트가 모두 빠진다).

에이전트 메모리(`~/.claude/agent-memory/<이름>-<이름>/`)는 남는다. 세 하네스가 같이 쓰는 폴더라 지우면 모든 하네스에서 사라진다.
