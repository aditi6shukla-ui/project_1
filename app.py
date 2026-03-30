 </div>
  <hr class="divider"/>
  <div class="badge">✅ Python Basics Mastered</div>
  <div class="footer">
    Issued on {date_str} &nbsp;|&nbsp; Python Coding Adventure &nbsp;|&nbsp; Powered by Streamlit
  </div>
</div>
</body>
</html>"""


def get_download_link(html: str, filename: str, label: str) -> str:
    b64 = base64.b64encode(html.encode()).decode()
    href = f'<a href="data:text/html;base64,{b64}" download="{filename}" style="text-decoration:none;">'
    button_html = (
        f'{href}<div class="stButton"><button style="'
        f'background:#00FF41;color:#000;font-family:Space Mono,monospace;'
        f'font-weight:700;border:2px solid #000;border-radius:8px;'
        f'box-shadow:4px 4px 0 #000;padding:0.6rem 1.4rem;cursor:pointer;'
        f'font-size:0.85rem;">{label}</button></div></a>'
    )
    return button_html


# ============================================================
# SIDEBAR
# ============================================================
def render_sidebar():
    xp = st.session_state.xp
    title, icon = get_character_info(xp)
    progress = xp_to_progress(xp)
    completed = len(st.session_state.completed_levels)
    max_xp = sum(v["xp_reward"] for v in LEVELS.values())

    with st.sidebar:
        st.markdown(
            '<p class="pixel-font" style="font-size:0.55rem;color:#00FF41;'
            'text-align:center;letter-spacing:0.2em;">PYTHON ADVENTURE</p>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div style="text-align:center;padding:0.8rem 0;">'
            f'<div style="font-size:3rem;">{icon}</div>'
            f'<div style="font-family:Space Mono,monospace;font-size:0.9rem;color:#fff;'
            f'font-weight:700;">{title}</div>'
            f'<div style="font-size:0.75rem;color:#888;margin-top:0.2rem;">Your Character</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

        st.markdown("---")

        # XP Bar
        st.markdown(
            f'<div class="stat-row"><span style="color:#888">XP</span>'
            f'<span class="xp-badge">{xp} / {max_xp}</span></div>',
            unsafe_allow_html=True,
        )
        st.progress(progress)

        st.markdown(
            f'<div class="stat-row"><span style="color:#888">Levels Done</span>'
            f'<span style="color:#00FF41;font-family:Space Mono,monospace;">'
            f'{completed} / 5</span></div>',
            unsafe_allow_html=True,
        )

        st.markdown("---")
        st.markdown(
            '<p style="font-family:Space Mono,monospace;font-size:0.7rem;'
            'color:#666;margin-bottom:0.5rem;">LEVEL MAP</p>',
            unsafe_allow_html=True,
        )

        for lvl_id, lvl in LEVELS.items():
            status = level_status(lvl_id)
            status_icon = "✅" if status == "done" else ("🔓" if status == "unlocked" else "🔒")
            color = "#00FF41" if status == "done" else ("#E8E8E8" if status == "unlocked" else "#555")
            st.markdown(
                f'<div style="display:flex;align-items:center;gap:0.5rem;'
                f'padding:0.3rem 0;font-size:0.75rem;">'
                f'<span>{status_icon}</span>'
                f'<span style="color:{color};font-family:Space Mono,monospace;">'
                f'L{lvl_id}: {lvl["subtitle"]}</span></div>',
                unsafe_allow_html=True,
            )

        st.markdown("---")
        if st.button("🏠 Adventure Hub", use_container_width=True):
            st.session_state.view = "hub"
            st.rerun()


# ============================================================
# HUB VIEW
# ============================================================
def render_hub():
    st.markdown(
        '<h1 class="neon-heading" style="font-size:1.6rem;margin-bottom:0.2rem;">'
        '🐍 Python Coding Adventure</h1>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<p style="color:#888;font-family:Space Mono,monospace;font-size:0.78rem;">'
        'Choose your next mission. Complete levels in order to unlock new challenges.</p>',
        unsafe_allow_html=True,
    )
    st.markdown("<hr class='divider'/>", unsafe_allow_html=True)

    cols = st.columns(3)
    level_ids = list(LEVELS.keys())

    for i, lvl_id in enumerate(level_ids):
        lvl = LEVELS[lvl_id]
        status = level_status(lvl_id)
        col = cols[i % 3]

        with col:
            border_color = (
                "#00FF41" if status == "done"
                else (lvl["color"] if status == "unlocked" else "#2A2A2A")
            )
            shadow = (
                "4px 4px 0 #00FF41" if status == "done"
                else ("4px 4px 0 #000" if status == "unlocked" else "none")
            )
            opacity = "1" if status != "locked" else "0.4"

            status_label = "✅ COMPLETE" if status == "done" else ("▶ PLAY" if status == "unlocked" else "🔒 LOCKED")
            label_color = "#00FF41" if status == "done" else ("#fff" if status == "unlocked" else "#555")

            score_html = ""
            if lvl_id in st.session_state.quiz_state:
                qs = st.session_state.quiz_state[lvl_id]
                if qs.get("submitted"):
                    sc = qs.get("score", 0)
                    score_html = f'<div style="font-size:0.7rem;color:#888;margin-top:0.3rem;">Score: {sc}/3 ⭐</div>'

            st.markdown(
                f'<div style="background:#181818;border:2px solid {border_color};'
                f'border-radius:8px;padding:1.2rem;box-shadow:{shadow};'
                f'text-align:center;margin-bottom:0.8rem;opacity:{opacity};">'
                f'<div style="font-size:2.2rem;margin-bottom:0.4rem;">{lvl["pixel_art"]}</div>'
                f'<div style="font-family:Space Mono,monospace;font-size:0.65rem;'
                f'color:{border_color};letter-spacing:0.2em;">LEVEL {lvl_id}</div>'
                f'<div style="font-family:Space Mono,monospace;font-size:0.82rem;'
                f'color:#fff;font-weight:700;margin:0.3rem 0;">{lvl["title"]}</div>'
                f'<div style="font-size:0.72rem;color:#888;margin-bottom:0.6rem;">{lvl["subtitle"]}</div>'
                f'<div style="font-family:Space Mono,monospace;font-size:0.65rem;'
                f'color:{label_color};">{status_label}</div>'
                f'{score_html}'
                f'</div>',
                unsafe_allow_html=True,
            )

            if status != "locked":
                btn_label = "Review" if status == "done" else "Start Level"
                if st.button(btn_label, key=f"hub_btn_{lvl_id}", use_container_width=True):
                    st.session_state.view = "level"
                    st.session_state.current_level = lvl_id
                    st.rerun()

    # Stats row
    st.markdown("<hr class='divider'/>", unsafe_allow_html=True)
    m1, m2, m3, m4 = st.columns(4)
    xp = st.session_state.xp
    title, icon = get_character_info(xp)
    max_xp = sum(v["xp_reward"] for v in LEVELS.values())

    with m1:
        st.markdown(
            f'<div class="card" style="text-align:center;padding:1rem;">'
            f'<div style="font-size:1.8rem;">{icon}</div>'
            f'<div style="font-family:Space Mono,monospace;font-size:0.75rem;color:#00FF41;">{title}</div>'
            f'<div style="font-size:0.7rem;color:#888;">Rank</div></div>',
            unsafe_allow_html=True,
        )
    with m2:
        st.markdown(
            f'<div class="card" style="text-align:center;padding:1rem;">'
            f'<div style="font-family:Space Mono,monospace;font-size:1.6rem;color:#fff;">{xp}</div>'
            f'<div style="font-family:Space Mono,monospace;font-size:0.75rem;color:#9D46FF;">XP Earned</div>'
            f'<div style="font-size:0.7rem;color:#888;">of {max_xp} total</div></div>',
            unsafe_allow_html=True,
        )
    with m3:
        done = len(st.session_state.completed_levels)
        st.markdown(
            f'<div class="card" style="text-align:center;padding:1rem;">'
            f'<div style="font-family:Space Mono,monospace;font-size:1.6rem;color:#fff;">{done}/5</div>'
            f'<div style="font-family:Space Mono,monospace;font-size:0.75rem;color:#00CFFF;">Levels Done</div>'
            f'<div style="font-size:0.7rem;color:#888;">Keep going!</div></div>',
            unsafe_allow_html=True,
        )
    with m4:
        stars = sum(
            st.session_state.quiz_state.get(l, {}).get("score", 0)
            for l in st.session_state.completed_levels
        )
        st.markdown(
            f'<div class="card" style="text-align:center;padding:1rem;">'
            f'<div style="font-family:Space Mono,monospace;font-size:1.6rem;color:#fff;">{stars}⭐</div>'
            f'<div style="font-family:Space Mono,monospace;font-size:0.75rem;color:#FF6B6B;">Stars</div>'
            f'<div style="font-size:0.7rem;color:#888;">quiz correct</div></div>',
            unsafe_allow_html=True,
        )


# ============================================================
# LEVEL VIEW
# ============================================================
def render_level(level_id: int):
    lvl = LEVELS[level_id]
    status = level_status(level_id)

    # Back button
    if st.button("← Back to Hub"):
        st.session_state.view = "hub"
        st.rerun()

    st.markdown("<hr class='divider'/>", unsafe_allow_html=True)

    # Header
    st.markdown(
        f'<div style="display:flex;align-items:center;gap:1rem;margin-bottom:0.5rem;">'
        f'<div style="font-size:3rem;background:#111;border:2px solid #2A2A2A;'
        f'border-radius:8px;padding:0.3rem 0.8rem;box-shadow:3px 3px 0 #000;">'
        f'{lvl["pixel_art"]}</div>'
        f'<div>'
        f'<div style="font-family:Space Mono,monospace;font-size:0.65rem;'
        f'color:{lvl["color"]};letter-spacing:0.25em;">LEVEL {level_id}</div>'
        f'<div style="font-family:Space Mono,monospace;font-size:1.3rem;'
        f'color:#fff;font-weight:700;">{lvl["icon"]} {lvl["title"]}</div>'
        f'<div style="font-size:0.82rem;color:#888;">{lvl["subtitle"]}</div>'
        f'</div></div>',
        unsafe_allow_html=True,
    )

    if not is_level_unlocked(level_id):
        st.markdown(
            f'<div class="locked-box">🔒 Complete Level {level_id-1} first to unlock this level.</div>',
            unsafe_allow_html=True,
        )
        return

    # Tabs
    tab_learn, tab_code, tab_quiz = st.tabs(["📖 Learn", "💻 Code Example", "🎯 Quiz"])

    # ── LEARN TAB ──
    with tab_learn:
        st.markdown(
            f'<div class="card-purple">{lvl["description"]}</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div class="info-box">💡 <strong>XP Reward:</strong> '
            f'Complete the quiz to earn <strong style="color:#00FF41">'
            f'+{lvl["xp_reward"]} XP</strong> (10 XP per correct answer + '
            f'{lvl["xp_reward"] - 30} bonus for completing the level).</div>',
            unsafe_allow_html=True,
        )

    # ── CODE TAB ──
    with tab_code:
        st.markdown(
            '<p style="color:#888;font-size:0.82rem;font-family:Space Mono,monospace;">'
            '// Study this snippet before taking the quiz</p>',
            unsafe_allow_html=True,
        )
        st.code(lvl["code_example"], language="python")

    # ── QUIZ TAB ──
    with tab_quiz:
        render_quiz(level_id, lvl)


def render_quiz(level_id: int, lvl: dict):
    questions = lvl["questions"]
    qs_data = st.session_state.quiz_state.get(level_id, {})
    already_passed = level_id in st.session_state.completed_levels
    submitted = qs_data.get("submitted", False)

    # Show milestone badge if just completed
    if st.session_state.show_badge == level_id:
        score = qs_data.get("score", 0)
        st.balloons()
        st.markdown(
            f'<div class="milestone">'
            f'<div style="font-size:3rem;">🏆</div>'
            f'<div style="font-family:Space Mono,monospace;color:#00FF41;'
            f'font-size:1rem;margin:0.5rem 0;">MILESTONE UNLOCKED!</div>'
            f'<div style="color:#fff;font-size:0.9rem;">'
            f'"{lvl["subtitle"]}" Complete — Score: {score}/3</div>'
            f'<div style="margin-top:0.8rem;">'
            f'<span class="xp-badge">+{lvl["xp_reward"]} XP</span></div>'
            f'</div>',
            unsafe_allow_html=True,
        )
        st.session_state.show_badge = None

    if already_passed and submitted:
        score = qs_data.get("score", 0)
        st.markdown(
            f'<div class="success-box">✅ Level complete! You scored {score}/3. '
            f'Review your answers below or head back to the Hub.</div>',
            unsafe_allow_html=True,
        )

    st.markdown(
        '<p style="font-family:Space Mono,monospace;font-size:0.78rem;'
        'color:#888;margin-bottom:1rem;">Answer all 3 questions, then submit.</p>',
        unsafe_allow_html=True,
    )

    user_answers = []
    for i, q in enumerate(questions):
        st.markdown(
            f'<div class="card" style="margin-bottom:0.6rem;">'
            f'<p style="font-family:Space Mono,monospace;font-size:0.82rem;'
            f'color:#fff;margin:0 0 0.8rem 0;">Q{i+1}: {q["q"]}</p></div>',
            unsafe_allow_html=True,
        )

        # Determine default index
        saved = qs_data.get("answers", [None, None, None])
        default_idx = 0
        if saved[i] is not None and saved[i] in q["options"]:
            default_idx = q["options"].index(saved[i])

        disabled = submitted and already_passed
        choice = st.radio(
            f"Q{i+1}",
            q["options"],
            index=default_idx,
            key=quiz_key(level_id, i),
            label_visibility="collapsed",
            disabled=disabled,
        )
        user_answers.append(choice)

        # Show answer feedback if submitted
        if submitted:
            if choice == q["answer"]:
                st.markdown(
                    f'<div class="success-box">✅ Correct! <code>{q["answer"]}</code></div>',
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f'<div style="background:rgba(255,68,68,0.08);border-left:4px solid #FF4444;'
                    f'border-radius:0 8px 8px 0;padding:0.7rem 1rem;margin:0.4rem 0;font-size:0.85rem;color:#FF8888;">'
                    f'❌ Your answer: <code>{choice}</code> — Correct: <code>{q["answer"]}</code></div>',
                    unsafe_allow_html=True,
                )
        st.markdown("")  # spacing

    # Submit button
    if not (submitted and already_passed):
        if st.button("⚡ Submit Answers", key=f"submit_{level_id}"):
            score = sum(1 for i, q in enumerate(questions) if user_answers[i] == q["answer"])

            # Save quiz result
            st.session_state.quiz_state[level_id] = {
                "answers": user_answers,
                "submitted": True,
                "score": score,
            }

            # Award XP and unlock
            if level_id not in st.session_state.completed_levels:
                xp_gain = score * 10 + (lvl["xp_reward"] - 30)  # base 10/q + level bonus
                st.session_state.xp += xp_gain
                st.session_state.completed_levels.add(level_id)
                st.session_state.show_badge = level_id

            st.rerun()

    # If level 5 completed, show certificate section
    if level_id == 5 and 5 in st.session_state.completed_levels:
        render_certificate()


# ============================================================
# CERTIFICATE SECTION
# ============================================================
def render_certificate():
    st.markdown("<hr class='divider'/>", unsafe_allow_html=True)
    st.markdown(
        '<div style="font-family:Space Mono,monospace;font-size:1rem;'
        'color:#00FF41;margin-bottom:0.5rem;">🏅 Certificate of Completion</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<p style="color:#888;font-size:0.85rem;">You\'ve conquered all 5 levels! '
        'Enter your name to generate your personalized completion certificate.</p>',
        unsafe_allow_html=True,
    )

    name_input = st.text_input(
        "Your Name",
        value=st.session_state.cert_name,
        placeholder="Enter your full name…",
        key="cert_name_field",
    )
    st.session_state.cert_name = name_input

    if name_input.strip():
        cert_html = build_certificate_html(
            name=name_input.strip(),
            xp=st.session_state.xp,
            date_str=datetime.now().strftime("%B %d, %Y"),
        )
        dl_link = get_download_link(
            cert_html,
            f"python_adventure_cert_{name_input.strip().replace(' ','_')}.html",
            "📥 Download Certificate",
        )
        st.markdown(dl_link, unsafe_allow_html=True)

        # Preview
        with st.expander("👁️ Preview Certificate"):
            title, icon = get_character_info(st.session_state.xp)
            st.markdown(
                f'<div class="cert-wrapper">'
                f'<div style="font-family:Space Mono,monospace;font-size:0.65rem;'
                f'color:#00FF41;letter-spacing:0.3em;margin-bottom:0.5rem;">🐍 PYTHON CODING ADVENTURE</div>'
                f'<div style="font-family:Space Mono,monospace;font-size:1.4rem;'
                f'color:#00FF41;text-shadow:0 0 15px rgba(0,255,65,0.5);">Certificate of Completion</div>'
                f'<div style="color:#888;font-size:0.8rem;margin:0.3rem 0 1rem;">This certifies that</div>'
                f'<div style="font-family:Space Mono,monospace;font-size:1.8rem;'
                f'color:#fff;margin-bottom:1rem;">{name_input}</div>'
                f'<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:1rem;margin:1rem 0;">'
                f'<div style="background:#1A1A1A;border:1px solid #2A2A2A;border-radius:8px;padding:0.8rem;">'
                f'<div style="color:#00FF41;font-family:Space Mono,monospace;">{st.session_state.xp}</div>'
                f'<div style="font-size:0.7rem;color:#666;">XP Earned</div></div>'
                f'<div style="background:#1A1A1A;border:1px solid #2A2A2A;border-radius:8px;padding:0.8rem;">'
                f'<div style="color:#00FF41;font-family:Space Mono,monospace;">'
                f'{len(st.session_state.completed_levels)}/5</div>'
                f'<div style="font-size:0.7rem;color:#666;">Levels Done</div></div>'
                f'<div style="background:#1A1A1A;border:1px solid #2A2A2A;border-radius:8px;padding:0.8rem;">'
                f'<div style="color:#00FF41;font-family:Space Mono,monospace;">{icon} {title}</div>'
                f'<div style="font-size:0.7rem;color:#666;">Final Rank</div></div>'
                f'</div>'
                f'<div style="display:inline-block;background:#6200EE;border:2px solid #000;'
                f'border-radius:6px;padding:0.3rem 1rem;font-family:Space Mono,monospace;'
                f'font-size:0.75rem;box-shadow:3px 3px 0 #000;margin-top:0.8rem;">'
                f'✅ Python Basics Mastered</div>'
                f'</div>',
                unsafe_allow_html=True,
            )
    else:
        st.markdown(
            '<div style="color:#666;font-size:0.82rem;font-style:italic;">'
            '↑ Enter your name above to unlock the download button.</div>',
            unsafe_allow_html=True,
        )


# ============================================================
# MAIN
# ============================================================
def main():
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
    init_state()
    render_sidebar()

    if st.session_state.view == "hub":
        render_hub()
    elif st.session_state.view == "level":
        render_level(st.session_state.current_level)


if __name__ == "__main__":
    main()
