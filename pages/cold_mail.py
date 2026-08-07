import textwrap
import streamlit as st
import datetime
import re
import json
from html import escape

import requests

from utils.ai_resume_analyzer import AIResumeAnalyzer

def render_clean_html(html_str):
    """Cleanly render HTML by stripping multiline indentation to prevent Markdown code block bugs."""
    if not html_str:
        return
    lines = [line.strip() for line in html_str.splitlines() if line.strip()]
    cleaned = chr(10).join(lines)
    st.markdown(cleaned, unsafe_allow_html=True)


def generate_ai_outreach(context, variations=False):
    """Generate outreach copy exclusively through the configured AI provider."""
    variation_instruction = "Create three distinct alternatives separated by `---`." if variations else "Create one best version."
    prompt = f"""You are an expert career strategist writing a high-converting, truthful cold email.

Recipient type: {context['recipient_type']}
Recipient name: {context['person_name'] or 'Hiring Manager'}
Optional public URL context: {context.get('url_input') or 'Not provided'}
Company: {context['target_company']}
Target role: {context['job_title']}
Purpose: {context['purpose']}
Tone: {context['tone']}
Length: {context['length']}
Call to action: {context['cta']}
Job description: {context['jd_text']}
Candidate summary: {context['resume_summary']}
Achievements: {context['achievements']}
Skills: {', '.join(context['skills'])}
Additional instructions: {context['instructions']}

Write only claims supported by the candidate summary and achievements. Do not invent employers, metrics, or personal details.
{variation_instruction}
For every email use exactly this format:
SUBJECT: concise subject line
BODY:
email body
"""
    response, model_used = AIResumeAnalyzer()._generate_ai_completion(prompt, temperature=0.65)
    match = re.search(r"(?im)^subject\s*:\s*(.+?)\s*$", response)
    subject = match.group(1).strip() if match else f"Interest in {context['job_title']} at {context['target_company']}"
    body = re.split(r"(?im)^body\s*:\s*", response, maxsplit=1)
    body = body[-1].strip() if len(body) > 1 else response.strip()
    return {"subject": subject, "body": body, "model": model_used}


def extract_ai_url_context(url):
    """Fetch public page text then ask the configured AI model for usable outreach context."""
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (compatible; AiResuMind/1.0)"}, timeout=12)
    response.raise_for_status()
    page_text = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", response.text))[:12000]
    if len(page_text) < 120:
        raise RuntimeError("The page did not expose enough public text to analyse.")
    prompt = f"""Extract factual job-outreach context from this public page. Return JSON only with keys
company, person_name, job_title, job_description. Use empty strings for unknown values; never invent details.

URL: {url}
PAGE TEXT: {page_text}
"""
    raw, model = AIResumeAnalyzer()._generate_ai_completion(prompt, temperature=0.1)
    json_match = re.search(r"\{.*\}", raw, re.S)
    if not json_match:
        raise RuntimeError("The AI response was not structured extraction data.")
    details = json.loads(json_match.group(0))
    return details, model

def render_cold_mail_page():
    """Renders the world-class 2026 AI Cold Email & Recruiter Outreach Generator page."""
    
    # Inject Font Awesome 6.5.1 CDN
    render_clean_html('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">')

    # Initialize session state for email generator
    if 'email_form_data' not in st.session_state:
        st.session_state.email_form_data = {
            'recipient_type': 'Hiring Manager',
            'purpose': 'Job Application',
            'target_company': '',
            'person_name': '',
            'job_title': '',
            'jd_text': '',
            'resume_summary': '',
            'achievements': '',
            'skills': [],
            'portfolio': '',
            'linkedin': '',
            'tone': 'Confident',
            'length': 'Medium',
            'cta': 'Schedule Interview',
            'instructions': '',
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
                        <i class="fa-solid fa-link" style="color:#4F8CFF; margin-right:6px;"></i> Public URL Context
                    </div>
                    <span class="arm-tag">
                        <i class="fa-solid fa-wand-magic-sparkles"></i> AI context import
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
        if st.button("Save URL Context", key="hero_url_btn", type="primary", use_container_width=True):
            if target_url.strip():
                st.session_state.email_form_data['url_input'] = target_url.strip()
                try:
                    with st.spinner("Reading available public page context with AI..."):
                        extracted, model = extract_ai_url_context(target_url.strip())
                    field_keys = {"company": "em2_company", "person_name": "em2_person", "job_title": "em2_title", "job_description": "em2_jd"}
                    for source_key, widget_key in field_keys.items():
                        value = extracted.get(source_key, "").strip()
                        if value:
                            st.session_state[widget_key] = value
                    st.session_state.url_context_status = f"AI extracted available public context via {model}. Review the fields before generating."
                    st.rerun()
                except Exception as exc:
                    st.session_state.url_context_status = f"Could not read this public page ({exc}). The URL will still be passed to the AI with your manual context."
            else:
                st.warning("Please enter a URL.")

    if st.session_state.get("url_context_status"):
        st.info(st.session_state.url_context_status)

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
                context = {**data, 'recipient_type': rec_type, 'target_company': company_input, 'job_title': job_title_input, 'purpose': purpose_input, 'person_name': person_input, 'tone': tone_input, 'jd_text': jd_area, 'resume_summary': summary_area, 'length': length_input, 'cta': cta_input, 'instructions': extra_instruct}
                try:
                    with st.spinner("Writing your personalized email with AI..."):
                        st.session_state.generated_outreach = generate_ai_outreach(context)
                    st.session_state.email_generated = True
                    st.rerun()
                except Exception as exc:
                    st.error(f"AI generation unavailable: {exc}")
        with bcol2:
            if st.button("Generate 3 Variations", type="secondary", use_container_width=True, key="em2_btn_vars"):
                context = {**data, 'recipient_type': rec_type, 'target_company': company_input, 'job_title': job_title_input, 'purpose': purpose_input, 'person_name': person_input, 'tone': tone_input, 'jd_text': jd_area, 'resume_summary': summary_area, 'length': length_input, 'cta': cta_input, 'instructions': extra_instruct}
                try:
                    with st.spinner("Creating AI outreach variations..."):
                        st.session_state.generated_outreach = generate_ai_outreach(context, variations=True)
                    st.session_state.email_generated = True
                    st.rerun()
                except Exception as exc:
                    st.error(f"AI generation unavailable: {exc}")

    with col_right:
        # Right Panel Generated Email Card
        outreach_status = f"{len(st.session_state.get('generated_outreach', {}).get('body', '').split())} words" if st.session_state.get('generated_outreach') else "Awaiting AI"
        render_clean_html(f"""
            <div style="background: #121214; border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 16px; padding: 18px; margin-bottom: 16px;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <div style="font-size: 11px; font-weight: 700; color: #86868B; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 4px;">GENERATED OUTREACH</div>
                        <h3 style="font-size: 18px; font-weight: 800; color: #F5F5F7; margin: 0;">
                            <i class="fa-solid fa-envelope-open-text" style="color:#4F8CFF; margin-right:6px;"></i> Recruiter Email Draft
                        </h3>
                    </div>
                    <span style="background: rgba(255,255,255,0.06); color: #F5F5F7; font-size: 11.5px; font-weight: 600; padding: 3px 12px; border-radius: 999px;">
                        {outreach_status}
                    </span>
                </div>
            </div>
        """)

        generated = st.session_state.get("generated_outreach")
        if generated:
            subject_line = generated["subject"]
            email_body_text = generated["body"]
            render_clean_html(f"""
                <div style="background:#0A0A0C; border:1px solid rgba(97,215,178,.2); border-radius:16px; padding:18px; margin-bottom:16px; font-family:Inter,sans-serif;">
                    <div style="display:flex;justify-content:space-between;gap:12px;border-bottom:1px solid rgba(255,255,255,.06);padding-bottom:8px;margin-bottom:12px;"><div><div style="font-size:11.5px;color:#86868B;">AI-generated subject</div><div style="font-size:14.5px;font-weight:700;color:#F5F5F7;margin-top:2px;">{escape(subject_line)}</div></div><span class="arm-tag">{escape(generated['model'])}</span></div>
                    <div style="font-size:13.5px;color:#F5F5F7;line-height:1.6;white-space:pre-line;">{escape(email_body_text)}</div>
                </div>
            """)
        else:
            subject_line, email_body_text = "", ""
            render_clean_html("""
                <div style="background:rgba(255,255,255,.025);border:1px dashed rgba(255,255,255,.14);border-radius:16px;padding:36px 22px;margin-bottom:16px;text-align:center;color:#9CA3AF;">
                    <div style="font-size:14px;font-weight:700;color:#F5F5F7;margin-bottom:6px;">Your AI email will appear here</div>
                    <div style="font-size:12.5px;line-height:1.5;">Add your context, then use Generate AI Email. No stock template is used.</div>
                </div>
            """)

        # Actions Row
        e1, e2, e3 = st.columns(3)
        with e1:
            if generated:
                st.download_button(label="Download TXT", data=f"Subject: {subject_line}\n\n{email_body_text}", file_name=f"Cold_Email_{data['target_company']}.txt", mime="text/plain", type="primary", use_container_width=True, key="em2_txt")
        with e2:
            if generated:
                st.download_button(label="Download HTML", data=f"<h3>Subject: {escape(subject_line)}</h3><pre>{escape(email_body_text)}</pre>", file_name=f"Cold_Email_{data['target_company']}.html", mime="text/html", type="secondary", use_container_width=True, key="em2_html")
        with e3:
            if st.button("Regenerate", key="em2_reg", type="secondary", use_container_width=True):
                st.session_state.generated_outreach = None
                st.rerun()

        if generated:
            render_clean_html(f"""<div style="background:rgba(97,215,178,.05);border:1px solid rgba(97,215,178,.18);border-radius:14px;padding:14px;margin-top:20px;color:#b6becb;font-size:12px;"><strong style="color:#f6f1e8;">Generation complete</strong><br>Created by {escape(generated['model'])}. Review every factual claim before sending.</div>""")

    render_clean_html('</div>')
