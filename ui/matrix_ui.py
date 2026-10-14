import streamlit as st
from engine import matrix
from engine.common import to_fr, tex, mat_tex
from ui.common import matrix_input, show_steps

OPS = ["A + B", "A − B", "k · A", "A × B", "Transpose (Aᵀ)", "Inverse (A⁻¹)"]


def render():
    st.header("🔢 Matrix (ມາຕຣິກ)")
    op = st.selectbox("ເລືອກການດຳເນີນການ", OPS, key="mx_op")
    c1, c2 = st.columns(2)
    if op.startswith("Inverse"):
        n = c1.selectbox("ຂະໜາດ n×n", [2, 3], key="mx_n")
        ra = ca = n
    else:
        ra = int(c1.number_input("ຈຳນວນແຖວຂອງ A", 1, 4, 2, key="mx_ra"))
        ca = int(c2.number_input("ຈຳນວນຖັນຂອງ A", 1, 4, 2, key="mx_ca"))
    A = matrix_input("Matrix A (ແກ້ໄຂຄ່າໃນຕາຕະລາງໄດ້ເລີຍ)", ra, ca, "mx_A")
    B = None
    if op in ("A + B", "A − B"):
        B = matrix_input("Matrix B (ຂະໜາດເທົ່າ A)", ra, ca, "mx_Bs",
                         [[float((i + j) % 3 + 1) for j in range(ca)] for i in range(ra)])
    elif op == "A × B":
        d1, d2 = st.columns(2)
        rb = int(d1.number_input("ຈຳນວນແຖວຂອງ B", 1, 4, ca, key="mx_rb"))
        cb = int(d2.number_input("ຈຳນວນຖັນຂອງ B", 1, 4, 2, key="mx_cb"))
        B = matrix_input("Matrix B", rb, cb, "mx_Bm",
                         [[float((i * 2 + j) % 4 + 1) for j in range(cb)] for i in range(rb)])
    k = None
    if op.startswith("k"):
        k = to_fr(st.number_input("ຄ່າ k", value=2.0, step=1.0, key="mx_k"))
    try:
        if op == "A + B":
            res = matrix.add(A, B, 1)
        elif op == "A − B":
            res = matrix.add(A, B, -1)
        elif op.startswith("k"):
            res = matrix.scalar(k, A)
        elif op == "A × B":
            res = matrix.multiply(A, B)
        elif op.startswith("Transpose"):
            res = matrix.transpose(A)
        else:
            res = matrix.inverse(A)
    except ValueError as e:
        st.error(str(e))
        return
    st.subheader("ຜົນລັບ")
    if res["result"] is None:
        st.warning("Matrix ນີ້ **ບໍ່ມີ Inverse** (det = 0)")
    else:
        st.latex(mat_tex(res["result"]))
    with st.expander("🪜 ຂັ້ນຕອນການແກ້", expanded=True):
        show_steps(res["steps"])
