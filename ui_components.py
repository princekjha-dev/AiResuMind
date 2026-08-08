import streamlit as st
import textwrap
from ui.components.Navigation import render_navigation
from ui.components.Footer import render_footer as ui_render_footer
from ui.components.Hero import render_hero
from ui.components.PageHeader import render_page_header
from ui.components.Card import render_card
from ui.components.MetricCard import render_metric_card


def render_clean_html(html_str):
    """Cleanly render HTML by stripping multiline indentation to prevent Markdown code block bugs."""
    if not html_str:
        return
    lines = [line.strip() for line in html_str.splitlines() if line.strip()]
    cleaned = chr(10).join(lines)
    st.markdown(cleaned, unsafe_allow_html=True)


def apply_modern_styles():
    """Apply modern master dark glass stylesheet"""
    with open("style/style.css", "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def render_top_nav(active_page="home"):
    """Delegate to ui.components.Navigation"""
    render_navigation(active_page)


def page_header(title, subtitle=None):
    """Delegate to ui.components.PageHeader"""
    render_page_header(title, subtitle)


def hero_section(
    title="Transform Your Resume Into an ATS-Beating Career Engine",
    subtitle="Analyze your resume, optimize it for real job descriptions, and build stronger applications with AI-powered career intelligence.",
    *args,
    **kwargs,
):
    """Delegate to ui.components.Hero"""
    render_hero(title, subtitle)


def feature_card(icon_class, title, description):
    """Delegate to ui.components.Card"""
    render_card(title, description, icon_class)


def render_trusted_by_section():
    """SECTION 2 — SOCIAL PROOF"""
    render_clean_html("""
        <div style="text-align: center; margin: 60px 0; padding: 40px 0; border-top: 1px solid rgba(255, 255, 255, 0.08); border-bottom: 1px solid rgba(255, 255, 255, 0.08);">
            <p style="font-size: 18px; font-weight: 500; color: #86868B; margin-bottom: 32px; letter-spacing: -0.01em;">
                Built for candidates who want more than keyword stuffing.
            </p>
            <div style="display: flex; justify-content: center; align-items: center; gap: 48px; flex-wrap: wrap; font-size: 15px; font-weight: 600; color: #F5F5F7;">
                <div style="display: flex; align-items: center; gap: 10px;">
                    <i class="fa-solid fa-bullseye" style="color: #60A5FA;"></i>
                    <span>ATS Optimization</span>
                </div>
                <div style="display: flex; align-items: center; gap: 10px;">
                    <i class="fa-solid fa-brain" style="color: #A855F7;"></i>
                    <span>Resume Intelligence</span>
                </div>
                <div style="display: flex; align-items: center; gap: 10px;">
                    <i class="fa-solid fa-sliders" style="color: #34D399;"></i>
                    <span>Job Matching</span>
                </div>
                <div style="display: flex; align-items: center; gap: 10px;">
                    <i class="fa-solid fa-wand-magic-sparkles" style="color: #EC4899;"></i>
                    <span>AI Career Tools</span>
                </div>
            </div>
        </div>
    """)


def render_feature_cards_grid():
    """SECTION 3 — PRODUCT EXPERIENCE (Everything you need to build a stronger application)"""
    render_clean_html("""
        <div style="text-align: center; margin-bottom: 56px;">
            <div style="font-size: 12px; font-weight: 700; color: #60A5FA; text-transform: uppercase; letter-spacing: 0.12em; margin-bottom: 12px;">
                INTELLIGENT SUITE
            </div>
            <h2 style="font-size: 48px !important; font-weight: 800 !important; color: #F5F5F7 !important; margin: 0 0 16px 0; letter-spacing: -0.03em;">
                Everything you need to build a stronger application.
            </h2>
            <p style="color: #86868B; font-size: 18px; max-width: 640px; margin: 0 auto; font-weight: 400; line-height: 1.6;">
                Real UI workflows engineered to transform candidate performance at every stage.
            </p>
        </div>
    """)

    features = [
        {
            "tag": "01 / AUDIT",
            "title": "Resume Analyzer",
            "description": "Deep semantic parsing benchmarking your document against top ATS screeners and target job descriptions.",
        },
        {
            "tag": "02 / GENERATION",
            "title": "Resume Builder",
            "description": "Prompt-based AI resume architect creating ATS-compliant executive resumes tailored to any job prompt.",
        },
        {
            "tag": "03 / OUTREACH",
            "title": "Cold Mail Generator",
            "description": "Generate personalized executive cold emails and LinkedIn messages with high response rates.",
        },
        {
            "tag": "04 / MATCHING",
            "title": "Job Search",
            "description": "Search active job openings across global tech platforms with real-time AI match scoring.",
        },
    ]

    cols1 = st.columns(2, gap="large")
    for idx in range(2):
        f = features[idx]
        with cols1[idx]:
            render_clean_html(f"""
                <div class="editorial-card" style="background: rgba(255,255,255,0.035); border: 1px solid rgba(255,255,255,0.08); border-radius: 24px; padding: 36px; height: 100%;">
                    <div style="font-size: 11px; font-weight: 700; color: #A855F7; margin-bottom: 12px; letter-spacing: 0.08em;">{f['tag']}</div>
                    <h3 style="font-size: 26px; font-weight: 700; color: #F5F5F7; margin: 0 0 12px 0; letter-spacing: -0.02em;">{f['title']}</h3>
                    <p style="font-size: 15px; color: #86868B; line-height: 1.6; margin: 0;">{f['description']}</p>
                </div>
            """)

    render_clean_html("<div style='height: 24px;'></div>")

    cols2 = st.columns(2, gap="large")
    for idx in range(2, 4):
        f = features[idx]
        with cols2[idx - 2]:
            render_clean_html(f"""
                <div class="editorial-card" style="background: rgba(255,255,255,0.035); border: 1px solid rgba(255,255,255,0.08); border-radius: 24px; padding: 36px; height: 100%;">
                    <div style="font-size: 11px; font-weight: 700; color: #A855F7; margin-bottom: 12px; letter-spacing: 0.08em;">{f['tag']}</div>
                    <h3 style="font-size: 26px; font-weight: 700; color: #F5F5F7; margin: 0 0 12px 0; letter-spacing: -0.02em;">{f['title']}</h3>
                    <p style="font-size: 15px; color: #86868B; line-height: 1.6; margin: 0;">{f['description']}</p>
                </div>
            """)


def render_product_showcase():
    """SECTION 5 — CAREER TOOLS GRID"""
    render_clean_html("""
        <div style="margin: 96px 0 48px 0; text-align: center;">
            <div style="font-size: 12px; font-weight: 700; color: #60A5FA; text-transform: uppercase; letter-spacing: 0.12em; margin-bottom: 12px;">
                COMPLETE PLATFORM
            </div>
            <h2 style="font-size: 48px !important; font-weight: 800 !important; color: #F5F5F7 !important; margin: 0 0 16px 0; letter-spacing: -0.03em;">
                Engineered for candidate success.
            </h2>
            <p style="color: #86868B; font-size: 18px; max-width: 640px; margin: 0 auto; line-height: 1.6;">
                A unified system designed to give you an unfair advantage in every job hunt.
            </p>
        </div>
    """)

    tools = [
        {
            "icon": "fa-file-shield",
            "title": "Single-Column ATS Layout",
            "desc": "Standardized layouts guaranteed to parse with zero errors across Workday, Greenhouse, and Lever.",
        },
        {
            "icon": "fa-chart-line-up",
            "title": "STAR Method Reframing",
            "desc": "Automatically rewrite plain bullet points into metric-rich Situation, Task, Action, Result achievements.",
        },
        {
            "icon": "fa-fire",
            "title": "Recruiter Roast Mode",
            "desc": "Brutally honest feedback highlighting vague phrasing, missing metrics, and formatting weaknesses.",
        },
        {
            "icon": "fa-paper-plane",
            "title": "1-Click PDF / DOCX Export",
            "desc": "Download clean, perfectly formatted executive resume files ready to submit to recruiters.",
        },
    ]

    cols = st.columns(4, gap="medium")
    for idx, t in enumerate(tools):
        with cols[idx]:
            render_clean_html(f"""
                <div class="editorial-card" style="background: rgba(255,255,255,0.035); border: 1px solid rgba(255,255,255,0.08); border-radius: 20px; padding: 28px;">
                    <div style="width: 44px; height: 44px; border-radius: 12px; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.08); display: flex; align-items: center; justify-content: center; font-size: 18px; color: #60A5FA; margin-bottom: 20px;">
                        <i class="fa-solid {t['icon']}"></i>
                    </div>
                    <h4 style="font-size: 18px; font-weight: 700; color: #F5F5F7; margin: 0 0 8px 0;">{t['title']}</h4>
                    <p style="font-size: 13.5px; color: #86868B; line-height: 1.5; margin: 0;">{t['desc']}</p>
                </div>
            """)


def render_analytics_preview_section():
    """SECTION 4 — RESUME INTELLIGENCE DEEP DIAGNOSTICS"""
    render_clean_html("""
        <div style="margin: 96px 0 40px 0; text-align: center;">
            <div style="font-size: 12px; font-weight: 700; color: #60A5FA; text-transform: uppercase; letter-spacing: 0.12em; margin-bottom: 12px;">
                DEEP DIAGNOSTICS
            </div>
            <h2 style="font-size: 48px !important; font-weight: 800 !important; color: #F5F5F7 !important; margin: 0 0 16px 0; letter-spacing: -0.03em;">
                Know exactly what your resume is missing.
            </h2>
            <p style="color: #86868B; font-size: 18px; max-width: 640px; margin: 0 auto 40px auto; line-height: 1.6;">
                Comprehensive scoring algorithms evaluating keyword density, formatting compliance, and impact metrics.
            </p>
        </div>

        <div style="background: #12141A; border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 28px; padding: 40px; box-shadow: 0 40px 100px rgba(0,0,0,0.7); margin-bottom: 56px;">
            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-bottom: 24px;">
                <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.07); border-radius: 18px; padding: 22px;">
                    <div style="font-size: 11px; font-weight: 700; color: #6E6E73; text-transform: uppercase; margin-bottom: 6px;">OVERALL ATS SCORE</div>
                    <div style="font-size: 32px; font-weight: 800; color: #F5F5F7;">94 / 100</div>
                    <div style="font-size: 13px; color: #10B981; font-weight: 600; margin-top: 4px;">Top 3% Candidate Cohort</div>
                </div>

                <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.07); border-radius: 18px; padding: 22px;">
                    <div style="font-size: 11px; font-weight: 700; color: #6E6E73; text-transform: uppercase; margin-bottom: 6px;">KEYWORD DENSITY</div>
                    <div style="font-size: 32px; font-weight: 800; color: #F5F5F7;">96%</div>
                    <div style="font-size: 13px; color: #86868B; font-weight: 500; margin-top: 4px;">18/20 High-Density Keywords Matched</div>
                </div>

                <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.07); border-radius: 18px; padding: 22px;">
                    <div style="font-size: 11px; font-weight: 700; color: #6E6E73; text-transform: uppercase; margin-bottom: 6px;">RECRUITER READINESS</div>
                    <div style="font-size: 32px; font-weight: 800; color: #F5F5F7;">VERIFIED</div>
                    <div style="font-size: 13px; color: #10B981; font-weight: 600; margin-top: 4px;">Passed Executive Screening</div>
                </div>
            </div>
        </div>
    """)


def render_primary_cta():
    """SECTION 6 — FINAL CTA"""
    render_clean_html("""
        <div style="background: linear-gradient(135deg, #12141C 0%, #1A1C28 100%); border: 1px solid rgba(255, 255, 255, 0.12); border-radius: 32px; padding: 72px 40px; text-align: center; margin: 96px 0 64px 0; box-shadow: 0 40px 100px rgba(0,0,0,0.7);">
            <h2 style="font-size: 56px !important; font-weight: 800 !important; color: #F5F5F7 !important; margin-bottom: 24px !important; letter-spacing: -0.04em; line-height: 1.08;">
                Your next opportunity<br>starts with a better application.
            </h2>
            <p style="color: #86868B; font-size: 18px; max-width: 600px; margin: 0 auto 40px auto; line-height: 1.6;">
                Upload your document now to receive instant ATS scoring, detailed skill gap analysis, and executive recommendations.
            </p>
        </div>
    """)

    col1, col2, col3 = st.columns([1, 1.3, 1])
    with col2:
        if st.button(
            "Start AI Resume Audit (Free to try)",
            key="primary_cta_btn",
            type="primary",
            use_container_width=True,
        ):
            st.session_state.page = "resume_analyzer"
            st.rerun()


def render_footer():
    """Delegate to ui.components.Footer"""
    ui_render_footer()