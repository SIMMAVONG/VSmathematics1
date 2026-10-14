import streamlit as st
from engine import determinant
from engine.common import tex
from ui.common import matrix_input, show_steps


def render():
    st.header("⬛ Determinant (ດີເຕີມີແນນ)")
    mode = st.radio("ເລືອກ", ["2×2", "3×3", "ແກ້ລະບົບສົມຜົນ (Cramer's Rule)"], horizontal=True, key="dt_mode")
    if mode in ("2×2", "3×3"):
        n = 2 if mode == "2×2" else 3
        dflt = [[3.0, 1.0], [4.0, 2.0]] if n == 2 else [[2.0, -1.0, 0.0], [1.0, 3.0, 2.0], [0.0, 5.0, -4.0]]
        M = matrix_input("ແກ້ໄຂຄ່າໃນຕາຕະລາງ", n, n, f"dt_M{n}", dflt)
        res = determinant.det2(M) if n == 2 else determinant.det3(M)
        st.latex(rf"\det A = {tex(res['value'])}")
        if res["value"] == 0:
            st.warning("det = 0 → Matrix ນີ້ບໍ່ມີ Inverse")
        with st.expander("🪜 ຂັ້ນຕອນການແກ້", expanded=True):
            show_steps(res["steps"])
    else:
        n = st.radio("ຈຳນວນຕົວແປ", [2, 3], horizontal=True, key="dt_n")
        dA = [[2.0, 1.0], [1.0, -1.0]] if n == 2 else [[1.0, 1.0, 1.0], [0.0, 2.0, 5.0], [2.0, 5.0, -1.0]]
        db = [[5.0], [1.0]] if n == 2 else [[6.0], [-4.0], [27.0]]
        A = matrix_input("ສຳປະສິດ (A)", n, n, f"dt_A{n}", dA)
        bcol = matrix_input("ຄ່າຄົງທີ່ (b)", n, 1, f"dt_b{n}", db)
        res = determinant.cramer(A, [r[0] for r in bcol])
        if res["unique"]:
            names = ["x", "y", "z"]
            st.success("ແກ້ລະບົບໄດ້ຄຳຕອບດຽວ ✅")
            st.latex(r",\ ".join(f"{names[i]} = {tex(v)}" for i, v in enumerate(res["solution"])))
        else:
            st.warning("ລະບົບນີ້ບໍ່ມີຄຳຕອບດຽວ (D = 0)")
        with st.expander("🪜 ຂັ້ນຕອນການແກ້", expanded=True):
            show_steps(res["steps"])
