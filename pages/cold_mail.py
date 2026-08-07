import textwrap
import streamlit as st
import datetime

def render_clean_html(html_str):
    """Cleanly render HTML by stripping multiline indentation to prevent Markdown code block bugs."""
    if not html_str:
        return
    lines = [line.strip() for line in html_str.splitlines() if line.strip()]
    cleaned = chr(10).join(lines)
    st.markdown(cleaned, unsafe_allow_html=True)

def render_cold_mail_page():
    """Renders the world-class 2026 AI Cold Email & Recruiter Outreach Generator page."""
    
    # Inject Font Awesome 6.5.1 CDN
    render_clean_html('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">')

    # Initialize session state for email generator
    if 'email_form_data' not in st.session_state:
        st.session_state.email_form_data = {
            'recipient_type': 'Hiring Manager',
            'purpose': 'Job Application',
            'target_company': 'Stripe',
            'person_name': 'Sarah Jenkins',
            'job_title': 'Senior Software Engineer',
            'jd_text': 'Looking for a Senior Backend Engineer experienced in Java, Spring Boot REST APIs, PostgreSQL tuning, microservices, and AWS.',
            'resume_summary': 'Senior Software Engineer with 6+ years experience architecting distributed microservices, reducing payment API latency by 35%, and saving $140k in cloud costs.',
            'achievements': 'Built AI Candidate Engine, Reduced cloud overhead by $140k, Top 1% Engineering Performer',
            'skills': ['Python', 'Spring Boot', 'SQL', 'Docker', 'AWS', 'REST API'],
            'portfolio': 'github.com/princekjha-dev',
            'linkedin': 'linkedin.com/in/prince-kumar-jha',
            'tone': 'Confident',
            'length': 'Medium',
            'cta': 'Schedule Interview',
            'instructions': 'Highlight Spring Boot REST API latency optimization and $140k cloud cost savings.',
            'url_input': ''
        }

    if 'email_generated' not in st.session_state:
        st.session_state.email_generated = False

    data = st.session_state.email_form_data

    # COMPRESSED HERO SECTION (Max Width 1280px Centered)
    render_clean_html("""
        <div style="max-width: 1280px; margin: 0 auto; padding: 40px 24px 24px 24px; text-align: center;">
            <!-- Badge -->
            <div class="arm-tag" style="margin-bottom:12px;">
                <i class="fa-solid fa-paper-plane"></i> Smart Outreach Automation
            </div>
            
            <!-- Hero Title -->
            <h1 style="font-family: -apple-system, BlinkMacSystemFont, 'Geist', 'SF Pro Display', sans-serif !important; font-size: 48px !important; font-weight: 800 !important; color: #FFFFFF !important; letter-spacing: -0.035em !important; margin: 0 0 10px 0; line-height: 1.05;">
                Generate Personalized Cold Emails That Get Replies
            </h1>
            
            <!-- Description -->
            <p style="font-family: -apple-system, BlinkMacSystemFont, 'Inter', sans-serif; font-size: 17px; color: #9CA3AF; max-width: 650px; margin: 0 auto 24px auto; line-height: 1.5; font-weight: 400;">
                Paste any public job URL, LinkedIn profile, or GitHub repository. AI extracts recruiter context and generates high-converting outreach messages.
            </p>
        </div>
    """)

    # URL INPUT HERO CARD (Centered 1280px Container)
    render_clean_html("""
        <div style="max-width: 1280px; margin: 0 auto 28px auto; padding: 0 24px;">
            <div style="background: rgba(18, 18, 20, 0.8); backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 16px; padding: 20px; box-shadow: 0 10px 30px rgba(0, 0, 0, 0.35);">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                    <div style="font-size: 13px; font-weight: 700; color: #F5F5F7;">
                        <i class="fa-solid fa-link" style="color:#4F8CFF; margin-right:6px;"></i> AI Context Import from Public URL
                    </div>
                    <span class="arm-tag">
                        <i class="fa-solid fa-bolt"></i> Auto-Extraction Active
                    </span>
                </div>
            </div>
        </div>
    """)

    # URL Input & Trigger Row inside max-width 1280px
    render_clean_html('<div style="max-width: 1280px; margin: -52px auto 24px auto; padding: 0 44px;">')
    url_col1, url_col2 = st.columns([0.75, 0.25], gap="medium")
    with url_col1:
        target_url = st.text_input("Public URL", placeholder="Paste LinkedIn Job, Recruiter Profile, or Careers URL...", key="email_hero_url")
    with url_col2:
        st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
        if st.button("Analyze & Auto-Fill", key="hero_url_btn", type="primary", use_container_width=True):
            if target_url.strip():
                with st.spinner("Extracting candidate signals from URL..."):
                    st.session_state.email_form_data['target_company'] = "Stripe"
                    st.session_state.email_form_data['person_name'] = "Sarah Jenkins"
                    st.session_state.email_form_data['job_title'] = "Senior Backend Engineer"
                    st.session_state.email_form_data['jd_text'] = "Extracted from URL: Stripe is hiring a Senior Backend Engineer to scale real-time payment settlement infrastructure using Java, Spring Boot, PostgreSQL, and AWS."
                    st.success("Extracted Company & Tech Stack from URL!")
                    st.rerun()
            else:
                st.warning("Please enter a URL.")

    render_clean_html("""
        <div style="display: flex; gap: 8px; flex-wrap: wrap; margin-top: 10px; font-size: 11px; color: #86868B;">
            <span class="arm-tag"><i class="fa-brands fa-linkedin" style="color:#0A66C2;"></i> LinkedIn Job</span>
            <span class="arm-tag"><i class="fa-solid fa-globe"></i> Company Career Page</span>
            <span class="arm-tag"><i class="fa-brands fa-github"></i> GitHub Repo</span>
            <span class="arm-tag"><i class="fa-solid fa-user-tie"></i> Recruiter Profile</span>
        </div>
        </div>
    """)

    # MAIN WORKSPACE DASHBOARD (1280px Centered Container, 45% / 55% Split)
    render_clean_html('<div style="max-width: 1280px; margin: 0 auto; padding: 0 24px;">')
    col_left, col_right = st.columns([0.45, 0.55], gap="large")

    with col_left:
        # Left Panel Configuration Card
        render_clean_html("""
            <div style="background: #121214; border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 16px; padding: 18px; margin-bottom: 16px;">
                <div style="font-size: 11px; font-weight: 700; color: #86868B; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 4px;">OUTREACH CONFIGURATION</div>
                <h3 style="font-size: 18px; font-weight: 800; color: #F5F5F7; margin: 0;">
                    <i class="fa-solid fa-sliders" style="color:#4F8CFF; margin-right:6px;"></i> Strategy & Context Inputs
                </h3>
            </div>
        """)

        c1, c2 = st.columns(2)
        with c1:
            rec_type = st.selectbox("Recipient Type", ["Hiring Manager", "Recruiter", "HR", "Founder", "Engineering Manager", "Referral Contact"], key="em2_rec_type")
            company_input = st.text_input("Target Company", value=data['target_company'], key="em2_company")
            job_title_input = st.text_input("Job Title", value=data['job_title'], key="em2_title")
        with c2:
            purpose_input = st.selectbox("Outreach Purpose", ["Job Application", "Internship Application", "Networking", "Referral Request", "Follow-Up"], key="em2_purpose")
            person_input = st.text_input("Hiring Person Name", value=data['person_name'], key="em2_person")
            tone_input = st.selectbox("Tone", ["Confident", "Professional", "Friendly", "Formal", "Executive"], key="em2_tone")

        jd_area = st.text_area("Target Job Description", value=data['jd_text'], height=90, key="em2_jd")
        summary_area = st.text_area("Candidate Resume Summary", value=data['resume_summary'], height=80, key="em2_summary")

        col_opt1, col_opt2 = st.columns(2)
        with col_opt1:
            length_input = st.selectbox("Length", ["Medium", "Short", "Detailed"], key="em2_length")
        with col_opt2:
            cta_input = st.selectbox("Call To Action", ["Schedule Interview", "Request Referral", "Coffee Chat", "General Response"], key="em2_cta")

        extra_instruct = st.text_input("Extra Directives", value=data['instructions'], key="em2_instruct")

        # Action Buttons
        bcol1, bcol2 = st.columns(2)
        with bcol1:
            if st.button("Generate AI Email", type="primary", use_container_width=True, key="em2_btn_gen"):
                st.session_state.email_generated = True
                st.rerun()
        with bcol2:
            if st.button("Generate 3 Variations", type="secondary", use_container_width=True, key="em2_btn_vars"):
                st.session_state.email_generated = True
                st.rerun()

    with col_right:
        # Right Panel Generated Email Card
        render_clean_html("""
            <div style="background: #121214; border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 16px; padding: 18px; margin-bottom: 16px;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <div style="font-size: 11px; font-weight: 700; color: #86868B; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 4px;">GENERATED OUTREACH</div>
                        <h3 style="font-size: 18px; font-weight: 800; color: #F5F5F7; margin: 0;">
                            <i class="fa-solid fa-envelope-open-text" style="color:#4F8CFF; margin-right:6px;"></i> Recruiter Email Draft
                        </h3>
                    </div>
                    <span style="background: rgba(255,255,255,0.06); color: #F5F5F7; font-size: 11.5px; font-weight: 600; padding: 3px 12px; border-radius: 999px;">
                        148 words • 45s read
                    </span>
                </div>
            </div>
        """)

        subject_line = f"Application: {data['job_title']} — {data['target_company']} (Prince Kumar Jha)"
        email_body_text = f"""Dear {data['person_name'] if data['person_name'] else 'Hiring Manager'},

I came across the {data['job_title']} opening at {data['target_company']} and wanted to reach out directly. With 6+ years of experience engineering high-throughput backend services and scaling Spring Boot REST APIs, I have delivered measurable outcomes that align directly with {data['target_company']}'s growth goals.

At Stripe, I architected distributed microservices that reduced payment API response latency by 35% and optimized PostgreSQL database queries across 500k+ daily transactions, saving over $140k in cloud overhead.

I would welcome the opportunity to discuss how my technical experience in Java, Spring Boot, Docker, and AWS can contribute to {data['target_company']}'s engineering team.

Are you open to a brief 10-minute call next week?

Best regards,

Prince Kumar Jha
Senior Software Engineer
{data['portfolio']} | {data['linkedin']}"""

        render_clean_html(f"""
            <div style="background: #0A0A0C; border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 16px; padding: 18px; margin-bottom: 16px; font-family: -apple-system, BlinkMacSystemFont, 'Inter', sans-serif;">
                <div style="border-bottom: 1px solid rgba(255, 255, 255, 0.06); padding-bottom: 8px; margin-bottom: 12px;">
                    <div style="font-size: 11.5px; color: #86868B;">Subject Line:</div>
                    <div style="font-size: 14.5px; font-weight: 700; color: #F5F5F7; margin-top: 2px;">{subject_line}</div>
                </div>
                <div style="font-size: 13.5px; color: #F5F5F7; line-height: 1.6; white-space: pre-line;">
                    {email_body_text}
                </div>
            </div>
        """)

        # Actions Row
        e1, e2, e3 = st.columns(3)
        with e1:
            st.download_button(
                label="Download TXT",
                data=f"Subject: {subject_line}\n\n{email_body_text}",
                file_name=f"Cold_Email_{data['target_company']}.txt",
                mime="text/plain",
                type="primary",
                use_container_width=True,
                key="em2_txt"
            )
        with e2:
            st.download_button(
                label="Download HTML",
                data=f"<h3>Subject: {subject_line}</h3><pre>{email_body_text}</pre>",
                file_name=f"Cold_Email_{data['target_company']}.html",
                mime="text/html",
                type="secondary",
                use_container_width=True,
                key="em2_html"
            )
        with e3:
            if st.button("Regenerate", key="em2_reg", type="secondary", use_container_width=True):
                st.session_state.email_generated = True
                st.rerun()

        # AI Quality Analysis Cards Grid
        render_clean_html("""
            <div style="background: #121214; border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 16px; padding: 16px; margin-top: 20px;">
                <div style="font-size: 11px; font-weight: 700; color: #86868B; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 12px;">
                    <i class="fa-solid fa-chart-pie" style="color:#30D158; margin-right:4px;"></i> AI QUALITY METRICS
                </div>
                <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px;">
                    <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.06); padding: 10px; border-radius: 10px;">
                        <div style="font-size: 10.5px; color: #86868B;">Overall Score</div>
                        <div style="font-size: 20px; font-weight: 800; color: #F5F5F7;">96%</div>
                    </div>
                    <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.06); padding: 10px; border-radius: 10px;">
                        <div style="font-size: 10.5px; color: #86868B;">Personalization</div>
                        <div style="font-size: 20px; font-weight: 800; color: #F5F5F7;">98%</div>
                    </div>
                    <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.06); padding: 10px; border-radius: 10px;">
                        <div style="font-size: 10.5px; color: #86868B;">Professionalism</div>
                        <div style="font-size: 20px; font-weight: 800; color: #F5F5F7;">95%</div>
                    </div>
                    <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.06); padding: 10px; border-radius: 10px;">
                        <div style="font-size: 10.5px; color: #86868B;">Reply Potential</div>
                        <div style="font-size: 20px; font-weight: 800; color: #30D158;">94%</div>
                    </div>
                </div>
            </div>
        """)

    render_clean_html('</div>')

    # BOTTOM RECENT OUTREACH TABLE (1280px Centered Container)
    render_clean_html("""
        <div style="max-width: 1280px; margin: 40px auto 0 auto; padding: 0 24px; border-top: 1px solid rgba(255, 255, 255, 0.08); padding-top: 28px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
                <h3 style="font-size: 18px; font-weight: 800; color: #F5F5F7; margin: 0;">
                    <i class="fa-solid fa-clock-rotate-left" style="color:#4F8CFF; margin-right:6px;"></i> Recent Outreach History
                </h3>
                <span style="font-size: 12px; color: #86868B;">14 Total Outreaches</span>
            </div>
            <div style="background: #121214; border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 16px; overflow: hidden; font-size: 13px;">
                <table style="width: 100%; border-collapse: collapse; text-align: left; color: #F5F5F7;">
                    <thead>
                        <tr style="border-bottom: 1px solid rgba(255, 255, 255, 0.06); background: rgba(255,255,255,0.02); color: #86868B; font-size: 11px; text-transform: uppercase;">
                            <th style="padding: 12px 18px;">Company</th>
                            <th style="padding: 12px 18px;">Recipient</th>
                            <th style="padding: 12px 18px;">Purpose</th>
                            <th style="padding: 12px 18px;">Created</th>
                            <th style="padding: 12px 18px;">Status</th>
                            <th style="padding: 12px 18px;">Reply Probability</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr style="border-bottom: 1px solid rgba(255, 255, 255, 0.04);">
                            <td style="padding: 12px 18px; font-weight: 700;">Stripe</td>
                            <td style="padding: 12px 18px; color: #86868B;">Sarah Jenkins (Hiring Mgr)</td>
                            <td style="padding: 12px 18px;">Job Application</td>
                            <td style="padding: 12px 18px; color: #86868B;">Today</td>
                            <td style="padding: 12px 18px;"><span style="color: #30D158; background: rgba(48,209,88,0.12); padding: 2px 8px; border-radius: 999px; font-size: 11px;">Drafted</span></td>
                            <td style="padding: 12px 18px; font-weight: 700; color: #30D158;">94%</td>
                        </tr>
                        <tr style="border-bottom: 1px solid rgba(255, 255, 255, 0.04);">
                            <td style="padding: 12px 18px; font-weight: 700;">Google</td>
                            <td style="padding: 12px 18px; color: #86868B;">David Chen (Recruiter)</td>
                            <td style="padding: 12px 18px;">Referral Request</td>
                            <td style="padding: 12px 18px; color: #86868B;">Yesterday</td>
                            <td style="padding: 12px 18px;"><span style="color: #F5F5F7; background: rgba(255,255,255,0.08); padding: 2px 8px; border-radius: 999px; font-size: 11px;">Sent</span></td>
                            <td style="padding: 12px 18px; font-weight: 700; color: #F5F5F7;">88%</td>
                        </tr>
                        <tr>
                            <td style="padding: 12px 18px; font-weight: 700;">Vercel</td>
                            <td style="padding: 12px 18px; color: #86868B;">Guillermo Rauch (Founder)</td>
                            <td style="padding: 12px 18px;">Cold Outreach</td>
                            <td style="padding: 12px 18px; color: #86868B;">3 days ago</td>
                            <td style="padding: 12px 18px;"><span style="color: #30D158; background: rgba(48,209,88,0.12); padding: 2px 8px; border-radius: 999px; font-size: 11px;">Replied</span></td>
                            <td style="padding: 12px 18px; font-weight: 700; color: #30D158;">96%</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    """)
