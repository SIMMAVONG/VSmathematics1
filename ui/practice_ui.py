import random
import streamlit as st
from engine import practice

TOPICS = practice.TOPICS


def render():
    st.header("📝 ແບບຝຶກຫັດ ແລະ Quiz")
    mode = st.radio("ໂໝດ", ["ຝຶກຫັດທີລະຂໍ້", "Quiz 5 ຂໍ້"], horizontal=True, key="pr_mode")
    topics = st.multiselect("ຫົວຂໍ້", list(TOPICS), default=list(TOPICS), key="pr_topics")
    if not topics:
        st.info("ເລືອກຢ່າງໜ້ອຍ 1 ຫົວຂໍ້")
        return
    _practice(topics) if mode.startswith("ຝຶກ") else _quiz(topics)


def _practice(topics):
    ss = st.session_state
    ss.setdefault("pr_seed", random.randrange(10**6))
    ss.setdefault("pr_right", 0)
    ss.setdefault("pr_total", 0)
    seed = ss["pr_seed"]
    rng = random.Random(seed)
    topic = rng.choice(topics)
    q = TOPICS[topic](rng)
    st.caption(f"ຫົວຂໍ້: {topic}  •  ຄະແນນ: {ss['pr_right']} / {ss['pr_total']}")
    st.markdown(q["question"])
    choice = st.radio("ເລືອກຄຳຕອບ", q["choices"], index=None, key=f"pr_choice_{seed}")
    done_key = f"pr_done_{seed}"
    c1, c2 = st.columns(2)
    if c1.button("✅ ກວດຄຳຕອບ", key=f"pr_chk_{seed}"):
        if choice is None:
            st.warning("ເລືອກຄຳຕອບກ່ອນ")
        elif done_key not in ss:
            ss[done_key] = choice == q["answer"]
            ss["pr_total"] += 1
            ss["pr_right"] += int(ss[done_key])
    if done_key in ss:
        if ss[done_key]:
            st.success("ຖືກຕ້ອງ! 🎉")
        else:
            st.error(f"ຍັງບໍ່ຖືກ — ຄຳຕອບທີ່ຖືກຄື **{q['answer']}**")
        st.markdown("💡 " + q["explain"])
    if c2.button("➡️ ຂໍ້ຕໍ່ໄປ", key=f"pr_next_{seed}"):
        ss["pr_seed"] = random.randrange(10**6)
        st.rerun()


def _quiz(topics):
    ss = st.session_state
    ss.setdefault("qz_seed", random.randrange(10**6))
    seed = ss["qz_seed"]
    rng = random.Random(seed)
    qs = [TOPICS[rng.choice(topics)](rng) for _ in range(5)]
    done = ss.get(f"qz_done_{seed}", False)
    with st.form(f"quiz_{seed}"):
        for i, q in enumerate(qs):
            st.markdown(f"**ຂໍ້ {i + 1}.** {q['question']}")
            st.radio("ຄຳຕອບ", q["choices"], index=None, key=f"qz_{seed}_{i}", disabled=done)
        sent = st.form_submit_button("📤 ສົ່ງຄຳຕອບ", disabled=done)
    if sent:
        ss[f"qz_done_{seed}"] = True
        st.rerun()
    if done:
        score = sum(ss.get(f"qz_{seed}_{i}") == q["answer"] for i, q in enumerate(qs))
        st.subheader(f"ຄະແນນ: {score} / 5")
        (st.success if score >= 4 else st.info if score >= 3 else st.warning)(
            "ເກັ່ງຫຼາຍ! 🌟" if score >= 4 else "ດີ — ທົບທວນຂໍ້ທີ່ຜິດອີກຄັ້ງ" if score >= 3 else "ສູ້ໆ — ລອງຝຶກຫັດຕື່ມ")
        for i, q in enumerate(qs):
            ok = ss.get(f"qz_{seed}_{i}") == q["answer"]
            st.markdown(f"{'✅' if ok else '❌'} **ຂໍ້ {i + 1}** — ຄຳຕອບທີ່ຖືກ: **{q['answer']}**  \n💡 {q['explain']}")
    if st.button("🔄 ເຮັດ Quiz ໃໝ່", key=f"qz_new_{seed}"):
        ss["qz_seed"] = random.randrange(10**6)
        st.rerun()
