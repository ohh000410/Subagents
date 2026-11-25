"""실측 시험(수동): build123d 로 단계마다 step_check → STEP → Inventor 가져오기(.ipt) → 체적 대조.
tools/.venv 로 실행. Inventor 가 떠 있으면 거부. 끝나면 자기 PID 0 확인, 출력은 임시 폴더(끝에 경로 출력).
"""
import math, os, sys, tempfile, time
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from build123d import Box, Cylinder, Pos, export_step
from b3d_tools import state, interference_mm3, overhang, step_to_ipt
from step_check import step_check, step_summary
from inventor_session import launch, kill_own

t0 = time.time()
out = tempfile.mkdtemp(prefix="b3d_ipt_")
res = []
part = Box(40, 30, 10)                                   # 중심 원점 → z -5..5
res.append(step_check("base box", state(None), state(part), exp_dV_cm3=40 * 30 * 10 / 1000,
                      exp_bbox=(-2, -1.5, -0.5, 2, 1.5, 0.5)))
s = state(part)
part = part - Pos(10, 0, 0) * Cylinder(3, 10)            # 관통 구멍
res.append(step_check("hole", s, state(part), exp_dV_cm3=-math.pi * 9 * 10 / 1000))
s = state(part)
part = part + Pos(-10, 0, 10) * Cylinder(5, 10)          # 위에 기둥 (z 5..15)
res.append(step_check("boss", s, state(part), exp_dV_cm3=math.pi * 25 * 10 / 1000))
print(step_summary(res))
print("interference boss vs hole-cylinder: %.3f mm3" % interference_mm3(Pos(-10, 0, 10) * Cylinder(5, 10), Pos(10, 0, 0) * Cylinder(3, 10)))
print("overhang: %.2f mm2" % overhang(part)[0])
step = os.path.join(out, "part.step")
export_step(part, step)
v_b3d = part.volume / 1000
print("[t=%.1fs] b3d done, V=%.6f cm3" % (time.time() - t0, v_b3d), flush=True)

app, pid = launch()
doc = None
try:
    print("[t=%.1fs] inventor up pid=%d" % (time.time() - t0, pid), flush=True)
    doc, v_inv = step_to_ipt(app, step, os.path.join(out, "part.ipt"))
    print("[t=%.1fs] imported V=%.6f cm3, rel err %.2e" % (time.time() - t0, v_inv, abs(v_inv - v_b3d) / v_b3d), flush=True)
finally:
    if doc is not None:
        doc.Close(True)
    app.Quit()
    kill_own(pid)
print("[t=%.1fs] done out=%s files=%s" % (time.time() - t0, out, sorted(os.listdir(out))))
