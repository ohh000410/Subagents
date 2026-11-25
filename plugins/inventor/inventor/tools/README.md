# inventor/tools

| 파일 | 용도 |
|---|---|
| `step_check.py` | 피처 단계 판정 `[STEP PASS/WARN/FAIL]`(체적·면 수 전후, 이론 dV, base extrude bbox)·체적 되읽기 헬퍼(`CacheResultsOnCompute=False`). 지시 = `../AGENT.md` 절차 2·5, 판단 기준·함정 = `../references/inventor_ipt_modeling.md` 「피처 단계 검증」 |
| `b3d_tools.py` | build123d 형상 → step_check 입력(`state`), 간섭 체적, FDM 오버행 면적, 최소 벽 두께(`min_thickness`), STEP → Inventor `.ipt`(`step_to_ipt`). 사용법 = `../references/inventor_b3d_modeling.md`. 실행 = `.venv`(`requirements.txt`: build123d·pywin32) |
| `b3d_req.py` | 요구사항 검사표(`Req`·`run_reqs` → `REQ SUMMARY`)와 제약 최적화(`optimize`: Optuna TPE, 실패 시도 기록, CSV, 상위 후보 촘촘한 재검사). 사용법 = `../references/inventor_b3d_modeling.md` 「요구사항 → 검사표 → 최적화」 |
| `inventor_session.py` | `launch()` = 이미 떠 있으면 거부(PID·창 제목), 아니면 기동 후 자기 PID 반환. `kill_own(pid)` = 자기 PID 만 종료, 끝났는지는 프로세스 목록으로 판정. 이름 일괄 종료 금지 |
| `tests/test_step_check.py` | 단독 시험(Inventor 불필요): `python -m unittest discover -s tests` |
| `tests/demo_b3d_optimize.py` | 덕트 4변수·4제약 재료 최소 최적화 시험(Inventor 불필요, 약 3분) |
| `tests/live_b3d_to_ipt.py` | build123d 3단계 → STEP → Inventor 가져오기 체적 대조 실측(수동, `.venv`) |
| `tests/live_step_check_inventor.py` | Inventor 실측 시험(수동 실행, 끝나면 프로세스 0 확인) |
