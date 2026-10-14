import random
import sys
from pathlib import Path
from fractions import Fraction as F

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import pytest
from engine import parabola, ellipse, determinant, matrix, arithmetic, logic, practice
from engine.common import to_fr


def M(rows):
    return [[to_fr(x) for x in r] for r in rows]


def V(xs):
    return [to_fr(x) for x in xs]


def test_parabola_basic():
    r = parabola.analyze(1, -2, -3)
    assert r["D"] == 16 and (r["h"], r["k"]) == (1, -4)
    assert r["roots_f"] == [-1.0, 3.0] and r["focus"] == (1, F(-15, 4)) and r["directrix"] == F(-17, 4)


def test_parabola_cases():
    assert parabola.analyze(1, -2, 1)["root_type"] == "one"
    assert parabola.analyze(1, 0, 1)["root_type"] == "none"
    assert len(parabola.analyze(1, 0, -2)["roots_f"]) == 2
    with pytest.raises(ValueError):
        parabola.analyze(0, 1, 1)


def test_ellipse():
    r = ellipse.analyze(5, 3)
    assert r["c_f"] == 4.0 and r["e_f"] == 0.8 and r["horizontal"]
    assert ellipse.analyze(3, 5)["horizontal"] is False
    assert ellipse.analyze(4, 4)["circle"]
    assert ellipse.locate_point(r, 5, 0)["status"] == "on"
    assert ellipse.locate_point(r, 0, 0)["status"] == "inside"
    assert ellipse.locate_point(r, 6, 0)["status"] == "outside"
    with pytest.raises(ValueError):
        ellipse.analyze(0, 3)


def test_determinant_and_cramer():
    assert determinant.det2(M([[3, 1], [4, 2]]))["value"] == 2
    assert determinant.det3(M([[2, -1, 0], [1, 3, 2], [0, 5, -4]]))["value"] == -48
    res = determinant.cramer(M([[2, 1], [1, -1]]), V([5, 1]))
    assert res["solution"] == [2, 1]
    res3 = determinant.cramer(M([[1, 1, 1], [0, 2, 5], [2, 5, -1]]), V([6, -4, 27]))
    assert res3["solution"] == [5, 3, -2]
    assert determinant.cramer(M([[1, 2], [2, 4]]), V([1, 2]))["unique"] is False


def test_matrix():
    A, B = M([[1, 2], [3, 4]]), M([[0, 1], [1, 0]])
    assert matrix.multiply(A, B)["result"] == M([[2, 1], [4, 3]])
    assert matrix.add(A, B, -1)["result"] == M([[1, 1], [2, 4]])
    assert matrix.transpose(A)["result"] == M([[1, 3], [2, 4]])
    inv = matrix.inverse(A)["result"]
    assert matrix.multiply(A, inv)["result"] == matrix.identity(2)
    A3 = M([[1, 2, 3], [4, 5, 1], [2, 3, 4]])
    assert matrix.multiply(A3, matrix.inverse(A3)["result"])["result"] == matrix.identity(3)
    assert matrix.inverse(M([[1, 2], [2, 4]]))["result"] is None
    with pytest.raises(ValueError):
        matrix.multiply(M([[1, 2, 3]]), M([[1, 2]]))
    with pytest.raises(ValueError):
        matrix.add(A, M([[1, 2, 3]]))


def test_arithmetic():
    assert arithmetic.operate("3/4", "5/6", "+")["result"] == F(19, 12)
    assert arithmetic.operate("3/4", "5/6", "-")["result"] == F(-1, 12)
    assert arithmetic.operate("2/3", "9/4", "×")["result"] == F(3, 2)
    assert arithmetic.operate(2, "-3/4", "÷")["result"] == F(-8, 3)
    with pytest.raises(ValueError):
        arithmetic.operate(1, 0, "÷")
    assert all(r["ok"] for r in arithmetic.properties(2, -3, F(1, 2)))
    assert all(r["ok"] for r in arithmetic.identities(F(1, 3), 7))


def test_logic():
    assert logic.truth_table("p -> q")["rows"][1] == ["T", "F", "F"]
    assert logic.truth_table("p | ~p")["kind"] == "tautology"
    assert logic.truth_table("p & ~p")["kind"] == "contradiction"
    assert logic.truth_table("(p -> q) <-> (~q -> ~p)")["kind"] == "tautology"
    assert logic.truth_table("p and not q")["kind"] == "contingent"
    assert logic.truth_table("p ∧ q → p")["kind"] == "tautology"
    for bad in ["", "p &", "(p", "pq", "p $ q"]:
        with pytest.raises(ValueError):
            logic.truth_table(bad)
    fam = logic.implication_family()
    assert fam["contrapositive_equiv"] and fam["converse_equiv_inverse"] and not fam["converse_equiv_original"]


def test_practice_generators():
    for seed in range(200):
        rng = random.Random(seed)
        for name, gen in practice.TOPICS.items():
            q = gen(rng)
            assert q["answer"] in q["choices"] and len(set(q["choices"])) == len(q["choices"]), name
