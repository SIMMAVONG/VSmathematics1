import pandas as pd
import streamlit as st
from engine.common import to_fr


def show_steps(steps):
    for i, s in enumerate(steps, 1):
        st.markdown(f"**ຂັ້ນທີ {i}. {s['title']}**")
        if s.get("text"):
            st.markdown(s["text"])
        ls = s.get("latex") or []
        if isinstance(ls, str):
            ls = [ls]
        for ltx in ls:
            st.latex(ltx)


def show_summary(summary):
    for label, value, is_latex in summary:
        if is_latex:
            st.markdown(f"- **{label}:** ${value}$")
        else:
            st.markdown(f"- **{label}:** {value}")


def matrix_input(label, rows, cols, key, default=None):
    """ຕາຕະລາງໃຫ້ແກ້ໄຂຄ່າໄດ້ ແລ້ວສົ່ງຄືນ list ຂອງ Fraction"""
    st.caption(label)
    if default is None:
        default = [[float((i * cols + j) % 5 + 1) for j in range(cols)] for i in range(rows)]
    df = pd.DataFrame(default, columns=[str(j + 1) for j in range(cols)],
                      index=[str(i + 1) for i in range(rows)], dtype=float)
    edited = st.data_editor(df, key=f"{key}_{rows}x{cols}", num_rows="fixed")
    vals = edited.fillna(0).values.tolist()
    return [[to_fr(v) for v in row] for row in vals]
