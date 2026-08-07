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
    title="Transform Your Resume into an ATS-Beating Executive Asset",
    subtitle="Receive high-precision AI feedback, benchmark keyword alignment against top job descriptions, and generate executive-ready documents engineered to pass screening filters.",
    *args,
    **kwargs,
):
    """Delegate to ui.components.Hero"""
    render_hero(title, subtitle)


def feature_card(icon_class, title, description):
    """Delegate to ui.components.Card"""
    render_card(title, description, icon_class)


def render_trusted_by_section():
    """Render Trusted By Tech Logos Section"""
    render_clean_html("""
        <div style="text-align: center; margin: 40px 0 64px 0; padding: 32px 0; border-top: 1px solid rgba(255, 255, 255, 0.08); border-bottom: 1px solid rgba(255, 255, 255, 0.08);">
            <div style="font-size: 11.5px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.14em; color: #6B7280; margin-bottom: 24px;">
                TRUSTED BY CANDIDATES LANDING OFFERS AT GLOBAL TECH LEADERS
            </div>
            <div style="display: flex; justify-content: center; align-items: center; gap: 48px; flex-wrap: wrap; font-size: 19px; font-weight: 700; color: #E5E7EB; letter-spacing: -0.02em;">
                <span>Google</span>
                <span>Microsoft</span>
                <span>OpenAI</span>
                <span>Amazon</span>
                <span>Stripe</span>
                <span>Meta</span>
                <span>Apple</span>
                <span>Adobe</span>
            </div>
        </div>
    """)


def render_feature_cards_grid():
    """Render 6 Executive Bento Cards grid in Apple/Linear style"""
    render_clean_html("""
        <div style="text-align: center; margin-bottom: 56px;">
            <div style="font-size: 12px; font-weight: 700; color: #60A5FA; text-transform: uppercase; letter-spacing: 0.12em; margin-bottom: 10px;">
                ENGINEERED FOR ATS DOMINANCE
            </div>
            <h2 style="font-size: 44px !important; font-weight: 800 !important; color: #FFFFFF !important; margin: 0 0 14px 0; letter-spacing: -0.03em;">
                Comprehensive AI Career Suite
            </h2>
            <p style="color: #9CA3AF; font-size: 17.5px; max-width: 640px; margin: 0 auto; font-weight: 400; line-height: 1.6;">
                Every tool is built specifically to maximize recruiter response rates, pass screening algorithms, and land executive interviews.
            </p>
        </div>
    """)

    features = [
        {
            "tag": "01",
            "title": "ATS Keyword Parser",
            "description": "Deep semantic evaluation matching your experience against target ATS screening algorithms and recruiter search queries.",
        },
        {
            "tag": "02",
            "title": "Prompt-Based AI Resume Builder",
            "description": "Craft executive-level, ATS-compliant resumes with AI-recommended action verbs, industry phrasing, and clean structure.",
        },
        {
            "tag": "03",
            "title": "Single-Column ATS Formatting",
            "description": "Ensure your resume adheres to single-column, standard-font ATS parsing rules guaranteed to parse cleanly.",
        },
        {
            "tag": "04",
            "title": "Personalized Cold Email Generator",
            "description": "Paste job URLs or recruiter profiles to generate targeted cold emails, LinkedIn DMs, and follow-ups with high response rates.",
        },
        {
            "tag": "05",
            "title": "Smart Job Matcher",
            "description": "Search active job listings from LinkedIn, Indeed, and Naukri with AI resume match percentages.",
        },
        {
            "tag": "06",
            "title": "Executive Career Telemetry",
            "description": "Track your application response metrics, resume iteration scores, and skill competency gap analysis over time.",
        },
    ]

    cols1 = st.columns(3, gap="medium")
    for idx in range(3):
        f = features[idx]
        with cols1[idx]:
            render_clean_html(f"""
                <div class="editorial-card">
                    <div style="font-size: 12px; font-weight: 700; color: #3B82F6; margin-bottom: 12px; letter-spacing: 0.05em;">{f['tag']}</div>
                    <h3 style="font-size: 20px; font-weight: 700; color: #FFFFFF; margin: 0 0 10px 0; letter-spacing: -0.01em;">{f['title']}</h3>
                    <p style="font-size: 14.5px; color: #9CA3AF; line-height: 1.6; margin: 0; font-weight: 400;">{f['description']}</p>
                </div>
            """)

    render_clean_html("<div style='height: 24px;'></div>")

    cols2 = st.columns(3, gap="medium")
    for idx in range(3, 6):
        f = features[idx]
        with cols2[idx - 3]:
            render_clean_html(f"""
                <div class="editorial-card">
                    <div style="font-size: 12px; font-weight: 700; color: #9333EA; margin-bottom: 12px; letter-spacing: 0.05em;">{f['tag']}</div>
                    <h3 style="font-size: 20px; font-weight: 700; color: #FFFFFF; margin: 0 0 10px 0; letter-spacing: -0.01em;">{f['title']}</h3>
                    <p style="font-size: 14.5px; color: #9CA3AF; line-height: 1.6; margin: 0; font-weight: 400;">{f['description']}</p>
                </div>
            """)


def render_product_showcase():
    """Render 4-step workflow showcase"""
    render_clean_html("""
        <div style="margin: 80px 0 48px 0; text-align: center;">
            <div style="font-size: 12px; font-weight: 700; color: #60A5FA; text-transform: uppercase; letter-spacing: 0.12em; margin-bottom: 10px;">
                WORKFLOW ACCELERATOR
            </div>
            <h2 style="font-size: 44px !important; font-weight: 800 !important; color: #FFFFFF !important; margin: 0 0 14px 0; letter-spacing: -0.03em;">
                Four Steps from Upload to Offer
            </h2>
            <p style="color: #9CA3AF; font-size: 17.5px; max-width: 640px; margin: 0 auto; line-height: 1.6;">
                Our AI workflow transforms your raw resume into a high-converting candidate portfolio.
            </p>
        </div>
    """)

    steps = [
        {
            "num": "01",
            "title": "Upload Resume",
            "desc": "Drag and drop your PDF or DOCX resume. Our parser extracts all work experience, skills, and formatting data instantly.",
        },
        {
            "num": "02",
            "title": "AI Deep Analysis",
            "desc": "We benchmark your document against 50+ ATS screening rules, recruiter search keywords, and industry metrics.",
        },
        {
            "num": "03",
            "title": "ATS Optimization",
            "desc": "Receive instant feedback, missing high-impact keywords, quantified achievement suggestions, and brutal roast mode critique.",
        },
        {
            "num": "04",
            "title": "Export & Land Offers",
            "desc": "Download your ATS-optimized resume, generate targeted cold emails, and practice mock interviews to ace your application.",
        },
    ]

    cols = st.columns(4, gap="medium")
    for idx, s in enumerate(steps):
        with cols[idx]:
            render_clean_html(f"""
                <div class="editorial-card" style="border-top: 2px solid #3B82F6 !important;">
                    <div style="font-size: 32px; font-weight: 800; color: #FFFFFF; margin-bottom: 12px; letter-spacing: -0.03em;">{s['num']}</div>
                    <h3 style="font-size: 19px; font-weight: 700; color: #FFFFFF; margin: 0 0 10px 0;">{s['title']}</h3>
                    <p style="font-size: 14px; color: #9CA3AF; line-height: 1.6; margin: 0;">{s['desc']}</p>
                </div>
            """)


def render_analytics_preview_section():
    """Render executive Telemetry Section dark analytics panel"""
    render_clean_html("""
        <div style="margin: 96px 0 40px 0; text-align: center;">
            <div style="font-size: 12px; font-weight: 700; color: #60A5FA; text-transform: uppercase; letter-spacing: 0.12em; margin-bottom: 10px;">
                EXECUTIVE TELEMETRY
            </div>
            <h2 style="font-size: 44px !important; font-weight: 800 !important; color: #FFFFFF !important; margin: 0 0 14px 0; letter-spacing: -0.03em;">
                Real-Time AI Analytics & Trajectory Insights
            </h2>
            <p style="color: #9CA3AF; font-size: 17.5px; max-width: 640px; margin: 0 auto 40px auto; line-height: 1.6;">
                Monitor your application callback rates, skill competency progression, and ATS keyword optimization over time.
            </p>
        </div>

        <div style="background: #0A0A0F; border: 1px solid rgba(255, 255, 255, 0.10); border-radius: 24px; padding: 40px; box-shadow: 0 30px 60px rgba(0,0,0,0.8); margin-bottom: 56px;">
            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-bottom: 24px;">
                <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 18px; padding: 22px;">
                    <div style="font-size: 11.5px; font-weight: 700; color: #6B7280; text-transform: uppercase; margin-bottom: 6px;">Profile Signal</div>
                    <div style="font-size: 22px; font-weight: 800; color: #FFFFFF;">Executive Alignment</div>
                    <div style="font-size: 13px; color: #10B981; font-weight: 600; margin-top: 4px;">Top 4% Candidate Cohort</div>
                </div>

                <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 18px; padding: 22px;">
                    <div style="font-size: 11.5px; font-weight: 700; color: #6B7280; text-transform: uppercase; margin-bottom: 6px;">Keyword Lift</div>
                    <div style="font-size: 22px; font-weight: 800; color: #FFFFFF;">+14.2% ATS Gain</div>
                    <div style="font-size: 13px; color: #9CA3AF; font-weight: 500; margin-top: 4px;">18/20 High-Density Keywords Matched</div>
                </div>

                <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 18px; padding: 22px;">
                    <div style="font-size: 11.5px; font-weight: 700; color: #6B7280; text-transform: uppercase; margin-bottom: 6px;">Recruiter Response Rate</div>
                    <div style="font-size: 22px; font-weight: 800; color: #FFFFFF;">3.8x Industry Baseline</div>
                    <div style="font-size: 13px; color: #10B981; font-weight: 600; margin-top: 4px;">Verified High Callback Potential</div>
                </div>
            </div>
        </div>
    """)


def render_primary_cta():
    """Render full-width Primary CTA section below Feature Cards"""
    render_clean_html("""
        <div style="background: linear-gradient(135deg, rgba(10,10,15,0.9) 0%, rgba(18,18,24,0.95) 100%); border: 1px solid rgba(59, 130, 246, 0.25); border-radius: 28px; padding: 60px; text-align: center; margin: 88px 0 48px 0; box-shadow: 0 30px 60px rgba(0,0,0,0.8);">
            <h2 style="font-size: 44px !important; font-weight: 800 !important; color: #FFFFFF !important; margin-bottom: 16px !important; letter-spacing: -0.03em;">Ready to Benchmark Your Resume?</h2>
            <p style="color: #9CA3AF; font-size: 18px; max-width: 660px; margin: 0 auto 36px auto; line-height: 1.6;">Upload your document now to receive instant ATS scoring, detailed skill gap analysis, and executive recommendations.</p>
        </div>
    """)

    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        if st.button(
            "Start Free Candidate Audit Now",
            key="primary_cta_btn",
            type="primary",
            use_container_width=True,
        ):
            st.session_state.page = "resume_analyzer"
            st.rerun()


def render_footer():
    """Delegate to ui.components.Footer"""
    ui_render_footer()