"""ຕົວສ້າງໂຈດແບບຝຶກຫັດ ແລະ Quiz (ຄຳຕອບຖືກກວດຈາກ engine ຂອງແຕ່ລະຫົວຂໍ້)"""
from fractions import Fraction
from .common import tex, tex_p, txt, mat_tex, poly_tex
from . import determinant, matrix, logic


def _mc(correct, wrongs, rng):
    correct = Fraction(correct)
    ans = txt(correct)
    out = []
    for w in [Fraction(w) for w in wrongs] + [correct + k for k in (1, -1, 2, -2, 3)]:
        s = txt(w)
        if s != ans and s not in out:
            out.append(s)
        if len(out) == 3:
            break
    choices = out + [ans]
    rng.shuffle(choices)
    return choices, ans


def q_arith(rng):
    n, s = rng.sample([2, 3, 4, 5, 6, 8], 2)
    m, r = rng.randint(1, n - 1), rng.randint(1, s - 1)
    a, b = Fraction(m, n), Fraction(r, s)
    if rng.random() < 0.5:
        correct = a + b
        q = f"ຄິດໄລ່ ${tex(a)} + {tex(b)}$"
        wrongs = [Fraction(m + r, n + s), a * b, correct + Fraction(1, n * s)]
        ex = f"ຫາຕົວຫານຮ່ວມກ່ອນ: ${tex(a)} + {tex(b)} = {tex(correct)}$ (ຢ່າບວກຕົວຫານເຂົ້າກັນ)"
    else:
        correct = a * b
        q = rf"ຄິດໄລ່ ${tex(a)} \times {tex(b)}$"
        wrongs = [a + b, a / b, correct + Fraction(1, n * s)]
        ex = rf"ຄູນຕົວເສດກັບຕົວເສດ ແລະ ຕົວຫານກັບຕົວຫານ: ${tex(a)} \times {tex(b)} = {tex(correct)}$"
    ch, ans = _mc(correct, wrongs, rng)
    return {"question": q, "choices": ch, "answer": ans, "explain": ex}


def q_parabola(rng):
    r1, r2 = rng.sample(range(-4, 5), 2)
    a = rng.choice([1, 2, -1, -2, 3])
    b, c = -a * (r1 + r2), a * r1 * r2
    eq = poly_tex(a, b, c)
    if rng.random() < 0.5:
        correct = Fraction(r1 + r2, 2)
        q = f"Parabola $y = {eq}$ ມີຈຸດຍອດຢູ່ທີ່ $x$ ເທົ່າໃດ?"
        wrongs = [-correct, r1 + r2, correct + 1, Fraction(b, a)]
        ex = rf"$x = -\dfrac{{b}}{{2a}} = -\dfrac{{{b}}}{{{2 * a}}} = {tex(correct)}$"
    else:
        correct = Fraction(b * b - 4 * a * c)
        q = f"ຕົວຈຳແນກ $D = b^2 - 4ac$ ຂອງ $y = {eq}$ ມີຄ່າເທົ່າໃດ?"
        wrongs = [b * b + 4 * a * c, 4 * a * c - b * b, b * b - 2 * a * c]
        ex = rf"$D = ({b})^2 - 4({a})({c}) = {tex(correct)}$"
    ch, ans = _mc(correct, wrongs, rng)
    return {"question": q, "choices": ch, "answer": ans, "explain": ex}


def q_ellipse(rng):
    M, m, c = rng.choice([(5, 3, 4), (13, 12, 5), (10, 6, 8), (5, 4, 3), (17, 15, 8),
                          (25, 24, 7), (13, 5, 12), (10, 8, 6)])
    big, small = (M * M, m * m) if rng.random() < 0.5 else (m * m, M * M)
    q = (rf"ຮູບໄຂ່ $\dfrac{{x^2}}{{{big}}} + \dfrac{{y^2}}{{{small}}} = 1$ ມີໂຟກັສຫ່າງຈາກຈຸດສູນກາງ "
         f"ເປັນໄລຍະ $c$ ເທົ່າໃດ?")
    ch, ans = _mc(c, [M - m, M + m, M * M - m * m, m], rng)
    ex = rf"$c^2 = {M * M} - {m * m} = {c * c}$ ດັ່ງນັ້ນ $c = {c}$"
    return {"question": q, "choices": ch, "answer": ans, "explain": ex}


def q_det(rng):
    if rng.random() < 0.6:
        M = [[Fraction(rng.randint(-5, 5)) for _ in range(2)] for _ in range(2)]
        (a, b), (c, d) = M
        wrongs = [a * d + b * c, a * c - b * d, b * c - a * d]
        q = f"ຄິດໄລ່ ${mat_tex(M, 'v')}$"
        ex = rf"$ad - bc = ({tex(a)})({tex(d)}) - ({tex(b)})({tex(c)})$"
    else:
        M = [[Fraction(rng.randint(-3, 3)) for _ in range(3)] for _ in range(3)]
        q = f"ຄິດໄລ່ ${mat_tex(M, 'v')}$"
        ex = "ກະຈາຍຕາມແຖວທີ 1 ດ້ວຍເຄື່ອງໝາຍ + − + ຫຼືໃຊ້ວິທີ Sarrus"
        wrongs = []
    correct = determinant.det(M)
    if not wrongs:
        wrongs = [correct + 1, -correct, correct + 2, correct - 2]
    ch, ans = _mc(correct, wrongs, rng)
    return {"question": q, "choices": ch, "answer": ans, "explain": ex + rf" $= {tex(correct)}$"}


def q_matrix(rng):
    A = [[Fraction(rng.randint(-3, 4)) for _ in range(2)] for _ in range(2)]
    B = [[Fraction(rng.randint(-3, 4)) for _ in range(2)] for _ in range(2)]
    i, j = rng.randint(0, 1), rng.randint(0, 1)
    AB = matrix.multiply(A, B)["result"]
    BA = matrix.multiply(B, A)["result"]
    correct = AB[i][j]
    q = rf"ກຳນົດ $A = {mat_tex(A)}$, $B = {mat_tex(B)}$. ຕຳແໜ່ງ $c_{{{i + 1}{j + 1}}}$ ຂອງ $AB$ ມີຄ່າເທົ່າໃດ?"
    wrongs = [BA[i][j], A[i][j] * B[i][j], A[i][0] * B[0][j]]
    ch, ans = _mc(correct, wrongs, rng)
    terms = " + ".join(f"({tex(A[i][t])})({tex(B[t][j])})" for t in range(2))
    ex = f"$c_{{{i + 1}{j + 1}}} = $ (ແຖວ {i + 1} ຂອງ A) × (ຖັນ {j + 1} ຂອງ B) $= {terms} = {tex(correct)}$"
    return {"question": q, "choices": ch, "answer": ans, "explain": ex}


def q_logic(rng):
    p, q_ = rng.choice([True, False]), rng.choice([True, False])
    f = rng.choice(["p -> q", "p <-> q", "~p | q", "~(p & q)", "p & ~q"])
    tree = logic.parse(f)
    val = logic.evaluate(tree, {"p": p, "q": q_})
    word = lambda b: "ຈິງ (T)" if b else "ເທັດ (F)"
    question = f"ກຳນົດ p ເປັນ **{word(p)}**, q ເປັນ **{word(q_)}**. ປະໂຫຍກ **{logic.to_str(tree)}** ມີຄ່າຄວາມຈິງເປັນຫຍັງ?"
    ex = "ກວດຈາກຕາຕະລາງຄວາມຈິງ: ຄ່າທີ່ໄດ້ຄື **" + word(val) + "**. (ຈື່: p → q ເປັນເທັດ ສະເພາະເມື່ອ p ຈິງ ແລະ q ເທັດ)"
    return {"question": question, "choices": ["ຈິງ (T)", "ເທັດ (F)"], "answer": word(val), "explain": ex}


TOPICS = {
    "ບວກ-ຄູນ (ເສດສ່ວນ)": q_arith,
    "Logic": q_logic,
    "Parabola": q_parabola,
    "Ellipse": q_ellipse,
    "Matrix": q_matrix,
    "Determinant": q_det,
}
