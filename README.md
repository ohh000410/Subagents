<div align="center">

# Subagents

**연구 전용 LLM 서브에이전트**<br>
Claude Code · Codex · Antigravity

![에이전트 9개](https://img.shields.io/badge/%EC%97%90%EC%9D%B4%EC%A0%84%ED%8A%B8-9%EA%B0%9C-2F80ED) ![플랫폼 Windows](https://img.shields.io/badge/%ED%94%8C%EB%9E%AB%ED%8F%BC-Windows-0078D6) ![라이선스 MIT](https://img.shields.io/badge/%EB%9D%BC%EC%9D%B4%EC%84%A0%EC%8A%A4-MIT-3DA639)

논문 그래프·CAD 모델링·광학 시뮬레이션 등 Windows 데스크톱 앱 기반 연구 작업을 위임받아<br>
앱 조작부터 결과 검증, 보고까지 수행하는 서브에이전트 모음

</div>

> 💡 AI 에이전트를 통한 설치: "github.com/ohh000410/subagents 의 AGENTS.md 를 읽고 필요한 에이전트를 설치해줘"

<br>

## 동작 구조

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/how-it-works-dark.png">
    <img src="assets/how-it-works.png" alt="사용자 → 메인 세션(Claude Code·Codex·Antigravity) → 서브에이전트(inventor) → Windows 앱 → 되읽어 검증 → 보고(판정·파일 경로)" width="85%">
  </picture>
</p>

검증을 통과하면 판정과 파일 경로를 보고하고, 실패하면 원인을 수정하여 다시 수행한다. 수행 중 확인된 환경 값·오류·해결법은 에이전트 메모리에 기록된다.

<br>

## 에이전트 구성

### 📄 문서·그림

<table>
<thead><tr><th width="28%">에이전트</th><th width="72%"><img src="assets/spacer.svg" width="100%" height="1" align="left" alt="">기능</th><th>필요 앱</th></tr></thead>
<tbody>
<tr><td nowrap><a href="plugins/doc-scan/README.md">doc-scan</a></td><td>문서 사진의 스캔본·PDF 변환</td><td nowrap>없음</td></tr>
<tr><td nowrap><a href="plugins/plot-digitizer/README.md">plot-digitizer</a></td><td>그래프 이미지의 수치 추출</td><td nowrap>웹 브라우저</td></tr>
<tr><td nowrap><a href="plugins/pptx-figure/README.md">pptx-figure</a></td><td>PowerPoint 도형 기반 그림 작성</td><td nowrap>PowerPoint</td></tr>
<tr><td nowrap><a href="plugins/origin-plot/README.md">origin-plot</a></td><td>논문 형식 그래프 작성</td><td nowrap>Origin 2019</td></tr>
</tbody>
</table>

### 🛠️ CAD·광학

<table>
<thead><tr><th width="28%">에이전트</th><th width="72%"><img src="assets/spacer.svg" width="100%" height="1" align="left" alt="">기능</th><th>필요 앱</th></tr></thead>
<tbody>
<tr><td nowrap><a href="plugins/inventor/README.md">inventor</a></td><td>부품 3D 모델·2D 도면 작성</td><td nowrap>Inventor 2027</td></tr>
<tr><td nowrap><a href="plugins/spaceclaim/README.md">spaceclaim</a></td><td>SPEOS·ANSYS 용 형상 작성</td><td nowrap>SpaceClaim v261</td></tr>
<tr><td nowrap><a href="plugins/speos/README.md">speos</a></td><td>광학 시뮬레이션 수행·결과 정리</td><td nowrap>SPEOS v261</td></tr>
</tbody>
</table>

### 🔬 시뮬레이션·계산

<table>
<thead><tr><th width="28%">에이전트</th><th width="72%"><img src="assets/spacer.svg" width="100%" height="1" align="left" alt="">기능</th><th>필요 앱</th></tr></thead>
<tbody>
<tr><td nowrap><a href="plugins/lumerical/README.md">lumerical</a></td><td>FDTD·RCWA 시뮬레이션 수행</td><td nowrap>Lumerical v242</td></tr>
<tr><td nowrap><a href="plugins/research-compute/README.md">research-compute</a></td><td>RCWA·산란·원거리장 복사 열전달</td><td nowrap>없음</td></tr>
</tbody>
</table>

<br>

## 설치

**Claude Code** — 대화창에서 다음을 입력한다.

```
/plugin marketplace add ohh000410/subagents
/plugin install inventor@ohh000410-subagents
```

`inventor` 대신 사용할 에이전트 이름을 지정한다. 설치 후 새 대화에서 "Inventor 로 이 부품 만들어줘"와 같이 요청하면 해당 에이전트에 위임된다.

**Codex · Antigravity** — 저장소를 내려받아 각 하네스에 연결한다.

```
git clone https://github.com/ohh000410/Subagents
```

- Codex: `codex/agents/` 의 에이전트 파일을 `~/.codex/agents/` 에 복사하고, `~/.codex/hooks.json` 의 `SubagentStart` 에 `hooks/subagent-start.ps1 -Harness codex` 를 등록한다. matcher 에는 설치한 에이전트 이름을, `additionalContextLimit` 에는 8000 을 지정한다. 이후 Codex 의 `/hooks` 에서 승인한다.
- Antigravity: `~/.gemini/config/agents.json` 의 `entries` 에 `{"path": "<저장소>/agy/agents"}` 를 추가한다.
- 설정 형식과 상세 절차는 [AGENTS.md](AGENTS.md) 를 참조한다.

<br>

## 운용 방식

- **상담 모드와 실행 모드:** 실행을 명시하지 않은 요청은 상담 모드로 처리한다. 앱 실행이나 파일 생성 없이 진단과 코드만 제시한다.
- **결과 검증:** 실행 모드에서는 결과를 되읽어 확인하고, PASS·WARN·FAIL 판정과 파일 경로를 보고한다.
- **에이전트 메모리:** 수행 중 확인한 PC 별 환경 값, 오류와 해결법, 소요 시간을 에이전트 메모리 폴더 `~/.claude/agent-memory/<플러그인>-<에이전트>/` 에 기록한다. 세 하네스가 같은 폴더를 공유하며, 초기 상태는 비어 있다. 메모마다 파일 하나와 `MEMORY.md` 말미의 링크 한 줄을 쓰는 Claude Code 기본 형식이므로 사용할수록 목록이 길어진다. 같은 작성자의 [Harness-Memory](https://github.com/ohh000410/Harness-Memory)를 함께 설치하면 이 폴더도 매일 밤 주제별 목차로 정리되고, 오래된 진행 기록은 보관 폴더로 이동한다. 에이전트 쪽 추가 설정은 필요 없다.
- **시작 훅:** 에이전트 파일에는 이름과 설명만 두고, 에이전트 시작 시 훅이 공통 규칙과 본문을 주입한다. 훅은 해당 에이전트가 시작될 때만 동작하며, Claude Code 에서는 플러그인 훅이, Codex·Antigravity 에서는 `hooks/subagent-start.ps1` 이 이 역할을 한다. 작성자가 실제로 사용하는 하네스와 같은 구조이다.

<br>

## 요구 사항

- Windows 와 Claude Code·Codex·Antigravity 중 하나 이상. 시작 훅이 Windows PowerShell 로 동작하므로 현재는 Windows 전용이다. Windows 앱을 사용하지 않는 doc-scan·plot-digitizer 등의 에이전트는 훅 실행 방식만 바꾸면 Linux·macOS 로 확장할 수 있다.
- 위 표의 필요 앱 열에 적힌, 사용할 에이전트의 대상 앱
- Python. 에이전트별 필요 패키지와 앱 설치 경로는 각 에이전트 README 의 "요구 사항"에 있으며, 경로가 다르면 첫 사용 시 에이전트가 확인을 요청한다.

<br>

## 라이선스

에이전트 지시문·references·도구 등 이 저장소의 파일은 MIT 라이선스를 따르며, 전문은 `LICENSE` 에 있다. 에이전트가 다루는 Inventor, Ansys SpaceClaim·SPEOS·Lumerical, Origin, PowerPoint 등의 앱과 도구가 사용하는 Python 패키지는 포함되어 있지 않으며, 각 라이선스에 따라 설치하고 해당 약관을 준수해야 한다.
