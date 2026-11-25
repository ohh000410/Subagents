"""요구사항 검사표와 제약 최적화 (build123d, tools/.venv).

검사표: 사용자 요구 한 줄 = Req 하나. 측정 함수 fn(parts, P, fine) → 숫자, 기준 lo/hi.
    kind = "constraint"(최적화가 지킬 것) / "check"(최종 검증만, 예: 무거운 계산·눈 확인 기록)
    REQ 표와 `REQ SUMMARY: FAIL n / PASS m` 을 출력 — FAIL 0 이어야 완료 보고.
최적화: build(P) → {이름: 형상}, 목표 objective(parts, P) → 숫자(작을수록 좋음).
    Optuna TPE + 제약(위반량 > 0 이면 불가능). 형상 생성 실패는 불가능으로 기록하고 계속.
    시도마다 CSV 한 줄. 끝나면 최적해를 fine=True(촘촘한 표본)로 다시 검사 — 최적화는 표본 사이 빈틈을 파고든다.
절차·예: ../references/inventor_b3d_modeling.md 「요구사항 → 최적화」
"""
import csv, math, time


class Req:
    def __init__(self, id, desc, fn, lo=None, hi=None, kind="constraint", unit=""):
        self.id, self.desc, self.fn, self.lo, self.hi, self.kind, self.unit = id, desc, fn, lo, hi, kind, unit

    def violation(self, v):
        """0 = 만족. 측정 실패(NaN·None)는 큰 위반."""
        if v is None or not math.isfinite(v):
            return 1e6
        return max(0.0, (self.lo - v) if self.lo is not None else 0.0) + max(0.0, (v - self.hi) if self.hi is not None else 0.0)

    def bound(self):
        return " ".join(s for s in ((">= %g" % self.lo) if self.lo is not None else "",
                                    ("<= %g" % self.hi) if self.hi is not None else "") if s)


def run_reqs(reqs, parts, P, fine=False, kinds=("constraint", "check"), echo=True):
    """[(Req, 값, 위반량)]. echo 면 표와 요약 줄 출력."""
    rows = []
    for r in reqs:
        if r.kind not in kinds:
            continue
        try:
            v = r.fn(parts, P, fine)
        except Exception:  # 측정 자체가 깨지면 FAIL 로 보이게
            v = None
        rows.append((r, v, r.violation(v)))
    if echo:
        for r, v, x in rows:
            print("%-4s %-28s %12s %-12s %s" % (r.id, r.desc, "-" if v is None else "%.4g%s" % (v, r.unit),
                                                 r.bound(), "PASS" if x == 0 else "FAIL (%.3g)" % x))
        print(req_summary(rows))
    return rows


def req_summary(rows):
    nf = sum(x > 0 for _, _, x in rows)
    return "REQ SUMMARY: FAIL %d / PASS %d" % (nf, len(rows) - nf)


def optimize(build, reqs, space, objective, P0=None, n_trials=200, seed=0, csv_path=None, echo_every=25, verify_top=10):
    """space = {이름: (lo, hi) | (lo, hi, "int") | [선택지...]}. 반환 (best_P, best_parts, study)."""
    import optuna
    optuna.logging.set_verbosity(optuna.logging.WARNING)
    cons = [r for r in reqs if r.kind == "constraint"]
    P0 = dict(P0 or {})
    f = open(csv_path, "w", newline="", encoding="utf-8") if csv_path else None
    w = csv.writer(f) if f else None
    if w:
        w.writerow(["trial", "ok", "objective"] + list(space) + [r.id for r in cons] + ["sec"])

    def sample(trial):
        P = dict(P0)
        for k, s in space.items():
            if isinstance(s, list):
                P[k] = trial.suggest_categorical(k, s)
            elif len(s) == 3 and s[2] == "int":
                P[k] = trial.suggest_int(k, s[0], s[1])
            else:
                P[k] = trial.suggest_float(k, s[0], s[1])
        return P

    def obj(trial):
        t = time.time()
        P = sample(trial)
        try:
            parts = build(P)
            viol = [x for _, _, x in run_reqs(cons, parts, P, fine=False, echo=False)]
            val = float(objective(parts, P))
            ok = True
        except Exception:   # 로프트 실패 등 — 불가능으로 두고 다음 시도
            viol, val, ok = [1e6] * len(cons), 1e12, False
        trial.set_user_attr("c", viol)
        for r, x in zip(cons, viol):   # Optuna 5: 제약은 trial 에 직접(constraints_func 는 폐기 예정)
            trial.set_constraint(r.id, x)
        if w:
            w.writerow([trial.number, ok, val] + [P[k] for k in space] + viol + [round(time.time() - t, 3)])
            f.flush()
        if echo_every and trial.number % echo_every == 0:
            print("[trial %d] ok=%s obj=%.4g max_viol=%.3g (%.2fs)" % (trial.number, ok, val, max(viol or [0]), time.time() - t), flush=True)
        return val

    sampler = optuna.samplers.TPESampler(seed=seed)
    study = optuna.create_study(direction="minimize", sampler=sampler)
    study.optimize(obj, n_trials=n_trials)
    if f:
        f.close()
    # 거친 검사를 통과한 해를 좋은 순으로 촘촘한 검사(fine=True)에 다시 넣는다 — 2026-10-30 시험에서 1위가
    # 벽 두께 표본 150개로는 통과, 1500개로는 1.68 mm 였다(최적화가 표본 사이 얇은 곳으로 간다)
    feas = sorted((t for t in study.trials if t.value is not None and all(c <= 0 for c in t.user_attrs["c"])), key=lambda t: t.value)
    for n, t in enumerate(feas[:verify_top]):
        P = dict(P0, **t.params)
        parts = build(P)
        if all(x == 0 for _, _, x in run_reqs(cons, parts, P, fine=True, echo=False)):
            print("[verify] %d번째 후보(trial %d)가 촘촘한 검사 통과 — 앞의 %d개는 탈락" % (n + 1, t.number, n), flush=True)
            return P, parts, study
    print("[verify] 거친 검사 통과 %d개 중 상위 %d개 모두 촘촘한 검사 탈락" % (len(feas), min(verify_top, len(feas))), flush=True)
    return None, None, study
