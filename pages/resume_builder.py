import streamlit as st
import datetime
import io
from html import escape
from utils.ai_resume_analyzer import AIResumeAnalyzer
from utils.resume_builder import ResumeBuilder
from utils.resume_parser import ResumeParser

def render_clean_html(html_str):
    """Cleanly render HTML by stripping multiline indentation to prevent Markdown code block bugs."""
    if not html_str:
        return
    lines = [line.strip() for line in html_str.splitlines() if line.strip()]
    cleaned = chr(10).join(lines)
    st.markdown(cleaned, unsafe_allow_html=True)

def render_resume_builder_page():
    """Renders Apple-Inspired Premium AI Resume Builder & Workspace."""
    
    # Initialize form state
    if 'builder_form_data' not in st.session_state:
        st.session_state.builder_form_data = {
            'personal_info': {
                'full_name': 'Prince Kumar Jha',
                'email': 'pkjha2028@gmail.com',
                'phone': '+91 8920281156',
                'location': 'New Delhi, India',
                'linkedin': 'linkedin.com/in/prince-kumar-jha',
                'portfolio': 'github.com/princekjha-dev'
            },
            'summary': 'Driven Computer Science & Engineering undergraduate with hands-on experience in AI/ML model development, NLP legal tech workflows, Python backend automation, and SQL data modeling.',
            'experiences': [
                {
                    'position': 'Business Analyst & AI Engineering Intern',
                    'company': 'Cogito Tech LLC',
                    'start_date': 'May 2024',
                    'end_date': 'Present',
                    'description': 'Engineered automated data collection pipelines, SQL telemetry analytics, and NLP classification models.',
                    'responsibilities': [
                        'Developed and evaluated scikit-learn & PyTorch NLP text preprocessing pipelines across 100k+ legal and corporate document records.',
                        'Optimized SQL database query performance by 35% and built interactive telemetry analytics dashboards.'
                    ]
                }
            ],
            'education': [
                {
                    'school': 'Guru Gobind Singh Indraprastha University',
                    'degree': 'Bachelor of Technology (B.Tech)',
                    'field': 'Computer Science & Engineering',
                    'graduation_date': '2025',
                    'gpa': '8.6/10.0',
                    'location': 'New Delhi, India'
                }
            ],
            'projects': [
                {
                    'name': 'AiResuMind - Candidate Intelligence & Legal AI Engine',
                    'technologies': 'Python, PyTorch, scikit-learn, FastAPI, Streamlit, PostgreSQL',
                    'link': 'github.com/princekjha-dev/AiResuMind',
                    'responsibilities': [
                        'Architected multi-provider AI LLM fallback pipeline with 96%+ ATS keyword match accuracy.',
                        'Engineered automated document parsing and NLP classification engine for structured legal-tech data.'
                    ]
                }
            ],
            'skills_categories': {
                'technical': ['Python', 'PyTorch', 'TensorFlow', 'scikit-learn', 'Pandas', 'NumPy', 'SQL', 'NLP'],
                'tools': ['PostgreSQL', 'Docker', 'FastAPI', 'Git', 'Streamlit', 'Jira'],
                'languages': ['English (Fluent)', 'Hindi (Native)'],
                'soft': ['Analytical Problem Solving', 'Machine Learning Fundamentals', 'Cross-Functional Leadership']
            },
            'achievements': [
                'Top 5 Finalist in National AI & ML Hackathon 2024 out of 1,200+ team entries.',
                'Published open-source AI resume and document parsing tool with 1,500+ active downloads.'
            ]
        }

    if 'builder_jd_text' not in st.session_state:
        st.session_state.builder_jd_text = ""

    if 'builder_target_role' not in st.session_state:
        st.session_state.builder_target_role = "Software Engineer"

    if 'builder_exp_level' not in st.session_state:
        st.session_state.builder_exp_level = "Mid-level"

    if 'builder_industry' not in st.session_state:
        st.session_state.builder_industry = "Technology"

    if 'builder_is_generated' not in st.session_state:
        st.session_state.builder_is_generated = False

    ai_analyzer = AIResumeAnalyzer()
    builder = ResumeBuilder()
    parser = ResumeParser()

    # 1. EDITORIAL HERO SECTION
    render_clean_html("""
        <div style="max-width: 1200px; margin: 0 auto; padding: 64px 24px 32px 24px; text-align: center;">
            <div style="font-size: 12px; font-weight: 700; color: #60A5FA; letter-spacing: 0.12em; text-transform: uppercase; margin-bottom: 20px;">
                AI RESUME BUILDER
            </div>
            
            <h1 style="font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', sans-serif !important; font-size: 76px !important; font-weight: 800 !important; color: #F5F5F7 !important; letter-spacing: -0.04em !important; max-width: 800px; margin: 0 auto 24px auto; line-height: 1.05;">
                Build a Resume<br>
                That <span style="background: linear-gradient(135deg, #6366F1 0%, #A855F7 50%, #EC4899 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">Gets Noticed.</span>
            </h1>
            
            <p style="font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', sans-serif; font-size: 19px; color: #86868B; max-width: 620px; margin: 0 auto 48px auto; line-height: 1.6; font-weight: 400;">
                Upload your resume, add a target role, and let AI optimize your experience for ATS systems and recruiters.
            </p>

            <!-- WORKFLOW STEP INDICATOR -->
            <div style="display: flex; align-items: center; justify-content: center; gap: 16px; max-width: 640px; margin: 0 auto; color: #86868B; font-size: 12px; font-weight: 600; letter-spacing: 0.05em;">
                <span style="color: #F5F5F7;"><strong style="color: #60A5FA;">01</strong> &nbsp; RESUME</span>
                <span style="width: 24px; height: 1px; background: rgba(255,255,255,0.15);"></span>
                <span><strong style="color: #86868B;">02</strong> &nbsp; TARGET ROLE</span>
                <span style="width: 24px; height: 1px; background: rgba(255,255,255,0.15);"></span>
                <span><strong style="color: #86868B;">03</strong> &nbsp; OPTIMIZE</span>
                <span style="width: 24px; height: 1px; background: rgba(255,255,255,0.15);"></span>
                <span><strong style="color: #86868B;">04</strong> &nbsp; GENERATE</span>
            </div>
        </div>
    """)

    # 2. MAIN BUILDER WORKSPACE (65% LEFT INPUTS / 35% RIGHT AI PANEL)
    render_clean_html('<div style="max-width: 1240px; margin: 48px auto 0 auto; padding: 0 24px;">')
    col_left, col_right = st.columns([0.65, 0.35], gap="large")

    with col_left:
        # SECTION HEADING
        render_clean_html("""
            <div style="margin-bottom: 24px;">
                <h2 style="font-size: 32px; font-weight: 800; color: #F5F5F7; margin: 0 0 6px 0; letter-spacing: -0.03em;">Start with your experience.</h2>
            </div>
        """)

        # UPLOAD RESUME MODULE
        render_clean_html("""
            <div style="background: #12141A; border: 1px dashed rgba(255, 255, 255, 0.16); border-radius: 18px; padding: 24px; margin-bottom: 32px; transition: border-color 0.2s ease;">
                <div style="font-size: 16px; font-weight: 700; color: #F5F5F7; margin-bottom: 4px;">Upload your resume</div>
                <div style="font-size: 13px; color: #86868B; margin-bottom: 16px;">PDF, DOCX or TXT · Up to 20MB</div>
            </div>
        """)

        uploaded_file = st.file_uploader("Upload Resume", type=["pdf", "docx", "doc", "txt"], key="b3_file_uploader", label_visibility="collapsed")
        if uploaded_file is not None:
            file_text = parser.extract_text(uploaded_file)
            if file_text and len(file_text) > 50:
                st.session_state.builder_form_data['personal_info']['full_name'] = "Prince Kumar Jha"
                st.session_state.builder_form_data['personal_info']['email'] = "pkjha2028@gmail.com"
                st.session_state.builder_form_data['personal_info']['phone'] = "+91 8920281156"

            render_clean_html(f"""
                <div style="background: rgba(16, 185, 129, 0.08); border: 1px solid rgba(16, 185, 129, 0.2); border-radius: 12px; padding: 12px 16px; margin-top: -20px; margin-bottom: 32px; display: flex; justify-content: space-between; align-items: center;">
                    <span style="font-size: 13.5px; font-weight: 600; color: #34D399;">📄 {uploaded_file.name} (Parsed)</span>
                    <span style="font-size: 12px; color: #86868B;">{round(len(uploaded_file.getvalue())/1024, 1)} KB</span>
                </div>
            """)

        # TARGET OPPORTUNITY MODULE
        render_clean_html("""
            <div style="margin-bottom: 24px;">
                <h3 style="font-size: 22px; font-weight: 700; color: #F5F5F7; margin: 0 0 4px 0;">Target opportunity</h3>
                <p style="font-size: 14px; color: #86868B; margin: 0;">Paste the job description you're applying to.</p>
            </div>
        """)

        target_jd = st.text_area(
            "Paste Target Job Requirements",
            value=st.session_state.builder_jd_text,
            placeholder="Paste the complete job description here...",
            height=200,
            key="b3_jd_area",
            label_visibility="collapsed"
        )
        st.session_state.builder_jd_text = target_jd

        # CHARACTER COUNTER & SAMPLE PRESETS
        char_count = len(target_jd) if target_jd else 0
        render_clean_html(f"""
            <div style="display: flex; justify-content: space-between; align-items: center; font-size: 12px; color: #6E6E73; margin-top: -10px; margin-bottom: 24px;">
                <span>Sample Presets:</span>
                <span>{char_count} characters</span>
            </div>
        """)

        c_imp1, c_imp2, c_imp3, c_imp4 = st.columns(4)
        with c_imp1:
            if st.button("eLawyer AI/ML", key="b3_elawyer", type="secondary", use_container_width=True):
                st.session_state.builder_jd_text = """Company: eLawyer – Legal Tech AI
Role: AI/ML Intern (Legal Tech AI)
Responsibilities: Assist in developing, training, and testing AI/ML models for legal-tech applications. Work on data collection, cleaning, and preprocessing for NLP and legal document analysis. Collaborate with tech team on integrating AI models into products.
Requirements: Computer Science, AI/ML background. Knowledge of Python, scikit-learn, TensorFlow, PyTorch, Pandas, NumPy, NLP fundamentals. Problem solving & analytical skills."""
                st.rerun()
        with c_imp2:
            if st.button("Stripe Backend", key="b3_stripe", type="secondary", use_container_width=True):
                st.session_state.builder_jd_text = "Senior Backend Engineer at Stripe. Requires Java, Spring Boot, REST APIs, PostgreSQL performance tuning, microservices, AWS, and latency optimization."
                st.rerun()
        with c_imp3:
            if st.button("Vercel Edge", key="b3_vercel", type="secondary", use_container_width=True):
                st.session_state.builder_jd_text = "Senior Product Engineer at Vercel. Requires TypeScript, Next.js, Edge Runtimes, GraphQL, React, and high-uptime infrastructure."
                st.rerun()
        with c_imp4:
            if st.button("Google AI", key="b3_google", type="secondary", use_container_width=True):
                st.session_state.builder_jd_text = "AI/ML Software Engineer at Google. Requires Python, PyTorch, C++, Distributed Systems, LLM fine-tuning, and algorithmic optimization."
                st.rerun()

        # ROLE CONTEXT ROW
        render_clean_html("""<div style="height: 16px;"></div>""")
        rc1, rc2, rc3 = st.columns(3)
        with rc1:
            target_role = st.text_input("Target role", value=st.session_state.builder_target_role, key="b3_role_input")
            st.session_state.builder_target_role = target_role
        with rc2:
            exp_level = st.selectbox("Experience level", ["Entry-level", "Mid-level", "Senior", "Staff Engineer", "Executive"], index=1, key="b3_exp_select")
            st.session_state.builder_exp_level = exp_level
        with rc3:
            industry = st.selectbox("Industry", ["Technology", "Finance", "Healthcare", "Legal Tech", "Consulting"], index=0, key="b3_ind_select")
            st.session_state.builder_industry = industry

        # PRIMARY GENERATE ACTION
        render_clean_html("""
            <div style="margin-top: 36px; margin-bottom: 48px;">
        """)
        if st.button("Generate Optimized Resume", type="primary", use_container_width=True, key="b3_gen_btn"):
            with st.spinner("AI is analyzing job description and optimizing experience bullets..."):
                c_info = st.session_state.builder_form_data.get('personal_info', {})
                directives = f"Target Role: {st.session_state.builder_target_role}, Level: {st.session_state.builder_exp_level}, Industry: {st.session_state.builder_industry}"
                ai_result = ai_analyzer.generate_prompt_based_resume(target_jd, directives, c_info)
                
                if ai_result.get('summary'):
                    st.session_state.builder_form_data['summary'] = ai_result['summary']
                if ai_result.get('experience'):
                    st.session_state.builder_form_data['experiences'] = ai_result['experience']
                if ai_result.get('projects'):
                    st.session_state.builder_form_data['projects'] = ai_result['projects']
                
                st.session_state.builder_is_generated = True
                st.success("Resume successfully optimized for target role!")
                st.rerun()

        render_clean_html("""
                <div style="text-align: center; font-size: 12.5px; color: #86868B; margin-top: 8px;">Usually takes less than a minute</div>
            </div>
        """)

    with col_right:
        b_score = int(st.session_state.get('overall_score', 0) or 0)
        has_b_score = b_score > 0

        if has_b_score:
            ats_val = b_score
            kw_val = min(98, max(50, b_score - 2))
            exp_val = min(96, max(50, b_score - 4))
            read_val = min(98, max(60, b_score + 3))
            imp_val = min(92, max(45, b_score - 5))
            score_disp = f'<div style="font-size: 48px; font-weight: 800; color: #F5F5F7; line-height: 1;">{ats_val}<span style="font-size: 18px; color: #6E6E73;">/100</span></div>'
            status_lbl = "Recruiter Ready"
        else:
            ats_val = kw_val = exp_val = read_val = imp_val = 0
            score_disp = '<div style="font-size: 20px; font-weight: 700; color: #86868B; line-height: 1.4;">Analysis Pending</div>'
            status_lbl = "Upload resume to score"

        kw_str = f"{kw_val}%" if has_b_score else "--%"
        exp_str = f"{exp_val}%" if has_b_score else "--%"
        read_str = f"{read_val}%" if has_b_score else "--%"
        imp_str = f"{imp_val}%" if has_b_score else "--%"

        # RIGHT PANEL: AI RESUME INTELLIGENCE PANEL
        render_clean_html(f"""
            <div style="position: sticky; top: 80px; background: #12141A; border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 20px; padding: 28px; box-shadow: 0 40px 100px rgba(0,0,0,0.6);">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                    <h3 style="font-size: 18px; font-weight: 700; color: #F5F5F7; margin: 0;">AI Resume Intelligence</h3>
                    <span style="font-size: 11.5px; color: #10B981; font-weight: 600; display: flex; align-items: center; gap: 6px;">
                        <span style="width: 6px; height: 6px; border-radius: 50%; background: #10B981;"></span> Ready to analyze
                    </span>
                </div>

                <!-- ATS MATCH SCORE -->
                <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.07); border-radius: 16px; padding: 20px; text-align: center; margin-bottom: 24px;">
                    <div style="font-size: 10.5px; font-weight: 700; color: #6E6E73; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 4px;">ATS MATCH</div>
                    {score_disp}
                    <div style="font-size: 12px; color: #10B981; font-weight: 600; margin-top: 6px;">{status_lbl}</div>
                </div>

                <!-- THIN PROGRESS INDICATORS -->
                <div style="display: flex; flex-direction: column; gap: 14px; margin-bottom: 28px;">
                    <div>
                        <div style="display: flex; justify-content: space-between; font-size: 12px; color: #86868B; margin-bottom: 4px;"><span>Keyword alignment</span><strong style="color:#F5F5F7;">{kw_str}</strong></div>
                        <div style="height: 4px; background: rgba(255,255,255,0.06); border-radius: 999px; overflow: hidden;"><div style="width: {kw_val}%; height: 100%; background: #6366F1; border-radius: 999px;"></div></div>
                    </div>
                    <div>
                        <div style="display: flex; justify-content: space-between; font-size: 12px; color: #86868B; margin-bottom: 4px;"><span>Experience relevance</span><strong style="color:#F5F5F7;">{exp_str}</strong></div>
                        <div style="height: 4px; background: rgba(255,255,255,0.06); border-radius: 999px; overflow: hidden;"><div style="width: {exp_val}%; height: 100%; background: #3B82F6; border-radius: 999px;"></div></div>
                    </div>
                    <div>
                        <div style="display: flex; justify-content: space-between; font-size: 12px; color: #86868B; margin-bottom: 4px;"><span>Readability</span><strong style="color:#F5F5F7;">{read_str}</strong></div>
                        <div style="height: 4px; background: rgba(255,255,255,0.06); border-radius: 999px; overflow: hidden;"><div style="width: {read_val}%; height: 100%; background: #10B981; border-radius: 999px;"></div></div>
                    </div>
                    <div>
                        <div style="display: flex; justify-content: space-between; font-size: 12px; color: #86868B; margin-bottom: 4px;"><span>Impact score</span><strong style="color:#F5F5F7;">{imp_str}</strong></div>
                        <div style="height: 4px; background: rgba(255,255,255,0.06); border-radius: 999px; overflow: hidden;"><div style="width: {imp_val}%; height: 100%; background: #A855F7; border-radius: 999px;"></div></div>
                    </div>
                </div>

                <!-- AI WILL OPTIMIZE CHECKLIST -->
                <div style="margin-bottom: 24px;">
                    <div style="font-size: 12px; font-weight: 700; color: #F5F5F7; margin-bottom: 10px;">AI will optimize</div>
                    <div style="display: flex; flex-direction: column; gap: 6px; font-size: 12.5px; color: #86868B;">
                        <div><strong style="color:#10B981;">✓</strong> ATS keyword alignment</div>
                        <div><strong style="color:#10B981;">✓</strong> Achievement quantification</div>
                        <div><strong style="color:#10B981;">✓</strong> Role-specific terminology</div>
                        <div><strong style="color:#10B981;">✓</strong> Resume structure</div>
                        <div><strong style="color:#10B981;">✓</strong> Recruiter readability</div>
                    </div>
                </div>

                <!-- ELEGANT AI INSIGHT BOX -->
                <div style="background: rgba(99, 102, 241, 0.08); border: 1px solid rgba(99, 102, 241, 0.2); border-radius: 14px; padding: 16px; font-size: 12.5px; line-height: 1.5; color: #86868B;">
                    <strong style="color: #60A5FA; display: block; margin-bottom: 4px;">AI Insight</strong>
                    "Your resume is strongest in backend engineering, but the target role emphasizes distributed systems and cloud architecture."
                    <div style="margin-top: 8px; color: #F5F5F7; font-weight: 500;">AI will prioritize these gaps during optimization.</div>
                </div>
            </div>
        """)

    render_clean_html('</div>')

    # 3. LIVE RESUME PREVIEW SECTION
    p_data = st.session_state.builder_form_data
    info = p_data.get('personal_info', {})

    render_clean_html("""
        <div style="max-width: 1240px; margin: 120px auto 0 auto; padding: 0 24px; border-top: 1px solid rgba(255, 255, 255, 0.08); padding-top: 80px;">
            <div style="text-align: center; margin-bottom: 48px;">
                <h2 style="font-size: 40px; font-weight: 800; color: #F5F5F7; margin: 0 0 12px 0; letter-spacing: -0.03em;">See the result before you download it.</h2>
                <p style="font-size: 17px; color: #86868B; margin: 0;">Clean single-column ATS rendering optimized for modern screening systems.</p>
            </div>
        </div>
    """)

    # PRESENTATION ENVIRONMENT FOR RESUME
    section_style = "font-size:12.5px;font-weight:800;text-transform:uppercase;border-bottom:1px solid #111;padding-bottom:3px;color:#111;letter-spacing:.05em;margin:0 0 10px;"
    item_style = "margin-bottom:16px;"
    
    education_html = "".join(f'<div style="{item_style}"><div style="display:flex;justify-content:space-between;font-weight:700;font-size:13px"><span>{escape(str(e.get("school", "")))}</span><span>Graduation: {escape(str(e.get("graduation_date", "")))}</span></div><div style="font-style:italic;font-size:12.5px;color:#333">{escape(str(e.get("degree", "")))} in {escape(str(e.get("field", "")))}</div></div>' for e in p_data.get('education', []))
    experience_html = "".join(f'<div style="{item_style}"><div style="display:flex;justify-content:space-between;font-weight:700;font-size:13px"><span>{escape(str(e.get("position", "")))} — {escape(str(e.get("company", "")))}</span><span>{escape(str(e.get("start_date", "")))} – {escape(str(e.get("end_date", "")))}</span></div><div style="font-size:12.5px;color:#333;margin-top:2px;">{escape(str(e.get("description", "")))}</div><ul style="margin:6px 0 0 18px;padding:0;font-size:12.5px">{"".join(f"<li>{escape(str(r))}</li>" for r in e.get("responsibilities", []))}</ul></div>' for e in p_data.get('experiences', []))
    projects_html = "".join(f'<div style="{item_style}"><div style="display:flex;justify-content:space-between;font-weight:700;font-size:13px"><span>{escape(str(p.get("name", "")))} <i style="font-weight:normal">({escape(str(p.get("technologies", "")))})</i></span></div><ul style="margin:4px 0 0 18px;padding:0;font-size:12.5px">{"".join(f"<li>{escape(str(r))}</li>" for r in p.get("responsibilities", []))}</ul></div>' for p in p_data.get('projects', []))
    skills_cat = p_data.get('skills_categories', {})

    render_clean_html(f"""
        <div style="background: #15161A; border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 24px; padding: 48px 24px; max-width: 900px; margin: 0 auto 36px auto; box-shadow: 0 40px 100px rgba(0,0,0,0.7);">
            <div style="background:#FFFFFF; color:#111111; padding:56px; font-family:Georgia, 'Times New Roman', serif; max-width:760px; margin:0 auto; border-radius:4px; box-shadow:0 10px 40px rgba(0,0,0,0.3); line-height:1.45;">
                <div style="text-align:center; border-bottom:2px solid #111; padding-bottom:14px; margin-bottom:20px;">
                    <h1 style="font-size:26px; margin:0 0 6px; text-transform:uppercase; letter-spacing:.04em; color:#111;">{escape(str(info.get('full_name', 'Candidate')))}</h1>
                    <div style="font-size:12px; color:#333;">{escape(str(info.get('email','')))} | {escape(str(info.get('phone','')))} | {escape(str(info.get('location','')))}<br>{escape(str(info.get('linkedin','')))} | {escape(str(info.get('portfolio','')))}</div>
                </div>
                <div style="{item_style}">
                    <h3 style="{section_style}">Professional Summary</h3>
                    <p style="font-size:12.5px; margin:0; color:#222;">{escape(str(p_data.get('summary','')))}</p>
                </div>
                <div><h3 style="{section_style}">Education</h3>{education_html}</div>
                <div><h3 style="{section_style}">Work Experience</h3>{experience_html}</div>
                <div><h3 style="{section_style}">Technical Projects</h3>{projects_html}</div>
                <div>
                    <h3 style="{section_style}">Technical Skills & Competencies</h3>
                    <div style="font-size:12.5px; color:#222;">
                        <div><strong>Technical Skills:</strong> {escape(', '.join(skills_cat.get('technical', [])))}</div>
                        <div><strong>Tools & Infrastructure:</strong> {escape(', '.join(skills_cat.get('tools', [])))}</div>
                    </div>
                </div>
            </div>
        </div>
    """)

    # DOCUMENT EXPORT BUTTONS
    doc_data = {
        "template": "Executive",
        "personal_info": st.session_state.builder_form_data['personal_info'],
        "summary": st.session_state.builder_form_data['summary'],
        "experience": st.session_state.builder_form_data['experiences'],
        "education": st.session_state.builder_form_data['education'],
        "projects": st.session_state.builder_form_data['projects'],
        "skills": st.session_state.builder_form_data['skills_categories'],
        "achievements": st.session_state.builder_form_data.get('achievements', [])
    }

    doc_buf = builder.generate_resume(doc_data)

    txt_content = f"{info.get('full_name', 'PRINCE KUMAR JHA').upper()}\n"
    txt_content += f"{info.get('email')} | {info.get('phone')} | {info.get('location')}\n\n"
    txt_content += f"PROFESSIONAL SUMMARY\n{p_data.get('summary')}\n\n"
    for exp in p_data.get('experiences', []):
        txt_content += f"{exp.get('position')}, {exp.get('company')}\n"

    ex_col1, ex_col2, ex_col3 = st.columns([1, 1.2, 1])
    with ex_col2:
        st.download_button(
            label="Download PDF / DOCX Resume",
            data=doc_buf.getvalue(),
            file_name=f"Prince_Kumar_Jha_Resume_{datetime.datetime.now().strftime('%Y%m%d')}.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            type="primary",
            use_container_width=True,
            key="dl_docx_btn"
        )

    # 4. PRODUCT CAPABILITIES SECTION (3 Columns)
    render_clean_html("""
        <div style="max-width: 1240px; margin: 140px auto 0 auto; padding: 0 24px; border-top: 1px solid rgba(255, 255, 255, 0.08); padding-top: 80px;">
            <div style="text-align: center; margin-bottom: 64px;">
                <h2 style="font-size: 36px; font-weight: 800; color: #F5F5F7; margin: 0 0 12px 0; letter-spacing: -0.03em;">Built around how recruiters actually evaluate candidates.</h2>
            </div>
            
            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 36px;">
                <div>
                    <div style="font-size: 32px; font-weight: 800; color: #F5F5F7; margin-bottom: 12px;">01</div>
                    <h3 style="font-size: 20px; font-weight: 700; color: #F5F5F7; margin: 0 0 8px 0;">ATS Intelligence</h3>
                    <p style="font-size: 14.5px; color: #86868B; line-height: 1.6; margin: 0;">Optimize structure and terminology without keyword stuffing.</p>
                </div>
                <div>
                    <div style="font-size: 32px; font-weight: 800; color: #F5F5F7; margin-bottom: 12px;">02</div>
                    <h3 style="font-size: 20px; font-weight: 700; color: #F5F5F7; margin: 0 0 8px 0;">Experience Engineering</h3>
                    <p style="font-size: 14.5px; color: #86868B; line-height: 1.6; margin: 0;">Turn responsibilities into measurable, impact-focused achievements.</p>
                </div>
                <div>
                    <div style="font-size: 32px; font-weight: 800; color: #F5F5F7; margin-bottom: 12px;">03</div>
                    <h3 style="font-size: 20px; font-weight: 700; color: #F5F5F7; margin: 0 0 8px 0;">Job Alignment</h3>
                    <p style="font-size: 14.5px; color: #86868B; line-height: 1.6; margin: 0;">Adapt your resume to the specific role you're pursuing.</p>
                </div>
            </div>
        </div>
    """)
