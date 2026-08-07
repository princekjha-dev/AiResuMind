import streamlit as st


def render_clean_html(html_str):
    """Cleanly render HTML — strips indentation to avoid markdown code blocks."""
    if not html_str:
        return
    lines = [line.strip() for line in html_str.splitlines() if line.strip()]
    cleaned = chr(10).join(lines)
    st.markdown(cleaned, unsafe_allow_html=True)


def render_hero(
    title="Transform Your Resume Into An ATS-Beating Career Engine",
    subtitle="Receive high-precision AI feedback, benchmark keyword alignment against top job descriptions, and generate executive-ready documents engineered to pass screening filters.",
):
    """
    Premium 2-column hero section.
    Left (50%): Badge + 64px headline + description + CTAs + trust metrics
    Right (50%): Floating glass dashboard preview card
    """

    render_clean_html("""
        <style>
        /* ── Page background with subtle radial gradients ── */
        .stApp, .main {
            background: #050505 !important;
        }
        .arm-bg-glow {
            position: fixed;
            pointer-events: none;
            z-index: 0;
        }
        .arm-bg-glow-tr {
            top: -200px;
            right: -200px;
            width: 700px;
            height: 700px;
            background: radial-gradient(circle at center, rgba(79,140,255,0.07) 0%, transparent 70%);
        }
        .arm-bg-glow-bl {
            bottom: -200px;
            left: -200px;
            width: 600px;
            height: 600px;
            background: radial-gradient(circle at center, rgba(34,197,94,0.05) 0%, transparent 70%);
        }

        /* ── Hero wrapper ── */
        .arm-hero-wrapper {
            max-width: 1280px;
            margin: 0 auto;
            padding: 72px 32px 96px 32px;
        }

        /* ── Hero 2-column grid ── */
        .arm-hero-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 80px;
            align-items: center;
        }

        /* ── Badge pill ── */
        .arm-badge {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            background: rgba(79, 140, 255, 0.10);
            border: 1px solid rgba(79, 140, 255, 0.28);
            color: #7EB8FF;
            padding: 5px 14px;
            border-radius: 9999px;
            font-size: 12.5px;
            font-weight: 600;
            letter-spacing: 0.02em;
            margin-bottom: 24px;
        }
        .arm-badge-dot {
            width: 6px;
            height: 6px;
            border-radius: 50%;
            background: #4F8CFF;
            animation: pulse-badge 2s infinite;
        }
        @keyframes pulse-badge {
            0%, 100% { opacity: 1; transform: scale(1); }
            50%       { opacity: 0.5; transform: scale(0.75); }
        }

        /* ── Headline ── */
        .arm-headline {
            font-family: -apple-system, BlinkMacSystemFont, 'Inter', sans-serif;
            font-size: 64px !important;
            font-weight: 800 !important;
            line-height: 1.05 !important;
            color: #FFFFFF !important;
            letter-spacing: -0.04em !important;
            max-width: 620px;
            margin: 0 0 28px 0 !important;
        }
        .arm-headline-accent {
            background: linear-gradient(90deg, #4F8CFF 0%, #22C55E 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        /* ── Description ── */
        .arm-desc {
            font-family: -apple-system, 'Inter', sans-serif;
            font-size: 18px !important;
            color: #9CA3AF !important;
            line-height: 1.65 !important;
            max-width: 560px;
            margin: 0 0 40px 0 !important;
            font-weight: 400 !important;
        }

        /* ── CTA row ── */
        .arm-cta-row {
            display: flex;
            align-items: center;
            gap: 16px;
            flex-wrap: wrap;
            margin-bottom: 48px;
        }

        /* ── Streamlit button overrides — hero CTAs ── */
        div.arm-cta-primary > div[data-testid="stButton"] > button {
            background: #4F8CFF !important;
            color: #FFFFFF !important;
            border: none !important;
            border-radius: 10px !important;
            font-size: 15px !important;
            font-weight: 600 !important;
            height: 52px !important;
            padding: 0 28px !important;
            box-shadow: 0 0 32px rgba(79,140,255,0.35) !important;
            transition: all 0.2s ease !important;
            letter-spacing: -0.01em !important;
        }
        div.arm-cta-primary > div[data-testid="stButton"] > button:hover {
            background: #6BA5FF !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 40px rgba(79,140,255,0.50) !important;
        }
        div.arm-cta-secondary > div[data-testid="stButton"] > button {
            background: transparent !important;
            color: #F5F5F7 !important;
            border: 1px solid rgba(255,255,255,0.18) !important;
            border-radius: 10px !important;
            font-size: 15px !important;
            font-weight: 500 !important;
            height: 52px !important;
            padding: 0 24px !important;
            box-shadow: none !important;
            transition: all 0.2s ease !important;
        }
        div.arm-cta-secondary > div[data-testid="stButton"] > button:hover {
            background: rgba(255,255,255,0.06) !important;
            border-color: rgba(255,255,255,0.35) !important;
        }

        /* ── Trust metrics bar ── */
        .arm-trust-row {
            display: flex;
            align-items: center;
            gap: 0;
            padding-top: 40px;
            border-top: 1px solid rgba(255,255,255,0.08);
        }
        .arm-trust-metric {
            display: flex;
            flex-direction: column;
            gap: 2px;
            padding-right: 28px;
            margin-right: 28px;
            border-right: 1px solid rgba(255,255,255,0.08);
        }
        .arm-trust-metric:last-child {
            border-right: none;
            padding-right: 0;
            margin-right: 0;
        }
        .arm-trust-num {
            font-size: 20px;
            font-weight: 800;
            color: #FFFFFF;
            letter-spacing: -0.02em;
            line-height: 1;
        }
        .arm-trust-num.green { color: #22C55E; }
        .arm-trust-label {
            font-size: 12.5px;
            color: #6B7280;
            font-weight: 400;
        }

        /* ── Right column: glass dashboard card ── */
        .arm-preview-card {
            background: rgba(22, 22, 22, 0.80);
            border: 1px solid rgba(255, 255, 255, 0.10);
            border-radius: 24px;
            box-shadow:
                0 40px 120px rgba(0,0,0,0.55),
                0 0 0 1px rgba(255,255,255,0.04) inset;
            padding: 28px;
            width: 100%;
            backdrop-filter: blur(24px);
            -webkit-backdrop-filter: blur(24px);
        }

        /* ── Mac-style window buttons ── */
        .arm-win-bar {
            display: flex;
            align-items: center;
            gap: 6px;
            margin-bottom: 20px;
        }
        .arm-win-btn {
            width: 12px;
            height: 12px;
            border-radius: 50%;
        }

        /* ── Score grid ── */
        .arm-score-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 10px;
            margin-bottom: 18px;
        }
        .arm-score-cell {
            background: rgba(255,255,255,0.035);
            border: 1px solid rgba(255,255,255,0.07);
            border-radius: 12px;
            padding: 14px;
        }
        .arm-score-label {
            font-size: 10px;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            color: #6B7280;
            margin-bottom: 4px;
        }
        .arm-score-val {
            font-size: 20px;
            font-weight: 800;
            color: #FFFFFF;
            letter-spacing: -0.02em;
            line-height: 1;
        }
        .arm-score-delta {
            font-size: 11px;
            font-weight: 600;
            color: #22C55E;
            margin-left: 4px;
        }

        /* ── Progress bars ── */
        .arm-progress-block {
            background: rgba(255,255,255,0.025);
            border: 1px solid rgba(255,255,255,0.06);
            border-radius: 14px;
            padding: 18px;
            margin-bottom: 12px;
        }
        .arm-progress-header {
            display: flex;
            justify-content: space-between;
            font-size: 12px;
            font-weight: 700;
            color: #E5E7EB;
            margin-bottom: 14px;
        }
        .arm-progress-tag {
            background: rgba(255,255,255,0.08);
            border-radius: 999px;
            padding: 2px 9px;
            font-size: 10.5px;
            font-weight: 600;
            color: #9CA3AF;
        }
        .arm-progress-row {
            margin-bottom: 10px;
        }
        .arm-progress-row:last-child { margin-bottom: 0; }
        .arm-progress-meta {
            display: flex;
            justify-content: space-between;
            font-size: 11.5px;
            color: #6B7280;
            margin-bottom: 5px;
        }
        .arm-progress-meta strong { color: #E5E7EB; font-weight: 600; }
        .arm-progress-track {
            height: 5px;
            background: rgba(255,255,255,0.07);
            border-radius: 999px;
            overflow: hidden;
        }
        .arm-progress-fill {
            height: 100%;
            border-radius: 999px;
        }

        /* ── AI Recommendation footer ── */
        .arm-ai-rec {
            background: rgba(79,140,255,0.07);
            border: 1px solid rgba(79,140,255,0.18);
            border-radius: 12px;
            padding: 14px 16px;
        }
        .arm-ai-rec-label {
            font-size: 10.5px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.07em;
            color: #4F8CFF;
            margin-bottom: 4px;
        }
        .arm-ai-rec-body {
            font-size: 12.5px;
            color: #9CA3AF;
            line-height: 1.5;
        }

        /* ── Responsive ── */
        @media (max-width: 1024px) {
            .arm-hero-grid {
                grid-template-columns: 60fr 40fr;
                gap: 48px;
            }
            .arm-headline { font-size: 52px !important; }
        }
        @media (max-width: 768px) {
            .arm-hero-grid {
                grid-template-columns: 1fr;
                gap: 48px;
            }
            .arm-hero-wrapper { padding: 48px 24px 72px 24px; }
            .arm-headline { font-size: 40px !important; max-width: 100%; }
            .arm-desc { font-size: 16px !important; max-width: 100%; }
            .arm-cta-row { flex-direction: column; }
            div.arm-cta-primary > div[data-testid="stButton"] > button,
            div.arm-cta-secondary > div[data-testid="stButton"] > button {
                width: 100% !important;
            }
        }
        </style>
    """)

    # ── Radial background glows (decorative only) ────────────────────────────
    render_clean_html("""
        <div class="arm-bg-glow arm-bg-glow-tr"></div>
        <div class="arm-bg-glow arm-bg-glow-bl"></div>
        <div class="arm-hero-wrapper">
    """)

    # ── Two-column grid via Streamlit columns ─────────────────────────────────
    left_col, right_col = st.columns([1, 1], gap="large")

    # ────────────────────────── LEFT COLUMN ──────────────────────────────────
    with left_col:
        render_clean_html(f"""
            <div class="arm-badge">
                <span class="arm-badge-dot"></span>
                AI Resume Intelligence
            </div>
            <h1 class="arm-headline">
                Transform Your Resume Into<br>
                <span class="arm-headline-accent">An ATS-Beating</span><br>
                Career Engine
            </h1>
            <p class="arm-desc">{subtitle}</p>
        """)

        # ── CTAs — rendered as Streamlit buttons inside styled wrappers ──
        render_clean_html('<div class="arm-cta-row">')

        cta1, cta2, _ = st.columns([1.6, 1.6, 1], gap="small")
        with cta1:
            st.markdown('<div class="arm-cta-primary">', unsafe_allow_html=True)
            if st.button("⚡ Analyze Free", key="hero_cta_analyze", type="primary"):
                st.session_state.page = "resume_analyzer"
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

        with cta2:
            st.markdown('<div class="arm-cta-secondary">', unsafe_allow_html=True)
            if st.button("▶ Watch Demo", key="hero_cta_demo"):
                st.session_state.page = "resume_builder"
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

        render_clean_html("</div>")

        # ── Trust metrics row ─────────────────────────────────────────────
        render_clean_html("""
            <div class="arm-trust-row">
                <div class="arm-trust-metric">
                    <span class="arm-trust-num">99.4%</span>
                    <span class="arm-trust-label">ATS Match Precision</span>
                </div>
                <div class="arm-trust-metric">
                    <span class="arm-trust-num">50,000+</span>
                    <span class="arm-trust-label">Resumes Audited</span>
                </div>
                <div class="arm-trust-metric">
                    <span class="arm-trust-num green">4.9 / 5.0</span>
                    <span class="arm-trust-label">Candidate Rating</span>
                </div>
            </div>
        """)

    # ────────────────────────── RIGHT COLUMN ─────────────────────────────────
    with right_col:
        render_clean_html("""
            <div class="arm-preview-card">

                <!-- Window chrome -->
                <div class="arm-win-bar">
                    <div class="arm-win-btn" style="background:#FF5F56"></div>
                    <div class="arm-win-btn" style="background:#FFBD2E"></div>
                    <div class="arm-win-btn" style="background:#27C93F"></div>
                    <span style="margin-left:10px;font-size:12px;color:#6B7280;font-weight:500;">
                        Candidate Intelligence Desktop
                    </span>
                    <div style="margin-left:auto;display:flex;gap:6px;font-size:11px;font-weight:600;">
                        <span style="background:rgba(255,255,255,0.10);color:#E5E7EB;padding:3px 10px;border-radius:999px;">Overview</span>
                        <span style="color:#6B7280;padding:3px 8px;">ATS Signal</span>
                        <span style="color:#6B7280;padding:3px 8px;">Keywords</span>
                        <span style="color:#6B7280;padding:3px 8px;">AI Insights</span>
                    </div>
                </div>

                <!-- Score grid -->
                <div class="arm-score-grid">
                    <div class="arm-score-cell">
                        <div class="arm-score-label">ATS Match Score</div>
                        <div class="arm-score-val">
                            94%<span class="arm-score-delta">+14%</span>
                        </div>
                    </div>
                    <div class="arm-score-cell">
                        <div class="arm-score-label">Profile Signal</div>
                        <div class="arm-score-val" style="font-size:16px;">Executive</div>
                    </div>
                    <div class="arm-score-cell">
                        <div class="arm-score-label">Callback Rate</div>
                        <div class="arm-score-val" style="color:#22C55E;">High (88%)</div>
                    </div>
                </div>

                <!-- Progress bars -->
                <div class="arm-progress-block">
                    <div class="arm-progress-header">
                        <span>ATS Telemetry Alignment</span>
                        <span class="arm-progress-tag">Verified High Match</span>
                    </div>

                    <div class="arm-progress-row">
                        <div class="arm-progress-meta">
                            <span>Resume Structure</span>
                            <strong>96%</strong>
                        </div>
                        <div class="arm-progress-track">
                            <div class="arm-progress-fill"
                                 style="width:96%;background:#E5E7EB;"></div>
                        </div>
                    </div>

                    <div class="arm-progress-row">
                        <div class="arm-progress-meta">
                            <span>Keyword Density &amp; Skills</span>
                            <strong>92%</strong>
                        </div>
                        <div class="arm-progress-track">
                            <div class="arm-progress-fill"
                                 style="width:92%;background:#22C55E;"></div>
                        </div>
                    </div>

                    <div class="arm-progress-row">
                        <div class="arm-progress-meta">
                            <span>Quantified Business Impact</span>
                            <strong>88%</strong>
                        </div>
                        <div class="arm-progress-track">
                            <div class="arm-progress-fill"
                                 style="width:88%;background:#4F8CFF;"></div>
                        </div>
                    </div>
                </div>

                <!-- AI Recommendation -->
                <div class="arm-ai-rec">
                    <div class="arm-ai-rec-label">AI Executive Recommendation</div>
                    <div class="arm-ai-rec-body">
                        Reframe project achievements using quantified STAR metrics
                        (+15% metric lift) and add missing target skills (SQL, System Design, BRD)
                        to guarantee 95%+ ATS parsing accuracy.
                    </div>
                </div>

            </div>
        """)

    # ── Close hero wrapper ────────────────────────────────────────────────────
    render_clean_html("</div>")
