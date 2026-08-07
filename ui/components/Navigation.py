import streamlit as st


def render_clean_html(html_str):
    """Cleanly render HTML by stripping multiline indentation."""
    if not html_str:
        return
    lines = [line.strip() for line in html_str.splitlines() if line.strip()]
    cleaned = chr(10).join(lines)
    st.markdown(cleaned, unsafe_allow_html=True)


def render_navigation(active_page='home'):
    """
    Compact 60px Sticky Navigation Bar — 1280px Centered Layout.
    Left: AiResuMind Wordmark  |  Center: Flat Horizontal Nav Links  |  Right: Sign In + Primary CTA
    """

    render_clean_html("""
        <style>
        /* ── Zero out Streamlit default top whitespace ── */
        .main .block-container,
        [data-testid="stAppViewBlockContainer"],
        [data-testid="stMainBlockContainer"],
        [data-testid="stVerticalBlock"] > div:first-child,
        .stMainBlockContainer,
        .block-container,
        section.main > div {
            padding-top: 0 !important;
            margin-top: 0 !important;
        }
        .stApp > header,
        [data-testid="stHeader"],
        #stHeader {
            display: none !important;
            height: 0 !important;
            min-height: 0 !important;
        }

        /* ── Sticky Nav Bar Container (Streamlit horizontal block target) ── */
        [data-testid="stHorizontalBlock"]:has(button[key*="arm_nav_"]) {
            position: sticky !important;
            top: 0 !important;
            z-index: 99999 !important;
            background: rgba(5, 5, 5, 0.94) !important;
            backdrop-filter: blur(20px) !important;
            -webkit-backdrop-filter: blur(20px) !important;
            border-bottom: 1px solid rgba(255, 255, 255, 0.08) !important;
            max-width: 1280px !important;
            margin: 0 auto 12px auto !important;
            padding: 0 16px !important;
            height: 60px !important;
            min-height: 60px !important;
            align-items: center !important;
        }

        /* ── Baseline Alignment for Header Columns ── */
        [data-testid="stHorizontalBlock"]:has(button[key*="arm_nav_"]) > div[data-testid="column"] {
            display: flex !important;
            align-items: center !important;
            height: 60px !important;
        }

        /* ── Flat Horizontal Nav Links (No chips, no capsules) ── */
        div.arm-st-navlink > div[data-testid="stButton"] > button,
        div.arm-st-navlink-active > div[data-testid="stButton"] > button {
            background: transparent !important;
            color: #9CA3AF !important;
            border: none !important;
            border-radius: 0 !important;
            font-size: 13.5px !important;
            font-weight: 500 !important;
            padding: 4px 8px !important;
            height: 32px !important;
            box-shadow: none !important;
            letter-spacing: -0.01em !important;
            white-space: nowrap !important;
            transition: color 0.15s ease, background-color 0.15s ease !important;
        }

        div.arm-st-navlink > div[data-testid="stButton"] > button:hover {
            background: rgba(255, 255, 255, 0.06) !important;
            color: #FFFFFF !important;
            border-radius: 6px !important;
        }

        div.arm-st-navlink-active > div[data-testid="stButton"] > button {
            color: #FFFFFF !important;
            font-weight: 600 !important;
            background: transparent !important;
            border-radius: 0 !important;
            border-bottom: 2px solid #FFFFFF !important;
        }

        /* ── Right Actions: Sign In (Ghost) ── */
        div.arm-st-btn-ghost > div[data-testid="stButton"] > button {
            background: transparent !important;
            color: #9CA3AF !important;
            border: none !important;
            border-radius: 6px !important;
            font-size: 13.5px !important;
            font-weight: 500 !important;
            padding: 4px 12px !important;
            height: 34px !important;
            box-shadow: none !important;
            white-space: nowrap !important;
            transition: color 0.15s ease, background 0.15s ease !important;
        }
        div.arm-st-btn-ghost > div[data-testid="stButton"] > button:hover {
            color: #FFFFFF !important;
            background: rgba(255, 255, 255, 0.06) !important;
        }

        /* ── Right Actions: Analyze Resume (Primary Solid CTA) ── */
        div.arm-st-btn-primary > div[data-testid="stButton"] > button {
            background: #FFFFFF !important;
            color: #000000 !important;
            border: none !important;
            border-radius: 8px !important;
            font-size: 13.5px !important;
            font-weight: 600 !important;
            padding: 0 16px !important;
            height: 36px !important;
            box-shadow: 0 2px 10px rgba(255, 255, 255, 0.12) !important;
            white-space: nowrap !important;
            transition: all 0.18s ease !important;
        }
        div.arm-st-btn-primary > div[data-testid="stButton"] > button:hover {
            background: #F0F0F0 !important;
            transform: translateY(-1px) !important;
            box-shadow: 0 4px 14px rgba(255, 255, 255, 0.22) !important;
        }
        </style>
    """)

    # Render Header row via Streamlit columns
    logo_col, nav_col, actions_col = st.columns([1.4, 6, 2.6], gap="small")

    with logo_col:
        render_clean_html("""
            <div style="display:flex;align-items:center;height:60px;gap:8px;">
                <div style="width:24px;height:24px;background:linear-gradient(135deg, #4F8CFF 0%, #22C55E 100%);border-radius:6px;display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:900;color:#fff;letter-spacing:-0.5px;flex-shrink:0;">Ai</div>
                <span style="font-family:-apple-system, 'Inter', sans-serif;font-size:16px;font-weight:700;color:#FFFFFF;letter-spacing:-0.4px;white-space:nowrap;">AiResuMind</span>
            </div>
        """)

    with nav_col:
        nav_items = [
            ("dashboard",      "Dashboard"),
            ("resume_analyzer","Resume Analyzer"),
            ("resume_builder", "Resume Builder"),
            ("interview_prep", "Interview Prep"),
            ("job_search",     "Job Search"),
        ]
        nav_sub = st.columns(len(nav_items), gap="small")
        for i, (key, label) in enumerate(nav_items):
            with nav_sub[i]:
                cls = "arm-st-navlink-active" if active_page == key else "arm-st-navlink"
                st.markdown(f'<div class="{cls}">', unsafe_allow_html=True)
                if st.button(label, key=f"arm_nav_{key}"):
                    st.session_state.page = key
                    st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)

    with actions_col:
        act_sub = st.columns([1, 1.4], gap="small")
        with act_sub[0]:
            st.markdown('<div class="arm-st-btn-ghost">', unsafe_allow_html=True)
            if st.button("Sign In", key="arm_nav_signin"):
                pass
            st.markdown("</div>", unsafe_allow_html=True)
        with act_sub[1]:
            st.markdown('<div class="arm-st-btn-primary">', unsafe_allow_html=True)
            if st.button("Analyze Resume", key="arm_nav_cta"):
                st.session_state.page = "resume_analyzer"
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

