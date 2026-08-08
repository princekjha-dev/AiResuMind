import streamlit as st

def render_clean_html(html_str):
    """Cleanly render HTML — strips indentation to avoid markdown code blocks."""
    if not html_str:
        return
    lines = [line.strip() for line in html_str.splitlines() if line.strip()]
    cleaned = chr(10).join(lines)
    st.markdown(cleaned, unsafe_allow_html=True)

def render_hero(
    title="Your career deserves better intelligence.",
    subtitle="Analyze your resume, understand your fit, build stronger applications, and make smarter career moves.",
):
    """
    Apple & Linear Inspired High-End Hero Component V5.
    Left Column: Eyebrow + Dramatic Editorial Typography + Tactile CTAs.
    Right Column: Realistic Resume Intelligence Telemetry Panel.
    """

    render_clean_html("""
        <style>
        .arm-hero-wrapper {
            max-width: 1280px;
            margin: 0 auto;
            padding: 72px 24px 80px 24px;
        }

        .arm-hero-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 64px;
            align-items: center;
        }

        .arm-eyebrow {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            font-size: 12px;
            font-weight: 700;
            letter-spacing: 0.12em;
            text-transform: uppercase;
            color: #60A5FA;
            margin-bottom: 24px;
        }

        .arm-eyebrow-dot {
            width: 6px;
            height: 6px;
            border-radius: 50%;
            background-color: #60A5FA;
            box-shadow: 0 0 8px #60A5FA;
        }

        .arm-headline {
            font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "Inter", sans-serif !important;
            font-size: 76px !important;
            font-weight: 800 !important;
            line-height: 1.05 !important;
            color: #F5F5F7 !important;
            letter-spacing: -0.04em !important;
            margin: 0 0 24px 0 !important;
        }

        .arm-headline-accent {
            background: linear-gradient(135deg, #6366F1 0%, #A855F7 50%, #EC4899 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        .arm-desc {
            font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "Inter", sans-serif !important;
            font-size: 19px !important;
            color: #86868B !important;
            line-height: 1.6 !important;
            margin: 0 0 40px 0 !important;
            font-weight: 400 !important;
            max-width: 520px !important;
        }

        /* Glass Telemetry Panel */
        .arm-panel-card {
            background: #12141A;
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 24px;
            box-shadow: 0 40px 100px rgba(0, 0, 0, 0.7);
            padding: 28px;
            transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
        }

        .arm-panel-card:hover {
            border-color: rgba(255, 255, 255, 0.16);
            transform: translateY(-4px);
        }

        .arm-win-bar {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 20px;
            padding-bottom: 16px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        }

        .arm-win-dots {
            display: flex;
            gap: 8px;
        }

        .arm-win-btn {
            width: 10px;
            height: 10px;
            border-radius: 50%;
        }

        .arm-panel-title {
            font-size: 12px;
            font-weight: 600;
            color: #6E6E73;
        }

        .arm-metrics-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 12px;
            margin-bottom: 24px;
        }

        .arm-metric-cell {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.07);
            border-radius: 14px;
            padding: 14px 16px;
        }

        .arm-metric-label {
            font-size: 10.5px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            color: #6E6E73;
            margin-bottom: 4px;
        }

        .arm-metric-val-row {
            display: flex;
            align-items: baseline;
            gap: 6px;
        }

        .arm-metric-num {
            font-size: 24px;
            font-weight: 800;
            color: #F5F5F7;
            letter-spacing: -0.02em;
        }

        .arm-metric-unit {
            font-size: 12px;
            color: #6E6E73;
        }

        .arm-vis-bar-wrap {
            margin-bottom: 12px;
        }

        .arm-vis-meta {
            display: flex;
            justify-content: space-between;
            font-size: 11.5px;
            color: #86868B;
            margin-bottom: 5px;
        }

        .arm-vis-track {
            height: 5px;
            background: rgba(255, 255, 255, 0.07);
            border-radius: 999px;
            overflow: hidden;
        }

        .arm-vis-fill {
            height: 100%;
            border-radius: 999px;
        }

        .arm-chips-row {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-top: 16px;
            padding-top: 14px;
            border-top: 1px solid rgba(255, 255, 255, 0.08);
        }

        .arm-chip {
            font-size: 11.5px;
            padding: 4px 10px;
            border-radius: 9999px;
            font-weight: 500;
        }
        .arm-chip.matched { background: rgba(16, 185, 129, 0.12); color: #34D399; border: 1px solid rgba(16, 185, 129, 0.2); }
        .arm-chip.missing { background: rgba(245, 158, 11, 0.12); color: #FBBF24; border: 1px solid rgba(245, 158, 11, 0.2); }

        .arm-readiness {
            margin-top: 16px;
            background: rgba(59, 130, 246, 0.08);
            border: 1px solid rgba(59, 130, 246, 0.2);
            border-radius: 12px;
            padding: 12px 14px;
            display: flex;
            align-items: center;
            gap: 10px;
            font-size: 12px;
            color: #F5F5F7;
        }

        @media (max-width: 1024px) {
            .arm-hero-grid { grid-template-columns: 1fr; gap: 40px; }
            .arm-headline { font-size: 56px !important; }
        }
        </style>
    """)

    render_clean_html('<div class="arm-hero-wrapper"><div class="arm-hero-grid">')

    left_col, right_col = st.columns([1, 1], gap="large")

    with left_col:
        render_clean_html(f"""
            <div>
                <div class="arm-eyebrow">
                    <span class="arm-eyebrow-dot"></span>
                    AI CAREER INTELLIGENCE PLATFORM
                </div>
                <h1 class="arm-headline">
                    Your career<br>
                    deserves better<br>
                    <span class="arm-headline-accent">intelligence.</span>
                </h1>
                <p class="arm-desc">{subtitle}</p>
            </div>
        """)

        btn_c1, btn_c2 = st.columns([1.5, 1.3])
        with btn_c1:
            if st.button("Start with your Resume", key="hero_cta_analyze", type="primary", use_container_width=True):
                st.session_state.page = "resume_analyzer"
                st.rerun()

        with btn_c2:
            if st.button("Explore the Platform", key="hero_cta_builder", use_container_width=True):
                st.session_state.page = "dashboard"
                st.rerun()

    with right_col:
        render_clean_html("""
            <div class="arm-panel-card">
                <div class="arm-win-bar">
                    <div class="arm-win-dots">
                        <div class="arm-win-btn" style="background:#FF5F56"></div>
                        <div class="arm-win-btn" style="background:#FFBD2E"></div>
                        <div class="arm-win-btn" style="background:#27C93F"></div>
                    </div>
                    <span class="arm-panel-title">AiResuMind Pro v5.0 — Intelligence Workspace</span>
                </div>

                <div class="arm-metrics-grid">
                    <div class="arm-metric-cell">
                        <div class="arm-metric-label">ATS SCORE</div>
                        <div class="arm-metric-val-row">
                            <span class="arm-metric-num">87</span>
                            <span class="arm-metric-unit">/ 100</span>
                        </div>
                    </div>
                    <div class="arm-metric-cell">
                        <div class="arm-metric-label">KEYWORD MATCH</div>
                        <div class="arm-metric-val-row">
                            <span class="arm-metric-num">82%</span>
                        </div>
                    </div>
                </div>

                <div class="arm-vis-bar-wrap">
                    <div class="arm-vis-meta"><span>Experience Relevance</span><strong style="color:#F5F5F7">91%</strong></div>
                    <div class="arm-vis-track"><div class="arm-vis-fill" style="width:91%; background:#A855F7"></div></div>
                </div>

                <div class="arm-vis-bar-wrap">
                    <div class="arm-vis-meta"><span>Impact Assessment</span><strong style="color:#F5F5F7">78%</strong></div>
                    <div class="arm-vis-track"><div class="arm-vis-fill" style="width:78%; background:#3B82F6"></div></div>
                </div>

                <div class="arm-chips-row">
                    <span class="arm-chip matched">Python</span>
                    <span class="arm-chip matched">Spring Boot</span>
                    <span class="arm-chip matched">PostgreSQL</span>
                    <span class="arm-chip missing">AWS Cloud</span>
                    <span class="arm-chip missing">Microservices</span>
                </div>

                <div class="arm-readiness">
                    <span style="width: 8px; height: 8px; border-radius: 50%; background: #34D399;"></span>
                    <span>AI Recommendation: Add cloud architecture evidence to experience section.</span>
                </div>
            </div>
        """)

    render_clean_html('</div></div>')
