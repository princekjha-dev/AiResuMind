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
    Premium sticky header — 72px height, 1280px container, 32px side padding.
    Left: AiResuMind logo  |  Center: nav links  |  Right: Sign In + Analyze Resume
    """

    # ── Inject one-time nav CSS ──────────────────────────────────────────────
    render_clean_html("""
        <style>
        /* ── Reset Streamlit top padding so header starts at top ── */
        .main .block-container {
            padding-top: 0 !important;
            margin-top: 0 !important;
        }
        section.main > div:first-child {
            padding-top: 0 !important;
        }

        /* ── Sticky header shell ── */
        .arm-header {
            position: sticky;
            top: 0;
            z-index: 1000;
            background: rgba(5, 5, 5, 0.88);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border-bottom: 1px solid rgba(255, 255, 255, 0.08);
            width: 100%;
        }

        /* ── Inner 1280px centering wrapper ── */
        .arm-header-inner {
            max-width: 1280px;
            margin: 0 auto;
            padding: 0 32px;
            height: 72px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 24px;
        }

        /* ── Logo ── */
        .arm-logo {
            display: flex;
            align-items: center;
            gap: 8px;
            text-decoration: none;
            flex-shrink: 0;
        }
        .arm-logo-icon {
            width: 28px;
            height: 28px;
            background: linear-gradient(135deg, #4F8CFF 0%, #22C55E 100%);
            border-radius: 7px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 14px;
            font-weight: 900;
            color: #fff;
            letter-spacing: -0.5px;
            flex-shrink: 0;
        }
        .arm-logo-text {
            font-family: -apple-system, 'Inter', sans-serif;
            font-size: 17px;
            font-weight: 700;
            color: #FFFFFF;
            letter-spacing: -0.4px;
            white-space: nowrap;
        }

        /* ── Center nav list ── */
        .arm-nav {
            display: flex;
            align-items: center;
            gap: 2px;
            flex: 1;
            justify-content: center;
        }

        /* ── Individual nav links ── */
        .arm-nav-link {
            position: relative;
            font-family: -apple-system, 'Inter', sans-serif;
            font-size: 14px;
            font-weight: 500;
            color: #9CA3AF;
            padding: 6px 12px;
            border-radius: 8px;
            cursor: pointer;
            transition: color 0.18s ease, background 0.18s ease;
            white-space: nowrap;
            border: none;
            background: none;
            text-decoration: none;
        }
        .arm-nav-link:hover {
            color: #FFFFFF;
            background: rgba(255, 255, 255, 0.06);
        }
        .arm-nav-link.active {
            color: #FFFFFF;
            font-weight: 600;
        }
        .arm-nav-link.active::after {
            content: '';
            position: absolute;
            bottom: -1px;
            left: 12px;
            right: 12px;
            height: 2px;
            background: #FFFFFF;
            border-radius: 999px;
            animation: underline-in 0.22s ease forwards;
        }
        @keyframes underline-in {
            from { transform: scaleX(0); opacity: 0; }
            to   { transform: scaleX(1); opacity: 1; }
        }

        /* ── Right action buttons ── */
        .arm-actions {
            display: flex;
            align-items: center;
            gap: 8px;
            flex-shrink: 0;
        }
        .arm-btn-ghost {
            font-family: -apple-system, 'Inter', sans-serif;
            font-size: 14px;
            font-weight: 500;
            color: #9CA3AF;
            background: transparent;
            border: 1px solid rgba(255,255,255,0.12);
            border-radius: 8px;
            padding: 0 16px;
            height: 40px;
            cursor: pointer;
            transition: all 0.18s ease;
            white-space: nowrap;
        }
        .arm-btn-ghost:hover {
            color: #FFFFFF;
            border-color: rgba(255,255,255,0.3);
            background: rgba(255,255,255,0.06);
        }
        .arm-btn-primary {
            font-family: -apple-system, 'Inter', sans-serif;
            font-size: 14px;
            font-weight: 600;
            color: #000000;
            background: #FFFFFF;
            border: none;
            border-radius: 8px;
            padding: 0 18px;
            height: 40px;
            cursor: pointer;
            transition: all 0.18s ease;
            white-space: nowrap;
        }
        .arm-btn-primary:hover {
            background: #F0F0F0;
            transform: translateY(-1px);
            box-shadow: 0 4px 16px rgba(255,255,255,0.18);
        }

        /* ── Streamlit button overrides for nav columns ── */
        div.arm-st-navlink > div[data-testid="stButton"] > button {
            background: transparent !important;
            color: #9CA3AF !important;
            border: none !important;
            border-radius: 8px !important;
            font-size: 14px !important;
            font-weight: 500 !important;
            padding: 6px 12px !important;
            height: 36px !important;
            box-shadow: none !important;
            letter-spacing: 0 !important;
        }
        div.arm-st-navlink > div[data-testid="stButton"] > button:hover {
            background: rgba(255,255,255,0.06) !important;
            color: #FFFFFF !important;
        }
        div.arm-st-navlink-active > div[data-testid="stButton"] > button {
            background: transparent !important;
            color: #FFFFFF !important;
            border: none !important;
            border-radius: 8px !important;
            font-size: 14px !important;
            font-weight: 600 !important;
            padding: 6px 12px !important;
            height: 36px !important;
            box-shadow: none !important;
            letter-spacing: 0 !important;
            border-bottom: 2px solid #FFFFFF !important;
        }
        div.arm-st-btn-ghost > div[data-testid="stButton"] > button {
            background: transparent !important;
            color: #9CA3AF !important;
            border: 1px solid rgba(255,255,255,0.14) !important;
            border-radius: 8px !important;
            font-size: 14px !important;
            font-weight: 500 !important;
            padding: 0 16px !important;
            height: 40px !important;
            box-shadow: none !important;
        }
        div.arm-st-btn-ghost > div[data-testid="stButton"] > button:hover {
            background: rgba(255,255,255,0.06) !important;
            color: #FFFFFF !important;
            border-color: rgba(255,255,255,0.3) !important;
        }
        div.arm-st-btn-primary > div[data-testid="stButton"] > button {
            background: #FFFFFF !important;
            color: #000000 !important;
            border: none !important;
            border-radius: 8px !important;
            font-size: 14px !important;
            font-weight: 600 !important;
            padding: 0 18px !important;
            height: 40px !important;
            box-shadow: none !important;
        }
        div.arm-st-btn-primary > div[data-testid="stButton"] > button:hover {
            background: #F0F0F0 !important;
            transform: translateY(-1px) !important;
            box-shadow: 0 4px 16px rgba(255,255,255,0.18) !important;
        }
        </style>
    """)

    # ── Logo (pure HTML, no interaction needed) ──────────────────────────────
    render_clean_html("""
        <div class="arm-header">
            <div class="arm-header-inner" id="arm-header-inner-top">
    """)

    # We render the interior via Streamlit columns to keep button interactivity
    # Logo | Nav | Actions  — proportions: logo=1.5, nav=6, actions=2.5
    logo_col, nav_col, actions_col = st.columns([1.5, 6, 2.5], gap="small")

    with logo_col:
        render_clean_html("""
            <div style="display:flex;align-items:center;height:72px;gap:8px;">
                <div class="arm-logo-icon">Ai</div>
                <span class="arm-logo-text">AiResuMind</span>
            </div>
        """)

    with nav_col:
        nav_items = [
            ("dashboard",      "Dashboard"),
            ("resume_analyzer","Resume Analyzer"),
            ("resume_builder", "Resume Builder"),
            ("cover_letter",   "Cover Letter"),
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
        act_sub = st.columns([1, 1.3], gap="small")
        with act_sub[0]:
            st.markdown('<div class="arm-st-btn-ghost">', unsafe_allow_html=True)
            if st.button("Sign In", key="arm_nav_signin"):
                pass  # placeholder — wire to auth later
            st.markdown("</div>", unsafe_allow_html=True)
        with act_sub[1]:
            st.markdown('<div class="arm-st-btn-primary">', unsafe_allow_html=True)
            if st.button("Analyze Resume", key="arm_nav_cta"):
                st.session_state.page = "resume_analyzer"
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

    # Close the header div
    render_clean_html("</div></div>")
