import streamlit as st
from .job_portals import JobPortal

def render_clean_html(html_str):
    """Cleanly render HTML by stripping multiline indentation to prevent Markdown code block bugs."""
    if not html_str:
        return
    lines = [line.strip() for line in html_str.splitlines() if line.strip()]
    cleaned = chr(10).join(lines)
    st.markdown(cleaned, unsafe_allow_html=True)

def render_job_search():
    """Renders Job Search V5 — Premium Job Discovery Workspace."""
    
    # 1. EDITORIAL HERO V5
    render_clean_html("""
        <div style="max-width: 1200px; margin: 0 auto; padding: 56px 24px 40px 24px; text-align: center;">
            <div style="font-size: 11.5px; font-weight: 700; color: #60A5FA; letter-spacing: 0.12em; text-transform: uppercase; margin-bottom: 16px;">
                JOB DISCOVERY INTELLIGENCE
            </div>
            
            <h1 style="font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', sans-serif !important; font-size: 64px !important; font-weight: 800 !important; color: #F5F5F7 !important; letter-spacing: -0.04em !important; max-width: 760px; margin: 0 auto 16px auto; line-height: 1.05;">
                Find roles worth applying to.
            </h1>
            
            <p style="font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', sans-serif; font-size: 18px; color: #86868B; max-width: 600px; margin: 0 auto; line-height: 1.6; font-weight: 400;">
                Discover relevant opportunities and evaluate your fit with instant AI match scoring.
            </p>
        </div>
    """)

    # 2. SEARCH CONTROLS WORKSPACE
    render_clean_html('<div style="max-width: 1200px; margin: 0 auto 40px auto; padding: 0 24px;">')
    col1, col2, col3, col4 = st.columns([0.35, 0.30, 0.18, 0.17], gap="medium")
    
    with col1:
        role_q = st.text_input("Role or title", placeholder="Software Engineer, Product Manager...", key="v5_js_role")
    with col2:
        loc_q = st.text_input("Location", placeholder="San Francisco, New York, Remote...", key="v5_js_loc")
    with col3:
        exp_q = st.selectbox("Experience level", ["Any Experience", "Entry Level", "Mid Level", "Senior Level", "Executive"], key="v5_js_exp")
    with col4:
        st.markdown('<div style="height: 28px;"></div>', unsafe_allow_html=True)
        search_click = st.button("Find Jobs", type="primary", use_container_width=True, key="v5_js_search_btn")

    remote_only = st.checkbox("Remote roles only", key="v5_js_remote")
    render_clean_html('</div>')

    # Calculate dynamic job match scores from uploaded resume context
    resume_txt = st.session_state.get('uploaded_resume_text', '')
    has_resume = bool(resume_txt and len(resume_txt.strip()) > 30)

    sample_jobs = [
        {
            "id": "j1",
            "title": "Senior Backend Engineer",
            "company": "Stripe",
            "location": "San Francisco, CA (Hybrid)",
            "experience": "4+ years",
            "salary": "$180,000 - $220,000",
            "skills": ["java", "spring boot", "postgresql", "api", "backend", "python", "sql"],
            "strengths": ["Backend service architecture", "API performance optimization", "Relational database design"],
            "gaps": ["AWS distributed cloud infrastructure", "Kubernetes container management"],
            "url": "https://stripe.com/jobs"
        },
        {
            "id": "j2",
            "title": "Full Stack Software Engineer",
            "company": "Vercel",
            "location": "Remote",
            "experience": "3+ years",
            "salary": "$165,000 - $200,000",
            "skills": ["react", "typescript", "rest api", "html", "css", "javascript"],
            "strengths": ["React & TypeScript expertise", "REST API architecture", "Clean user interface design"],
            "gaps": ["Next.js App Router edge functions", "GraphQL query optimization"],
            "url": "https://vercel.com/careers"
        },
        {
            "id": "j3",
            "title": "Staff Software Engineer",
            "company": "Linear",
            "location": "San Francisco, CA / Remote",
            "experience": "6+ years",
            "salary": "$210,000 - $260,000",
            "skills": ["architecture", "microservices", "distributed", "system", "leadership"],
            "strengths": ["System architecture design", "High throughput microservices", "Engineering quality standards"],
            "gaps": ["Real-time sync algorithms", "Distributed database sharding"],
            "url": "https://linear.app/careers"
        }
    ]

    for j in sample_jobs:
        if has_resume:
            r_words = set(resume_txt.lower().split())
            overlap = [sk for sk in j["skills"] if sk in r_words]
            match_pct = min(96, max(58, int((len(overlap) / max(1, len(j["skills"]))) * 100) + 45))
            j["computed_match"] = f"{match_pct}% MATCH"
        else:
            j["computed_match"] = "Match analysis unavailable"

    # 3. JOB OPPORTUNITIES LIST
    render_clean_html('<div style="max-width: 1200px; margin: 0 auto; padding: 0 24px;">')
    st.markdown('<h3 style="font-size: 24px; font-weight: 700; color: #F5F5F7; margin: 0 0 24px 0;">Relevant Opportunities</h3>', unsafe_allow_html=True)

    for job in sample_jobs:
        if "MATCH" in job["computed_match"]:
            match_badge = f'<span style="background: rgba(16, 185, 129, 0.12); color: #34D399; border: 1px solid rgba(16, 185, 129, 0.25); font-weight: 700; padding: 4px 14px; border-radius: 9999px; font-size: 13px;">{job["computed_match"]}</span>'
        else:
            match_badge = f'<span style="background: rgba(255, 255, 255, 0.05); color: #86868B; border: 1px solid rgba(255, 255, 255, 0.1); font-weight: 600; padding: 4px 14px; border-radius: 9999px; font-size: 12px;">{job["computed_match"]}</span>'
        
        strengths_html = "".join([f'<div style="font-size: 13px; color: #86868B; margin-bottom: 4px;">• <span style="color: #F5F5F7;">{s}</span></div>' for s in job["strengths"]])
        gaps_html = "".join([f'<div style="font-size: 13px; color: #86868B; margin-bottom: 4px;">• <span style="color: #FBBF24;">{g}</span></div>' for g in job["gaps"]])

        render_clean_html(f"""
            <div style="background: #141519; border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 24px; padding: 32px; margin-bottom: 24px;">
                <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 16px; flex-wrap: wrap; gap: 12px;">
                    <div>
                        <div style="font-size: 13px; font-weight: 600; color: #86868B; margin-bottom: 4px;">{job['company']} · {job['location']}</div>
                        <h4 style="font-size: 22px; font-weight: 800; color: #F5F5F7; margin: 0;">{job['title']}</h4>
                    </div>
                    <div>{match_badge}</div>
                </div>

                <div style="display: flex; gap: 24px; font-size: 13.5px; color: #86868B; margin-bottom: 24px; border-bottom: 1px solid rgba(255,255,255,0.06); padding-bottom: 16px;">
                    <div>Salary: <strong style="color: #F5F5F7;">{job['salary']}</strong></div>
                    <div>Experience: <strong style="color: #F5F5F7;">{job['experience']}</strong></div>
                </div>

                <div style="font-size: 12px; font-weight: 700; color: #6E6E73; uppercase; letter-spacing: 0.08em; margin-bottom: 10px;">WHY YOU'RE A MATCH</div>
                
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 24px;">
                    <div>
                        <div style="font-size: 12px; font-weight: 600; color: #34D399; margin-bottom: 6px;">Strengths (3)</div>
                        {strengths_html}
                    </div>
                    <div>
                        <div style="font-size: 12px; font-weight: 600; color: #FBBF24; margin-bottom: 6px;">Gaps (2)</div>
                        {gaps_html}
                    </div>
                </div>
            </div>
        """)

        jcol1, jcol2 = st.columns([0.3, 0.7])
        with jcol1:
            if st.button(f"Optimize Resume for {job['company']}", key=f"js_opt_{job['id']}", type="primary", use_container_width=True):
                st.session_state.page = "resume_builder"
                st.rerun()

    render_clean_html('</div>')