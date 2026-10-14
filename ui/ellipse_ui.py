import streamlit as st
from engine import ellipse
from engine.common import tex
from ui import plots
from ui.common import show_steps, show_summary


def render():
    st.header("🥚 Ellipse (ຮູບໄຂ່)")
    st.latex(r"\dfrac{(x-h)^2}{a^2} + \dfrac{(y-k)^2}{b^2} = 1")
    c1, c2 = st.columns([1, 2])
    with c1:
        a = st.slider("a (ກິ່ງແກນແນວ x)", 0.5, 10.0, 5.0, 0.5, key="el_a")
        b = st.slider("b (ກິ່ງແກນແນວ y)", 0.5, 10.0, 3.0, 0.5, key="el_b")
        h = st.slider("h (ສູນກາງ x)", -5.0, 5.0, 0.0, 0.5, key="el_h")
        k = st.slider("k (ສູນກາງ y)", -5.0, 5.0, 0.0, 0.5, key="el_k")
    try:
        res = ellipse.analyze(a, b, h, k)
    except ValueError as e:
        c2.error(str(e))
        return
    t1, t2, t3 = st.tabs(["📋 ຜົນລັບ", "🪜 ຂັ້ນຕອນການແກ້", "📍 ກວດຈຸດ"])
    fig = plots.ellipse_fig(res)
    with t3:
        p1, p2 = st.columns(2)
        x0 = p1.number_input("x ຂອງຈຸດ P", value=3.0, step=0.5, key="el_x0")
        y0 = p2.number_input("y ຂອງຈຸດ P", value=1.0, step=0.5, key="el_y0")
        loc = ellipse.locate_point(res, x0, y0)
        st.latex(rf"\dfrac{{({tex(x0)}-{tex(res['h'])})^2}}{{{tex(res['a'] ** 2)}}} + "
                 rf"\dfrac{{({tex(y0)}-{tex(res['k'])})^2}}{{{tex(res['b'] ** 2)}}} = {tex(loc['value'])}")
        {"on": st.success, "inside": st.info, "outside": st.warning}[loc["status"]](
            {"on": "ຄ່າ = 1 → ຈຸດ P ຢູ່ **ເທິງ** ຮູບໄຂ່",
             "inside": "ຄ່າ < 1 → ຈຸດ P ຢູ່ **ພາຍໃນ** ຮູບໄຂ່",
             "outside": "ຄ່າ > 1 → ຈຸດ P ຢູ່ **ພາຍນອກ** ຮູບໄຂ່"}[loc["status"]])
        fig = plots.point_on_ellipse(fig, float(x0), float(y0), loc["status"])
    c2.plotly_chart(fig, key="el_fig")
    with t1:
        show_summary(res["summary"])
    with t2:
        show_steps(res["steps"])
