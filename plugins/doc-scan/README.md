# doc-scan

문서 사진의 스캔본·PDF 변환

에이전트 설명: 문서·종이를 휴대폰으로 찍은 사진을 스캔본처럼 후처리하는 에이전트. 종이 모서리를 찾아 반듯하게 펴고(원근 보정), 그림자·조명 얼룩을 지우고, 컬러·흑백 스캔 파일과 PDF 를 만든다. "이 사진 스캔본으로 만들어줘", "문서 사진 펴줘", "스캔한 것처럼 해줘", "사진 여러 장 PDF 로 묶어줘" 요청 시 사용. 글자 인식(OCR)·요약은 하지 않는다.

## 설치

```
/plugin marketplace add ohh000410/subagents
/plugin install doc-scan@ohh000410-subagents
```

설치 후 에이전트 이름은 `doc-scan:doc-scan` 이다. 함께 설치되는 `hooks/hooks.json` 훅이 이 에이전트가 시작될 때만 동작하여
공통 규칙과 본문을 주입한다.

Codex·Antigravity 에서는 저장소를 내려받아 `codex/agents/doc-scan.toml`·`agy/agents/doc-scan/` 을 연결하며, 절차는 저장소 [README](../../README.md#설치)와 [AGENTS.md](../../AGENTS.md)에 있다.

## 요구 사항

- Windows PowerShell — 위 훅이 사용하며 Windows 에 기본으로 포함되어 있다.
| 항목 | 값 |
|---|---|
| 도구 | `doc-scan\tools\.venv\Scripts\python.exe doc-scan\tools\scan.py` — 마지막 줄 JSON. 없으면 `doc-scan\tools\setup.ps1` |
| 읽는 형식 | jpg·png·heic(아이폰)·webp·bmp·tif. EXIF 회전 반영 |
| 쓰는 형식 | color → `<이름>_color.jpg`, gray → `_gray.png`, bw → `_bw.png`, `--pdf <이름>.pdf`(첫 번째 mode 로) |

도구·예제 코드가 사용하는 Python 패키지: `numpy`, `opencv-python-headless`, `pillow`, `pillow-heif`

## 첫 사용

- 에이전트가 앱 경로·venv 같은 환경 값을 찾지 못하면 사용자에게 확인한다. 확인된 값은 에이전트 메모리 `~/.claude/agent-memory/doc-scan-doc-scan/` 에 기록된다.
- 도구 환경: `doc-scan/tools/setup.ps1` 이 `doc-scan/tools/.venv` 를 생성한다. 플러그인 업데이트 후에는 다시 생성한다.

## 구성 파일

- `agents/doc-scan.md` — 이름·설명·도구·모델과 파일 위치·메모리 안내만 담은 에이전트 껍데기
- `doc-scan/AGENT.md` — 본문. 에이전트 시작 시 훅이 공통 계약과 함께 주입
- `hooks/` — `doc-scan:doc-scan` 시작 시에만 동작하는 Windows PowerShell 시작 훅
- `doc-scan/references/` — 1개 파일
- `doc-scan/tools/` — 5개 파일
- `policies/` — 훅이 주입하는 공통 계약, 실패 처리·GUI 창 멈춤 대처 공통 정책
- `LICENSE` — MIT

## 라이선스

에이전트 지시문·references·도구 등 이 저장소의 파일은 MIT 라이선스를 따르며, 전문은 `LICENSE` 에 있다. 에이전트가 다루는 Inventor, Ansys SpaceClaim·SPEOS·Lumerical, Origin, PowerPoint 등의 앱과 도구가 사용하는 Python 패키지는 포함되어 있지 않으며, 각 라이선스에 따라 설치하고 해당 약관을 준수해야 한다.
