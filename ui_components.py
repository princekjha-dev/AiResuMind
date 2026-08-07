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
    with open('style/style.css', 'r') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def render_top_nav(active_page='home'):
    """Delegate to ui.components.Navigation"""
    render_navigation(active_page)

def page_header(title, subtitle=None):
    """Delegate to ui.components.PageHeader"""
    render_page_header(title, subtitle)

def hero_section(title="Transform Your Resume into an ATS-Beating Executive Asset", 
                 subtitle="Receive high-precision AI feedback, benchmark keyword alignment against top job descriptions, and generate executive-ready documents engineered to pass screening filters.",
                 *args, **kwargs):
    """Delegate to ui.components.Hero"""
    render_hero(title, subtitle)

def feature_card(icon_class, title, description):
    """Delegate to ui.components.Card"""
    render_card(title, description, icon_class)

def render_trusted_by_section():
    """Render Trusted By Tech Logos Section"""
    render_clean_html("""
        <div style="text-align: center; margin: 48px 0 72px 0; padding: 36px 0; border-top: 1px solid rgba(255, 255, 255, 0.08); border-bottom: 1px solid rgba(255, 255, 255, 0.08);">
            <div style="font-size: 11.5px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.14em; color: #86868B; margin-bottom: 24px;">
                TRUSTED BY CANDIDATES LANDING OFFERS AT GLOBAL TECH LEADERS
            </div>
            <div style="display: flex; justify-content: center; align-items: center; gap: 52px; flex-wrap: wrap; font-size: 20px; font-weight: 800; color: #F5F5F7; letter-spacing: -0.02em;">
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
    """Render 6 Executive Feature Cards grid in Apple 24px rounded cards with zero emojis"""
    render_clean_html("""
        <div style="text-align: center; margin-bottom: 56px;">
            <div style="font-size: 12px; font-weight: 700; color: #86868B; text-transform: uppercase; letter-spacing: 0.12em; margin-bottom: 10px;">
                ENGINEERED FOR ATS DOMINANCE
            </div>
            <h2 style="font-size: 44px !important; font-weight: 800 !important; color: #F5F5F7 !important; margin: 0 0 14px 0; letter-spacing: -0.03em;">
                Comprehensive AI Career Suite
            </h2>
            <p style="color: #86868B; font-size: 18px; max-width: 640px; margin: 0 auto; font-weight: 400;">
                Every component is built specifically to maximize recruiter response rates, pass screening algorithms, and land executive interviews.
            </p>
        </div>
    """)

    features = [
        {
            "tag": "01",
            "title": "ATS Keyword Parser",
            "description": "Deep semantic evaluation matching your experience against target ATS screening algorithms and recruiter search queries."
        },
        {
            "tag": "02",
            "title": "Prompt-Based AI Resume Builder",
            "description": "Craft executive-level, ATS-compliant resumes with AI-recommended action verbs, industry phrasing, and clean structure."
        },
        {
            "tag": "03",
            "title": "AI Single-Column ATS Formatting",
            "description": "Ensure your resume adheres to single-column, standard-font ATS parsing rules guaranteed to parse cleanly."
        },
        {
            "tag": "04",
            "title": "STAR-Based AI Mock Interviews",
            "description": "Practice real-time technical & behavioral questions tailored to your job description with instant AI scoring."
        },
        {
            "tag": "05",
            "title": "Smart Job-Market Insights",
            "description": "Search active job listings from LinkedIn, Indeed, and Naukri with AI resume match percentages."
        },
        {
            "tag": "06",
            "title": "Executive Career Telemetry",
            "description": "Track your application response metrics, resume iteration scores, and skill competency gap analysis over time."
        }
    ]

    cols1 = st.columns(3, gap="medium")
    for idx in range(3):
        f = features[idx]
        with cols1[idx]:
            render_clean_html(f"""
                <div class="editorial-card" style="background: #121215; border: 1px solid rgba(255,255,255,0.1); border-radius: 24px; padding: 28px; height: 100%;">
                    <div style="font-size: 12px; font-weight: 700; color: #86868B; margin-bottom: 12px; letter-spacing: 0.05em;">{f['tag']}</div>
                    <h3 style="font-size: 20px; font-weight: 700; color: #F5F5F7; margin: 0 0 10px 0; letter-spacing: -0.01em;">{f['title']}</h3>
                    <p style="font-size: 14.5px; color: #86868B; line-height: 1.6; margin: 0; font-weight: 400;">{f['description']}</p>
                </div>
            """)

    render_clean_html("<div style='height: 24px;'></div>")

    cols2 = st.columns(3, gap="medium")
    for idx in range(3, 6):
        f = features[idx]
        with cols2[idx - 3]:
            render_clean_html(f"""
                <div class="editorial-card" style="background: #121215; border: 1px solid rgba(255,255,255,0.1); border-radius: 24px; padding: 28px; height: 100%;">
                    <div style="font-size: 12px; font-weight: 700; color: #86868B; margin-bottom: 12px; letter-spacing: 0.05em;">{f['tag']}</div>
                    <h3 style="font-size: 20px; font-weight: 700; color: #F5F5F7; margin: 0 0 10px 0; letter-spacing: -0.01em;">{f['title']}</h3>
                    <p style="font-size: 14.5px; color: #86868B; line-height: 1.6; margin: 0; font-weight: 400;">{f['description']}</p>
                </div>
            """)

def render_product_showcase():
    """Render 4-step workflow showcase with zero emojis"""
    render_clean_html("""
        <div style="margin: 80px 0 48px 0; text-align: center;">
            <div style="font-size: 12px; font-weight: 700; color: #86868B; text-transform: uppercase; letter-spacing: 0.12em; margin-bottom: 10px;">
                HOW IT WORKS
            </div>
            <h2 style="font-size: 44px !important; font-weight: 800 !important; color: #F5F5F7 !important; margin: 0 0 14px 0; letter-spacing: -0.03em;">
                Four Steps from Upload to Offer
            </h2>
            <p style="color: #86868B; font-size: 18px; max-width: 640px; margin: 0 auto;">
                Our AI workflow transforms your raw resume into a high-converting candidate portfolio.
            </p>
        </div>
    """)

    steps = [
        {"num": "01", "title": "Upload Resume", "desc": "Drag and drop your PDF or DOCX resume. Our parser extracts all work experience, skills, and formatting data instantly."},
        {"num": "02", "title": "AI Deep Analysis", "desc": "We benchmark your document against 50+ ATS screening rules, recruiter search keywords, and industry metrics."},
        {"num": "03", "title": "ATS Optimization", "desc": "Receive instant feedback, missing high-impact keywords, quantified achievement suggestions, and brutal roast mode critique."},
        {"num": "04", "title": "Export & Land Offers", "desc": "Download your ATS-optimized resume, generate targeted cover letters, and practice mock interviews to ace your application."}
    ]

    cols = st.columns(4, gap="medium")
    for idx, s in enumerate(steps):
        with cols[idx]:
            render_clean_html(f"""
                <div class="editorial-card" style="background: #121215; border: 1px solid rgba(255,255,255,0.1); border-top: 2px solid #F5F5F7; border-radius: 24px; padding: 28px; height: 100%;">
                    <div style="font-size: 32px; font-weight: 800; color: #F5F5F7; margin-bottom: 12px; letter-spacing: -0.03em;">{s['num']}</div>
                    <h3 style="font-size: 19px; font-weight: 700; color: #F5F5F7; margin: 0 0 10px 0;">{s['title']}</h3>
                    <p style="font-size: 14px; color: #86868B; line-height: 1.65; margin: 0;">{s['desc']}</p>
                </div>
            """)

def render_analytics_preview_section():
    """Render executive Telemetry Section dark analytics panel with zero emojis"""
    render_clean_html("""
        <div style="margin: 96px 0 40px 0; text-align: center;">
            <div style="font-size: 12px; font-weight: 700; color: #86868B; text-transform: uppercase; letter-spacing: 0.12em; margin-bottom: 10px;">
                EXECUTIVE TELEMETRY
            </div>
            <h2 style="font-size: 44px !important; font-weight: 800 !important; color: #F5F5F7 !important; margin: 0 0 14px 0; letter-spacing: -0.03em;">
                Real-Time AI Analytics & Trajectory Insights
            </h2>
            <p style="color: #86868B; font-size: 18px; max-width: 640px; margin: 0 auto 40px auto;">
                Monitor your application callback rates, skill competency progression, and ATS keyword optimization over time.
            </p>
        </div>

        <div style="background: #0A0A0C; border: 1px solid rgba(255, 255, 255, 0.12); border-radius: 24px; padding: 40px; box-shadow: 0 30px 60px rgba(0,0,0,0.8); margin-bottom: 56px;">
            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-bottom: 24px;">
                <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 18px; padding: 22px;">
                    <div style="font-size: 11.5px; font-weight: 700; color: #86868B; text-transform: uppercase; margin-bottom: 6px;">Profile Signal</div>
                    <div style="font-size: 22px; font-weight: 800; color: #F5F5F7;">Executive Alignment</div>
                    <div style="font-size: 13px; color: #30D158; font-weight: 600; margin-top: 4px;">Top 4% Candidate Cohort</div>
                </div>

                <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 18px; padding: 22px;">
                    <div style="font-size: 11.5px; font-weight: 700; color: #86868B; text-transform: uppercase; margin-bottom: 6px;">Keyword Lift</div>
                    <div style="font-size: 22px; font-weight: 800; color: #F5F5F7;">+14.2% ATS Gain</div>
                    <div style="font-size: 13px; color: #86868B; font-weight: 500; margin-top: 4px;">18/20 High-Density Keywords Matched</div>
                </div>

                <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 18px; padding: 22px;">
                    <div style="font-size: 11.5px; font-weight: 700; color: #86868B; text-transform: uppercase; margin-bottom: 6px;">Recruiter Response Rate</div>
                    <div style="font-size: 22px; font-weight: 800; color: #30D158;">3.4x Baseline</div>
                    <div style="font-size: 13px; color: #86868B; font-weight: 500; margin-top: 4px;">Verified Recruiter Search Visibility</div>
                </div>
            </div>

            <div style="background: rgba(255, 255, 255, 0.04); border: 1px solid rgba(255, 255, 255, 0.12); border-radius: 18px; padding: 22px 26px;">
                <div style="font-size: 13px; font-weight: 700; color: #F5F5F7; margin-bottom: 6px; text-transform: uppercase; letter-spacing: 0.04em;">AI Executive Recommendation</div>
                <div style="font-size: 14px; color: #86868B; line-height: 1.6;">
                    "Reframe project achievements using quantified STAR metrics (+15% metric lift) and incorporate missing target domain keywords (SQL, System Design, BRD) to guarantee 95%+ ATS parsing accuracy across Workday, Greenhouse, and Lever."
                </div>
            </div>
        </div>
    """)

def render_testimonials_section():
    """Render executive Candidate Testimonials with zero emojis"""
    render_clean_html("""
        <div style="margin: 80px 0 48px 0; text-align: center;">
            <div style="font-size: 12px; font-weight: 700; color: #86868B; text-transform: uppercase; letter-spacing: 0.12em; margin-bottom: 10px;">
                CANDIDATE SUCCESS STORIES
            </div>
            <h2 style="font-size: 44px !important; font-weight: 800 !important; color: #F5F5F7 !important; margin: 0 0 14px 0; letter-spacing: -0.03em;">
                Loved by Engineers, Managers & Executives
            </h2>
        </div>
    """)

    testimonials = [
        {
            "name": "Sarah Jenkins",
            "role": "Staff Software Engineer at Stripe",
            "quote": "AiResuMind helped me identify missing system design keywords that ATS filters were dropping. Increased my interview callback rate by 3x within a week!"
        },
        {
            "name": "David Chen",
            "role": "Product Lead at Vercel",
            "quote": "The AI cover letter generator and interview prep suite saved me dozens of hours. The feedback was brutally honest and ridiculously accurate."
        },
        {
            "name": "Alex Rivera",
            "role": "Senior Data Scientist at Meta",
            "quote": "Going from an ATS score of 62% to 94% completely changed my job search. Passed screening at every Tier 1 tech company I applied to."
        }
    ]

    cols = st.columns(3, gap="medium")
    for idx, t in enumerate(testimonials):
        with cols[idx]:
            render_clean_html(f"""
                <div class="editorial-card" style="background: #121215; border: 1px solid rgba(255,255,255,0.1); border-radius: 24px; padding: 28px;">
                    <p style="color: #F5F5F7; font-size: 15px; line-height: 1.7; margin-bottom: 24px; font-weight: 400;">"{t['quote']}"</p>
                    <div style="border-top: 1px solid rgba(255,255,255,0.08); padding-top: 16px;">
                        <div style="font-weight: 700; color: #F5F5F7; font-size: 15px;">{t['name']}</div>
                        <div style="color: #86868B; font-size: 13px; margin-top: 2px;">{t['role']}</div>
                    </div>
                </div>
            """)

def render_pricing_section():
    """Render transparent SaaS pricing cards in Apple 24px rounded containers with zero emojis"""
    render_clean_html("""
        <div style="margin: 88px 0 48px 0; text-align: center;">
            <div style="font-size: 12px; font-weight: 700; color: #86868B; text-transform: uppercase; letter-spacing: 0.12em; margin-bottom: 10px;">
                SIMPLE TRANSPARENT PRICING
            </div>
            <h2 style="font-size: 44px !important; font-weight: 800 !important; color: #F5F5F7 !important; margin: 0 0 14px 0; letter-spacing: -0.03em;">
                Invest in Your Next Career Move
            </h2>
        </div>
    """)

    plans = [
        {"name": "Free Starter", "price": "$0", "period": "forever", "desc": "Essential ATS checks for job seekers", "features": ["3 AI Resume Scans / mo", "Basic ATS Match Score", "Standard Resume Templates", "Community Support"], "cta": "Get Started Free", "popular": False},
        {"name": "Pro Executive", "price": "$19", "period": "per month", "desc": "Full suite for serious candidates", "features": ["Unlimited AI Resume Analyses", "94%+ ATS Keyword Optimization", "AI STAR Interview Prep Engine", "Job Search & Salary Insights"], "cta": "Start Pro Trial", "popular": True},
        {"name": "Enterprise Coaching", "price": "$49", "period": "per month", "desc": "For executives & career transitions", "features": ["Everything in Pro Plan", "1-on-1 AI Resume Redesign", "Priority Recruiter Email Engine", "Dedicated Career Telemetry", "24/7 Priority Support"], "cta": "Upgrade to Enterprise", "popular": False}
    ]

    cols = st.columns(3, gap="medium")
    for idx, p in enumerate(plans):
        border_style = "border: 1px solid #FFFFFF; box-shadow: 0 0 30px rgba(255, 255, 255, 0.15);" if p['popular'] else "border: 1px solid rgba(255,255,255,0.1);"
        pop_badge = '<div style="background: #F5F5F7; color: #000000; font-size: 11px; font-weight: 800; text-transform: uppercase; padding: 4px 14px; border-radius: 9999px; display: inline-block; margin-bottom: 16px;">MOST POPULAR</div>' if p['popular'] else ''
        
        feats = "".join([f'<div style="font-size: 14px; color: #86868B; margin-bottom: 12px;"><span style="color: #F5F5F7; margin-right: 10px;">•</span> {ft}</div>' for ft in p['features']])
        
        with cols[idx]:
            render_clean_html(f"""
                <div class="editorial-card" style="background: #121215; {border_style} border-radius: 24px; padding: 32px; height: 100%;">
                    {pop_badge}
                    <h3 style="font-size: 22px; font-weight: 700; color: #F5F5F7; margin: 0 0 6px 0;">{p['name']}</h3>
                    <p style="font-size: 14px; color: #86868B; margin-bottom: 20px;">{p['desc']}</p>
                    <div style="font-size: 44px; font-weight: 800; color: #F5F5F7; margin-bottom: 24px; letter-spacing: -0.03em;">{p['price']} <span style="font-size: 14px; font-weight: 500; color: #86868B;">/{p['period']}</span></div>
                    <div style="margin-bottom: 32px;">{feats}</div>
                </div>
            """)
            if st.button(p['cta'], key=f"plan_btn_{idx}", type="primary" if p['popular'] else "secondary", use_container_width=True):
                st.session_state.page = "resume_analyzer"
                st.rerun()

def render_faq_section():
    """Render FAQ accordions with zero emojis"""
    render_clean_html("""
        <div style="margin: 88px 0 40px 0; text-align: center;">
            <div style="font-size: 12px; font-weight: 700; color: #86868B; text-transform: uppercase; letter-spacing: 0.12em; margin-bottom: 10px;">
                FREQUENTLY ASKED QUESTIONS
            </div>
            <h2 style="font-size: 44px !important; font-weight: 800 !important; color: #F5F5F7 !important; margin: 0; letter-spacing: -0.03em;">
                Everything You Need to Know
            </h2>
        </div>
    """)

    faqs = [
        ("How does the ATS Resume Analyzer calculate my score?", "Our AI evaluates your document against 50+ applicant tracking system rules including keyword frequency, quantified metric density, formatting hierarchy, and role competency match."),
        ("Will my resume pass real corporate ATS systems like Workday, Greenhouse, or Lever?", "Yes! All resume templates and content recommendations generated by AiResuMind adhere strictly to single-column, standard-font ATS parsing guidelines guaranteed to parse without table or column corruption."),
        ("Is my uploaded resume data secure?", "Your privacy is guaranteed. Uploaded documents are parsed securely in memory for instant analysis and are never sold or shared with third parties.")
    ]

    for q, a in faqs:
        with st.expander(q):
            st.write(a)

def render_primary_cta():
    """Render full-width Primary CTA section below Feature Cards with zero emojis"""
    render_clean_html("""
        <div style="background: #0A0A0C; border: 1px solid rgba(255, 255, 255, 0.12); border-radius: 28px; padding: 60px; text-align: center; margin: 88px 0 48px 0; box-shadow: 0 30px 60px rgba(0,0,0,0.8);">
            <h2 style="font-size: 44px !important; font-weight: 800 !important; color: #F5F5F7 !important; margin-bottom: 16px !important; letter-spacing: -0.03em;">Ready to Benchmark Your Resume?</h2>
            <p style="color: #86868B; font-size: 18px; max-width: 660px; margin: 0 auto 36px auto;">Upload your document now to receive instant ATS scoring, detailed skill gap analysis, and executive recommendations.</p>
        </div>
    """)
    
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        if st.button("Upload & Analyze Resume Now", key="primary_cta_btn", type="primary", use_container_width=True):
            st.session_state.page = "resume_analyzer"
            st.rerun()

def render_footer():
    """Delegate to ui.components.Footer"""
    ui_render_footer()