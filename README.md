# 📐 ສື່ການສອນຄະນິດສາດ (Streamlit)

ເຄື່ອງມືຊ່ວຍສອນຄະນິດສາດ ມ.4–ມ.7: ບວກ-ຄູນ, Logic, Parabola, Ellipse, Matrix, Determinant + ແບບຝຶກຫັດ/Quiz

## 1) ຣັນໃນເຄື່ອງ (VS Code)
ເປີດໂຟນເດີ `math_app` ໃນ VS Code → ເປີດ Terminal ແລ້ວພິມ:

```bash
pip install -r requirements.txt
streamlit run app.py
```
ໜ້າເວັບຈະເປີດທີ່ http://localhost:8501

## 2) ທົດສອບ
```bash
pip install pytest
python -m pytest tests -q
```

## 3) ໂຄງສ້າງ
```
app.py          ໜ້າຫຼັກ + ເມນູ
engine/         ສະໝອງຄຳນວນ (Python ລ້ວນ, ບໍ່ຜູກກັບ Streamlit, ທົດສອບງ່າຍ)
ui/             ໜ້າຈໍຂອງແຕ່ລະຫົວຂໍ້ + ກຣາຟ
tests/          pytest (engine) + AppTest (ເປີດທຸກໜ້າກວດ error)
```
ເພີ່ມຫົວຂໍ້ໃໝ່: ສ້າງ `engine/xxx.py` (ຮັບຄ່າ → ສົ່ງ dict ທີ່ມີ `steps`, `summary`) + `ui/xxx_ui.py`
ທີ່ມີຟັງຊັນ `render()` ແລ້ວເພີ່ມໃສ່ `PAGES` ໃນ `app.py`.
ເພີ່ມໂຈດແບບຝຶກຫັດ: ຂຽນຟັງຊັນ `q_xxx(rng)` ໃນ `engine/practice.py` ແລ້ວເພີ່ມໃສ່ `TOPICS`.

## 4) Deploy ຜ່ານ GitHub + Streamlit Community Cloud
1. ສ້າງ repository ໃໝ່ໃນ GitHub (ເຊັ່ນ `math-teaching-app`)
2. ໃນ Terminal ຂອງໂຟນເດີ `math_app`:
```bash
git init
git add .
git commit -m "first version"
git branch -M main
git remote add origin https://github.com/<ຊື່ຜູ້ໃຊ້>/math-teaching-app.git
git push -u origin main
```
3. ເຂົ້າ https://share.streamlit.io → ລັອກອິນດ້ວຍ GitHub → **Create app** (ຫຼື New app)
4. ເລືອກ repository, branch = `main`, Main file path = `app.py` → **Deploy**
5. ໄດ້ລິ້ງ `https://<ຊື່>.streamlit.app` ສົ່ງໃຫ້ນັກຮຽນເປີດໄດ້ທັງມືຖື ແລະ ຄອມ
6. ເວລາແກ້ code: `git add . && git commit -m "..." && git push` — ແອັບຈະອັບເດດເອງ

ໝາຍເຫດ: ໜ້າຕາຂອງເວັບ Streamlit Cloud ອາດປ່ຽນເລັກນ້ອຍ — ຖ້າຊື່ປຸ່ມຕ່າງກັນ ໃຫ້ຫາປຸ່ມສ້າງແອັບໃໝ່.
ແອັບຟຣີອາດ "ນອນ" ຫຼັງບໍ່ມີຄົນໃຊ້ໄລຍະໜຶ່ງ — ກົດປຸ່ມປຸກ ແລ້ວລໍຖ້າສອງສາມວິນາທີ.
