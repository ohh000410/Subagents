# build123d 모델링 → Inventor 마무리

기본 모델링 경로. 형상 반복(파라미터 바꿔 다시 실행)은 build123d, 최종 `.ipt`·도면은 Inventor.

## 실행

- 인터프리터 `tools/.venv/Scripts/python.exe` (build123d·pywin32·optuna, `tools/requirements.txt`). 없으면 `python -m venv tools/.venv` 후 `pip install -r tools/requirements.txt`.
- 스크립트에서 `sys.path` 에 `tools` 를 넣고:

```python
from build123d import *
from b3d_tools import state, interference_mm3, overhang, step_to_ipt
from step_check import step_check, step_summary
res = []
s = state(None); part = Box(40, 30, 10)
res.append(step_check("base", s, state(part), exp_dV_cm3=12.0, exp_bbox=(-2, -1.5, -0.5, 2, 1.5, 0.5)))
s = state(part); part = part - Pos(10, 0, 0) * Cylinder(3, 10)
res.append(step_check("hole", s, state(part), exp_dV_cm3=-0.282743))
print(step_summary(res))
export_step(part, "part.step"); export_stl(part, "part.stl")
```

- `state()` 는 step_check 단위로 바꿔 줌(체적 cm3, 면 수, bbox cm). 판정 기준은 Inventor 와 같음 — 「피처 단계 검증」(`inventor_ipt_modeling.md`).
- 간섭: `interference_mm3(a, b)` = 겹친 체적, 0 이면 없음. 조립 경로 검사는 조각을 `Pos(...)` 로 옮겨 가며 반복.
- FDM 오버행: `overhang(shape, max_deg=45)` = 아래를 향하고 수평에서 45° 보다 눕은 삼각형 면적(mm2)과 그 z 일부. 바닥(z 최소)에 닿은 면은 뺌. 실측: 옆으로 튀어나온 선반 밑면 100 mm2, 45° 경사 0, 26.6° 경사 223.6 mm2.
- 벽(Shell): OCCT `offset` 대신 안쪽 단면을 따로 만들어(같은 꼭짓점 수) 로프트하고 바깥에서 뺌 — 정확하고 빠름. 로프트는 단면들의 edge 수를 맞춤(다르면 면이 비틀림).

## 요구사항 → 검사표 → 최적화

요구가 많을 때. 도구 `tools/b3d_req.py`(`Req`·`run_reqs`·`optimize`), 예 `tools/tests/demo_b3d_optimize.py`.

1. 사용자 요구를 한 줄씩 `Req(id, 설명, 측정 함수, lo/hi)` 로 — 측정할 수 없는 것("보기 좋게")은 `kind="check"` 로 남기고 눈으로 확인. **이 표를 모델링 전에 사용자에게 보여 확인받음.**
2. 분류: ① 구조로 보장(형상 함수가 늘 만족 — 변수에서 뺌) ② 제약(위반량, 0 = 만족) ③ 목표 1~2개(재료·높이 등). ①로 옮길 수 있는 것을 최대한 옮김. "보장"도 측정으로 확인 — 기운 벽의 법선 두께 = 수평 두께 × cos(기울기)(45° 면 2 → 1.41).
3. 형상은 `build(P) → {이름: 형상}` 하나, 파라미터는 `P` 한 곳. 실행마다 `run_reqs` 로 표 전체와 `REQ SUMMARY` — FAIL 0 이어야 완료 보고. 피처별 `[STEP]` 검사와 함께(둘은 다른 것을 봄).
4. 변수가 많으면 `optimize(build, reqs, space, objective, n_trials=...)`: Optuna TPE + 제약, 형상 생성 실패는 불가능으로 기록하고 계속, 시도마다 CSV. 무거운 검사(광선 추적·넘어짐)는 `kind="check"` 로 최적화 밖에.
5. 측정 함수는 `fine` 인자를 받음 — 최적화 중엔 거친 표본, 끝에 상위 후보를 촘촘한 표본으로 다시 검사해 통과한 첫 해를 돌려줌(`verify_top`). 최적화 해는 표본 사이 얇은 곳에 몰림 — 시험 1~3위: 두께 표본 150개 통과, 1500개 탈락(1.68 mm).
6. 시험 결과(변수 4, 제약 4, 200회): 평가 1회 약 0.7초, 전체 2.7분, 4위 후보가 촘촘한 검사 통과(벽 1.951, 오버행 0).

측정 도구: `overhang`(아래 참고), `min_thickness(shape, n)` = 표면 삼각형 n 개에서 법선 반대로 쏜 직선이 들어가고 나오는 거리(덕트 이론 1.990 → 1.989, 상자 벽 5.0, ㄷ자 2.0 확인). `interference_mm3`.

## 마무리 (절차 통과 뒤)

1. 기본 — STEP 가져오기: `app, pid = launch()` → `doc, v = step_to_ipt(app, step, ipt)` → build123d 체적과 대조(실측 상대 오차 1.85e-15) → 도면이 필요하면 그 `.ipt` 로 도면 절차 → `finally` 에서 `doc.Close(True)`·`app.Quit()`·`kill_own(pid)`. 결과 `.ipt` 는 피처 트리 없는 바디 하나.
2. 피처 트리 `.ipt` 를 요청받았을 때만 — 같은 형상을 Inventor COM 으로 다시 작성(`inventor_ipt_modeling.md`), 체적·bbox 를 build123d 값과 대조.

## 시간 (2026-10-30 실측)

| 작업 | 시간 |
|---|---|
| build123d import | 3 s (첫 실행 8 s) |
| D형→원형 로프트 + 2 mm 벽 | 0.07 s |
| 간섭 / 체적·bbox / 오버행 / STEP+STL | 0.04 / 0.004 / 0.001 / 0.04 s |
| 홈 1000개 톱니 프로파일 extrude | 0.77 s |
| 3단계 부품 → STEP → Inventor 기동 + 가져오기 + 저장 + 종료 | 21.7 s (기동 12.4, 가져오기 8.1) |

시험: `tools/tests/live_b3d_to_ipt.py` (수동, Inventor 실측).
