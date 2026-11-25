# plot-digitizer

그래프 이미지의 수치 추출

에이전트 설명: 논문·문헌 figure(polar half-circle, cartesian line/scatter)의 곡선을 정량 데이터(angle/x vs value)로 추출하는 에이전트. cross-validation·선행연구 참고값 추출 등 그래프에서 수치를 읽어내야 할 때 use proactively. 이미지가 없거나 저해상도면 원본 PDF에서 직접 고해상도로 확보하고(벡터/raster 구분), half-circle polar는 축 클릭 없이 자동 캘리브(반원 기하 교차검증)를 시도하며, 필요 시 picker 서버로 사용자 클릭 캘리브를 받는다. 항상 csv + 추출 검증 overlay + 캘리브 체크 overlay png를 반환한다. "이 그래프 디지타이즈해줘", "논문 figure 값 추출", "polar plot 곡선 읽어줘" 요청에 호출.

## 설치

```
/plugin marketplace add ohh000410/subagents
/plugin install plot-digitizer@ohh000410-subagents
```

설치 후 에이전트 이름은 `plot-digitizer:plot-digitizer` 이다. 함께 설치되는 `hooks/hooks.json` 훅이 이 에이전트가 시작될 때만 동작하여
공통 규칙과 본문을 주입한다.

Codex·Antigravity 에서는 저장소를 내려받아 `codex/agents/plot-digitizer.toml`·`agy/agents/plot-digitizer/` 을 연결하며, 절차는 저장소 [README](../../README.md#설치)와 [AGENTS.md](../../AGENTS.md)에 있다.

## 요구 사항

- Windows PowerShell — 위 훅이 사용하며 Windows 에 기본으로 포함되어 있다.
- 환경: Python(`<python>`) = 이 PC 환경 값(메모리) — numpy, opencv-python, matplotlib, Pillow

도구·예제 코드가 사용하는 Python 패키지: `matplotlib`, `numpy`, `pillow`, `pymupdf`

## 첫 사용

- 에이전트가 앱 경로·venv 같은 환경 값을 찾지 못하면 사용자에게 확인한다. 확인된 값은 에이전트 메모리 `~/.claude/agent-memory/plot-digitizer-plot-digitizer/` 에 기록된다.
- 도구 설명: `plot-digitizer/tools/README.md`

## 구성 파일

- `agents/plot-digitizer.md` — 이름·설명·도구·모델과 파일 위치·메모리 안내만 담은 에이전트 껍데기
- `plot-digitizer/AGENT.md` — 본문. 에이전트 시작 시 훅이 공통 계약과 함께 주입
- `hooks/` — `plot-digitizer:plot-digitizer` 시작 시에만 동작하는 Windows PowerShell 시작 훅
- `plot-digitizer/references/` — 2개 파일
- `plot-digitizer/tools/` — 6개 파일
- `policies/` — 훅이 주입하는 공통 계약, 실패 처리·GUI 창 멈춤 대처 공통 정책
- `LICENSE` — MIT

## 라이선스

에이전트 지시문·references·도구 등 이 저장소의 파일은 MIT 라이선스를 따르며, 전문은 `LICENSE` 에 있다. 에이전트가 다루는 Inventor, Ansys SpaceClaim·SPEOS·Lumerical, Origin, PowerPoint 등의 앱과 도구가 사용하는 Python 패키지는 포함되어 있지 않으며, 각 라이선스에 따라 설치하고 해당 약관을 준수해야 한다.
