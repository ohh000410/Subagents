"""build123d 모델링 헬퍼 — 형상 반복은 build123d(OCCT, 창·기동 없음), 최종 .ipt·도면은 Inventor.

실행: tools/.venv (build123d + pywin32, requirements.txt). 판정은 Inventor 와 같은 step_check 를 쓴다.
    from b3d_tools import state, interference_mm3, overhang, step_to_ipt
    from step_check import step_check, step_summary
    s0 = state(None); s1 = state(part)            # (cm3, 면 수, bbox cm) — step_check 단위
    r = step_check("base", s0, s1, exp_dV_cm3=..., exp_bbox=...)
근거(2026-10-30 실측): 로프트+2 mm 벽·간섭·체적·내보내기가 0.2초, 홈 1000개 0.8초
(Inventor 는 기동만 7~12초, 여러 단계 부품이 단계마다 4~11분, Shell 은 15분 멈춤).
"""


def state(shape):
    """step_check 입력 (체적 cm3, 면 수, bbox cm 6개). None = 빈 상태."""
    if shape is None:
        return 0.0, 0, None
    bb = shape.bounding_box()
    return (shape.volume / 1000.0, len(shape.faces()),
            tuple(v / 10.0 for v in (bb.min.X, bb.min.Y, bb.min.Z, bb.max.X, bb.max.Y, bb.max.Z)))


def interference_mm3(a, b):
    """두 형상이 겹치는 체적(mm3). 0 이면 간섭 없음."""
    common = a & b
    return common.volume if common is not None else 0.0


def overhang(shape, max_deg=45.0, tol=0.05):
    """FDM 오버행: 아래를 향한 면 중 수평에서 max_deg 보다 눕은 삼각형 면적(mm2) — 바닥(z 최소)에 닿은 면은 뺌.
    반환 (면적 mm2, 그 중심 z 목록 일부). 면 법선은 곡면이라 면 하나로 못 봄 → 삼각형으로."""
    import math
    verts, tris = shape.tessellate(tol)
    zmin = shape.bounding_box().min.Z
    lim = -math.cos(math.radians(max_deg))   # 법선 z 가 이보다 작으면(더 아래를 향하면) 오버행
    area, zs = 0.0, []
    for i, j, k in tris:
        a, b, c = verts[i], verts[j], verts[k]
        n = (b - a).cross(c - a)
        L = n.length
        if L == 0:
            continue
        cz = (a.Z + b.Z + c.Z) / 3
        if n.Z / L < lim and cz > zmin + 1e-3:
            area += L / 2
            zs.append(round(cz, 2))
    return area, sorted(set(zs))[:10]


def min_thickness(shape, n=300, tol=0.1):
    """최소 벽 두께(mm)와 그 위치. 표면 삼각형 n 개(고르게 건너뛰며)마다 바깥에서 법선 반대로 직선을 쏴
    들어가는 점과 나오는 점 사이 거리. 표본 사이의 더 얇은 곳은 놓칠 수 있다 → 최종 검증은 n 을 키움.
    삼각형 중심은 곡면보다 최대 tol 안쪽이라, 중심에서 바로 쏘면 자기 면을 0.005 mm 로 잡았다(2026-10-30) → 3·tol 바깥에서 쏨."""
    from build123d import Axis
    verts, tris = shape.tessellate(tol)
    step = max(1, len(tris) // n)
    best, where = float("inf"), None
    for i, j, k in tris[::step]:
        a, b, c = verts[i], verts[j], verts[k]
        nrm = (b - a).cross(c - a)
        if nrm.length == 0:
            continue
        nrm = nrm.normalized()
        p = (a + b + c) / 3 + nrm * (3 * tol)
        ds = sorted(d for d in ((q - p).dot(-nrm) for q, _ in shape.find_intersection_points(Axis(p, -nrm))) if d > 0)
        if len(ds) >= 2 and ds[1] - ds[0] < best:
            best, where = ds[1] - ds[0], (round(p.X, 2), round(p.Y, 2), round(p.Z, 2))
    return best, where


def step_to_ipt(app, step_path, ipt_path):
    """Inventor 에서 STEP 를 열어 .ipt 로 저장하고 (part_doc, 체적 cm3) 반환. 피처 트리 없이 바디 하나.
    app = inventor_session.launch() 로 띄운 자기 세션. 문서 닫기는 호출한 쪽 finally 에서 Close(True)."""
    from step_check import read_volume_cm3
    doc = app.Documents.Open(str(step_path), True)
    doc.SaveAs(str(ipt_path), False)
    return doc, read_volume_cm3(doc)
