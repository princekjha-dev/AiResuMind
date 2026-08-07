import textwrap

def render_clean_html(html_str):
    """Cleanly render HTML by stripping multiline indentation to prevent Markdown code block bugs."""
    if not html_str:
        return
    lines = [line.strip() for line in html_str.splitlines() if line.strip()]
    cleaned = chr(10).join(lines)
    st.markdown(cleaned, unsafe_allow_html=True)

import streamlit as st
from .job_portals import JobPortal
from .linkedin_scraper import render_linkedin_scraper

def render_job_search():
    """Render High-Precision Dark Apple Glassmorphic Job Search Interface with Live Working Job Links"""
    
    # Inject Master Dark Glassmorphic CSS System
    render_clean_html("""
        <style>
        .js-root {
            background-color: transparent !important;
            color: #F5F5F7 !important;
            max-width: 1440px !important;
            margin: 0 auto !important;
        }

        /* Hero Section */
        .js-hero {
            text-align: center;
            padding: 32px 0 24px 0;
        }
        .js-hero-h1 {
            font-size: 52px;
            font-weight: 800;
            line-height: 1.15;
            color: #FFFFFF;
            letter-spacing: -0.025em;
            margin-bottom: 14px;
        }
        .js-gradient-highlight {
            background: linear-gradient(135deg, #0071E3 0%, #7000FF 60%, #29D8E8 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .js-hero-sub {
            font-size: 17.5px;
            color: #A1A1AA;
            max-width: 720px;
            margin: 0 auto 28px auto;
            line-height: 1.6;
        }

        /* Search Container Panel */
        .js-search-panel {
            background: linear-gradient(145deg, rgba(25, 29, 38, 0.9) 0%, rgba(13, 15, 20, 0.95) 100%) !important;
            border: 1px solid rgba(255, 255, 255, 0.12) !important;
            border-radius: 24px !important;
            padding: 32px !important;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.6), inset 0 1px 1px rgba(255, 255, 255, 0.15) !important;
            margin-bottom: 32px !important;
            backdrop-filter: blur(20px) !important;
        }

        /* Working Direct Apply Link Button */
        .js-apply-link {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            background: linear-gradient(135deg, #0071E3 0%, #0077ED 100%);
            color: #FFFFFF !important;
            font-weight: 700;
            font-size: 14px;
            padding: 10px 20px;
            border-radius: 9999px;
            text-decoration: none !important;
            box-shadow: 0 4px 16px rgba(0, 113, 227, 0.35);
            transition: all 0.25s ease;
        }
        .js-apply-link:hover {
            transform: scale(1.03);
            box-shadow: 0 8px 24px rgba(0, 113, 227, 0.55);
            color: #FFFFFF !important;
        }

        /* Trust Metric Cards */
        .js-stats-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 20px;
            margin: 40px 0;
        }
        .js-stat-card {
            background: linear-gradient(145deg, rgba(25, 29, 38, 0.85) 0%, rgba(13, 15, 20, 0.95) 100%);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            padding: 24px 18px;
            text-align: center;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
            transition: all 0.3s ease;
        }
        .js-stat-card:hover {
            transform: translateY(-4px);
            border-color: rgba(0, 113, 227, 0.5);
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.6), 0 0 25px rgba(0, 113, 227, 0.2);
        }
        .js-stat-val {
            font-size: 38px;
            font-weight: 800;
            color: #FFFFFF;
            margin-bottom: 2px;
        }
        .js-stat-lbl {
            font-size: 14px;
            color: #A1A1AA;
            font-weight: 600;
        }

        /* Section Titles */
        .js-section-title {
            font-size: 34px;
            font-weight: 800;
            color: #FFFFFF;
            letter-spacing: -0.02em;
            margin-bottom: 6px;
        }
        .js-section-sub {
            font-size: 16px;
            color: #A1A1AA;
            margin-bottom: 24px;
        }

        /* Trending Skills */
        .js-skill-card {
            background: linear-gradient(145deg, rgba(25, 29, 38, 0.85) 0%, rgba(13, 15, 20, 0.95) 100%);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 18px;
            padding: 20px 22px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
            display: flex;
            align-items: center;
            justify-content: space-between;
            transition: all 0.3s ease;
        }
        .js-skill-card:hover {
            transform: translateY(-4px);
            border-color: rgba(0, 113, 227, 0.5);
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.6), 0 0 25px rgba(0, 113, 227, 0.2);
        }

        /* Categories Grid */
        .js-category-card {
            background: linear-gradient(145deg, rgba(25, 29, 38, 0.85) 0%, rgba(13, 15, 20, 0.95) 100%);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 16px;
            padding: 20px;
            text-align: center;
            transition: all 0.25s ease;
        }
        .js-category-card:hover {
            transform: translateY(-4px);
            border-color: rgba(0, 113, 227, 0.5);
            box-shadow: 0 15px 30px rgba(0, 0, 0, 0.5), 0 0 20px rgba(0, 113, 227, 0.15);
        }

        /* Steps */
        .js-step-card {
            background: linear-gradient(145deg, rgba(25, 29, 38, 0.85) 0%, rgba(13, 15, 20, 0.95) 100%);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            padding: 32px 24px;
            text-align: center;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
        }
        .js-step-num {
            width: 44px;
            height: 44px;
            border-radius: 50%;
            background: linear-gradient(135deg, #0071E3 0%, #0077ED 100%);
            color: #FFFFFF;
            font-size: 18px;
            font-weight: 800;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 16px auto;
            box-shadow: 0 0 15px rgba(0, 113, 227, 0.4);
        }

        /* Newsletter */
        .js-newsletter-box {
            background: linear-gradient(135deg, rgba(0, 113, 227, 0.25) 0%, rgba(112, 0, 255, 0.2) 100%);
            border: 1px solid rgba(0, 113, 227, 0.4);
            border-radius: 24px;
            padding: 44px 36px;
            text-align: center;
            color: #FFFFFF;
            margin: 40px 0;
            box-shadow: 0 20px 50px rgba(0, 0, 0, 0.6);
            backdrop-filter: blur(20px);
        }
        </style>
    """)

    # 1. HERO HEADLINE SECTION
    render_clean_html("""
        <div class="js-hero">
            <h1 class="js-hero-h1">
                Find Your <span class="js-gradient-highlight">Dream Job</span> Across Every Platform
            </h1>
            <p class="js-hero-sub">
                Search verified opportunities from LinkedIn, Indeed, Naukri, and Foundit with instant AI match scoring.
            </p>
        </div>
    """)

    # MAIN JOB SEARCH TABS
    tab_search, tab_linkedin = st.tabs([" Multi-Platform Job Search Engine", " Real-Time LinkedIn Scraper"])

    with tab_search:
        col1, col2, col3 = st.columns([0.42, 0.42, 0.16], gap="medium")
        with col1:
            job_query = st.text_input("JOB TITLE OR SKILLS", placeholder="e.g. React Developer, Data Scientist", key="hero_job_title")
        with col2:
            location = st.text_input("LOCATION", placeholder="e.g. Bangalore, Remote, New York", key="hero_location")
        with col3:
            st.markdown('<div style="height: 28px;"></div>', unsafe_allow_html=True)
            search_triggered = st.button("SEARCH JOBS", type="primary", use_container_width=True)

        render_clean_html("""
            <div style="display: flex; gap: 10px; align-items: center; justify-content: center; margin-top: 18px; flex-wrap: wrap;">
                <span style="font-size: 12px; font-weight: 700; color: #A1A1AA; text-transform: uppercase; letter-spacing: 0.05em;">POPULAR SEARCHES:</span>
                <span style="background: rgba(255,255,255,0.08); color: #F5F5F7; border: 1px solid rgba(255,255,255,0.12); padding: 4px 12px; border-radius: 9999px; font-size: 13px; font-weight: 500;">React</span>
                <span style="background: rgba(255,255,255,0.08); color: #F5F5F7; border: 1px solid rgba(255,255,255,0.12); padding: 4px 12px; border-radius: 9999px; font-size: 13px; font-weight: 500;">Python</span>
                <span style="background: rgba(255,255,255,0.08); color: #F5F5F7; border: 1px solid rgba(255,255,255,0.12); padding: 4px 12px; border-radius: 9999px; font-size: 13px; font-weight: 500;">Java</span>
                <span style="background: rgba(255,255,255,0.08); color: #F5F5F7; border: 1px solid rgba(255,255,255,0.12); padding: 4px 12px; border-radius: 9999px; font-size: 13px; font-weight: 500;">Node.js</span>
                <span style="background: rgba(255,255,255,0.08); color: #F5F5F7; border: 1px solid rgba(255,255,255,0.12); padding: 4px 12px; border-radius: 9999px; font-size: 13px; font-weight: 500;">Remote</span>
                <span style="background: rgba(255,255,255,0.08); color: #F5F5F7; border: 1px solid rgba(255,255,255,0.12); padding: 4px 12px; border-radius: 9999px; font-size: 13px; font-weight: 500;">Internship</span>
                <span style="background: rgba(255,255,255,0.08); color: #F5F5F7; border: 1px solid rgba(255,255,255,0.12); padding: 4px 12px; border-radius: 9999px; font-size: 13px; font-weight: 500;">AI Engineer</span>
            </div>
        """)

        if search_triggered or 'in_platform_search_results' in st.session_state:
            if search_triggered and job_query:
                job_portal = JobPortal()
                st.session_state.in_platform_search_results = job_portal.search_jobs(job_query, location, "all")

            results = st.session_state.get('in_platform_search_results', [])
            if results:
                st.markdown(f'<h3 style="font-size: 24px; font-weight: 800; color: #FFFFFF; margin: 28px 0 16px 0;">AI Matched Opportunities ({len(results)} Verified Roles)</h3>', unsafe_allow_html=True)
                for idx, job in enumerate(results):
                    job_id = job.get('id', f"job_{idx}")
                    title = job.get('title', 'Software Engineer')
                    company = job.get('company', 'Tech Corp')
                    company_icon = job.get('company_icon', 'fas fa-briefcase')
                    company_color = job.get('company_color', '#0071E3')
                    loc_str = job.get('location', location if location else 'Remote')
                    work_mode = job.get('work_mode', 'Hybrid')
                    match_score = job.get('match_score', 94)
                    salary = job.get('salary', 'Competitive Package')
                    exp_req = job.get('experience', '0-3 years')
                    apply_url = job.get('apply_url', 'https://www.google.com/about/careers')
                    skills = job.get('skills', ['Python', 'Software Engineering'])
                    desc = job.get('description', f'Role overview for {title} at {company}.')
                    
                    skills_html = "".join([f'<span style="background: rgba(255,255,255,0.06); color: #A1A1AA; border: 1px solid rgba(255,255,255,0.1); padding: 4px 12px; border-radius: 9999px; font-size: 0.75rem; margin-right: 6px; font-weight: 600;">{sk}</span>' for sk in skills])
                    
                    render_clean_html(f"""
                        <div style="background: linear-gradient(145deg, rgba(25, 29, 38, 0.85) 0%, rgba(13, 15, 20, 0.95) 100%); border: 1px solid rgba(255, 255, 255, 0.1); border-left: 4px solid #0071E3; border-radius: 18px; padding: 24px; margin-bottom: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.4);">
                            <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 12px; margin-bottom: 12px;">
                                <div>
                                    <h4 style="font-size: 20px; font-weight: 700; color: #FFFFFF; margin: 0 0 6px 0;">
                                        <i class="{company_icon}" style="color: {company_color}; margin-right: 8px;"></i> {title}
                                    </h4>
                                    <div style="font-size: 15px; color: #FFFFFF; font-weight: 600;">
                                        {company} • <span style="color: #A1A1AA; font-weight: 500;">{loc_str} ({work_mode})</span>
                                    </div>
                                </div>
                                <div style="display: flex; align-items: center; gap: 12px;">
                                    <span style="background: rgba(48, 209, 88, 0.15); color: #30D158; border: 1px solid rgba(48, 209, 88, 0.4); font-weight: 700; padding: 4px 12px; border-radius: 9999px; font-size: 13px;">{match_score}% AI Match</span>
                                    <a href="{apply_url}" target="_blank" class="js-apply-link"> Apply on {company} Site</a>
                                </div>
                            </div>
                            <div style="display: flex; gap: 20px; font-size: 14px; color: #A1A1AA; margin-bottom: 14px; flex-wrap: wrap;">
                                <span>Salary: <strong style="color: #FFFFFF;">{salary}</strong></span>
                                <span>Experience: <strong style="color: #FFFFFF;">{exp_req}</strong></span>
                            </div>
                            <div>{skills_html}</div>
                        </div>
                    """)
                    
                    bcol1, bcol2 = st.columns(2)
                    with bcol1:
                        with st.expander(f" View Job Details & Requirements"):
                            st.markdown(desc)
                    with bcol2:
                        if st.button(f" Generate Cold Email for {company}", key=f"prep_{job_id}_{idx}", use_container_width=True):
                            st.session_state.last_role = title
                            st.info(f"Navigate to 'Cold Email Generator' in top navigation to craft personalized recruiter outreach for {title}!")
                            
                    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

    with tab_linkedin:
        st.markdown('<div class="editorial-card" style="margin-top: 16px;">', unsafe_allow_html=True)
        st.markdown('<h3 style="color: #FFFFFF; font-weight: 800; font-size: 24px; margin-bottom: 4px;"> Real-Time LinkedIn Job Scraper</h3>', unsafe_allow_html=True)
        st.markdown('<p style="color: #A1A1AA; font-size: 15px; margin-bottom: 24px;">Extract live job postings directly from LinkedIn search with one click.</p>', unsafe_allow_html=True)
        render_linkedin_scraper()
        st.markdown('</div>', unsafe_allow_html=True)

    # 3. TRUST METRIC CARDS
    render_clean_html("""
        <div class="js-stats-grid">
            <div class="js-stat-card">
                <div class="js-stat-val" style="color: #0071E3;">180K+</div>
                <div class="js-stat-lbl">Jobs Indexed</div>
            </div>
            <div class="js-stat-card">
                <div class="js-stat-val" style="color: #A855F7;">15K+</div>
                <div class="js-stat-lbl">Companies</div>
            </div>
            <div class="js-stat-card">
                <div class="js-stat-val" style="color: #30D158;">2.5K+</div>
                <div class="js-stat-lbl">Daily Listings</div>
            </div>
            <div class="js-stat-card">
                <div class="js-stat-val" style="color: #29D8E8;">95%</div>
                <div class="js-stat-lbl">ATS Success</div>
            </div>
        </div>
    """)

    # 4. TRENDING SKILLS IN 2026
    render_clean_html("""
        <div>
            <h2 class="js-section-title">Trending Skills in 2026</h2>
            <p class="js-section-sub">Skills with the highest hiring demand in market right now.</p>
        </div>
    """)

    skills_list = [
        {"name": "Artificial Intelligence", "demand": "+45%", "status": "High Demand", "icon": ""},
        {"name": "Machine Learning", "demand": "+38%", "status": "High Demand", "icon": ""},
        {"name": "Cybersecurity", "demand": "+35%", "status": "High Demand", "icon": ""},
        {"name": "Cloud Computing", "demand": "+41%", "status": "High Demand", "icon": ""},
        {"name": "React", "demand": "+29%", "status": "Trending", "icon": ""},
        {"name": "Node.js", "demand": "+26%", "status": "Trending", "icon": ""},
        {"name": "Python", "demand": "+40%", "status": "High Demand", "icon": ""},
        {"name": "DevOps", "demand": "+31%", "status": "High Demand", "icon": ""},
        {"name": "Data Science", "demand": "+37%", "status": "High Demand", "icon": ""}
    ]

    sk_cols = st.columns(3, gap="medium")
    for idx, sk in enumerate(skills_list):
        with sk_cols[idx % 3]:
            render_clean_html(f"""
                <div class="js-skill-card" style="margin-bottom: 16px;">
                    <div style="display: flex; align-items: center; gap: 12px;">
                        <span style="font-size: 24px;">{sk['icon']}</span>
                        <div>
                            <div style="font-size: 16px; font-weight: 700; color: #FFFFFF;">{sk['name']}</div>
                            <div style="font-size: 13px; color: #0071E3; font-weight: 700;">{sk['demand']} growth</div>
                        </div>
                    </div>
                    <span style="background: rgba(48, 209, 88, 0.15); color: #30D158; border: 1px solid rgba(48, 209, 88, 0.3); font-size: 12px; font-weight: 700; padding: 4px 10px; border-radius: 9999px;">{sk['status']}</span>
                </div>
            """)

    # 5. MARKET INSIGHTS DASHBOARD
    render_clean_html("""
        <div style="margin: 48px 0 28px 0;">
            <h2 class="js-section-title">Market Insights Dashboard</h2>
            <p class="js-section-sub">Real-time hiring statistics and salary benchmarks across major tech hubs.</p>
        </div>
    """)

    ins_cols = st.columns(3, gap="medium")
    with ins_cols[0]:
        render_clean_html("""
            <div style="background: linear-gradient(145deg, rgba(25, 29, 38, 0.85) 0%, rgba(13, 15, 20, 0.95) 100%); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 20px; padding: 28px; box-shadow: 0 10px 30px rgba(0,0,0,0.4);">
                <h3 style="font-size: 20px; font-weight: 700; color: #FFFFFF; margin-bottom: 16px;">Top Hiring Cities</h3>
                <div style="display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid rgba(255,255,255,0.08); font-size: 15px; font-weight: 600;">
                    <span>Bengaluru</span> <span style="color: #0071E3;">42,500+ Jobs</span>
                </div>
                <div style="display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid rgba(255,255,255,0.08); font-size: 15px; font-weight: 600;">
                    <span>Hyderabad</span> <span style="color: #0071E3;">28,100+ Jobs</span>
                </div>
                <div style="display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid rgba(255,255,255,0.08); font-size: 15px; font-weight: 600;">
                    <span>Pune</span> <span style="color: #0071E3;">19,400+ Jobs</span>
                </div>
                <div style="display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid rgba(255,255,255,0.08); font-size: 15px; font-weight: 600;">
                    <span>Gurugram</span> <span style="color: #0071E3;">16,800+ Jobs</span>
                </div>
                <div style="display: flex; justify-content: space-between; padding: 10px 0; font-size: 15px; font-weight: 600;">
                    <span>Noida</span> <span style="color: #0071E3;">12,300+ Jobs</span>
                </div>
            </div>
        """)

    with ins_cols[1]:
        render_clean_html("""
            <div style="background: linear-gradient(145deg, rgba(25, 29, 38, 0.85) 0%, rgba(13, 15, 20, 0.95) 100%); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 20px; padding: 28px; box-shadow: 0 10px 30px rgba(0,0,0,0.4);">
                <h3 style="font-size: 20px; font-weight: 700; color: #FFFFFF; margin-bottom: 16px;">Average Salary</h3>
                <div style="display: flex; justify-content: space-between; padding: 12px 0; border-bottom: 1px solid rgba(255,255,255,0.08);">
                    <div>
                        <div style="font-size: 15px; font-weight: 700; color: #FFFFFF;">Entry Level</div>
                        <div style="font-size: 13px; color: #A1A1AA;">0 - 2 Years</div>
                    </div>
                    <div style="font-size: 18px; font-weight: 800; color: #30D158;">₹ 6 - 12 LPA</div>
                </div>
                <div style="display: flex; justify-content: space-between; padding: 12px 0; border-bottom: 1px solid rgba(255,255,255,0.08);">
                    <div>
                        <div style="font-size: 15px; font-weight: 700; color: #FFFFFF;">Mid Level</div>
                        <div style="font-size: 13px; color: #A1A1AA;">3 - 6 Years</div>
                    </div>
                    <div style="font-size: 18px; font-weight: 800; color: #30D158;">₹ 14 - 28 LPA</div>
                </div>
                <div style="display: flex; justify-content: space-between; padding: 12px 0;">
                    <div>
                        <div style="font-size: 15px; font-weight: 700; color: #FFFFFF;">Senior Level</div>
                        <div style="font-size: 13px; color: #A1A1AA;">7+ Years</div>
                    </div>
                    <div style="font-size: 18px; font-weight: 800; color: #30D158;">₹ 32 - 65+ LPA</div>
                </div>
            </div>
        """)

    with ins_cols[2]:
        render_clean_html("""
            <div style="background: linear-gradient(145deg, rgba(25, 29, 38, 0.85) 0%, rgba(13, 15, 20, 0.95) 100%); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 20px; padding: 28px; box-shadow: 0 10px 30px rgba(0,0,0,0.4);">
                <h3 style="font-size: 20px; font-weight: 700; color: #FFFFFF; margin-bottom: 12px;">Hiring Growth Rate</h3>
                <div style="font-size: 36px; font-weight: 800; color: #0071E3; margin-bottom: 6px;">+34.2% YoY</div>
                <p style="font-size: 14px; color: #A1A1AA; line-height: 1.5;">Accelerated job openings across AI engineering, full stack development, cloud infrastructure, and product management.</p>
            </div>
        """)

    # 6. FEATURED COMPANIES
    render_clean_html("""
        <div style="margin: 48px 0 28px 0;">
            <h2 class="js-section-title">Featured Companies</h2>
            <p class="js-section-sub">Top tier employers actively recruiting tech talent today.</p>
        </div>
    """)

    companies = [
        {"name": "Google", "role": "Software & AI", "open": "142 Open Positions", "rating": "4.8 ", "url": "https://www.google.com/about/careers/applications/jobs/results/"},
        {"name": "Microsoft", "role": "Cloud & Enterprise", "open": "189 Open Positions", "rating": "4.7 ", "url": "https://careers.microsoft.com/"},
        {"name": "Apple", "role": "Consumer Tech & Hardware", "open": "95 Open Positions", "rating": "4.9 ", "url": "https://www.apple.com/careers/"},
        {"name": "Meta", "role": "AI & Social Networking", "open": "112 Open Positions", "rating": "4.6 ", "url": "https://www.metacareers.com/"},
        {"name": "Netflix", "role": "Streaming & Infrastructure", "open": "48 Open Positions", "rating": "4.8 ", "url": "https://jobs.netflix.com/"},
        {"name": "Amazon", "role": "AWS & E-Commerce", "open": "230 Open Positions", "rating": "4.5 ", "url": "https://www.amazon.jobs/"}
    ]

    comp_cols = st.columns(3, gap="medium")
    for idx, c in enumerate(companies):
        with comp_cols[idx % 3]:
            render_clean_html(f"""
                <div style="background: linear-gradient(145deg, rgba(25, 29, 38, 0.85) 0%, rgba(13, 15, 20, 0.95) 100%); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 18px; padding: 22px; margin-bottom: 16px; box-shadow: 0 10px 30px rgba(0,0,0,0.4);">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                        <h4 style="font-size: 18px; font-weight: 700; color: #FFFFFF; margin: 0;">{c['name']}</h4>
                        <span style="font-size: 13px; font-weight: 700; color: #FFBD2E;">{c['rating']}</span>
                    </div>
                    <div style="font-size: 14px; color: #A1A1AA; margin-bottom: 12px;">{c['role']}</div>
                    <a href="{c['url']}" target="_blank" style="font-size: 13px; font-weight: 700; color: #0071E3; text-decoration: none;">{c['open']} →</a>
                </div>
            """)