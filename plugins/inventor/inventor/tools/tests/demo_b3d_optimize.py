"""시험: D형(폭 60, 아래 평평) → 원형 출구로 비스듬히 올라가는 2 mm 덕트를 재료 최소로 (tools/.venv, Inventor 불필요).
변수 R(출구 반지름)·H(높이)·cy(출구 중심 y)·t(단면에서 잰 수평 벽, 안쪽 단면 = 바깥 − t).
기울어진 벽의 실제 두께(법선 방향)는 t·cos(기울기) — 처음에 t = 2 고정으로 두었더니 150회 중 135회가 벽 1.9 미만이었다(45° 면 1.41).
제약: 서포트 없음(45° 오버행 ≤ 1 mm2), 출구 안쪽 면적 ≥ 1600 mm2, 벽 ≥ 1.9 mm, 출구 치우침 cy ≥ 90.
예상: 바깥 위쪽 벽 기울기 (cy+R−50)/H 와 아래쪽 안쪽 벽 (cy−R)/H 가 둘 다 ≤ 1 → R ≈ 25, cy = 90, H ≈ 65 부근
(로프트는 점을 직선으로 잇지 않아 실제 한계는 조금 다름).
"""
import math, os, sys, tempfile, time
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from build123d import BuildLine, BuildSketch, Circle, Line, Plane, Pos, Solid, ThreePointArc, make_face, export_step
from b3d_tools import min_thickness, overhang
from b3d_req import Req, run_reqs, optimize

W, R0 = 60.0, 20.0


def d_wire(z, inset=0.0):
    a = W / 2 - inset
    with BuildSketch(Plane.XY.offset(z)) as s:
        with BuildLine():
            Line((-a, inset), (a, inset)); Line((a, inset), (a, R0))
            ThreePointArc((a, R0), (0, R0 + a), (-a, R0)); Line((-a, R0), (-a, inset))
        make_face()
    return s.sketch.faces()[0].outer_wire()


def c_wire(z, r, cy):
    return (Plane.XY.offset(z) * Pos(0, cy) * Circle(r).face()).outer_wire()


def build(P):
    outer = Solid.make_loft([d_wire(0), c_wire(P["H"], P["R"], P["cy"])])
    inner = Solid.make_loft([d_wire(-0.01, P["t"]), c_wire(P["H"] + 0.01, P["R"] - P["t"], P["cy"])])
    return {"duct": outer - inner}


reqs = [
    Req("R1", "서포트 없음(45° 오버행)", lambda p, P, fine: overhang(p["duct"], 45, tol=0.05 if fine else 0.2)[0], hi=1.0, unit=" mm2"),
    Req("R2", "출구 안쪽 면적", lambda p, P, fine: math.pi * (P["R"] - P["t"]) ** 2, lo=1600, unit=" mm2"),
    Req("R3", "벽 두께", lambda p, P, fine: min_thickness(p["duct"], n=1500 if fine else 150)[0], lo=1.9, unit=" mm"),
    Req("R4", "출구 치우침", lambda p, P, fine: P["cy"], lo=90, unit=" mm"),
]
space = {"R": (15.0, 40.0), "H": (40.0, 200.0), "cy": (60.0, 120.0), "t": (2.0, 3.5)}

if __name__ == "__main__":
    t0 = time.time()
    out = tempfile.mkdtemp(prefix="b3d_opt_")
    P, parts, study = optimize(build, reqs, space, lambda p, P: p["duct"].volume,
                               n_trials=int(sys.argv[1]) if len(sys.argv) > 1 else 150, seed=1,
                               csv_path=os.path.join(out, "trials.csv"))
    print("[t=%.1fs] best %s" % (time.time() - t0, {k: round(v, 2) for k, v in (P or {}).items()}))
    if P:
        print("volume %.0f mm3" % parts["duct"].volume)
        run_reqs(reqs, parts, P, fine=True)          # 촘촘한 표본으로 최종 검증
        export_step(parts["duct"], os.path.join(out, "best.step"))
    print("[t=%.1fs] out=%s" % (time.time() - t0, out))
