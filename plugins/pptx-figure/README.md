# pptx-figure

PowerPoint 도형 기반 그림 작성

에이전트 설명: PowerPoint 네이티브 도형으로 그림을 만드는 상담·실행 에이전트. python-pptx 로 개념도·모식도·단면도를 그리거나 논문 figure 의 **요소 하나**를 도형으로 재현하고, 편집 가능한 .pptx 와 원본 대조 결과를 반환한다. 여러 요소를 한 그림으로 합치는 것은 호출자(메인 세션)가 한다. "PPT 도형으로 그려줘", "이 논문 그림 재현해줘", "개념도 파워포인트로", "figure 따라 그려줘", 불리언 병합·3D 돌출·투명도·그라디언트 등 PPT 도형 기능 질문에 사용한다. 데이터 플롯(→ origin-plot)·3D 모델링·물리 해석은 관할 외.

## 설치

```
/plugin marketplace add ohh000410/subagents
/plugin install pptx-figure@ohh000410-subagents
```

설치 후 에이전트 이름은 `pptx-figure:pptx-figure` 이다. 함께 설치되는 `hooks/hooks.json` 훅이 이 에이전트가 시작될 때만 동작하여
공통 규칙과 본문을 주입한다.

Codex·Antigravity 에서는 저장소를 내려받아 `codex/agents/pptx-figure.toml`·`agy/agents/pptx-figure/` 을 연결하며, 절차는 저장소 [README](../../README.md#설치)와 [AGENTS.md](../../AGENTS.md)에 있다.

## 요구 사항

- Windows PowerShell — 위 훅이 사용하며 Windows 에 기본으로 포함되어 있다.
- Python(`<python>`): 이 PC 환경 값(메모리)의 절대경로 (python-pptx·pywin32 가 있는 것)
- 도형 생성 python-pptx / 병합·3D 되읽기·PNG export COM. COM: `pres.Close()` → 직접 띄운 PowerPoint 만 `app.Quit()`(이미 떠 있던 것은 둠) → 프로세스 잔존 확인

도구·예제 코드가 사용하는 Python 패키지: `numpy`, `pillow`, `python-pptx`, `pywin32`, `scipy`

## 첫 사용

- 에이전트가 앱 경로·venv 같은 환경 값을 찾지 못하면 사용자에게 확인한다. 확인된 값은 에이전트 메모리 `~/.claude/agent-memory/pptx-figure-pptx-figure/` 에 기록된다.

## 구성 파일

- `agents/pptx-figure.md` — 이름·설명·도구·모델과 파일 위치·메모리 안내만 담은 에이전트 껍데기
- `pptx-figure/AGENT.md` — 본문. 에이전트 시작 시 훅이 공통 계약과 함께 주입
- `hooks/` — `pptx-figure:pptx-figure` 시작 시에만 동작하는 Windows PowerShell 시작 훅
- `pptx-figure/references/` — 6개 파일
- `policies/` — 훅이 주입하는 공통 계약, 실패 처리·GUI 창 멈춤 대처 공통 정책
- `LICENSE` — MIT

## 라이선스

에이전트 지시문·references·도구 등 이 저장소의 파일은 MIT 라이선스를 따르며, 전문은 `LICENSE` 에 있다. 에이전트가 다루는 Inventor, Ansys SpaceClaim·SPEOS·Lumerical, Origin, PowerPoint 등의 앱과 도구가 사용하는 Python 패키지는 포함되어 있지 않으며, 각 라이선스에 따라 설치하고 해당 약관을 준수해야 한다.
