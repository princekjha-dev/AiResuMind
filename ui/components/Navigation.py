import streamlit as st


def render_clean_html(html_str):
    """Cleanly render HTML by stripping multiline indentation."""
    if not html_str:
        return
    lines = [line.strip() for line in html_str.splitlines() if line.strip()]
    cleaned = chr(10).join(lines)
    st.markdown(cleaned, unsafe_allow_html=True)


def render_navigation(active_page=None):
    """
    Apple & Linear Inspired Sticky Glassmorphism Navigation Bar.
    - Centered max-width container (1280px).
    - Subtle glassmorphism: background rgba(10,12,15,0.65) with backdrop-filter blur(20px).
    - AiResuMind logo on the left.
    - Minimal navigation links: Dashboard, Resume Analyzer, Resume Builder, Cold Mail, Job Search.
    - Right side: Clean Sign In button.
    """

    current_page = active_page or st.session_state.get("page", "home")
    if hasattr(st, "query_params"):
        st.query_params["page"] = current_page

    nav_items = [
        ("dashboard", "Dashboard"),
        ("resume_analyzer", "Resume Analyzer"),
        ("resume_builder", "Resume Builder"),
        ("cold_mail", "Cold Mail"),
        ("job_search", "Job Search"),
    ]

    is_auth = st.session_state.get("user_authenticated", False)
    auth_label = "Profile" if is_auth else "Sign In"
    auth_target = "dashboard" if is_auth else "signin"

    li_elements = []
    for page_key, label in nav_items:
        is_active = current_page == page_key
        active_cls = " active" if is_active else ""
        li_elements.append(
            f'<li class="arm-nav-li">'
            f'<a href="?page={page_key}" target="_self" class="arm-nav-a{active_cls}">{label}</a>'
            f"</li>"
        )
    nav_links_html = "".join(li_elements)

    html_str = f"""
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    <style>
    /* Reset Streamlit default container top spacing */
    .main .block-container,
    [data-testid="stAppViewBlockContainer"],
    [data-testid="stMainBlockContainer"],
    [data-testid="stVerticalBlock"] > div:first-child,
    .stMainBlockContainer,
    .block-container,
    section.main > div {{
        padding-top: 0 !important;
        margin-top: 0 !important;
    }}
    .stApp > header,
    [data-testid="stHeader"],
    #stHeader {{
        display: none !important;
        height: 0 !important;
        min-height: 0 !important;
    }}

    /* Sticky Glassmorphism Header */
    header.arm-site-header {{
        position: sticky !important;
        top: 0 !important;
        left: 0 !important;
        right: 0 !important;
        z-index: 999999 !important;
        width: 100% !important;
        height: 56px !important;
        background-color: rgba(10, 12, 15, 0.65) !important;
        backdrop-filter: blur(20px) !important;
        -webkit-backdrop-filter: blur(20px) !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08) !important;
        margin-bottom: 0 !important;
    }}

    /* Inner Max-Width Container */
    div.arm-header-inner {{
        max-width: 1280px !important;
        margin: 0 auto !important;
        padding: 0 24px !important;
        height: 56px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: space-between !important;
        box-sizing: border-box !important;
    }}

    /* Brand Logo */
    a.arm-brand-logo {{
        display: flex !important;
        align-items: center !important;
        gap: 10px !important;
        text-decoration: none !important;
        flex-shrink: 0 !important;
        cursor: pointer !important;
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
        margin: 0 !important;
    }}

    div.arm-brand-icon {{
        width: 26px !important;
        height: 26px !important;
        border-radius: 7px !important;
        background: linear-gradient(135deg, #6366F1 0%, #A855F7 50%, #EC4899 100%) !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        font-size: 12px !important;
        color: #ffffff !important;
    }}

    span.arm-brand-title {{
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "Inter", sans-serif !important;
        font-size: 16px !important;
        font-weight: 700 !important;
        color: #ffffff !important;
        letter-spacing: -0.025em !important;
        white-space: nowrap !important;
    }}

    /* Navigation Links */
    nav.arm-main-nav {{
        display: flex !important;
        align-items: center !important;
        margin-left: 32px !important;
        margin-right: auto !important;
        background: transparent !important;
        border: none !important;
    }}

    ul.arm-nav-ul {{
        display: flex !important;
        align-items: center !important;
        list-style: none !important;
        margin: 0 !important;
        padding: 0 !important;
        gap: 28px !important;
    }}

    li.arm-nav-li {{
        display: inline-flex !important;
        align-items: center !important;
        height: 56px !important;
    }}

    a.arm-nav-a {{
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "Inter", sans-serif !important;
        font-size: 14px !important;
        font-weight: 500 !important;
        color: #86868B !important;
        text-decoration: none !important;
        white-space: nowrap !important;
        transition: color 150ms ease, transform 150ms ease !important;
    }}

    a.arm-nav-a:hover {{
        color: #F5F5F7 !important;
        transform: translateY(-1px) !important;
    }}

    a.arm-nav-a.active {{
        color: #FFFFFF !important;
        font-weight: 600 !important;
    }}

    /* Right Action Button */
    div.arm-header-right {{
        display: flex !important;
        align-items: center !important;
        flex-shrink: 0 !important;
    }}

    a.arm-auth-btn {{
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "Inter", sans-serif !important;
        font-size: 13.5px !important;
        font-weight: 500 !important;
        color: #F5F5F7 !important;
        text-decoration: none !important;
        background: rgba(255, 255, 255, 0.08) !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        border-radius: 9999px !important;
        padding: 7px 18px !important;
        white-space: nowrap !important;
        transition: transform 150ms ease, background 150ms ease !important;
    }}

    a.arm-auth-btn:hover {{
        background: rgba(255, 255, 255, 0.16) !important;
        border-color: rgba(255, 255, 255, 0.24) !important;
        transform: translateY(-1px) !important;
    }}

    /* Responsive */
    @media (max-width: 900px) {{
        div.arm-header-inner {{ padding: 0 16px !important; }}
        nav.arm-main-nav {{ margin-left: 16px !important; }}
        ul.arm-nav-ul {{ gap: 16px !important; }}
    }}
    </style>

    <header class="arm-site-header">
      <div class="arm-header-inner">
        <!-- Logo -->
        <a href="?page=home" target="_self" class="arm-brand-logo">
          <div class="arm-brand-icon">
            <i class="fa-solid fa-sparkles"></i>
          </div>
          <span class="arm-brand-title">AiResuMind</span>
        </a>

        <!-- Navigation links -->
        <nav class="arm-main-nav">
          <ul class="arm-nav-ul">
            {nav_links_html}
          </ul>
        </nav>
      </div>
    </header>
    """
    render_clean_html(html_str)
