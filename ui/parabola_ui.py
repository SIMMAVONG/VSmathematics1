import streamlit as st
from engine import parabola
from ui import plots
from ui.common import show_steps, show_summary


def render():
    st.header("📈 Parabola (ພາຣາໂບລາ)")
    st.latex(r"y = ax^2 + bx + c")
    c1, c2 = st.columns([1, 2])
    with c1:
        a = st.slider("a", -5.0, 5.0, 1.0, 0.5, key="pa_a")
        b = st.slider("b", -10.0, 10.0, -2.0, 0.5, key="pa_b")
        c = st.slider("c", -10.0, 10.0, -3.0, 0.5, key="pa_c")
    try:
        res = parabola.analyze(a, b, c)
    except ValueError as e:
        c2.error(str(e))
        return
    c2.plotly_chart(plots.parabola_fig(res), key="pa_fig")
    t1, t2, t3 = st.tabs(["📋 ຜົນລັບ", "🪜 ຂັ້ນຕອນການແກ້", "💡 ຂໍ້ສັງເກດ"])
    with t1:
        show_summary(res["summary"])
    with t2:
        show_steps(res["steps"])
    with t3:
        st.markdown("""
- **a** ກຳນົດທິດ ແລະ ຄວາມແຄບ: a > 0 ເປີດຂຶ້ນ, a < 0 ເປີດລົງ, |a| ຫຼາຍ ຍິ່ງແຄບ
- **c** ຄືຈຸດທີ່ກຣາຟຕັດແກນ y
- **D = b² − 4ac** ບອກຈຳນວນຮາກ: D > 0 ສອງຮາກ, D = 0 ຮາກດຽວ, D < 0 ບໍ່ມີຮາກຈິງ
- ລອງເລື່ອນ **c** ຂຶ້ນ/ລົງ ແລ້ວສັງເກດ D ປ່ຽນຈາກ > 0 → 0 → < 0
""")
