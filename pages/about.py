import textwrap
import streamlit as st

def render_clean_html(html_str):
    """Cleanly render HTML by stripping multiline indentation to prevent Markdown code block bugs."""
    if not html_str:
        return
    lines = [line.strip() for line in html_str.splitlines() if line.strip()]
    cleaned = chr(10).join(lines)
    st.markdown(cleaned, unsafe_allow_html=True)

def render_about_page():
    """Renders the official AiResuMind Platform Intelligence & Mission page."""
    render_clean_html("""
    <div style="max-width: 1200px; margin: 0 auto; padding: 20px 0 60px 0;">
        <!-- Header -->
        <div style="text-align: center; margin-bottom: 48px;">
            <div style="display: inline-flex; align-items: center; gap: 8px; background: rgba(255, 255, 255, 0.06); border: 1px solid rgba(255, 255, 255, 0.12); color: #F5F5F7; padding: 6px 18px; border-radius: 9999px; font-size: 12.5px; font-weight: 600; margin-bottom: 20px; letter-spacing: 0.04em;">
                AiResuMind • Platform Vision & Architecture
            </div>
            <h1 style="font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', sans-serif !important; font-size: 48px !important; font-weight: 800 !important; color: #FFFFFF !important; letter-spacing: -0.03em !important; margin: 0 0 16px 0;">
                AI-Powered Career Intelligence Engine
            </h1>
            <p style="font-size: 18px; color: #86868B; max-width: 800px; margin: 0 auto; line-height: 1.6;">
                Engineered for job seekers, students, professionals, and career switchers aiming for high-impact corporate and tech roles.
            </p>
        </div>

        <!-- Mission Card 1 -->
        <div style="background: #121215; border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 24px; padding: 36px; margin-bottom: 28px;">
            <div style="font-size: 12px; font-weight: 700; color: #86868B; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 12px;">SINGLE INTELLIGENT WORKSPACE</div>
            <h2 style="font-size: 26px; font-weight: 800; color: #F5F5F7; margin: 0 0 16px 0;">All-in-One Candidate Intelligence</h2>
            <p style="font-size: 16px; color: #86868B; line-height: 1.7; margin: 0 0 20px 0;">
                AiResuMind is an AI-powered career intelligence platform built for job seekers, students, professionals, and career switchers. Audit resumes against ATS algorithms, optimize every section with actionable AI feedback, generate tailored resumes and cover letters, and prepare for interviews—all from a single intelligent workspace.
            </p>
            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; margin-top: 24px;">
                <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.06); padding: 18px; border-radius: 16px;">
                    <div style="font-size: 14px; font-weight: 700; color: #F5F5F7; margin-bottom: 6px;">ATS Scoring Engine</div>
                    <div style="font-size: 13px; color: #86868B;">Deep semantic evaluation against screening algorithms.</div>
                </div>
                <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.06); padding: 18px; border-radius: 16px;">
                    <div style="font-size: 14px; font-weight: 700; color: #F5F5F7; margin-bottom: 6px;">Document Generator</div>
                    <div style="font-size: 13px; color: #86868B;">Instant Executive, Academic & Modern PDF/DOCX export.</div>
                </div>
                <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.06); padding: 18px; border-radius: 16px;">
                    <div style="font-size: 14px; font-weight: 700; color: #30D158; margin-bottom: 6px;">AI Recruiter Coach</div>
                    <div style="font-size: 13px; color: #86868B;">Actionable feedback explaining recruiter scan rationale.</div>
                </div>
            </div>
        </div>

        <!-- Mission Card 2 -->
        <div style="background: #121215; border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 24px; padding: 36px; margin-bottom: 28px;">
            <div style="font-size: 12px; font-weight: 700; color: #86868B; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 12px;">NATIVE APPLICATION INTERFACE</div>
            <h2 style="font-size: 26px; font-weight: 800; color: #F5F5F7; margin: 0 0 16px 0;">Interactive vs Static Keyword Stuffing</h2>
            <p style="font-size: 16px; color: #86868B; line-height: 1.7; margin: 0;">
                Unlike traditional resume builders that rely on generic templates and keyword stuffing, AiResuMind delivers a fully interactive career intelligence platform. Every ATS report, resume preview, keyword analysis, AI suggestion, and interview insight is rendered as a native application interface—creating a premium experience that feels fast, modern, and production-ready.
            </p>
        </div>

        <!-- Mission Card 3 -->
        <div style="background: #121215; border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 24px; padding: 36px;">
            <div style="font-size: 12px; font-weight: 700; color: #86868B; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 12px;">UNIFIED DESIGN SYSTEM</div>
            <h2 style="font-size: 26px; font-weight: 800; color: #F5F5F7; margin: 0 0 16px 0;">Enterprise-Grade Polish & Customization</h2>
            <p style="font-size: 16px; color: #86868B; line-height: 1.7; margin: 0;">
                Every component is fully responsive, customizable, and engineered for clarity. Colors, typography, spacing, and dashboards are driven by a unified design system, allowing you to personalize the platform while maintaining a polished, enterprise-grade appearance. Whether you're targeting your first internship, a FAANG opportunity, or an executive role, AiResuMind helps you build application materials that are optimized for both recruiters and modern Applicant Tracking Systems.
            </p>
        </div>
    </div>
    """)
