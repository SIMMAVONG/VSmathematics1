import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from streamlit.testing.v1 import AppTest

PAGES = ["🏠 ໜ້າຫຼັກ", "➕✖️ 1. ບວກ-ຄູນ", "🧠 2. Logic", "📈 3. Parabola", "🥚 4. Ellipse",
         "🔢 5. Matrix", "⬛ 6. Determinant", "📝 ແບບຝຶກຫັດ / Quiz"]


def run_page(name):
    at = AppTest.from_file(str(ROOT / "app.py"), default_timeout=30).run()
    assert not at.exception, at.exception
    at.sidebar.radio[0].set_value(name).run()
    assert not at.exception, (name, at.exception)
    return at


def test_all_pages_render():
    for p in PAGES:
        run_page(p)


def test_parabola_a_zero_shows_error():
    at = run_page("📈 3. Parabola")
    at.slider(key="pa_a").set_value(0.0).run()
    assert not at.exception and len(at.error) == 1


def test_arithmetic_div_zero_error():
    at = run_page("➕✖️ 1. ບວກ-ຄູນ")
    at.text_input(key="ar_b").set_value("0").run()
    at.selectbox(key="ar_op").set_value("÷").run()
    assert not at.exception and len(at.error) == 1


def test_matrix_all_ops():
    at = run_page("🔢 5. Matrix")
    for op in ["A + B", "A − B", "k · A", "A × B", "Transpose (Aᵀ)", "Inverse (A⁻¹)"]:
        at.selectbox(key="mx_op").set_value(op).run()
        assert not at.exception, (op, at.exception)


def test_logic_error_input():
    at = run_page("🧠 2. Logic")
    at.text_input[0].set_value("p &").run()
    assert not at.exception and len(at.error) == 1


def test_practice_flow_and_quiz():
    at = run_page("📝 ແບບຝຶກຫັດ / Quiz")
    at.radio[1].set_value(at.radio[1].options[0]).run()
    at.button[0].click().run()
    assert not at.exception
    at.radio(key="pr_mode").set_value("Quiz 5 ຂໍ້").run()
    assert not at.exception
    at.button[0].click().run()
    assert not at.exception
