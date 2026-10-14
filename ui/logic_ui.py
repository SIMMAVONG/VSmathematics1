import pandas as pd
import streamlit as st
from engine import logic

EXAMPLES = ["p -> q", "p & q", "p | q", "~(p & q)", "~p | ~q", "p <-> q",
            "(p -> q) <-> (~q -> ~p)", "p | ~p", "(p & q) -> r"]


def render():
    st.header("🧠 Logic (ຕັກກະສາດ)")
    t1, t2 = st.tabs(["📊 ຕາຕະລາງຄວາມຈິງ", "🔁 If-Then: Converse / Contrapositive"])
    with t1:
        st.markdown("ໃຊ້ຕົວແປ **p, q, r, s** ແລະ ເຄື່ອງໝາຍ: `&` ແລະ, `|` ຫຼື, `~` ບໍ່, `->` ຖ້າ…ແລ້ວ, `<->` ກໍຕໍ່ເມື່ອ. "
                    "ຫຼືພິມ `and`, `or`, `not` ກໍໄດ້")
        ex = st.selectbox("ເລືອກຕົວຢ່າງ", EXAMPLES, key="lg_ex")
        expr = st.text_input("ຫຼືພິມສູດເອງ", ex, key=f"lg_expr_{ex}")
        try:
            tt = logic.truth_table(expr)
        except ValueError as e:
            st.error(str(e))
        else:
            st.markdown(f"ສູດ: **{tt['expr']}**")
            st.dataframe(pd.DataFrame(tt["rows"], columns=tt["headers"]), hide_index=True)
            msg = {"tautology": "✅ **Tautology** — ຈິງສະເໝີ ບໍ່ວ່າ p, q ຈະເປັນຫຍັງ",
                   "contradiction": "❌ **Contradiction** — ເທັດສະເໝີ",
                   "contingent": "ℹ️ **Contingency** — ຈິງ ຫຼື ເທັດ ຂຶ້ນກັບຄ່າຂອງຕົວແປ"}[tt["kind"]]
            st.info(msg)
        st.caption("T = ຈິງ (True), F = ເທັດ (False)")
    with t2:
        st.markdown("ຈາກປະໂຫຍກ **ຖ້າ p ແລ້ວ q** (p → q) ສ້າງປະໂຫຍກກ່ຽວຂ້ອງໄດ້ 3 ແບບ:")
        fam = logic.implication_family()
        st.dataframe(pd.DataFrame(fam["rows"], columns=fam["headers"]), hide_index=True)
        st.success("p → q ມີຄ່າຄວາມຈິງ **ເທົ່າກັບ** Contrapositive (¬q → ¬p) ທຸກແຖວ"
                   if fam["contrapositive_equiv"] else "ບໍ່ເທົ່າກັນ")
        st.warning("p → q **ບໍ່ເທົ່າກັບ** Converse (q → p) — ແຕ່ Converse ເທົ່າກັບ Inverse"
                   if not fam["converse_equiv_original"] else "")
        st.markdown("**ຕົວຢ່າງ:** ຖ້າ x = −3 ແລ້ວ x² = 9 (ຈິງ). Converse: ຖ້າ x² = 9 ແລ້ວ x = −3 (**ເທັດ** ເພາະ x ອາດເປັນ 3)")
