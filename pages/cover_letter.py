import textwrap

def render_clean_html(html_str):
    """Cleanly render HTML by stripping multiline indentation to prevent Markdown code block bugs."""
    if not html_str:
        return
    lines = [line.strip() for line in html_str.splitlines() if line.strip()]
    cleaned = chr(10).join(lines)
    st.markdown(cleaned, unsafe_allow_html=True)

import streamlit as st
from utils.cover_letter import CoverLetterGenerator

def render_cover_letter_page():
    """Renders the modular AI Cover Letter & Outreach Suite Page with Dark Glassmorphic Design."""
    render_clean_html("""
        <div style="margin-bottom: 2rem;">
            <div style="font-size: 13px; font-weight: 800; color: #5EEAD4; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 8px;">
                CANDIDATE OUTREACH SUITE
            </div>
            <h1 style="font-size: 42px !important; font-weight: 900 !important; color: #FFFFFF !important; margin-bottom: 8px !important;">
                AI Cover Letter & Outreach Generator
            </h1>
            <p style="color: #94A3B8; font-size: 17px; margin-top: 0;">
                Generate compelling cover letters, recruiter cold emails, LinkedIn DMs, and post-interview follow-ups tailored to your target role.
            </p>
        </div>
    """)
    
    col1, col2 = st.columns(2, gap="large")
    with col1:
        job_title = st.text_input("TARGET JOB TITLE", placeholder="e.g. Senior Backend Engineer", key="cl_job_title")
        company = st.text_input("COMPANY NAME", placeholder="e.g. Google, Microsoft", key="cl_company")
        tone = st.selectbox("TONE & STYLE", ["Professional & Executive", "Enthusiastic & Modern", "Concise & Direct", "Creative"], key="cl_tone")
    with col2:
        jd_text = st.text_area("JOB DESCRIPTION (OPTIONAL)", placeholder="Paste JD text here for tailored keyword alignment...", height=110, key="cl_jd")
        user_notes = st.text_area("KEY ACCOMPLISHMENTS / NOTES (OPTIONAL)", placeholder="e.g. Scaled API throughput to 10M req/day...", height=110, key="cl_notes")
        
    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
    if st.button(" GENERATE COVER LETTER & OUTREACH", type="primary", use_container_width=True, key="cl_gen_btn"):
        if job_title.strip():
            with st.spinner("AI is crafting customized cover letter and outreach templates..."):
                cl_gen = CoverLetterGenerator()
                letter = cl_gen.generate_cover_letter(job_title, company, tone, jd_text, user_notes)
                
                tab_cl, tab_email, tab_linkedin = st.tabs([" Cover Letter", " Recruiter Cold Email", " LinkedIn Connection DM"])
                
                with tab_cl:
                    st.markdown("<h3 style='color: #FFFFFF; font-weight: 800; font-size: 22px; margin-top: 16px;'>Tailored Executive Cover Letter</h3>", unsafe_allow_html=True)
                    render_clean_html(f"""
                        <div class="editorial-card" style="white-space: pre-wrap; color: #FFFFFF; font-size: 15.5px; line-height: 1.75;">
                            {letter}
                        </div>
                    """)
                    
                with tab_email:
                    recruiter_email = f"Subject: Application for {job_title} position at {company or 'your company'}\n\nDear Hiring Manager,\n\nI recently came across the {job_title} role at {company or 'your company'} and wanted to reach out directly. With my background in technology development and automated systems, I am confident in my ability to add immediate value to your team.\n\nI have attached my ATS-optimized resume for your review. Would you be open to a brief 10-minute call next week to discuss how my skill set aligns with your team's goals?\n\nBest regards,\nCandidate"
                    render_clean_html(f"""
                        <div class="editorial-card" style="white-space: pre-wrap; color: #FFFFFF; font-size: 15.5px; line-height: 1.75;">
                            {recruiter_email}
                        </div>
                    """)
                    
                with tab_linkedin:
                    linkedin_dm = f"Hi [Recruiter Name], I saw the {job_title} position at {company or 'your team'} and was thoroughly impressed by your company's recent engineering work. Given my background building scalable AI software systems, I'd love to connect and share my resume!"
                    render_clean_html(f"""
                        <div class="editorial-card" style="white-space: pre-wrap; color: #FFFFFF; font-size: 15.5px; line-height: 1.75;">
                            {linkedin_dm}
                        </div>
                    """)
        else:
            st.warning("Please enter a Target Job Title.")
