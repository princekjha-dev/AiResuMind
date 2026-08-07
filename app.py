import textwrap

def render_clean_html(html_str):
    """Cleanly render HTML by stripping multiline indentation to prevent Markdown code block bugs."""
    if not html_str:
        return
    lines = [line.strip() for line in html_str.splitlines() if line.strip()]
    cleaned = chr(10).join(lines)
    st.markdown(cleaned, unsafe_allow_html=True)

"""
AiResuMind - Main Application
"""
from jobs.job_search import render_job_search
from datetime import datetime
import ui_components
from ui_components import (
    apply_modern_styles, hero_section, page_header, render_top_nav, render_feature_cards_grid,
    render_primary_cta, render_footer
)

def render_trusted_by_section():
    if hasattr(ui_components, 'render_trusted_by_section'):
        ui_components.render_trusted_by_section()

def render_product_showcase():
    if hasattr(ui_components, 'render_product_showcase'):
        ui_components.render_product_showcase()

def render_testimonials_section():
    if hasattr(ui_components, 'render_testimonials_section'):
        ui_components.render_testimonials_section()

def render_pricing_section():
    if hasattr(ui_components, 'render_pricing_section'):
        ui_components.render_pricing_section()

def render_analytics_preview_section():
    if hasattr(ui_components, 'render_analytics_preview_section'):
        ui_components.render_analytics_preview_section()

def render_faq_section():
    if hasattr(ui_components, 'render_faq_section'):
        ui_components.render_faq_section()
from feedback.feedback import FeedbackManager
import io
import requests
from dashboard.dashboard import DashboardManager
from config.courses import COURSES_BY_CATEGORY, RESUME_VIDEOS, INTERVIEW_VIDEOS, get_courses_for_role, get_category_for_role
from config.job_roles import JOB_ROLES
from config.database import (
    get_database_connection, save_resume_data, save_analysis_data,
    init_database, save_ai_analysis_data
)
from utils.ai_resume_analyzer import AIResumeAnalyzer
from utils.resume_builder import ResumeBuilder
from utils.resume_analyzer import ResumeAnalyzer
from utils.cover_letter import CoverLetterGenerator
from utils.interview_prep import InterviewPrepGenerator
import traceback
import pandas as pd
import streamlit as st
import datetime

from pages.resume_analyzer import render_resume_analyzer_page
from pages.resume_builder import render_resume_builder_page
from pages.cover_letter import render_cover_letter_page
from pages.interview_prep import render_interview_prep_page
from pages.about import render_about_page

# Set page config at the very beginning
st.set_page_config(
    page_title="Application",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="collapsed"
)


class ResumeApp:
    def __init__(self):
        """Initialize the application"""
        if 'form_data' not in st.session_state:
            st.session_state.form_data = {
                'personal_info': {
                    'full_name': '',
                    'email': '',
                    'phone': '',
                    'location': '',
                    'linkedin': '',
                    'portfolio': ''
                },
                'summary': '',
                'experiences': [],
                'education': [],
                'projects': [],
                'skills_categories': {
                    'technical': [],
                    'soft': [],
                    'languages': [],
                    'tools': []
                }
            }

        # Initialize navigation state
        if 'page' not in st.session_state:
            st.session_state.page = 'home'

        # Initialize admin state
        if 'is_admin' not in st.session_state:
            st.session_state.is_admin = False

        self.pages = {
            "HOME": self.render_home,
            "RESUME ANALYZER": render_resume_analyzer_page,
            "RESUME BUILDER": render_resume_builder_page,
            "COVER LETTER": render_cover_letter_page,
            "INTERVIEW PREP": render_interview_prep_page,
            "DASHBOARD": self.render_dashboard,
            "JOB SEARCH": self.render_job_search,
            "FEEDBACK": self.render_feedback_page,
            "ABOUT": render_about_page
        }

        # Initialize dashboard manager
        self.dashboard_manager = DashboardManager()

        self.analyzer = ResumeAnalyzer()
        self.ai_analyzer = AIResumeAnalyzer()
        self.builder = ResumeBuilder()
        self.job_roles = JOB_ROLES

        # Initialize session state
        if 'user_id' not in st.session_state:
            st.session_state.user_id = 'default_user'
        if 'selected_role' not in st.session_state:
            st.session_state.selected_role = None

        # Initialize database
        init_database()

        # Load external CSS
        with open('style/style.css') as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

        # Load Google Fonts (Fraunces & Inter)
        render_clean_html("""
            <link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;600;700;800&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
        """)

        if 'resume_data' not in st.session_state:
            st.session_state.resume_data = []
        if 'ai_analysis_stats' not in st.session_state:
            st.session_state.ai_analysis_stats = {
                'score_distribution': {},
                'total_analyses': 0,
                'average_score': 0
            }

    def load_lottie_url(self, url: str):
        """Load Lottie animation from URL"""
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()

    def apply_global_styles(self):
        render_clean_html("""
        <style>
        /* Custom Scrollbar */
        ::-webkit-scrollbar {
            width: 6px;
            height: 6px;
        }

        ::-webkit-scrollbar-track {
            background: var(--bg-primary);
        }

        ::-webkit-scrollbar-thumb {
            background: #D1D5DB;
            border-radius: 3px;
        }

        /* ── Zero default Streamlit top gap ── */
        .main .block-container {
            padding-top: 0 !important;
            margin-top: 0 !important;
        }
        [data-testid="stAppViewBlockContainer"] {
            padding-top: 0 !important;
        }
        .stApp > header { display: none !important; }

        /* Hide Streamlit sidebar & toggle entirely */
        section[data-testid="stSidebar"],
        div[data-testid="stSidebarCollapsedControl"],
        button[data-testid="baseButton-headerNoPadding"],
        [data-testid="collapsedControl"],
        .st-emotion-cache-1cypcdb {
            display: none !important;
            width: 0 !important;
            min-width: 0 !important;
            overflow: hidden !important;
        }

        /* Global Styles */
        .main-header {
            background: var(--bg-surface);
            border: 1px solid var(--border-subtle);
            padding: 2rem;
            border-radius: var(--radius-lg);
            margin-bottom: 2rem;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
            text-align: center;
        }

        .main-header h1 {
            color: var(--text-primary);
            font-size: 2.25rem;
            font-weight: 700;
            margin: 0;
        }

        /* Template Card Styles */
        .template-container {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 1.5rem;
            padding: 0.5rem;
        }

        .template-card {
            background: var(--bg-surface);
            border-radius: var(--radius-lg);
            padding: 1.75rem;
            position: relative;
            border: 1px solid var(--border-subtle);
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
            transition: all 0.2s ease;
        }

        .template-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 16px rgba(11, 122, 94, 0.1);
            border-color: var(--accent);
        }

        .template-icon {
            font-size: 2.5rem;
            color: var(--accent);
            margin-bottom: 1.25rem;
        }

        .template-title {
            font-size: 1.35rem;
            font-weight: 700;
            color: var(--text-primary);
            margin-bottom: 0.75rem;
        }

        .template-description {
            color: var(--text-secondary);
            margin-bottom: 1.25rem;
            font-size: 0.9rem;
            line-height: 1.5;
        }

        /* Feature List Styles */
        .feature-list {
            list-style: none;
            padding: 0;
            margin: 1.25rem 0;
        }

        .feature-item {
            display: flex;
            align-items: center;
            margin-bottom: 0.75rem;
            color: var(--text-primary);
            font-size: 0.9rem;
        }

        .feature-icon {
            color: var(--accent);
            margin-right: 0.75rem;
            font-size: 1rem;
        }

        /* Button Styles */
        .action-button {
            background: var(--accent);
            color: #FFFFFF;
            padding: 0.75rem 1.5rem;
            border-radius: var(--radius-md);
            border: none;
            font-weight: 600;
            font-size: 0.9rem;
            cursor: pointer;
            width: 100%;
            text-align: center;
            transition: all 0.15s ease-in-out;
            box-shadow: 0 1px 2px rgba(0,0,0,0.05);
        }

        .action-button:hover {
            background: var(--accent-hover);
            color: #FFFFFF;
            transform: translateY(-1px);
            box-shadow: 0 4px 8px rgba(11, 122, 94, 0.2);
        }

        /* Form Section Styles */
        .form-section {
            background: var(--bg-surface);
            border-radius: var(--radius-lg);
            padding: 2rem;
            margin: 1.5rem 0;
            border: 1px solid var(--border-subtle);
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        }

        .form-section-title {
            font-size: 1.35rem;
            font-weight: 700;
            color: var(--text-primary);
            margin-bottom: 1.25rem;
            padding-bottom: 0.5rem;
            border-bottom: 2px solid var(--border-subtle);
        }

        .form-group {
            margin-bottom: 1.25rem;
        }

        .form-label {
            color: var(--text-primary);
            font-weight: 600;
            font-size: 0.9rem;
            margin-bottom: 0.5rem;
            display: block;
        }

        .form-input {
            width: 100%;
            padding: 0.75rem 1rem;
            border-radius: var(--radius-md);
            border: 1px solid var(--border-subtle);
            background: var(--bg-surface);
            color: var(--text-primary);
            transition: all 0.15s ease;
        }

        .form-input:focus {
            border-color: var(--accent);
            box-shadow: 0 0 0 3px rgba(11, 122, 94, 0.15);
            outline: none;
        }

        /* Skill Tags */
        .skill-tag-container {
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
            margin-top: 0.75rem;
        }

        .skill-tag {
            background: var(--bg-surface-raised);
            color: var(--text-primary);
            padding: 0.4rem 0.85rem;
            border-radius: 9999px;
            border: 1px solid var(--border-subtle);
            font-size: 0.85rem;
            font-weight: 500;
            transition: all 0.15s ease;
            cursor: pointer;
        }

        .skill-tag:hover {
            background: var(--success-bg);
            color: var(--success-text);
            border-color: #A7F3D0;
        }

        /* Progress Circle */
        .progress-container {
            position: relative;
            width: 140px;
            height: 140px;
            margin: 1.5rem auto;
        }

        .progress-circle {
            transform: rotate(-90deg);
            width: 100%;
            height: 100%;
        }

        .progress-circle circle {
            fill: none;
            stroke-width: 8;
            stroke-linecap: round;
            stroke: var(--accent);
            transform-origin: 50% 50%;
            transition: all 0.3s ease;
        }

        .progress-text {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            font-size: 1.5rem;
            font-weight: 700;
            color: var(--text-primary);
        }
        .main .block-container {
            padding-top: 0 !important;
            padding-bottom: 2rem;
        }
        .feature-card {
            background-color: var(--bg-surface);
            border: 1px solid var(--border-subtle);
            border-radius: var(--radius-lg);
            padding: 1.5rem;
            margin-bottom: 1rem;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
        }
        
        /* Animations */
        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateY(15px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .animate-slide-in {
            animation: slideIn 0.3s ease-out forwards;
        }

        /* Responsive Design */
        @media (max-width: 768px) {
            .template-container {
                grid-template-columns: 1fr;
            }

            .main-header {
                padding: 1.25rem;
            }

            .main-header h1 {
                font-size: 1.75rem;
            }

            .template-card {
                padding: 1.25rem;
            }

            .action-button {
                padding: 0.7rem 1.25rem;
            }
        }
        </style>
        """)
        
    def add_footer(self):
        """Add a clean, neutral footer to all pages."""
        render_footer()


    def export_to_excel(self):
        """Export resume data to Excel"""
        conn = get_database_connection()

        # Get resume data with analysis
        query = """
            SELECT
                rd.name, rd.email, rd.phone, rd.linkedin, rd.github, rd.portfolio,
                rd.summary, rd.target_role, rd.target_category,
                rd.education, rd.experience, rd.projects, rd.skills,
                ra.ats_score, ra.keyword_match_score, ra.format_score, ra.section_score,
                ra.missing_skills, ra.recommendations,
                rd.created_at
            FROM resume_data rd
            LEFT JOIN resume_analysis ra ON rd.id = ra.resume_id
        """

        try:
            # Read data into DataFrame
            df = pd.read_sql_query(query, conn)

            # Create Excel writer object
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name='Resume Data')

            return output.getvalue()
        except Exception as e:
            print(f"Error exporting to Excel: {str(e)}")
            return None
        finally:
            conn.close()

    def render_dashboard(self):
        """Render the dashboard page"""
        self.dashboard_manager.render_dashboard()


    def render_empty_state(self, icon, message):
        """Render an empty state with icon and message"""
        return f"""
            <div style='text-align: center; padding: 2rem; color: #666;'>
                <i class='{icon}' style='font-size: 2rem; margin-bottom: 1rem; color: #aaaaaa;'></i>
                <p style='margin: 0;'>{message}</p>
            </div>
        """

    def analyze_resume(self, resume_text):
        """Analyze resume and store results"""
        analytics = self.analyzer.analyze_resume(resume_text)
        st.session_state.analytics_data = analytics
        return analytics

    def handle_resume_upload(self):
        """Handle resume upload and analysis"""
        uploaded_file = st.file_uploader(
            "Upload your resume", type=['pdf', 'docx', 'doc', 'txt', 'PDF', 'DOCX'])

        if uploaded_file is not None:
            try:
                # Extract text from resume safely
                analyzer = self.ai_analyzer
                fname = (uploaded_file.name or "").lower()
                ftype = (uploaded_file.type or "").lower()

                if fname.endswith(".pdf") or "pdf" in ftype:
                    resume_text = analyzer.extract_text_from_pdf(uploaded_file)
                elif fname.endswith(".docx") or fname.endswith(".doc") or "word" in ftype or "officedocument" in ftype:
                    resume_text = analyzer.extract_text_from_docx(uploaded_file)
                else:
                    if hasattr(uploaded_file, 'seek'):
                        uploaded_file.seek(0)
                    resume_text = uploaded_file.getvalue().decode('utf-8', errors='ignore')

                # Store resume data
                st.session_state.resume_data = {
                    'filename': uploaded_file.name,
                    'content': resume_text,
                    'upload_time': datetime.now().isoformat()
                }

                # Analyze resume
                self.analyzer.analyze_resume({'raw_text': resume_text}, None)

                return True
            except Exception as e:
                st.error(f"Error processing resume: {str(e)}")
                return False
        return False

    def render_builder(self):
        apply_modern_styles()
        hero_section(
            "Prompt-Based AI Resume Builder",
            "Instantly build an ATS-aligned, executive resume tailored to any Job Description (JD) using custom AI prompts.",
            "Powered by multi-provider AI engine to optimize keywords, metric bullet points, and ATS compliance."
        )

        # AI Generator Card
        with st.expander("AI Auto-Generator (Target Job Description & Custom Prompt)", expanded=True):
            st.markdown("Provide a target **Job Description (JD)** and optional **AI Prompt Instructions** below to auto-generate a complete, ATS-optimized resume structure:")
            
            pcol1, pcol2 = st.columns(2)
            with pcol1:
                target_jd = st.text_area(
                    "Target Job Description (JD)",
                    placeholder="Paste the target job description, requirements, or key skills here...",
                    height=130,
                    key="builder_jd_input"
                )
            with pcol2:
                custom_prompt = st.text_area(
                    "Custom AI Instructions / Career Prompt",
                    placeholder="e.g. 'Senior Full Stack Engineer with 4 years experience. Emphasize React, Python, System Design, and cloud deployments.'",
                    height=130,
                    key="builder_prompt_input"
                )

            if st.button("GENERATE TAILORED RESUME WITH AI", type="primary", use_container_width=True):
                if target_jd.strip() or custom_prompt.strip():
                    with st.spinner("AI is analyzing Job Description & drafting ATS-aligned resume content..."):
                        c_info = st.session_state.form_data.get('personal_info', {})
                        ai_result = self.ai_analyzer.generate_prompt_based_resume(target_jd, custom_prompt, c_info)
                        
                        # Populate session state form_data
                        if ai_result.get('summary'):
                            st.session_state.form_data['summary'] = ai_result['summary']
                        if ai_result.get('experience'):
                            st.session_state.form_data['experiences'] = ai_result['experience']
                        if ai_result.get('projects'):
                            st.session_state.form_data['projects'] = ai_result['projects']
                        if ai_result.get('education'):
                            st.session_state.form_data['education'] = ai_result['education']
                        if ai_result.get('skills'):
                            st.session_state.form_data['skills_categories'] = ai_result['skills']
                        if ai_result.get('personal_info') and ai_result['personal_info'].get('title'):
                            st.session_state.form_data['personal_info']['title'] = ai_result['personal_info']['title']
                            
                        st.success(f"Successfully generated ATS-tailored resume content! (Model: {ai_result.get('model_used', 'AI')})")
                else:
                    st.warning("Please provide a Job Description or Custom Prompt to run AI generation.")

        st.markdown("<hr style='border-color: var(--border-subtle); margin: 2rem 0;'>", unsafe_allow_html=True)
        st.subheader("Manual Form Review & Customization")

        # Template selection
        template_options = ["Modern", "Professional", "Minimal", "Creative"]
        selected_template = st.selectbox("Select Resume Template", template_options)

        # Personal Information
        st.subheader("Personal Information")

        col1, col2 = st.columns(2)
        with col1:
            # Get existing values from session state
            existing_name = st.session_state.form_data['personal_info']['full_name']
            existing_email = st.session_state.form_data['personal_info']['email']
            existing_phone = st.session_state.form_data['personal_info']['phone']

            # Input fields with existing values
            full_name = st.text_input("Full Name", value=existing_name)
            email = st.text_input(
    "Email",
    value=existing_email,
     key="email_input")
            phone = st.text_input("Phone", value=existing_phone)

            # Immediately update session state after email input
            if 'email_input' in st.session_state:
                st.session_state.form_data['personal_info']['email'] = st.session_state.email_input

        with col2:
            # Get existing values from session state
            existing_location = st.session_state.form_data['personal_info']['location']
            existing_linkedin = st.session_state.form_data['personal_info']['linkedin']
            existing_portfolio = st.session_state.form_data['personal_info']['portfolio']

            # Input fields with existing values
            location = st.text_input("Location", value=existing_location)
            linkedin = st.text_input("LinkedIn URL", value=existing_linkedin)
            portfolio = st.text_input(
    "Portfolio Website", value=existing_portfolio)

        # Update personal info in session state
        st.session_state.form_data['personal_info'] = {
            'full_name': full_name,
            'email': email,
            'phone': phone,
            'location': location,
            'linkedin': linkedin,
            'portfolio': portfolio
        }

        # Professional Summary
        st.subheader("Professional Summary")
        summary = st.text_area("Professional Summary", value=st.session_state.form_data.get('summary', ''), height=150,
                             help="Write a brief summary highlighting your key skills and experience")

        # Experience Section
        st.subheader("Work Experience")
        if 'experiences' not in st.session_state.form_data:
            st.session_state.form_data['experiences'] = []

        if st.button("Add Experience"):
            st.session_state.form_data['experiences'].append({
                'company': '',
                'position': '',
                'start_date': '',
                'end_date': '',
                'description': '',
                'responsibilities': [],
                'achievements': []
            })

        for idx, exp in enumerate(st.session_state.form_data['experiences']):
            with st.expander(f"Experience {idx + 1}", expanded=True):
                col1, col2 = st.columns(2)
                with col1:
                    exp['company'] = st.text_input(
    "Company Name",
    key=f"company_{idx}",
    value=exp.get(
        'company',
         ''))
                    exp['position'] = st.text_input(
    "Position", key=f"position_{idx}", value=exp.get(
        'position', ''))
                with col2:
                    exp['start_date'] = st.text_input(
    "Start Date", key=f"start_date_{idx}", value=exp.get(
        'start_date', ''))
                    exp['end_date'] = st.text_input(
    "End Date", key=f"end_date_{idx}", value=exp.get(
        'end_date', ''))

                exp['description'] = st.text_area("Role Overview", key=f"desc_{idx}",
                                                value=exp.get(
                                                    'description', ''),
                                                help="Brief overview of your role and impact")

                # Responsibilities
                st.markdown("##### Key Responsibilities")
                resp_text = st.text_area("Enter responsibilities (one per line)",
                                       key=f"resp_{idx}",
                                       value='\n'.join(
                                           exp.get('responsibilities', [])),
                                       height=100,
                                       help="List your main responsibilities, one per line")
                exp['responsibilities'] = [r.strip()
                                                   for r in resp_text.split('\n') if r.strip()]

                # Achievements
                st.markdown("##### Key Achievements")
                achv_text = st.text_area("Enter achievements (one per line)",
                                       key=f"achv_{idx}",
                                       value='\n'.join(
                                           exp.get('achievements', [])),
                                       height=100,
                                       help="List your notable achievements, one per line")
                exp['achievements'] = [a.strip()
                                               for a in achv_text.split('\n') if a.strip()]

                if st.button("Remove Experience", key=f"remove_exp_{idx}"):
                    st.session_state.form_data['experiences'].pop(idx)
                    st.rerun()

        # Projects Section
        st.subheader("Projects")
        if 'projects' not in st.session_state.form_data:
            st.session_state.form_data['projects'] = []

        if st.button("Add Project"):
            st.session_state.form_data['projects'].append({
                'name': '',
                'technologies': '',
                'description': '',
                'responsibilities': [],
                'achievements': [],
                'link': ''
            })

        for idx, proj in enumerate(st.session_state.form_data['projects']):
            with st.expander(f"Project {idx + 1}", expanded=True):
                proj['name'] = st.text_input(
    "Project Name",
    key=f"proj_name_{idx}",
    value=proj.get(
        'name',
         ''))
                proj['technologies'] = st.text_input("Technologies Used", key=f"proj_tech_{idx}",
                                                   value=proj.get(
                                                       'technologies', ''),
                                                   help="List the main technologies, frameworks, and tools used")

                proj['description'] = st.text_area("Project Overview", key=f"proj_desc_{idx}",
                                                 value=proj.get(
                                                     'description', ''),
                                                 help="Brief overview of the project and its goals")

                # Project Responsibilities
                st.markdown("##### Key Responsibilities")
                proj_resp_text = st.text_area("Enter responsibilities (one per line)",
                                            key=f"proj_resp_{idx}",
                                            value='\n'.join(
                                                proj.get('responsibilities', [])),
                                            height=100,
                                            help="List your main responsibilities in the project")
                proj['responsibilities'] = [r.strip()
                                                    for r in proj_resp_text.split('\n') if r.strip()]

                # Project Achievements
                st.markdown("##### Key Achievements")
                proj_achv_text = st.text_area("Enter achievements (one per line)",
                                            key=f"proj_achv_{idx}",
                                            value='\n'.join(
                                                proj.get('achievements', [])),
                                            height=100,
                                            help="List the project's key achievements and your contributions")
                proj['achievements'] = [a.strip()
                                                for a in proj_achv_text.split('\n') if a.strip()]

                proj['link'] = st.text_input("Project Link (optional)", key=f"proj_link_{idx}",
                                           value=proj.get('link', ''),
                                           help="Link to the project repository, demo, or documentation")

                if st.button("Remove Project", key=f"remove_proj_{idx}"):
                    st.session_state.form_data['projects'].pop(idx)
                    st.rerun()

        # Education Section
        st.subheader("Education")
        if 'education' not in st.session_state.form_data:
            st.session_state.form_data['education'] = []

        if st.button("Add Education"):
            st.session_state.form_data['education'].append({
                'school': '',
                'degree': '',
                'field': '',
                'graduation_date': '',
                'gpa': '',
                'achievements': []
            })

        for idx, edu in enumerate(st.session_state.form_data['education']):
            with st.expander(f"Education {idx + 1}", expanded=True):
                col1, col2 = st.columns(2)
                with col1:
                    edu['school'] = st.text_input(
    "School/University",
    key=f"school_{idx}",
    value=edu.get(
        'school',
         ''))
                    edu['degree'] = st.text_input(
    "Degree", key=f"degree_{idx}", value=edu.get(
        'degree', ''))
                with col2:
                    edu['field'] = st.text_input(
    "Field of Study",
    key=f"field_{idx}",
    value=edu.get(
        'field',
         ''))
                    edu['graduation_date'] = st.text_input("Graduation Date", key=f"grad_date_{idx}",
                                                         value=edu.get('graduation_date', ''))

                edu['gpa'] = st.text_input(
    "GPA (optional)",
    key=f"gpa_{idx}",
    value=edu.get(
        'gpa',
         ''))

                # Educational Achievements
                st.markdown("##### Achievements & Activities")
                edu_achv_text = st.text_area("Enter achievements (one per line)",
                                           key=f"edu_achv_{idx}",
                                           value='\n'.join(
                                               edu.get('achievements', [])),
                                           height=100,
                                           help="List academic achievements, relevant coursework, or activities")
                edu['achievements'] = [a.strip()
                                               for a in edu_achv_text.split('\n') if a.strip()]

                if st.button("Remove Education", key=f"remove_edu_{idx}"):
                    st.session_state.form_data['education'].pop(idx)
                    st.rerun()

        # Skills Section
        st.subheader("Skills")
        if 'skills_categories' not in st.session_state.form_data:
            st.session_state.form_data['skills_categories'] = {
                'technical': [],
                'soft': [],
                'languages': [],
                'tools': []
            }

        col1, col2 = st.columns(2)
        with col1:
            tech_skills = st.text_area("Technical Skills (one per line)",
                                     value='\n'.join(
    st.session_state.form_data['skills_categories']['technical']),
                                     height=150,
                                     help="Programming languages, frameworks, databases, etc.")
            st.session_state.form_data['skills_categories']['technical'] = [
                s.strip() for s in tech_skills.split('\n') if s.strip()]

            soft_skills = st.text_area("Soft Skills (one per line)",
                                     value='\n'.join(
    st.session_state.form_data['skills_categories']['soft']),
                                     height=150,
                                     help="Leadership, communication, problem-solving, etc.")
            st.session_state.form_data['skills_categories']['soft'] = [
                s.strip() for s in soft_skills.split('\n') if s.strip()]

        with col2:
            languages = st.text_area("Languages (one per line)",
                                   value='\n'.join(
    st.session_state.form_data['skills_categories']['languages']),
                                   height=150,
                                   help="Programming or human languages with proficiency level")
            st.session_state.form_data['skills_categories']['languages'] = [
                l.strip() for l in languages.split('\n') if l.strip()]

            tools = st.text_area("Tools & Technologies (one per line)",
                               value='\n'.join(
    st.session_state.form_data['skills_categories']['tools']),
                               height=150,
                               help="Development tools, software, platforms, etc.")
            st.session_state.form_data['skills_categories']['tools'] = [
                t.strip() for t in tools.split('\n') if t.strip()]

        # Update form data in session state
        st.session_state.form_data.update({
            'summary': summary
        })

        # Generate Resume button
        if st.button("Generate Resume", type="primary"):
            print(
    f"Email input value: {
        st.session_state.get(
            'email_input',
             '')}")

            # Get the current values from form
            current_name = st.session_state.form_data['personal_info']['full_name'].strip(
            )
            current_email = st.session_state.email_input if 'email_input' in st.session_state else ''

            # Validate required fields
            if not current_name:
                st.error("Please enter your full name.")
                return

            if not current_email:
                st.error("Please enter your email address.")
                return

            # Update email in form data one final time
            st.session_state.form_data['personal_info']['email'] = current_email

            try:
                # Prepare resume data with current form values
                resume_data = {
                    "personal_info": st.session_state.form_data['personal_info'],
                    "summary": st.session_state.form_data.get('summary', '').strip(),
                    "experience": st.session_state.form_data.get('experiences', []),
                    "education": st.session_state.form_data.get('education', []),
                    "projects": st.session_state.form_data.get('projects', []),
                    "skills": st.session_state.form_data.get('skills_categories', {
                        'technical': [],
                        'soft': [],
                        'languages': [],
                        'tools': []
                    }),
                    "template": selected_template
                }

                try:
                    # Generate resume
                    resume_buffer = self.builder.generate_resume(resume_data)
                    if resume_buffer:
                        try:
                            # Save resume data to database
                            save_resume_data(resume_data)

                            # Offer the resume for download
                            st.success("Resume generated successfully.")

                            st.download_button(
                                label="Download Resume",
                                data=resume_buffer,
                                file_name=f"{
    current_name.replace(
        ' ', '_')}_resume.docx",
                                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                                on_click=lambda: st.balloons()
                            )
                        except Exception as db_error:
                            print(
    f"Warning: Failed to save to database: {
        str(db_error)}")
                            # Still allow download even if database save fails
                            st.warning(
                                "Resume generated but could not be saved to database.")

                            st.download_button(
                                label="Download Resume",
                                data=resume_buffer,
                                file_name=f"{current_name.replace(' ', '_')}_resume.docx",
                                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                            )
                    else:
                        st.error(
                            "Failed to generate resume. Please try again.")
                        print("Resume buffer was None")
                except Exception as gen_error:
                    print(f"Error during resume generation: {str(gen_error)}")
                    print(f"Full traceback: {traceback.format_exc()}")
                    st.error(f"Error generating resume: {str(gen_error)}")

            except Exception as e:
                print(f"Error preparing resume data: {str(e)}")
                print(f"Full traceback: {traceback.format_exc()}")
                st.error(f"Error preparing resume data: {str(e)}")

    def render_about(self):
        """Render the about page"""
        # Apply modern styles
        from ui_components import apply_modern_styles
        import base64
        import os

        # Function to load image as base64
        def get_image_as_base64(file_path):
            try:
                with open(file_path, "rb") as image_file:
                    encoded = base64.b64encode(image_file.read()).decode()
                    return f"data:image/jpeg;base64,{encoded}"
            except:
                return None

        # Get image path and convert to base64
        image_path = os.path.join(
    os.path.dirname(__file__),
    "assets",
     "logo.jpg")
        get_image_as_base64(image_path)

        apply_modern_styles()

        # Add Font Awesome icons and custom CSS
        render_clean_html("""
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
            <style>
                .profile-section, .vision-section, .feature-card {
                    text-align: center;
                    padding: 2rem;
                    background: var(--bg-surface);
                    border: 1px solid var(--border-subtle);
                    border-radius: 20px;
                    margin: 2rem auto;
                    max-width: 800px;
                    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
                }

                .profile-image {
                    width: 200px;
                    height: 200px;
                    border-radius: 50%;
                    margin: 0 auto 1.5rem;
                    display: block;
                    object-fit: cover;
                    border: 4px solid var(--accent);
                }

                .profile-name {
                    font-size: 2.5rem;
                    color: var(--text-primary);
                    margin-bottom: 0.5rem;
                }

                .profile-title {
                    font-size: 1.2rem;
                    color: var(--text-secondary);
                    margin-bottom: 1.5rem;
                }

                .social-links {
                    display: flex;
                    justify-content: center;
                    gap: 1.5rem;
                    margin: 2rem 0;
                }

                .social-link {
                    font-size: 2rem;
                    color: var(--text-secondary);
                    transition: all 0.3s ease;
                    padding: 0.5rem;
                    border-radius: 50%;
                    background: var(--bg-surface-raised);
                    border: 1px solid var(--border-subtle);
                    width: 60px;
                    height: 60px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    text-decoration: none;
                }

                .social-link:hover {
                    transform: translateY(-5px);
                    background: var(--accent);
                    color: white;
                    box-shadow: 0 5px 15px rgba(11, 122, 94, 0.3);
                }

                .bio-text {
                    color: var(--text-primary);
                    line-height: 1.8;
                    font-size: 1.1rem;
                    margin-top: 2rem;
                    text-align: left;
                }

                .vision-text {
                    color: var(--text-primary);
                    line-height: 1.8;
                    font-size: 1.1rem;
                    font-style: italic;
                    margin: 1.5rem 0;
                    text-align: left;
                }

                .vision-icon {
                    font-size: 2.5rem;
                    color: var(--accent);
                    margin-bottom: 1rem;
                }

                .vision-title {
                    font-size: 2rem;
                    color: var(--text-primary);
                    margin-bottom: 1rem;
                }

                .features-grid {
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                    gap: 2rem;
                    margin: 2rem auto;
                    max-width: 1200px;
                }

                .feature-card {
                    padding: 2rem;
                    margin: 0;
                }

                .feature-icon {
                    font-size: 2.5rem;
                    color: var(--accent);
                    margin-bottom: 1rem;
                }

                .feature-title {
                    font-size: 1.5rem;
                    color: var(--text-primary);
                    margin: 1rem 0;
                }

                .feature-description {
                    color: var(--text-secondary);
                    line-height: 1.6;
                }
            </style>
        """)

        # Hero Section
        render_clean_html("""
            <div class="hero-section">
                <h1 class="hero-title">About AiResuMind</h1>
                <p class="hero-subtitle">An AI-driven platform for resume analysis and career development</p>
            </div>
        """)

        # Project description
        render_clean_html("""
            <div class='profile-section'>
                <h2 class='profile-name'>AiResuMind</h2>
                <p class='profile-title'>AI-powered resume analysis and career development platform</p>
                <p class='bio-text'>
                    AiResuMind uses advanced AI models to help job seekers analyse their resumes,
                    detect skill gaps, and receive targeted recommendations through data-driven insights.
                </p>
            </div>
        """)

        # Vision Section
        render_clean_html("""
            <div class="vision-section">
                <i class="fas fa-lightbulb vision-icon"></i>
                <h2 class="vision-title">Project Goal</h2>
                <p class="vision-text">
                    AiResuMind aims to make resume feedback accessible and actionable. By combining structured
                    ATS scoring with AI-generated analysis, it gives job seekers clear, concrete steps
                    to improve their documents at any stage of their career.
                </p>
            </div>
        """)

        # Features Section
        render_clean_html("""
            <div class="features-grid">
                <div class="feature-card">
                    <i class="fas fa-robot feature-icon"></i>
                    <h3 class="feature-title">AI-Powered Analysis</h3>
                    <p class="feature-description">
                        Advanced AI algorithms provide detailed insights and suggestions to optimize your resume for maximum impact.
                    </p>
                </div>
                <div class="feature-card">
                    <i class="fas fa-chart-line feature-icon"></i>
                    <h3 class="feature-title">Data-Driven Insights</h3>
                    <p class="feature-description">
                        Make informed decisions with our analytics-based recommendations and industry insights.
                    </p>
                </div>
                <div class="feature-card">
                    <i class="fas fa-shield-alt feature-icon"></i>
                    <h3 class="feature-title">Privacy First</h3>
                    <p class="feature-description">
                        Your data security is our priority. We ensure your information is always protected and private.
                    </p>
                </div>
            </div>
            <div style="text-align: center; margin: 3rem 0;">
                <a href="?page=analyzer" class="cta-button">
                    Start Your Journey
                    <i class="fas fa-arrow-right" style="margin-left: 10px;"></i>
                </a>
            </div>
        """)

    def render_analyzer(self):
        """Render the resume analyzer page"""
        apply_modern_styles()

        # Page Header
        page_header(
            "Resume Analyzer",
            "Get instant AI-powered feedback to optimize your resume"
        )

        # Create tabs for Normal Analyzer and AI Analyzer
        analyzer_tabs = st.tabs(["Standard Analyzer", "AI Analyzer"])

        with analyzer_tabs[0]:
            # Job Role Selection
            categories = list(self.job_roles.keys())
            selected_category = st.selectbox(
    "Job Category", categories, key="standard_category")

            roles = list(self.job_roles[selected_category].keys())
            selected_role = st.selectbox(
    "Specific Role", roles, key="standard_role")

            role_info = self.job_roles[selected_category][selected_role]

            # Display role information
            skills_html = "".join([f'<span class="skill-tag" style="margin-right: 6px; margin-bottom: 6px; display: inline-block;">{skill}</span>' for skill in role_info['required_skills']])
            render_clean_html(f"""
            <div style='background-color: var(--bg-surface); padding: 20px; border-radius: var(--radius-lg); margin: 15px 0; border: 1px solid var(--border-subtle); box-shadow: 0 1px 3px rgba(0,0,0,0.05);'>
                <h3 style='color: var(--text-primary); margin-top: 0; font-weight: 700; font-size: 1.25rem;'>{selected_role}</h3>
                <p style='color: var(--text-secondary); line-height: 1.5; font-size: 0.9rem;'>{role_info['description']}</p>
                <h4 style='color: var(--text-primary); font-weight: 600; font-size: 0.95rem; margin-top: 15px; margin-bottom: 10px;'>Required Skills:</h4>
                <div>
                    {skills_html}
                </div>
            </div>
            """)

            uploaded_file = st.file_uploader(
                "Upload your resume", type=['pdf', 'docx', 'doc', 'txt', 'PDF', 'DOCX', 'DOC'], key="standard_file")

            if not uploaded_file:
                # Display empty state with a prominent upload button
                st.markdown(
                    self.render_empty_state(
                    "fas fa-cloud-upload-alt",
                    "Upload your resume to get started with standard analysis"
                    ),
                    unsafe_allow_html=True
                )
                # Add a prominent upload button
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    render_clean_html("""
                    <style>
                    .upload-button {
                        background: var(--accent);
                        color: white;
                        border: none;
                        border-radius: 10px;
                        padding: 15px 25px;
                        font-size: 18px;
                        font-weight: bold;
                        cursor: pointer;
                        width: 100%;
                        text-align: center;
                        margin: 20px 0;
                        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
                        transition: all 0.3s ease;
                    }
                    .upload-button:hover {
                        transform: translateY(-3px);
                        box-shadow: 0 6px 15px rgba(0,0,0,0.1);
                    }

                    """)

            if uploaded_file:
                # Add a prominent analyze button
                analyze_standard = st.button("Analyze My Resume",
                                    type="primary",
                                    width='stretch',
                                    key="analyze_standard_button")

                if analyze_standard:
                    with st.spinner("Analyzing your document..."):
                        # Get file content safely with extension fallback and pointer reset
                        text = ""
                        fname = (uploaded_file.name or "").lower()
                        ftype = (uploaded_file.type or "").lower()
                        
                        try:
                            if fname.endswith(".pdf") or "pdf" in ftype:
                                try:
                                    text = self.ai_analyzer.extract_text_from_pdf(uploaded_file)
                                except Exception:
                                    text = self.analyzer.extract_text_from_pdf(uploaded_file)
                            elif fname.endswith(".docx") or fname.endswith(".doc") or "word" in ftype or "officedocument" in ftype:
                                try:
                                    text = self.ai_analyzer.extract_text_from_docx(uploaded_file)
                                except Exception:
                                    text = self.analyzer.extract_text_from_docx(uploaded_file)
                            else:
                                if hasattr(uploaded_file, 'seek'):
                                    uploaded_file.seek(0)
                                text = uploaded_file.getvalue().decode('utf-8', errors='ignore')
                                
                            if not text or text.strip() == "":
                                st.error("Could not extract text from the uploaded file. Please ensure your PDF or DOCX file contains readable text.")
                                return
                        except Exception as e:
                            st.error(f"Error reading file: {str(e)}")
                            return

                        # Analyze the document
                        analysis = self.analyzer.analyze_resume({'raw_text': text}, role_info)
                        
                        # Check if analysis returned an error
                        if 'error' in analysis:
                            st.error(analysis['error'])
                            return



                        # Save resume data to database
                        resume_data = {
                            'personal_info': {
                                'name': analysis.get('name', ''),
                                'email': analysis.get('email', ''),
                                'phone': analysis.get('phone', ''),
                                'linkedin': analysis.get('linkedin', ''),
                                'github': analysis.get('github', ''),
                                'portfolio': analysis.get('portfolio', '')
                            },
                            'summary': analysis.get('summary', ''),
                            'target_role': selected_role,
                            'target_category': selected_category,
                            'education': analysis.get('education', []),
                            'experience': analysis.get('experience', []),
                            'projects': analysis.get('projects', []),
                            'skills': analysis.get('skills', []),
                            'template': ''
                        }

                        # Save to database
                        try:
                            resume_id = save_resume_data(resume_data)

                            # Save analysis data
                            analysis_data = {
                                'resume_id': resume_id,
                                'ats_score': analysis['ats_score'],
                                'keyword_match_score': analysis['keyword_match']['score'],
                                'format_score': analysis['format_score'],
                                'section_score': analysis['section_score'],
                                'missing_skills': ','.join(analysis['keyword_match']['missing_skills']),
                                'recommendations': ','.join(analysis['suggestions'])
                            }
                            save_analysis_data(resume_id, analysis_data)
                            st.success("Resume data saved successfully!")
                        except Exception as e:
                            st.error(f"Error saving to database: {str(e)}")
                            print(f"Database error: {e}")

                        # Show results based on document type
                        if analysis.get('document_type') != 'resume':
                            st.error(
    f"This appears to be a {analysis['document_type']} document, not a resume.")
                            st.warning(
                                "Please upload a proper resume for ATS analysis.")
                            return
                        # Display results in a modern card layout
                    col1, col2 = st.columns(2)

                    with col1:
                        # ATS Score Card with circular progress
                        score_val = int(analysis.get('ats_score', 0))
                        score_color = '#0B7A5E' if score_val >= 80 else '#D97706' if score_val >= 60 else '#DC2626'
                        status_str = 'Excellent' if score_val >= 80 else 'Good' if score_val >= 60 else 'Needs Improvement'
                        
                        render_clean_html(f"""
                        <div style="background: var(--bg-surface); border: 1px solid var(--border-subtle); padding: 20px; border-radius: 12px; box-shadow: 0 1px 3px rgba(0,0,0,0.05); text-align: center;">
                            <h3 style="color: var(--text-primary); margin-bottom: 15px; font-weight: 700; font-size: 1.25rem;">ATS Score</h3>
                            <div style="position: relative; width: 140px; height: 140px; margin: 0 auto;">
                                <div style="
                                    position: absolute;
                                    width: 140px;
                                    height: 140px;
                                    border-radius: 50%;
                                    background: conic-gradient(
                                        {score_color} 0% {score_val}%,
                                        #E2E8F0 {score_val}% 100%
                                    );
                                    display: flex;
                                    align-items: center;
                                    justify-content: center;
                                ">
                                    <div style="
                                        width: 110px;
                                        height: 110px;
                                        background: var(--bg-surface);
                                        border: 1px solid var(--border-subtle);
                                        border-radius: 50%;
                                        display: flex;
                                        align-items: center;
                                        justify-content: center;
                                        font-size: 26px;
                                        font-weight: 800;
                                        color: {score_color};
                                    ">
                                        {score_val}
                                    </div>
                                </div>
                            </div>
                            <div style="text-align: center; margin-top: 15px;">
                                <span style="
                                    font-size: 1rem;
                                    color: {score_color};
                                    font-weight: 700;
                                    padding: 4px 14px;
                                    background: var(--bg-surface-raised);
                                    border-radius: 20px;
                                    border: 1px solid var(--border-subtle);
                                ">
                                    {status_str}
                                </span>
                            </div>
                        </div>
                        """)

                        # Skills Match Card
                        render_clean_html("""
                        <div style="background: var(--bg-surface); border: 1px solid var(--border-subtle); padding: 20px; border-radius: 12px; box-shadow: 0 1px 3px rgba(0,0,0,0.05); margin-top: 15px;">
                            <h3 style="color: var(--text-primary); margin-bottom: 15px; font-weight: 700; font-size: 1.25rem;">Skills Match</h3>
                        """)

                        st.metric(
                            "Keyword Match", f"{int(analysis.get('keyword_match', {}).get('score', 0))}%")

                        if analysis['keyword_match']['missing_skills']:
                            st.markdown("<h4 style='color: var(--text-primary); font-weight: 600; margin-top: 10px;'>Missing Skills:</h4>", unsafe_allow_html=True)
                            for skill in analysis['keyword_match']['missing_skills']:
                                st.markdown(f"<p style='color: var(--text-primary); font-size: 0.95rem; margin-bottom: 4px;'>• {skill}</p>", unsafe_allow_html=True)

                        st.markdown("</div>", unsafe_allow_html=True)

                    with col2:
                        # Format Score Card
                        render_clean_html("""
                        <div style="background: var(--bg-surface); border: 1px solid var(--border-subtle); padding: 20px; border-radius: 12px; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
                            <h3 style="color: var(--text-primary); margin-bottom: 15px; font-weight: 700; font-size: 1.25rem;">Format Analysis</h3>
                        """)

                        st.metric("Format Score",
                                  f"{int(analysis.get('format_score', 0))}%")
                        st.metric("Section Score",
                                  f"{int(analysis.get('section_score', 0))}%")

                        st.markdown("</div>", unsafe_allow_html=True)

                        # Suggestions Card with improved UI
                        render_clean_html("""
                        <div style="background: var(--bg-surface); border: 1px solid var(--border-subtle); padding: 20px; border-radius: 12px; box-shadow: 0 1px 3px rgba(0,0,0,0.05); margin-top: 15px;">
                            <h3 style="color: var(--text-primary); margin-bottom: 15px; font-weight: 700; font-size: 1.25rem;">Resume Improvement Suggestions</h3>
                        """)

                        # Contact Section
                        if analysis.get('contact_suggestions'):
                            render_clean_html("""
                            <div style='background-color: var(--bg-surface-raised); border: 1px solid var(--border-subtle); padding: 15px; border-radius: 10px; margin: 10px 0;'>
                                <h4 style='color: var(--text-primary); margin-top: 0; margin-bottom: 10px; font-size: 1rem; font-weight: 700;'>Contact Information</h4>
                                <ul style='list-style-type: none; padding-left: 0; margin: 0;'>
                            """)
                            for suggestion in analysis.get('contact_suggestions', []):
                                st.markdown(f"<li style='margin-bottom: 8px; color: var(--text-primary); font-size: 0.95rem; line-height: 1.5; font-weight: 500;'> {suggestion}</li>", unsafe_allow_html=True)
                            st.markdown("</ul></div>", unsafe_allow_html=True)

                        # Summary Section
                        if analysis.get('summary_suggestions'):
                            render_clean_html("""
                            <div style='background-color: var(--bg-surface-raised); border: 1px solid var(--border-subtle); padding: 15px; border-radius: 10px; margin: 10px 0;'>
                                <h4 style='color: var(--text-primary); margin-top: 0; margin-bottom: 10px; font-size: 1rem; font-weight: 700;'>Professional Summary</h4>
                                <ul style='list-style-type: none; padding-left: 0; margin: 0;'>
                            """)
                            for suggestion in analysis.get('summary_suggestions', []):
                                st.markdown(f"<li style='margin-bottom: 8px; color: var(--text-primary); font-size: 0.95rem; line-height: 1.5; font-weight: 500;'> {suggestion}</li>", unsafe_allow_html=True)
                            st.markdown("</ul></div>", unsafe_allow_html=True)

                        # Skills Section
                        if analysis.get('skills_suggestions') or analysis['keyword_match']['missing_skills']:
                            render_clean_html("""
                            <div style='background-color: var(--bg-surface-raised); border: 1px solid var(--border-subtle); padding: 15px; border-radius: 10px; margin: 10px 0;'>
                                <h4 style='color: var(--text-primary); margin-top: 0; margin-bottom: 10px; font-size: 1rem; font-weight: 700;'>Skills</h4>
                                <ul style='list-style-type: none; padding-left: 0; margin: 0;'>
                            """)
                            for suggestion in analysis.get('skills_suggestions', []):
                                st.markdown(f"<li style='margin-bottom: 8px; color: var(--text-primary); font-size: 0.95rem; line-height: 1.5; font-weight: 500;'> {suggestion}</li>", unsafe_allow_html=True)
                            if analysis['keyword_match']['missing_skills']:
                                st.markdown("<li style='margin-bottom: 8px; color: var(--text-primary); font-size: 0.95rem; line-height: 1.5; font-weight: 600;'> Consider adding these relevant skills:</li>", unsafe_allow_html=True)
                                for skill in analysis['keyword_match']['missing_skills']:
                                    st.markdown(f"<li style='margin-left: 20px; margin-bottom: 4px; color: var(--text-secondary); font-size: 0.9rem;'>• {skill}</li>", unsafe_allow_html=True)
                            st.markdown("</ul></div>", unsafe_allow_html=True)

                        # Experience Section
                        if analysis.get('experience_suggestions'):
                            render_clean_html("""
                            <div style='background-color: var(--bg-surface-raised); border: 1px solid var(--border-subtle); padding: 15px; border-radius: 10px; margin: 10px 0;'>
                                <h4 style='color: var(--text-primary); margin-top: 0; margin-bottom: 10px; font-size: 1rem; font-weight: 700;'>Work Experience</h4>
                                <ul style='list-style-type: none; padding-left: 0; margin: 0;'>
                            """)
                            for suggestion in analysis.get('experience_suggestions', []):
                                st.markdown(f"<li style='margin-bottom: 8px; color: var(--text-primary); font-size: 0.95rem; line-height: 1.5; font-weight: 500;'> {suggestion}</li>", unsafe_allow_html=True)
                            st.markdown("</ul></div>", unsafe_allow_html=True)

                        # Education Section
                        if analysis.get('education_suggestions'):
                            render_clean_html("""
                            <div style='background-color: var(--bg-surface-raised); border: 1px solid var(--border-subtle); padding: 15px; border-radius: 10px; margin: 10px 0;'>
                                <h4 style='color: var(--text-primary); margin-top: 0; margin-bottom: 10px; font-size: 1rem; font-weight: 700;'>Education</h4>
                                <ul style='list-style-type: none; padding-left: 0; margin: 0;'>
                            """)
                            for suggestion in analysis.get('education_suggestions', []):
                                st.markdown(f"<li style='margin-bottom: 8px; color: var(--text-primary); font-size: 0.95rem; line-height: 1.5; font-weight: 500;'> {suggestion}</li>", unsafe_allow_html=True)
                            st.markdown("</ul></div>", unsafe_allow_html=True)

                        # General Formatting Suggestions
                        if analysis.get('format_suggestions'):
                            render_clean_html("""
                            <div style='background-color: var(--bg-surface-raised); border: 1px solid var(--border-subtle); padding: 15px; border-radius: 10px; margin: 10px 0;'>
                                <h4 style='color: var(--text-primary); margin-top: 0; margin-bottom: 10px; font-size: 1rem; font-weight: 700;'>Formatting</h4>
                                <ul style='list-style-type: none; padding-left: 0; margin: 0;'>
                            """)
                            for suggestion in analysis.get('format_suggestions', []):
                                st.markdown(f"<li style='margin-bottom: 8px; color: var(--text-primary); font-size: 0.95rem; line-height: 1.5; font-weight: 500;'> {suggestion}</li>", unsafe_allow_html=True)
                            st.markdown("</ul></div>", unsafe_allow_html=True)

                        st.markdown("</div>", unsafe_allow_html=True)

                        # Course Recommendations
                    render_clean_html("""
                        <div class="feature-card">
                            <h2>Recommended Courses</h2>
                        """)

                        # Get courses based on role and category
                    courses = get_courses_for_role(selected_role)
                    if not courses:
                            category = get_category_for_role(selected_role)
                            courses = COURSES_BY_CATEGORY.get(
                                category, {}).get(selected_role, [])

                        # Display courses in a grid
                    cols = st.columns(2)
                    for i, course in enumerate(
                        courses[:6]):  # Show top 6 courses
                            with cols[i % 2]:
                                render_clean_html(f"""
                                <div style='background-color: var(--bg-surface); border: 1px solid var(--border-subtle); padding: 15px; border-radius: 10px; margin: 10px 0;'>
                                    <h4 style='color: var(--text-primary); margin-top: 0;'>{course[0]}</h4>
                                    <a href='{course[1]}' target='_blank' style='color: var(--accent); font-weight: 600;'>View Course →</a>
                                </div>
                                """)

                    st.markdown("</div>", unsafe_allow_html=True)

                        # Learning Resources
                    render_clean_html("""
                        <div class="feature-card">
                            <h2>Helpful Videos</h2>
                        """)

                    tab1, tab2 = st.tabs(["Resume Tips", "Interview Tips"])

                    with tab1:
                            # Resume Videos
                            for category, videos in RESUME_VIDEOS.items():
                                st.subheader(category)
                                cols = st.columns(2)
                                for i, video in enumerate(videos):
                                    with cols[i % 2]:
                                        st.video(video[1])

                    with tab2:
                            # Interview Videos
                            for category, videos in INTERVIEW_VIDEOS.items():
                                st.subheader(category)
                                cols = st.columns(2)
                                for i, video in enumerate(videos):
                                    with cols[i % 2]:
                                        st.video(video[1])

                    st.markdown("</div>", unsafe_allow_html=True)

        with analyzer_tabs[1]:
            render_clean_html("""
            <div style='background-color: var(--bg-surface); padding: 20px; border-radius: 10px; margin: 10px 0; border: 1px solid var(--border-subtle); box-shadow: 0 1px 3px rgba(0,0,0,0.05);'>
                <h3 style='color: var(--text-primary); margin-top: 0;'>AI-Powered Resume Analysis</h3>
                <p style='color: var(--text-secondary); margin-bottom: 5px;'>Get detailed insights from advanced AI models that analyze your resume and provide personalized recommendations.</p>
                <p style='color: var(--text-primary); font-weight: 600;'>Upload your resume to get AI-powered analysis and recommendations.</p>
            </div>
            """)

            # AI Model Selection
            st.selectbox(
                "Select AI Model",
                ["OpenRouter"],
                help="Choose the AI model to analyze your resume"
            )
             
            # Add job description input option
            use_custom_job_desc = st.checkbox("Use custom job description", value=False, 
                                             help="Enable this to provide a specific job description for more targeted analysis")
            
            custom_job_description = ""
            if use_custom_job_desc:
                custom_job_description = st.text_area(
                    "Paste the job description here",
                    height=200,
                    placeholder="Paste the full job description from the company here for more targeted analysis...",
                    help="Providing the actual job description will help the AI analyze your resume specifically for this position"
                )
                
                render_clean_html("""
                <div style='background-color: var(--bg-surface-raised); padding: 15px; border-radius: 10px; margin: 10px 0; border: 1px solid var(--border-subtle); color: var(--text-primary);'>
                    <p><i class="fas fa-lightbulb" style="color: var(--accent);"></i> <strong>Tip:</strong> Including the actual job description improves analysis accuracy and produces more targeted recommendations.</p>
                </div>
                """)
            
            # Brutal Roast Mode toggle (off by default)
            enable_roast = st.checkbox(
                "Also roast me (brutally honest mode)",
                value=False,
                help="Opt in for a blunt, comedic critique of the document's writing, structure, and content. Each point still includes an actionable fix. Targets the document only — not you personally."
            )
             
                        # Add AI Analyzer Stats in an expander
            with st.expander("AI Analyzer Statistics", expanded=False):
                try:
                    # Add a reset button for admin users
                    if st.session_state.get('is_admin', False):
                        if st.button(
    "Reset AI Analysis Statistics",
    type="secondary",
     key="reset_ai_stats_button_2"):
                            from config.database import reset_ai_analysis_stats
                            result = reset_ai_analysis_stats()
                            if result["success"]:
                                st.success(result["message"])
                            else:
                                st.error(result["message"])
                            # Refresh the page to show updated stats
                            st.experimental_rerun()

                    # Get detailed AI analysis statistics
                    from config.database import get_detailed_ai_analysis_stats
                    ai_stats = get_detailed_ai_analysis_stats()

                    if ai_stats["total_analyses"] > 0:
                        # Create a more visually appealing layout
                        render_clean_html("""
                        <style>
                        .stats-card {
                            background: var(--bg-surface);
                            border: 1px solid var(--border-subtle);
                            border-radius: 10px;
                            padding: 15px;
                            margin-bottom: 15px;
                            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
                            text-align: center;
                        }
                        .stats-value {
                            font-size: 28px;
                            font-weight: bold;
                            color: var(--text-primary);
                            margin: 10px 0;
                        }
                        .stats-label {
                            font-size: 14px;
                            color: var(--text-secondary);
                            text-transform: uppercase;
                            letter-spacing: 1px;
                        }
                        .score-card {
                            background: var(--bg-surface);
                            border: 1px solid var(--border-subtle);
                            border-radius: 10px;
                            padding: 15px;
                            margin-bottom: 15px;
                            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
                            text-align: center;
                        }
                        </style>
                        """)

                        col1, col2, col3 = st.columns(3)

                        with col1:
                            render_clean_html(f"""
                            <div class="stats-card">
                                <div class="stats-label">Total AI Analyses</div>
                                <div class="stats-value">{ai_stats["total_analyses"]}</div>
                            </div>
                            """)

                        with col2:
                            render_clean_html(f"""
                            <div class="stats-card">
                                <div class="stats-label">Average Resume Score</div>
                                <div class="stats-value">{ai_stats["average_score"]}/100</div>
                            </div>
                            """)

                        with col3:
                            # Create a gauge chart for average score
                            import plotly.graph_objects as go
                            fig = go.Figure(go.Indicator(
                                mode="gauge+number",
                                value=ai_stats["average_score"],
                                domain={'x': [0, 1], 'y': [0, 1]},
                                title={
    'text': "Score", 'font': {
        'size': 14, 'color': 'white'}},
                                gauge={
                                    'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "white"},
                                    'bar': {'color': "#aaaaaa" if ai_stats["average_score"] >= 80 else "#FFEB3B" if ai_stats["average_score"] >= 60 else "#FF5252"},
                                    'bgcolor': "rgba(0,0,0,0)",
                                    'borderwidth': 2,
                                    'bordercolor': "white",
                                    'steps': [
                                        {'range': [
                                            0, 40], 'color': 'rgba(100, 100, 100, 0.3)'},
                                        {'range': [
                                            40, 70], 'color': 'rgba(150, 150, 150, 0.3)'},
                                        {'range': [
                                            70, 100], 'color': 'rgba(200, 200, 200, 0.3)'}
                                    ],
                                }
                            ))

                            fig.update_layout(
                                paper_bgcolor='rgba(0,0,0,0)',
                                plot_bgcolor='rgba(0,0,0,0)',
                                font={'color': "white"},
                                height=150,
                                margin=dict(l=10, r=10, t=30, b=10)
                            )

                            st.plotly_chart(fig, width='stretch')

                        # Display model usage with enhanced visualization
                        if ai_stats["model_usage"]:
                            st.markdown("### Model Usage")
                            model_data = pd.DataFrame(ai_stats["model_usage"])

                            # Create a more colorful pie chart
                            import plotly.express as px
                            fig = px.pie(
                                model_data,
                                values="count",
                                names="model",
                                color_discrete_sequence=['#555555','#888888','#aaaaaa','#cccccc','#eeeeee'],
                                hole=0.4
                            )

                            fig.update_traces(
                                textposition='inside',
                                textinfo='percent+label',
                                marker=dict(
    line=dict(
        color='#000000',
         width=1.5))
                            )

                            fig.update_layout(
                                margin=dict(l=20, r=20, t=30, b=20),
                                height=300,
                                paper_bgcolor='rgba(0,0,0,0)',
                                plot_bgcolor='rgba(0,0,0,0)',
                                font=dict(color="#ffffff", size=14),
                                legend=dict(
                                    orientation="h",
                                    yanchor="bottom",
                                    y=-0.1,
                                    xanchor="center",
                                    x=0.5
                                ),
                                title={
                                    'text': 'AI Model Distribution',
                                    'y': 0.95,
                                    'x': 0.5,
                                    'xanchor': 'center',
                                    'yanchor': 'top',
                                    'font': {'size': 18, 'color': 'white'}
                                }
                            )

                            st.plotly_chart(fig, width='stretch')

                        # Display top job roles with enhanced visualization
                        if ai_stats["top_job_roles"]:
                            st.markdown("### Top Job Roles")
                            roles_data = pd.DataFrame(
                                ai_stats["top_job_roles"])

                            # Create a more colorful bar chart
                            fig = px.bar(
                                roles_data,
                                x="role",
                                y="count",
                                color="count",
                                color_continuous_scale=['#111111','#333333','#555555','#888888','#cccccc'],
                                labels={
    "role": "Job Role", "count": "Number of Analyses"}
                            )

                            fig.update_traces(
                                marker_line_width=1.5,
                                marker_line_color="white",
                                opacity=0.9
                            )

                            fig.update_layout(
                                margin=dict(l=20, r=20, t=50, b=30),
                                height=350,
                                paper_bgcolor='rgba(0,0,0,0)',
                                plot_bgcolor='rgba(0,0,0,0)',
                                font=dict(color="#ffffff", size=14),
                                title={
                                    'text': 'Most Analyzed Job Roles',
                                    'y': 0.95,
                                    'x': 0.5,
                                    'xanchor': 'center',
                                    'yanchor': 'top',
                                    'font': {'size': 18, 'color': 'white'}
                                },
                                xaxis=dict(
                                    title="",
                                    tickangle=-45,
                                    tickfont=dict(size=12)
                                ),
                                yaxis=dict(
                                    title="Number of Analyses",
                                    gridcolor="rgba(255, 255, 255, 0.1)"
                                ),
                                coloraxis_showscale=False
                            )

                            st.plotly_chart(fig, width='stretch')

                            # Add a timeline chart for analysis over time (mock
                            # data for now)
                            st.markdown("### Analysis Trend")
                            st.info(
                                "This is a conceptual visualization. To implement actual time-based analysis, additional data collection would be needed.")

                            # Create mock data for timeline
                            import datetime
                            import numpy as np

                            today = datetime.datetime.now()
                            dates = [
    (today -
    datetime.timedelta(
        days=i)).strftime('%Y-%m-%d') for i in range(7)]
                            dates.reverse()

                            # Generate some random data that sums to
                            # total_analyses
                            total = ai_stats["total_analyses"]
                            if total > 7:
                                values = np.random.dirichlet(
                                    np.ones(7)) * total
                                values = [round(v) for v in values]
                                # Adjust to make sure sum equals total
                                diff = total - sum(values)
                                values[-1] += diff
                            else:
                                values = [0] * 7
                                for i in range(total):
                                    values[-(i % 7) - 1] += 1

                            trend_data = pd.DataFrame({
                                'Date': dates,
                                'Analyses': values
                            })

                            fig = px.line(
                                trend_data,
                                x='Date',
                                y='Analyses',
                                markers=True,
                                line_shape='spline',
                                color_discrete_sequence=["#aaaaaa"]
                            )

                            fig.update_traces(
                                line=dict(width=3),
                                marker=dict(
    size=8, line=dict(
        width=2, color='white'))
                            )

                            fig.update_layout(
                                margin=dict(l=20, r=20, t=50, b=30),
                                height=300,
                                paper_bgcolor='rgba(0,0,0,0)',
                                plot_bgcolor='rgba(0,0,0,0)',
                                font=dict(color="#ffffff", size=14),
                                title={
                                    'text': 'Analysis Activity (Last 7 Days)',
                                    'y': 0.95,
                                    'x': 0.5,
                                    'xanchor': 'center',
                                    'yanchor': 'top',
                                    'font': {'size': 18, 'color': 'white'}
                                },
                                xaxis=dict(
                                    title="",
                                    gridcolor="rgba(255, 255, 255, 0.1)"
                                ),
                                yaxis=dict(
                                    title="Number of Analyses",
                                    gridcolor="rgba(255, 255, 255, 0.1)"
                                )
                            )

                            st.plotly_chart(fig, width='stretch')

                        # Display score distribution if available
                        if ai_stats["score_distribution"]:
                            render_clean_html("""
                            <h3 style='text-align: center; margin-bottom: 20px; background: var(--bg-surface-raised); border: 1px solid var(--border-subtle); padding: 15px; border-radius: 10px; color: var(--text-primary); box-shadow: 0 1px 3px rgba(0,0,0,0.05);'>
                                Score Distribution Analysis
                            </h3>
                            """)

                            score_data = pd.DataFrame(
                                ai_stats["score_distribution"])

                            # Create a more visually appealing bar chart for
                            # score distribution
                            fig = px.bar(
                                score_data,
                                x="range",
                                y="count",
                                color="range",
                                color_discrete_map={
                                    "0-20": "#FF5252",
                                    "21-40": "#FF7043",
                                    "41-60": "#FFEB3B",
                                    "61-80": "#8BC34A",
                                    "81-100": "#aaaaaa"
                                },
                                labels={
    "range": "Score Range",
     "count": "Number of Resumes"},
                                text="count"  # Display count values on bars
                            )

                            fig.update_traces(
                                marker_line_width=2,
                                marker_line_color="white",
                                opacity=0.9,
                                textposition='outside',
                                textfont=dict(
    color="white", size=14, family="Arial, sans-serif"),
                                hovertemplate="<b>Score Range:</b> %{x}<br><b>Number of Resumes:</b> %{y}<extra></extra>"
                            )

                            # Add a gradient background to the chart
                            fig.update_layout(
                                margin=dict(l=20, r=20, t=50, b=30),
                                height=400,  # Increase height for better visibility
                                paper_bgcolor='rgba(0,0,0,0)',
                                plot_bgcolor='rgba(0,0,0,0)',
                                font=dict(
    color="#ffffff", size=14, family="Arial, sans-serif"),
                                # title={
                                #     # 'text': 'Resume Score Distribution',
                                #     'y': 0.95,
                                #     'x': 0.5,
                                #     'xanchor': 'center',
                                #     'yanchor': 'top',
                                #     'font': {'size': 22, 'color': 'white', 'family': 'Arial, sans-serif', 'weight': 'bold'}
                                # },
                                xaxis=dict(
                                    title=dict(
    text="Score Range", font=dict(
        size=16, color="white")),
                                    categoryorder="array",
                                    categoryarray=[
    "0-20", "21-40", "41-60", "61-80", "81-100"],
                                    tickfont=dict(size=14, color="white"),
                                    gridcolor="rgba(255, 255, 255, 0.1)"
                                ),
                                yaxis=dict(
                                    title=dict(
    text="Number of Resumes", font=dict(
        size=16, color="white")),
                                    tickfont=dict(size=14, color="white"),
                                    gridcolor="rgba(255, 255, 255, 0.1)",
                                    zeroline=False
                                ),
                                showlegend=False,
                                bargap=0.2,  # Adjust gap between bars
                                shapes=[
                                    # Add gradient background
                                    dict(
                                        type="rect",
                                        xref="paper",
                                        yref="paper",
                                        x0=0,
                                        y0=0,
                                        x1=1,
                                        y1=1,
                                        fillcolor="rgba(20, 20, 20, 0.5)",
                                        layer="below",
                                        line_width=0,
                                    )
                                ]
                            )

                            # Add annotations for insights
                            if len(score_data) > 0:
                                max_count_idx = score_data["count"].idxmax()
                                max_range = score_data.iloc[max_count_idx]["range"]
                                score_data.iloc[max_count_idx]["count"]

                                fig.add_annotation(
                                    x=0.5,
                                    y=1.12,
                                    xref="paper",
                                    yref="paper",
                                    text=f"Most resumes fall in the {max_range} score range",
                                    showarrow=False,
                                    font=dict(size=14, color="#FFEB3B"),
                                    bgcolor="rgba(0,0,0,0.5)",
                                    bordercolor="#FFEB3B",
                                    borderwidth=1,
                                    borderpad=4,
                                    opacity=0.8
                                )

                            # Display the chart in a styled container
                            render_clean_html("""
                            <div style='background: var(--bg-surface); padding: 20px; border-radius: var(--radius-lg); margin: 15px 0; border: 1px solid var(--border-subtle); box-shadow: 0 1px 3px rgba(0,0,0,0.05);'>
                            """)

                            st.plotly_chart(fig, width='stretch')

                            # Add descriptive text below the chart
                            render_clean_html("""
                            <p style='color: var(--text-secondary); text-align: center; font-style: italic; margin-top: 10px; font-size: 0.85rem;'>
                                This chart shows the distribution of resume scores across different ranges, helping identify common performance levels.
                            </p>
                            </div>
                            """)

                        # Display recent analyses if available
                        if ai_stats["recent_analyses"]:
                            render_clean_html("""
                            <h3 style='text-align: center; margin-bottom: 20px; background: var(--bg-surface); padding: 15px; border-radius: var(--radius-md); color: var(--text-primary); border: 1px solid var(--border-subtle); box-shadow: 0 1px 3px rgba(0,0,0,0.05); font-weight: 700;'>
                                Recent Resume Analyses
                            </h3>
                            """)

                            # Create a more modern styled table for recent
                            # analyses
                            render_clean_html("""
                            <style>
                            .modern-analyses-table {
                                width: 100%;
                                border-collapse: separate;
                                border-spacing: 0 8px;
                                margin-bottom: 20px;
                                font-family: 'Arial', sans-serif;
                            }
                            .modern-analyses-table th {
                                background: var(--bg-surface-raised);
                                color: var(--text-primary);
                                border-bottom: 2px solid var(--border-subtle);
                                padding: 15px;
                                text-align: left;
                                font-weight: bold;
                                font-size: 14px;
                                text-transform: uppercase;
                                letter-spacing: 1px;
                                border-radius: 8px;
                            }
                            .modern-analyses-table td {
                                padding: 15px;
                                background-color: var(--bg-surface);
                                border-top: 1px solid var(--border-subtle);
                                border-bottom: 1px solid var(--border-subtle);
                                color: var(--text-primary);
                            }
                            .modern-analyses-table tr td:first-child {
                                border-top-left-radius: 8px;
                                border-bottom-left-radius: 8px;
                            }
                            .modern-analyses-table tr td:last-child {
                                border-top-right-radius: 8px;
                                border-bottom-right-radius: 8px;
                            }
                            .modern-analyses-table tr:hover td {
                                background-color: var(--bg-surface-raised);
                                transform: translateY(-2px);
                                transition: all 0.2s ease;
                                box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
                            }
                            .model-badge {
                                display: inline-block;
                                padding: 6px 12px;
                                border-radius: 20px;
                                font-weight: bold;
                                text-align: center;
                                font-size: 12px;
                                letter-spacing: 0.5px;
                                border: 1px solid var(--border-subtle);
                                background: var(--bg-surface-raised);
                                color: var(--text-primary);
                            }
                            .score-pill {
                                display: inline-block;
                                padding: 8px 15px;
                                border-radius: 20px;
                                font-weight: bold;
                                text-align: center;
                                min-width: 70px;
                                border: 1px solid var(--border-subtle);
                                background: var(--bg-surface-raised);
                                color: var(--text-primary);
                            }
                            .date-badge {
                                display: inline-block;
                                padding: 6px 12px;
                                border-radius: 20px;
                                background-color: var(--bg-surface-raised);
                                color: var(--text-secondary);
                                border: 1px solid var(--border-subtle);
                                font-size: 12px;
                            }
                            .role-badge {
                                display: inline-block;
                                padding: 6px 12px;
                                border-radius: 8px;
                                background-color: var(--bg-surface-raised);
                                color: var(--text-primary);
                                border: 1px solid var(--border-subtle);
                                font-size: 13px;
                                max-width: 200px;
                                white-space: nowrap;
                                overflow: hidden;
                                text-overflow: ellipsis;
                            }
                            </style>

                            <div style='background: var(--bg-surface); padding: 20px; border-radius: var(--radius-lg); margin: 15px 0; border: 1px solid var(--border-subtle); box-shadow: 0 1px 3px rgba(0,0,0,0.05);'>
                            <table class="modern-analyses-table">
                                <tr>
                                    <th>AI Model</th>
                                    <th>Score</th>
                                    <th>Job Role</th>
                                    <th>Date</th>
                                </tr>
                            """)

                            for analysis in ai_stats["recent_analyses"]:
                                score = analysis["score"]
                                score_class = "score-high" if score >= 80 else "score-medium" if score >= 60 else "score-low"

                                # Determine model class
                                model_name = analysis["model"]
                                model_class = "model-openrouter" if "OpenRouter" in model_name or "Claude" in model_name else "model-gemini"

                                # Format the date
                                try:
                                    from datetime import datetime
                                    date_obj = datetime.strptime(
                                        analysis["date"], "%Y-%m-%d %H:%M:%S")
                                    formatted_date = date_obj.strftime(
                                        "%b %d, %Y")
                                except:
                                    formatted_date = analysis["date"]

                                render_clean_html(f"""
                                <tr>
                                    <td><div class="model-badge {model_class}">{model_name}</div></td>
                                    <td><div class="score-pill {score_class}">{score}/100</div></td>
                                    <td><div class="role-badge">{analysis["job_role"]}</div></td>
                                    <td><div class="date-badge">{formatted_date}</div></td>
                                </tr>
                                """)

                            render_clean_html("""
                            </table>

                            <p style='color: var(--text-secondary); text-align: center; font-style: italic; margin-top: 15px; font-size: 0.85rem;'>
                                These are the most recent resume analyses performed by our AI models.
                            </p>
                            </div>
                            """)
                    else:
                        st.info(
                            "No AI analysis data available yet. Upload and analyze resumes to see statistics here.")
                except Exception as e:
                    st.error(f"Error loading AI analysis statistics: {str(e)}")

            # Job Role Selection for AI Analysis
            categories = list(self.job_roles.keys())
            selected_category = st.selectbox(
    "Job Category", categories, key="ai_category")

            roles = list(self.job_roles[selected_category].keys())
            selected_role = st.selectbox("Specific Role", roles, key="ai_role")

            role_info = self.job_roles[selected_category][selected_role]

            # Display role information
            skills_html_ai = "".join([f'<span class="skill-tag" style="margin-right: 6px; margin-bottom: 6px; display: inline-block;">{skill}</span>' for skill in role_info['required_skills']])
            render_clean_html(f"""
            <div style='background-color: var(--bg-surface); padding: 20px; border-radius: var(--radius-lg); margin: 15px 0; border: 1px solid var(--border-subtle); box-shadow: 0 1px 3px rgba(0,0,0,0.05);'>
                <h3 style='color: var(--text-primary); margin-top: 0; font-weight: 700; font-size: 1.25rem;'>{selected_role}</h3>
                <p style='color: var(--text-secondary); line-height: 1.5; font-size: 0.9rem;'>{role_info['description']}</p>
                <h4 style='color: var(--text-primary); font-weight: 600; font-size: 0.95rem; margin-top: 15px; margin-bottom: 10px;'>Required Skills:</h4>
                <div>
                    {skills_html_ai}
                </div>
            </div>
            """)

            uploaded_file = st.file_uploader(
                "Upload your resume", type=['pdf', 'docx', 'doc', 'txt', 'PDF', 'DOCX', 'DOC'], key="ai_file")

            if not uploaded_file:
            # Display empty state with a prominent upload button
                st.markdown(
                self.render_empty_state(
            "fas fa-robot",
                        "Upload your resume to get AI-powered analysis and recommendations"
        ),
        unsafe_allow_html=True
    )
            else:
                # Add a prominent analyze button
                analyze_ai = st.button("Analyze with AI",
                                type="primary",
                                width='stretch',
                                key="analyze_ai_button")

                if analyze_ai:
                    # Single text extraction step with seek(0) reset and robust fallback
                    import importlib
                    import utils.ai_resume_analyzer
                    importlib.reload(utils.ai_resume_analyzer)
                    from utils.ai_resume_analyzer import AIResumeAnalyzer
                    analyzer = AIResumeAnalyzer()
                    resume_text = ""
                    fname = (uploaded_file.name or "").lower()
                    ftype = (uploaded_file.type or "").lower()

                    try:
                        if fname.endswith(".pdf") or "pdf" in ftype:
                            resume_text = analyzer.extract_text_from_pdf(uploaded_file)
                        elif fname.endswith(".docx") or fname.endswith(".doc") or "word" in ftype or "officedocument" in ftype:
                            resume_text = analyzer.extract_text_from_docx(uploaded_file)
                        else:
                            if hasattr(uploaded_file, 'seek'):
                                uploaded_file.seek(0)
                            resume_text = uploaded_file.getvalue().decode('utf-8', errors='ignore')
                    except Exception as e:
                        st.error(f"Error reading file: {str(e)}")
                        st.stop()

                    if not resume_text or not resume_text.strip():
                        st.error("Could not extract readable text from your resume. Please make sure the file is not empty or password-protected.")
                        st.stop()

                    # Analyze with AI
                    try:
                        with st.spinner("AI is analyzing your resume..."):
                            progress_bar = st.progress(0)
                            selected_model = "OpenRouter"
                            progress_bar.progress(30)
                            
                            job_role = selected_role if selected_role else "Not specified"
                            progress_bar.progress(50)
                            
                            # Analyze the resume with OpenRouter
                            if use_custom_job_desc and custom_job_description:
                                analysis_result = analyzer.analyze_resume_with_openrouter(
                                    resume_text, job_role=job_role, job_description=custom_job_description)
                                st.session_state['used_custom_job_desc'] = True
                            else:
                                analysis_result = analyzer.analyze_resume_with_openrouter(
                                    resume_text, job_role=job_role)
                                st.session_state['used_custom_job_desc'] = False

                                
                            # Update progress
                            progress_bar.progress(80)
                            
                            # Save the analysis to the database
                            if analysis_result and "error" not in analysis_result:
                                # Extract the resume score
                                resume_score = analysis_result.get(
                                    "resume_score", 0)
                                
                                # Save to database
                                save_ai_analysis_data(
                                    None,  # No user_id needed
                                    {
                                        "model_used": selected_model,
                                        "resume_score": resume_score,
                                        "job_role": job_role
                                    }
                                )
                            # Complete the progress
                            progress_bar.progress(100)
                            
                            # Display the analysis result
                            if analysis_result and "error" not in analysis_result:
                                st.success("Analysis complete.")
                                
                                # Extract data from the analysis
                                full_response = analysis_result.get(
                                    "analysis", "")
                                resume_score = analysis_result.get(
                                    "resume_score", 0)
                                ats_score = analysis_result.get(
                                    "ats_score", 0)
                                model_used = analysis_result.get(
                                    "model_used", selected_model)
                                
                                # Store the full response in session state for download
                                st.session_state['full_analysis'] = full_response
                                
                                # Display the analysis in a nice format
                                st.markdown("## Full Analysis Report")
                                
                                # Get current date
                                from datetime import datetime
                                current_date = datetime.now().strftime("%B %d, %Y")
                                
                                # Create a modern styled header for the report
                                render_clean_html(f"""
                                <div style="background-color: var(--bg-surface); padding: 20px; border-radius: 10px; margin-bottom: 20px; border: 1px solid var(--border-subtle); box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
                                    <h2 style="color: var(--text-primary); margin-bottom: 10px;">AI Resume Analysis Report</h2>
                                    <div style="display: flex; flex-wrap: wrap; gap: 20px;">
                                        <div style="flex: 1; min-width: 200px;">
                                            <p style="color: var(--text-primary);"><strong>Job Role:</strong> {job_role if job_role else "Not specified"}</p>
                                            <p style="color: var(--text-primary);"><strong>Analysis Date:</strong> {current_date}</p>
                                        </div>
                                        <div style="flex: 1; min-width: 200px;">
                                            <p style="color: var(--text-primary);"><strong>AI Model:</strong> {model_used}</p>
                                            <p style="color: var(--text-primary);"><strong>Overall Score:</strong> {resume_score}/100 - {"Excellent" if resume_score >= 80 else "Good" if resume_score >= 60 else "Needs Improvement"}</p>
                                            {f'<p style="color: var(--text-secondary);"><strong>Custom Job Description Used</strong></p>' if st.session_state.get('used_custom_job_desc', False) else ''}
                                        </div>
                                    </div>
                                </div>
                                """)
                                
                                # Add gauge charts for scores
                                import plotly.graph_objects as go
                                
                                col1, col2 = st.columns(2)
                                
                                with col1:
                                    # Resume Score Gauge
                                    fig1 = go.Figure(go.Indicator(
                                        mode="gauge+number",
                                        value=resume_score,
                                        domain={'x': [0, 1], 'y': [0, 1]},
                                        title={'text': "Resume Score", 'font': {'size': 16}},
                                        gauge={
                                            'axis': {'range': [0, 100], 'tickwidth': 1},
                                            'bar': {'color': "#0B7A5E" if resume_score >= 80 else "#D97706" if resume_score >= 60 else "#DC2626"},
                                            'bgcolor': "white",
                                            'borderwidth': 2,
                                            'bordercolor': "gray",
                                            'steps': [
                                                {'range': [0, 40], 'color': 'rgba(220, 38, 38, 0.1)'},
                                                {'range': [40, 60], 'color': 'rgba(217, 119, 6, 0.1)'},
                                                {'range': [60, 80], 'color': 'rgba(11, 122, 94, 0.1)'},
                                                {'range': [80, 100], 'color': 'rgba(5, 150, 105, 0.1)'}
                                            ],
                                            'threshold': {
                                                'line': {'color': "red", 'width': 4},
                                                'thickness': 0.75,
                                                'value': 60
                                            }
                                        }
                                    ))
                                    
                                    fig1.update_layout(
                                        height=250,
                                        margin=dict(l=20, r=20, t=50, b=20),
                                    )
                                    
                                    st.plotly_chart(fig1, width='stretch')
                                    
                                    status = "Excellent" if resume_score >= 80 else "Good" if resume_score >= 60 else "Needs Improvement"
                                    st.markdown(f"<div style='text-align: center; font-weight: bold;'>{status}</div>", unsafe_allow_html=True)
                                
                                with col2:
                                    # ATS Score Gauge
                                    fig2 = go.Figure(go.Indicator(
                                        mode="gauge+number",
                                        value=ats_score,
                                        domain={'x': [0, 1], 'y': [0, 1]},
                                        title={'text': "ATS Optimization Score", 'font': {'size': 16}},
                                        gauge={
                                            'axis': {'range': [0, 100], 'tickwidth': 1},
                                            'bar': {'color': "#0B7A5E" if ats_score >= 80 else "#D97706" if ats_score >= 60 else "#DC2626"},
                                            'bgcolor': "white",
                                            'borderwidth': 2,
                                            'bordercolor': "gray",
                                            'steps': [
                                                {'range': [0, 40], 'color': 'rgba(220, 38, 38, 0.1)'},
                                                {'range': [40, 60], 'color': 'rgba(217, 119, 6, 0.1)'},
                                                {'range': [60, 80], 'color': 'rgba(11, 122, 94, 0.1)'},
                                                {'range': [80, 100], 'color': 'rgba(5, 150, 105, 0.1)'}
                                            ],
                                            'threshold': {
                                                'line': {'color': "red", 'width': 4},
                                                'thickness': 0.75,
                                                'value': 60
                                            }
                                        }
                                    ))
                                    
                                    fig2.update_layout(
                                        height=250,
                                        margin=dict(l=20, r=20, t=50, b=20),
                                    )
                                    
                                    st.plotly_chart(fig2, width='stretch')
                                    
                                    status = "Excellent" if ats_score >= 80 else "Good" if ats_score >= 60 else "Needs Improvement"
                                    st.markdown(f"<div style='text-align: center; font-weight: bold;'>{status}</div>", unsafe_allow_html=True)

                                # Add Job Description Match Score if custom job description was used
                                if st.session_state.get('used_custom_job_desc', False) and custom_job_description:
                                    # Extract job match score from analysis result or calculate it
                                    job_match_score = analysis_result.get("job_match_score", 0)
                                    if not job_match_score and "job_match" in analysis_result:
                                        job_match_score = analysis_result["job_match"].get("score", 0)
                                    
                                    # If we have a job match score, display it
                                    if job_match_score:
                                        render_clean_html("""
                                        <h3 style="background: var(--bg-surface-raised); color: var(--text-primary); border: 1px solid var(--border-subtle); padding: 10px; border-radius: 5px; margin-top: 20px;">
                                            <i class="fas fa-handshake"></i> Job Description Match Analysis
                                        </h3>
                                        """)
                                        
                                        col1, col2 = st.columns(2)
                                        
                                        with col1:
                                            # Job Match Score Gauge
                                            fig3 = go.Figure(go.Indicator(
                                                mode="gauge+number",
                                                value=job_match_score,
                                                domain={'x': [0, 1], 'y': [0, 1]},
                                                title={'text': "Job Match Score", 'font': {'size': 16}},
                                                gauge={
                                                    'axis': {'range': [0, 100], 'tickwidth': 1},
                                                    'bar': {'color': "#0B7A5E" if job_match_score >= 80 else "#D97706" if job_match_score >= 60 else "#DC2626"},
                                                    'bgcolor': "white",
                                                    'borderwidth': 2,
                                                    'bordercolor': "gray",
                                                    'steps': [
                                                        {'range': [0, 40], 'color': 'rgba(220, 38, 38, 0.1)'},
                                                        {'range': [40, 60], 'color': 'rgba(217, 119, 6, 0.1)'},
                                                        {'range': [60, 80], 'color': 'rgba(11, 122, 94, 0.1)'},
                                                        {'range': [80, 100], 'color': 'rgba(5, 150, 105, 0.1)'}
                                                    ],
                                                    'threshold': {
                                                        'line': {'color': "red", 'width': 4},
                                                        'thickness': 0.75,
                                                        'value': 60
                                                    }
                                                }
                                            ))
                                            
                                            fig3.update_layout(
                                                height=250,
                                                margin=dict(l=20, r=20, t=50, b=20),
                                            )
                                            
                                            st.plotly_chart(fig3, width='stretch')
                                            
                                            match_status = "Excellent Match" if job_match_score >= 80 else "Good Match" if job_match_score >= 60 else "Low Match"
                                            st.markdown(f"<div style='text-align: center; font-weight: bold;'>{match_status}</div>", unsafe_allow_html=True)
                                        
                                        with col2:
                                            render_clean_html("""
                                            <div style="background-color: var(--bg-surface); padding: 20px; border-radius: 10px; height: 100%; border: 1px solid var(--border-subtle);">
                                                <h4 style="color: var(--text-primary); margin-bottom: 15px;">What This Means</h4>
                                                <p style="color: var(--text-primary);">This score represents how well your resume matches the specific job description you provided.</p>
                                                <ul style="color: var(--text-primary); padding-left: 20px;">
                                                    <li><strong>80-100:</strong> Excellent match - your resume is highly aligned with this job</li>
                                                    <li><strong>60-79:</strong> Good match - your resume matches many requirements</li>
                                                    <li><strong>Below 60:</strong> Consider tailoring your resume more specifically to this job</li>
                                                </ul>
                                            </div>
                                            """)
                                

                                # Format the full response with better styling
                                formatted_analysis = full_response
                                
                                # Replace section headers with styled headers
                                section_styles = {
                                    "## Overall Assessment": """<div class="report-section">
                                        <h3 style="background: var(--bg-surface-raised); color: var(--text-primary); border: 1px solid var(--border-subtle); padding: 10px; border-radius: 5px;">
                                            <i class="fas fa-chart-line"></i> Overall Assessment
                                        </h3>
                                        <div class="section-content">""",
                                        
                                    "## Professional Profile Analysis": """<div class="report-section">
                                        <h3 style="background: var(--bg-surface-raised); color: var(--text-primary); border: 1px solid var(--border-subtle); padding: 10px; border-radius: 5px;">
                                            <i class="fas fa-user-tie"></i> Professional Profile Analysis
                                        </h3>
                                        <div class="section-content">""",
                                        
                                    "## Skills Analysis": """<div class="report-section">
                                        <h3 style="background: var(--bg-surface-raised); color: var(--text-primary); border: 1px solid var(--border-subtle); padding: 10px; border-radius: 5px;">
                                            <i class="fas fa-tools"></i> Skills Analysis
                                        </h3>
                                        <div class="section-content">""",
                                        
                                    "## Experience Analysis": """<div class="report-section">
                                        <h3 style="background: var(--bg-surface-raised); color: var(--text-primary); border: 1px solid var(--border-subtle); padding: 10px; border-radius: 5px;">
                                            <i class="fas fa-briefcase"></i> Experience Analysis
                                        </h3>
                                        <div class="section-content">""",
                                        
                                    "## Education Analysis": """<div class="report-section">
                                        <h3 style="background: var(--bg-surface-raised); color: var(--text-primary); border: 1px solid var(--border-subtle); padding: 10px; border-radius: 5px;">
                                            <i class="fas fa-graduation-cap"></i> Education Analysis
                                        </h3>
                                        <div class="section-content">""",
                                        
                                    "## Key Strengths": """<div class="report-section">
                                        <h3 style="background: var(--bg-surface-raised); color: var(--text-primary); border: 1px solid var(--border-subtle); padding: 10px; border-radius: 5px;">
                                            <i class="fas fa-check-circle"></i> Key Strengths
                                        </h3>
                                        <div class="section-content">""",
                                        
                                    "## Areas for Improvement": """<div class="report-section">
                                        <h3 style="background: var(--bg-surface-raised); color: var(--text-primary); border: 1px solid var(--border-subtle); padding: 10px; border-radius: 5px;">
                                            <i class="fas fa-exclamation-circle"></i> Areas for Improvement
                                        </h3>
                                        <div class="section-content">""",
                                        
                                    "## ATS Optimization Assessment": """<div class="report-section">
                                        <h3 style="background: var(--bg-surface-raised); color: var(--text-primary); border: 1px solid var(--border-subtle); padding: 10px; border-radius: 5px;">
                                            <i class="fas fa-robot"></i> ATS Optimization Assessment
                                        </h3>
                                        <div class="section-content">""",
                                        
                                    "## Recommended Courses": """<div class="report-section">
                                        <h3 style="background: var(--bg-surface-raised); color: var(--text-primary); border: 1px solid var(--border-subtle); padding: 10px; border-radius: 5px;">
                                            <i class="fas fa-book"></i> Recommended Courses
                                        </h3>
                                        <div class="section-content">""",
                                        
                                    "## Resume Score": """<div class="report-section">
                                        <h3 style="background: var(--bg-surface-raised); color: var(--text-primary); border: 1px solid var(--border-subtle); padding: 10px; border-radius: 5px;">
                                            <i class="fas fa-star"></i> Resume Score
                                        </h3>
                                        <div class="section-content">""",
                                        
                                    "## Role Alignment Analysis": """<div class="report-section">
                                        <h3 style="background: var(--bg-surface-raised); color: var(--text-primary); border: 1px solid var(--border-subtle); padding: 10px; border-radius: 5px;">
                                            <i class="fas fa-bullseye"></i> Role Alignment Analysis
                                        </h3>
                                        <div class="section-content">""",
                                        
                                    "## Job Match Analysis": """<div class="report-section">
                                        <h3 style="background: var(--bg-surface-raised); color: var(--text-primary); border: 1px solid var(--border-subtle); padding: 10px; border-radius: 5px;">
                                            <i class="fas fa-handshake"></i> Job Match Analysis
                                        </h3>
                                        <div class="section-content">""",
                                }
                                
                                # Apply the styling to each section
                                for section, style in section_styles.items():
                                    if section in formatted_analysis:
                                        formatted_analysis = formatted_analysis.replace(
                                            section, style)
                                        # Add closing div tags
                                        next_section = False
                                        for next_sec in section_styles.keys():
                                            if next_sec != section and next_sec in formatted_analysis.split(style)[1]:
                                                split_text = formatted_analysis.split(style)[1].split(next_sec)
                                                formatted_analysis = formatted_analysis.split(style)[0] + style + split_text[0] + "</div></div>" + next_sec + "".join(split_text[1:])
                                                next_section = True
                                                break
                                        if not next_section:
                                            formatted_analysis = formatted_analysis + "</div></div>"
                                
                                # Remove any extra closing div tags that might have been added
                                formatted_analysis = formatted_analysis.replace("</div></div></div></div>", "</div></div>")
                                
                                # Ensure we don't have any orphaned closing tags at the end
                                if formatted_analysis.endswith("</div>"):
                                    # Count opening and closing div tags
                                    open_tags = formatted_analysis.count("<div")
                                    close_tags = formatted_analysis.count("</div>")
                                    
                                    # If we have more closing than opening tags, remove the extras
                                    if close_tags > open_tags:
                                        excess = close_tags - open_tags
                                        formatted_analysis = formatted_analysis[:-6 * excess]
                                
                                # Clean up any visible HTML tags that might appear in the text
                                formatted_analysis = formatted_analysis.replace("&lt;/div&gt;", "")
                                formatted_analysis = formatted_analysis.replace("&lt;div&gt;", "")
                                formatted_analysis = formatted_analysis.replace("<div>", "<div>")  # Ensure proper opening
                                formatted_analysis = formatted_analysis.replace("</div>", "</div>")  # Ensure proper closing
                                
                                # Add CSS for the report
                                render_clean_html("""
                                <style>
                                    .report-section {
                                        margin-bottom: 25px;
                                        border: 1px solid var(--border-subtle);
                                        border-radius: 8px;
                                        overflow: hidden;
                                        background-color: var(--bg-surface);
                                    }
                                    .section-content {
                                        padding: 15px;
                                        background-color: var(--bg-surface);
                                        color: var(--text-primary);
                                    }
                                    .report-section h3 {
                                        margin-top: 0;
                                        font-weight: 600;
                                        color: var(--text-primary);
                                    }
                                    .report-section ul {
                                        padding-left: 20px;
                                    }
                                    .report-section p {
                                        color: var(--text-primary);
                                        margin-bottom: 10px;
                                    }
                                    .report-section li {
                                        color: var(--text-primary);
                                        margin-bottom: 5px;
                                    }
                                </style>
                                """)

                                # Display the formatted analysis
                                render_clean_html(f"""
                                <div style="background-color: var(--bg-surface); padding: 20px; border-radius: 10px; border: 1px solid var(--border-subtle); color: var(--text-primary);">
                                    {formatted_analysis}
                                </div>
                                """)

                                # Create a PDF report
                                pdf_buffer = self.ai_analyzer.generate_pdf_report(
                                    analysis_result={
                                        "score": resume_score,
                                        "ats_score": ats_score,
                                        "model_used": model_used,
                                        "full_response": full_response,
                                        "strengths": analysis_result.get("strengths", []),
                                        "weaknesses": analysis_result.get("weaknesses", []),
                                        "used_custom_job_desc": st.session_state.get('used_custom_job_desc', False),
                                        "custom_job_description": custom_job_description if st.session_state.get('used_custom_job_desc', False) else ""
                                    },
                                    candidate_name=st.session_state.get(
                                        'candidate_name', 'Candidate'),
                                    job_role=selected_role
                                )

                                # PDF download button
                                if pdf_buffer:
                                    st.download_button(
                                        label="Download PDF Report",
                                        data=pdf_buffer,
                                        file_name=f"resume_analysis_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
                                        mime="application/pdf",
                                        width='stretch'
                                    )
                                else:
                                    st.error("PDF generation failed. Please try again later.")

                                # Brutal Roast Mode — additive, isolated, does not alter scores
                                if enable_roast:
                                    st.markdown("---")
                                    render_clean_html("""
                                    <div style="border:1px solid var(--border-subtle);border-radius:10px;padding:1.5rem;
                                         margin-top:1rem;background-color:var(--bg-surface);color:var(--text-primary);box-shadow:0 1px 3px rgba(0,0,0,0.05);">
                                    <h3 style="color:var(--text-primary);font-weight:700;letter-spacing:0.04em;margin-bottom:0.5rem;margin-top:0;">
                                        Brutal Roast
                                    </h3>
                                    <p style="color:var(--text-secondary);font-size:0.875rem;margin-bottom:1rem;">
                                        Blunt feedback on the document writing, structure, and content choices.
                                    </p>
                                    """)
                                    with st.spinner("Generating roast..."):
                                        try:
                                            _roast_text = analyzer.generate_roast(resume_text)
                                            if _roast_text and not _roast_text.startswith("Roast unavailable"):
                                                st.markdown(
                                                    f"<div style='color:var(--text-primary);white-space:pre-wrap;line-height:1.7;font-size:0.95rem;background:var(--bg-surface-raised);padding:1rem;border-radius:8px;border:1px solid var(--border-subtle);'>"
                                                    f"{_roast_text}</div>",
                                                    unsafe_allow_html=True
                                                )
                                            else:
                                                st.info(_roast_text or "Roast generation returned no content.")
                                        except Exception as _re:
                                            st.error(f"Roast generation failed: {str(_re)}")
                                    st.markdown("</div>", unsafe_allow_html=True)

                            else:
                                st.error(f"Analysis failed: {analysis_result.get('error', 'Unknown error')}")
                    except Exception as ai_error:
                        st.error(f"Error during AI analysis: {str(ai_error)}")
                        import traceback as tb
                        st.code(tb.format_exc())


    def render_home(self):
        apply_modern_styles()
        
        # 1. Hero Section with Real HD Product Mockup Frame
        hero_section(
            "Transform Your Resume into an ATS-Beating Executive Asset",
            "Receive high-precision AI feedback, benchmark keyword alignment against top job descriptions, and generate executive-ready documents engineered to pass screening filters."
        )
        
        # 2. Features Section (6 Cards Grid)
        render_feature_cards_grid()

        # 3. Product Showcase (4-Step Workflow)
        render_product_showcase()

        # 4. Executive Analytics Telemetry Preview
        render_analytics_preview_section()

        # 5. Primary Call to Action Banner
        render_primary_cta()

    def render_job_search(self):
        """Render the job search page"""
        render_job_search()


    def render_feedback_page(self):
        """Render the feedback page"""
        apply_modern_styles()
        
        # Page Header
        page_header(
            "Feedback & Suggestions",
            "Help us improve by sharing your thoughts"
        )
        
        # Initialize feedback manager
        feedback_manager = FeedbackManager()
        
        # Create tabs for form and stats
        form_tab, stats_tab = st.tabs(["Submit Feedback", "Feedback Stats"])
        
        with form_tab:
            feedback_manager.render_feedback_form()
            
        with stats_tab:
            feedback_manager.render_feedback_stats()

    def render_cover_letter_page(self):
        """Render AI Cover Letter & Candidate Outreach Suite page"""
        apply_modern_styles()
        hero_section(
            "AI Cover Letter & Outreach Suite",
            "Generate executive cover letters, recruiter cold emails, LinkedIn DMs, post-based replies, and interview follow-ups powered by AI.",
            "Multi-format outreach engine designed for high response rates and ATS compliance."
        )
        
        outreach_mode = st.selectbox(
            "Select Outreach Format",
            [
                "Executive Cover Letter",
                "Cold Email to Recruiter / Hiring Manager",
                "LinkedIn Connection Note & InMail DM",
                "LinkedIn / Twitter Post-Based DM (Reply to Hiring Post)",
                "Post-Interview Thank You & Follow-Up"
            ]
        )
        
        with st.form("cover_letter_outreach_form"):
            col1, col2 = st.columns(2)
            with col1:
                candidate_name = st.text_input("Your Full Name", value="Prince Kumar Jha")
                job_title = st.text_input("Target Job Title", value="Senior AI / Software Engineer")
                company_name = st.text_input("Target Company Name", value="Google / Hugging Face")
                recruiter_name = st.text_input("Recruiter / Interviewer Name (Optional)", value="Hiring Manager")
            with col2:
                experience_years = st.number_input("Years of Relevant Experience", min_value=0, max_value=30, value=4)
                skills_input = st.text_input("Key Skills (comma separated)", value="Python, PyTorch, React, FastAPI, System Design")
                tone = st.selectbox("Tone Profile", ["Professional", "Executive", "Passionate", "Engaging", "Creative"])
            
            if outreach_mode == "LinkedIn / Twitter Post-Based DM (Reply to Hiring Post)":
                context_text = st.text_area(
                    "Recruiter Post / Tweet Snippet",
                    placeholder="Paste the recruiter's hiring post or tweet here (e.g. 'Looking for a Senior Python Engineer to build scalable microservices...')...",
                    height=100
                )
            elif outreach_mode == "Post-Interview Thank You & Follow-Up":
                context_text = st.text_area(
                    "Key Interview Discussion Point",
                    placeholder="Briefly describe what you discussed during the interview (e.g. 'our conversation about microservices latency and team culture')...",
                    height=100
                )
            else:
                context_text = st.text_area(
                    "Target Job Description / Key Context (Optional)",
                    placeholder="Paste job description highlights here for AI-driven alignment...",
                    height=100
                )
            
            submit_outreach = st.form_submit_button("GENERATE OUTREACH CONTENT", type="primary", use_container_width=True)
            
        if submit_outreach:
            with st.spinner(f"AI is crafting your {outreach_mode.lower()}..."):
                generator = CoverLetterGenerator()
                skills_list = [s.strip() for s in skills_input.split(",") if s.strip()]
                
                if outreach_mode == "Executive Cover Letter":
                    result_text = generator.generate_cover_letter(candidate_name, job_title, company_name, skills_list, experience_years, context_text, tone)
                elif outreach_mode == "Cold Email to Recruiter / Hiring Manager":
                    result_text = generator.generate_cold_email(candidate_name, job_title, company_name, recruiter_name, skills_list, context_text, tone)
                elif outreach_mode == "LinkedIn Connection Note & InMail DM":
                    result_text = generator.generate_linkedin_dm(candidate_name, job_title, company_name, recruiter_name, skills_list, tone)
                elif outreach_mode == "LinkedIn / Twitter Post-Based DM (Reply to Hiring Post)":
                    result_text = generator.generate_post_based_dm(candidate_name, job_title, company_name, context_text, skills_list, tone)
                else:  # Post-Interview Thank You & Follow-Up
                    result_text = generator.generate_interview_followup(candidate_name, job_title, company_name, recruiter_name, context_text, tone)
            
            st.success(f"AI {outreach_mode} Generated Successfully!")
            
            # Metric analytics bar
            words = len(result_text.split())
            chars = len(result_text)
            read_time = max(1, round(words / 200))
            
            mcol1, mcol2, mcol3, mcol4 = st.columns(4)
            with mcol1:
                st.metric("Total Words", f"{words} words")
            with mcol2:
                st.metric("Characters", f"{chars}")
            with mcol3:
                st.metric("Estimated Read Time", f"~{read_time} min")
            with mcol4:
                st.metric("Tone Profile", tone)
            
            st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)
            
            # Display formatted markdown card + interactive text area
            st.markdown(f"#### Generated {outreach_mode}")
            render_clean_html(f"""
                <div style='background: #FFFFFF; border: 1px solid var(--border-subtle); border-left: 5px solid #10B981; border-radius: 12px; padding: 1.5rem 1.75rem; margin: 0.75rem 0 1.25rem 0; box-shadow: 0 4px 16px rgba(15, 23, 42, 0.04); font-family: "Inter", sans-serif; line-height: 1.7; color: #0F172A; white-space: pre-wrap; font-size: 0.95rem;'>
{result_text}
                </div>
            """)
            
            with st.expander("Edit / Copy Raw Plaintext", expanded=False):
                st.text_area("Plaintext Editor", value=result_text, height=250)
            
            # Interactive skill pop-ups
            if skills_list:
                st.markdown("#### Key Skills Embedded:")
                skill_cols = st.columns(min(len(skills_list), 5))
                for idx, sk in enumerate(skills_list[:5]):
                    with skill_cols[idx % 5]:
                        if st.button(f"{sk}", key=f"sk_pop_{idx}"):
                            st.info(f"**{sk}** has been strategically positioned to demonstrate relevant expertise to {company_name}.")
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            dcol1, dcol2 = st.columns(2)
            with dcol1:
                st.download_button(
                    label="Download Outreach Content (.txt)",
                    data=result_text,
                    file_name=f"{candidate_name.replace(' ', '_')}_{outreach_mode.replace(' ', '_')}.txt",
                    mime="text/plain",
                    use_container_width=True
                )
            with dcol2:
                st.info("Tip: You can copy the text above directly into LinkedIn messages, email clients, or job portals.")

    def render_interview_prep_page(self):
        """Render AI Mock Interview Prep page with 6 core role options available"""
        apply_modern_styles()
        hero_section(
            "AI Mock Interview Prep",
            "Master technical, behavioral, and system design interview questions tailored to top tier tech roles.",
            "Powered by multi-provider AI engine with STAR framework breakdowns, interactive practice modes, and real-time answer evaluation."
        )
        
        prep_gen = InterviewPrepGenerator()
        available_roles = prep_gen.available_roles
        
        with st.form("interview_prep_form"):
            st.markdown("### Target Role & Customization Form")
            col1, col2 = st.columns([2, 1])
            with col1:
                prep_role = st.selectbox("Role Category (6 Core Options)", available_roles, index=0)
            with col2:
                custom_skills = st.text_input("Focus Skills / Tech Stack", value="Python, System Design, SQL")
            
            submit_prep = st.form_submit_button("SUBMIT & GENERATE AI INTERVIEW QUESTIONS", type="primary", use_container_width=True)

        if submit_prep:
            with st.spinner("AI is generating targeted interview questions, answer strategies, and STAR frameworks..."):
                skills_list = [s.strip() for s in custom_skills.split(",") if s.strip()]
                st.session_state.current_prep_data = prep_gen.generate_interview_prep(prep_role, skills_list)
                st.session_state.last_role = prep_role
                st.session_state.prep_submitted = True
                st.success("Successfully generated role-specific interview prep data!")
        elif 'current_prep_data' not in st.session_state:
            # Generate default initial prep data silently for immediate view
            skills_list = [s.strip() for s in custom_skills.split(",") if s.strip()]
            st.session_state.current_prep_data = prep_gen.generate_interview_prep(prep_role, skills_list)
            st.session_state.last_role = prep_role

        data = st.session_state.get('current_prep_data', {})
        if not data:
            st.info("Form Ready — Select your target role above and click SUBMIT to generate AI questions.")
            return
            
        is_ai = data.get("is_ai_generated", False)
        render_clean_html(f"""
            <div style='display: flex; justify-content: space-between; align-items: center; background: var(--bg-surface); padding: 1rem 1.25rem; border-radius: 12px; border: 1px solid var(--border-subtle); margin: 1.25rem 0;'>
                <div style='font-size: 1.15rem; font-weight: 700; color: var(--text-primary);'>
                    Targeting: <span style='color: var(--accent);'>{data.get('role', prep_role)}</span>
                </div>
                <div style='background: var(--accent-light); color: var(--accent); font-weight: 700; padding: 0.3rem 0.8rem; border-radius: 9999px; font-size: 0.8rem; border: 1px solid var(--success-border);'>
                    {'Real-Time AI Generated' if is_ai else 'Structured Expert Bank'}
                </div>
            </div>
        """)
        
        questions = data.get("questions", [])
        study_guide_text = f"AI MOCK INTERVIEW STUDY GUIDE - {data.get('role', prep_role)}\n" + "="*60 + "\n\n"

        for idx, q in enumerate(questions):
            q_type = q.get("type", "Technical")
            diff = q.get("difficulty", "Medium")
            q_text = q.get("question", "")
            ans = q.get("answer_guide", "")
            star = q.get("star_framework", {})
            keywords = q.get("keywords", [])
            
            diff_color = "#10B981" if diff == "Easy" else "#D97706" if diff == "Medium" else "#DC2626"
            
            study_guide_text += f"QUESTION #{idx+1} [{q_type}] ({diff}):\n{q_text}\n\nANSWER GUIDE:\n{ans}\n\n"
            if star:
                study_guide_text += f"STAR BREAKDOWN:\n- Situation: {star.get('situation','')}\n- Task: {star.get('task','')}\n- Action: {star.get('action','')}\n- Result: {star.get('result','')}\n\n"
            study_guide_text += "-"*50 + "\n\n"

            with st.expander(f"Question #{idx+1} [{q_type}] • {q_text}", expanded=(idx == 0)):
                render_clean_html(f"""
                    <div style='margin-bottom: 1rem;'>
                        <span style='background: var(--bg-surface-raised); color: {diff_color}; font-weight: 700; font-size: 0.75rem; padding: 0.2rem 0.6rem; border-radius: 6px; border: 1px solid var(--border-subtle);'>Difficulty: {diff}</span>
                        <span style='background: var(--accent-light); color: var(--accent); font-weight: 700; font-size: 0.75rem; padding: 0.2rem 0.6rem; border-radius: 6px; margin-left: 0.5rem; border: 1px solid var(--success-border);'>{q_type}</span>
                    </div>
                """)
                
                # Answer Strategy Guide Card
                render_clean_html(f"""
                    <div style='background: linear-gradient(145deg, rgba(25, 29, 38, 0.9) 0%, rgba(13, 15, 20, 0.95) 100%); border: 1px solid rgba(255, 255, 255, 0.12); border-left: 5px solid #30D158; border-radius: 12px; padding: 1.25rem 1.5rem; margin: 1rem 0 1.5rem 0; box-shadow: 0 4px 12px rgba(0,0,0,0.4);'>
                        <div style='font-size: 0.8rem; font-weight: 800; color: #30D158; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.6rem;'>ANSWER STRATEGY GUIDE</div>
                        <div style='color: #FFFFFF; font-size: 0.95rem; line-height: 1.7;'>{ans}</div>
                    </div>
                """)
                
                # STAR Framework Breakdown Visual Cards
                if star:
                    st.markdown("<h4 style='color: var(--text-primary); margin-top: 1rem; margin-bottom: 0.75rem; font-weight: 700;'>STAR Framework Breakdown Matrix</h4>", unsafe_allow_html=True)
                    sc1, sc2 = st.columns(2)
                    with sc1:
                        render_clean_html(f"""
                            <div style='background: #F0F9FF; border: 1px solid #BAE6FD; border-left: 4px solid #0284C7; border-radius: 10px; padding: 1rem 1.25rem; margin-bottom: 1rem;'>
                                <div style='font-size: 0.75rem; font-weight: 800; color: #0369A1; text-transform: uppercase; letter-spacing: 0.04em; margin-bottom: 0.35rem;'>SITUATION</div>
                                <div style='color: #0F172A; font-size: 0.925rem; line-height: 1.55;'>{star.get('situation', 'N/A')}</div>
                            </div>
                        """)
                        render_clean_html(f"""
                            <div style='background: #F5F3FF; border: 1px solid #DDD6FE; border-left: 4px solid #7C3AED; border-radius: 10px; padding: 1rem 1.25rem; margin-bottom: 1rem;'>
                                <div style='font-size: 0.75rem; font-weight: 800; color: #6D28D9; text-transform: uppercase; letter-spacing: 0.04em; margin-bottom: 0.35rem;'>TASK</div>
                                <div style='color: #0F172A; font-size: 0.925rem; line-height: 1.55;'>{star.get('task', 'N/A')}</div>
                            </div>
                        """)
                    with sc2:
                        render_clean_html(f"""
                            <div style='background: #ECFDF5; border: 1px solid #A7F3D0; border-left: 4px solid #10B981; border-radius: 10px; padding: 1rem 1.25rem; margin-bottom: 1rem;'>
                                <div style='font-size: 0.75rem; font-weight: 800; color: #047857; text-transform: uppercase; letter-spacing: 0.04em; margin-bottom: 0.35rem;'>ACTION</div>
                                <div style='color: #0F172A; font-size: 0.925rem; line-height: 1.55;'>{star.get('action', 'N/A')}</div>
                            </div>
                        """)
                        render_clean_html(f"""
                            <div style='background: #FFF7ED; border: 1px solid #FFEDD5; border-left: 4px solid #F97316; border-radius: 10px; padding: 1rem 1.25rem; margin-bottom: 1rem;'>
                                <div style='font-size: 0.75rem; font-weight: 800; color: #C2410C; text-transform: uppercase; letter-spacing: 0.04em; margin-bottom: 0.35rem;'>RESULT & IMPACT</div>
                                <div style='color: #0F172A; font-size: 0.925rem; line-height: 1.55;'>{star.get('result', 'N/A')}</div>
                            </div>
                        """)
                
                if keywords:
                    st.markdown("#### Key Concepts & Terminology:")
                    kw_cols = st.columns(min(len(keywords), 4))
                    for k_idx, kw in enumerate(keywords[:4]):
                        with kw_cols[k_idx % 4]:
                            if st.button(f"{kw}", key=f"kw_btn_{idx}_{k_idx}"):
                                st.info(f"**{kw}**: Mentioning this key technical concept signals deep hands-on expertise to interviewers for {prep_role} positions.")
                
                # Interactive Practice Box with Real AI Evaluation
                st.markdown("<hr style='margin: 1.25rem 0; border-color: var(--border-subtle);'>", unsafe_allow_html=True)
                st.markdown("#### Self-Practice Mode")
                user_ans = st.text_area("Draft your response to practice:", key=f"user_ans_{idx}", placeholder="Type your response using the STAR framework (Situation, Task, Action, Result)...", height=110)
                
                if st.button("Evaluate My Answer with AI", key=f"eval_btn_{idx}"):
                    if user_ans and len(user_ans.strip()) >= 10:
                        with st.spinner("AI is evaluating your response against the STAR framework..."):
                            eval_res = prep_gen.evaluate_user_answer(q_text, user_ans, data.get('role', prep_role), star)
                            
                            score = eval_res.get('score', 80)
                            badge_bg = "var(--success-bg)" if score >= 80 else "var(--warning-bg)"
                            badge_text = "var(--success-text)" if score >= 80 else "var(--warning-text)"
                            
                            render_clean_html(f"""
                                <div style='background: var(--bg-surface-raised); border: 1px solid var(--border-subtle); border-radius: 12px; padding: 1.25rem; margin-top: 1rem;'>
                                    <div style='display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;'>
                                        <h4 style='margin: 0; color: var(--text-primary);'>AI Answer Evaluation Report</h4>
                                        <span style='background: {badge_bg}; color: {badge_text}; font-weight: 800; font-size: 1rem; padding: 0.3rem 0.8rem; border-radius: 9999px;'>Score: {score} / 100</span>
                                    </div>
                                    <p style='color: var(--text-secondary); margin-bottom: 1rem; line-height: 1.5;'>{eval_res.get('feedback', '')}</p>
                                </div>
                            """)
                            
                            ec1, ec2 = st.columns(2)
                            with ec1:
                                st.markdown("**Key Strengths:**")
                                for st_item in eval_res.get('strengths', []):
                                    st.markdown(f"- {st_item}")
                            with ec2:
                                st.markdown("**Recommendations for Improvement:**")
                                for imp_item in eval_res.get('improvements', []):
                                    st.markdown(f"- {imp_item}")
                    else:
                        st.warning("Please type a response (at least 10 characters) before running AI evaluation.")

        st.markdown("<br>", unsafe_allow_html=True)
        st.download_button(
            label="Download Interview Prep Study Guide (.txt)",
            data=study_guide_text,
            file_name=f"{data.get('role', 'Interview')}_Prep_Guide.txt",
            mime="text/plain",
            use_container_width=True
        )




    def main(self):
        """Main application entry point"""
        self.apply_global_styles()

        # Force home page on first load
        if 'initial_load' not in st.session_state:
            st.session_state.initial_load = True
            st.session_state.page = 'home'
            st.rerun()

        # Get current page and render sticky Top Nav
        current_page = st.session_state.get('page', 'home')
        render_top_nav(current_page)

        # Reload sub-page modules to guarantee clean execution without cached duplicate handlers
        import importlib
        import pages.resume_analyzer
        import pages.resume_builder
        import pages.cover_letter
        import pages.interview_prep
        import pages.about

        importlib.reload(pages.resume_analyzer)
        importlib.reload(pages.resume_builder)
        importlib.reload(pages.cover_letter)
        importlib.reload(pages.interview_prep)
        importlib.reload(pages.about)

        page_dispatch = {
            "home": self.render_home,
            "resume_analyzer": pages.resume_analyzer.render_resume_analyzer_page,
            "resume_builder": pages.resume_builder.render_resume_builder_page,
            "cover_letter": pages.cover_letter.render_cover_letter_page,
            "interview_prep": pages.interview_prep.render_interview_prep_page,
            "dashboard": self.render_dashboard,
            "job_search": self.render_job_search,
            "feedback": self.render_feedback_page,
            "about": pages.about.render_about_page
        }

        # Render current page content
        target_func = page_dispatch.get(current_page, self.render_home)
        target_func()

        # Add global footer
        self.add_footer()

if __name__ == "__main__":
    app = ResumeApp()
    app.main()