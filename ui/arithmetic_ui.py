import streamlit as st
from engine import arithmetic
from engine.common import parse_fr, tex, dec
from ui import plots
from ui.common import show_steps


def render():
    st.header("➕✖️ ການບວກ ແລະ ການຄູນ")
    st.caption("ໃສ່ຈຳນວນເຕັມ, ທົດສະນິຍົມ ຫຼື ເສດສ່ວນ ເຊັ່ນ 3, -2, 0.75, 3/5")
    t1, t2 = st.tabs(["🧮 ເສດສ່ວນ + − × ÷", "🔍 ຄຸນສົມບັດ ແລະ ສູດ"])
    with t1:
        c1, c2, c3 = st.columns([2, 1, 2])
        a_txt = c1.text_input("ຈຳນວນ a", "3/4", key="ar_a")
        op = c2.selectbox("ເຄື່ອງໝາຍ", ["+", "-", "×", "÷"], key="ar_op")
        b_txt = c3.text_input("ຈຳນວນ b", "5/6", key="ar_b")
        try:
            a, b = parse_fr(a_txt), parse_fr(b_txt)
            res = arithmetic.operate(a, b, op)
        except ValueError as e:
            st.error(str(e))
        else:
            st.latex(res["equation"])
            if op in ("+", "-"):
                st.plotly_chart(plots.number_line_fig({"a": a, "b": b, "ຜົນ": res["result"]}), key="ar_nl")
            with st.expander("🪜 ຂັ້ນຕອນການແກ້", expanded=True):
                show_steps(res["steps"])
    with t2:
        c1, c2, c3 = st.columns(3)
        try:
            a = parse_fr(c1.text_input("a", "2", key="ar_pa"))
            b = parse_fr(c2.text_input("b", "-3", key="ar_pb"))
            c = parse_fr(c3.text_input("c", "1/2", key="ar_pc"))
        except ValueError as e:
            st.error(str(e))
            return
        st.subheader("ຄຸນສົມບັດຂອງການບວກ ແລະ ຄູນ")
        for r in arithmetic.properties(a, b, c):
            st.markdown(f"**{r['name']}**: ${r['lhs']} = {tex(r['lv'])}$ ແລະ ${r['rhs']} = {tex(r['rv'])}$ → "
                        + ("✅ ເທົ່າກັນ" if r["ok"] else "❌"))
        st.subheader("ສູດຄູນພິເສດ (ໃຊ້ a ແລະ b)")
        for r in arithmetic.identities(a, b):
            st.markdown(f"${r['lhs']} = {tex(r['lv'])}$ ແລະ ${r['rhs']} = {tex(r['rv'])}$ → "
                        + ("✅ ເທົ່າກັນ" if r["ok"] else "❌"))
