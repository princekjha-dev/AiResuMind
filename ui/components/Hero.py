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
    Apple & Linear Inspired Ultra-Premium Landing Hero.
    Left Column: Pill badge + Headline + Subtitle + Action CTAs + Trust metrics.
    Right Column: Floating glass telemetry dashboard preview card.
    """

    render_clean_html("""
        <style>
        .arm-hero-wrapper {
            max-width: 1280px;
            margin: 0 auto;
            padding: 60px 24px 80px 24px;
        }

        .arm-hero-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 64px;
            align-items: center;
        }

        .arm-badge {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            background: rgba(59, 130, 246, 0.10);
            border: 1px solid rgba(59, 130, 246, 0.28);
            color: #60A5FA;
            padding: 6px 16px;
            border-radius: 9999px;
            font-size: 13px;
            font-weight: 600;
            letter-spacing: 0.01em;
            margin-bottom: 24px;
        }

        .arm-badge-dot {
            width: 7px;
            height: 7px;
            border-radius: 50%;
            background: #3B82F6;
            box-shadow: 0 0 10px #3B82F6;
        }

        .arm-headline {
            font-family: -apple-system, BlinkMacSystemFont, 'Inter', sans-serif;
            font-size: 56px !important;
            font-weight: 800 !important;
            line-height: 1.08 !important;
            color: #FFFFFF !important;
            letter-spacing: -0.035em !important;
            margin: 0 0 24px 0 !important;
        }

        .arm-headline-accent {
            background: linear-gradient(135deg, #3B82F6 0%, #9333EA 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        .arm-desc {
            font-family: -apple-system, BlinkMacSystemFont, 'Inter', sans-serif;
            font-size: 17.5px !important;
            color: #9CA3AF !important;
            line-height: 1.6 !important;
            margin: 0 0 36px 0 !important;
            font-weight: 400 !important;
        }

        .arm-cta-row {
            display: flex;
            align-items: center;
            gap: 16px;
            margin-bottom: 40px;
        }

        .arm-trust-row {
            display: flex;
            align-items: center;
            gap: 32px;
            padding-top: 32px;
            border-top: 1px solid rgba(255, 255, 255, 0.08);
        }

        .arm-trust-metric {
            display: flex;
            flex-direction: column;
            gap: 2px;
        }

        .arm-trust-num {
            font-size: 22px;
            font-weight: 800;
            color: #FFFFFF;
            letter-spacing: -0.02em;
            line-height: 1;
        }

        .arm-trust-num.green { color: #10B981; }

        .arm-trust-label {
            font-size: 12.5px;
            color: #6B7280;
            font-weight: 400;
        }

        /* Glass Preview Card */
        .arm-preview-card {
            background: rgba(18, 18, 24, 0.85);
            border: 1px solid rgba(255, 255, 255, 0.10);
            border-radius: 24px;
            box-shadow: 0 30px 80px rgba(0, 0, 0, 0.6);
            padding: 28px;
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
        }

        .arm-win-bar {
            display: flex;
            align-items: center;
            gap: 6px;
            margin-bottom: 20px;
        }

        .arm-win-btn {
            width: 11px;
            height: 11px;
            border-radius: 50%;
        }

        .arm-score-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 12px;
            margin-bottom: 20px;
        }

        .arm-score-cell {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.07);
            border-radius: 14px;
            padding: 14px;
        }

        .arm-score-label {
            font-size: 10.5px;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            color: #6B7280;
            margin-bottom: 4px;
        }

        .arm-score-val {
            font-size: 20px;
            font-weight: 800;
            color: #FFFFFF;
            letter-spacing: -0.02em;
        }

        .arm-score-delta {
            font-size: 11px;
            font-weight: 600;
            color: #10B981;
            margin-left: 4px;
        }

        .arm-progress-block {
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid rgba(255, 255, 255, 0.06);
            border-radius: 16px;
            padding: 18px;
            margin-bottom: 16px;
        }

        .arm-progress-header {
            display: flex;
            justify-content: space-between;
            font-size: 12px;
            font-weight: 600;
            color: #E5E7EB;
            margin-bottom: 12px;
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
            margin-bottom: 4px;
        }

        .arm-progress-track {
            height: 5px;
            background: rgba(255, 255, 255, 0.07);
            border-radius: 999px;
            overflow: hidden;
        }

        .arm-progress-fill {
            height: 100%;
            border-radius: 999px;
        }

        .arm-ai-rec {
            background: rgba(59, 130, 246, 0.08);
            border: 1px solid rgba(59, 130, 246, 0.2);
            border-radius: 14px;
            padding: 14px 16px;
        }

        .arm-ai-rec-label {
            font-size: 10.5px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            color: #60A5FA;
            margin-bottom: 4px;
        }

        .arm-ai-rec-body {
            font-size: 12.5px;
            color: #9CA3AF;
            line-height: 1.5;
        }

        @media (max-width: 900px) {
            .arm-hero-grid {
                grid-template-columns: 1fr;
                gap: 40px;
            }
            .arm-headline { font-size: 40px !important; }
        }
        </style>
    """)

    render_clean_html('<div class="arm-hero-wrapper"><div class="arm-hero-grid">')

    # Left Column
    left_col, right_col = st.columns([1, 1], gap="large")

    with left_col:
        render_clean_html(f"""
            <div>
                <div class="arm-badge">
                    <span class="arm-badge-dot"></span>
                    AI Resume Intelligence v4.0
                </div>
                <h1 class="arm-headline">
                    Transform Your Resume Into<br>
                    <span class="arm-headline-accent">An ATS-Beating</span><br>
                    Career Engine
                </h1>
                <p class="arm-desc">{subtitle}</p>
            </div>
        """)

        btn_c1, btn_c2, _ = st.columns([1.6, 1.6, 1])
        with btn_c1:
            if st.button("Start AI Audit Free", key="hero_cta_analyze", type="primary"):
                st.session_state.page = "resume_analyzer"
                st.rerun()

        with btn_c2:
            if st.button("Try Resume Builder", key="hero_cta_builder"):
                st.session_state.page = "resume_builder"
                st.rerun()

        render_clean_html("""
            <div class="arm-trust-row">
                <div class="arm-trust-metric">
                    <span class="arm-trust-num">99.4%</span>
                    <span class="arm-trust-label">ATS Match Accuracy</span>
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

    with right_col:
        render_clean_html("""
            <div class="arm-preview-card">
                <div class="arm-win-bar">
                    <div class="arm-win-btn" style="background:#FF5F56"></div>
                    <div class="arm-win-btn" style="background:#FFBD2E"></div>
                    <div class="arm-win-btn" style="background:#27C93F"></div>
                    <span style="margin-left:8px;font-size:12px;color:#6B7280;font-weight:500;">
                        Candidate Intelligence Telemetry
                    </span>
                </div>

                <div class="arm-score-grid">
                    <div class="arm-score-cell">
                        <div class="arm-score-label">ATS Match Score</div>
                        <div class="arm-score-val">94%<span class="arm-score-delta">+14%</span></div>
                    </div>
                    <div class="arm-score-cell">
                        <div class="arm-score-label">Profile Signal</div>
                        <div class="arm-score-val" style="font-size:15px;">Executive</div>
                    </div>
                    <div class="arm-score-cell">
                        <div class="arm-score-label">Callback Rate</div>
                        <div class="arm-score-val" style="color:#10B981;">High (88%)</div>
                    </div>
                </div>

                <div class="arm-progress-block">
                    <div class="arm-progress-header">
                        <span>ATS Keyword Alignment</span>
                        <span style="color:#10B981;">Verified High Match</span>
                    </div>

                    <div class="arm-progress-row">
                        <div class="arm-progress-meta"><span>Resume Structure</span><strong>96%</strong></div>
                        <div class="arm-progress-track"><div class="arm-progress-fill" style="width:96%;background:#E5E7EB;"></div></div>
                    </div>

                    <div class="arm-progress-row">
                        <div class="arm-progress-meta"><span>Keyword Density & Skills</span><strong>92%</strong></div>
                        <div class="arm-progress-track"><div class="arm-progress-fill" style="width:92%;background:#10B981;"></div></div>
                    </div>

                    <div class="arm-progress-row">
                        <div class="arm-progress-meta"><span>Quantified Business Impact</span><strong>88%</strong></div>
                        <div class="arm-progress-track"><div class="arm-progress-fill" style="width:88%;background:#3B82F6;"></div></div>
                    </div>
                </div>

                <div class="arm-ai-rec">
                    <div class="arm-ai-rec-label">AI Executive Recommendation</div>
                    <div class="arm-ai-rec-body">
                        Reframe project achievements using quantified STAR metrics (+15% score lift)
                        and add missing high-density target skills (System Architecture, Distributed Systems) to pass ATS screening.
                    </div>
                </div>
            </div>
        """)

    render_clean_html("</div></div>")
