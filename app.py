#python -m streamlit run app.py
import streamlit as st

st.set_page_config(page_title="ສື່ການສອນຄະນິດສາດ", page_icon="📐", layout="wide")

from ui import (home, arithmetic_ui, logic_ui, parabola_ui, ellipse_ui,  # noqa: E402
                matrix_ui, determinant_ui, practice_ui)

PAGES = {
    "🏠 ໜ້າຫຼັກ": home.render,
    "➕✖️ 1. ບວກ-ຄູນ": arithmetic_ui.render,
    "🧠 2. Logic": logic_ui.render,
    "📈 3. Parabola": parabola_ui.render,
    "🥚 4. Ellipse": ellipse_ui.render,
    "🔢 5. Matrix": matrix_ui.render,
    "⬛ 6. Determinant": determinant_ui.render,
    "📝 ແບບຝຶກຫັດ / Quiz": practice_ui.render,
}

st.sidebar.title("📐 ເມນູ")
choice = st.sidebar.radio("ເລືອກຫົວຂໍ້", list(PAGES), label_visibility="collapsed")
PAGES[choice]()
