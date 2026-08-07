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
    Exact implementation of user's React/Tailwind Navbar component in Streamlit.
    - Zero boxed buttons on nav links.
    - Pure flat text navigation links: Dashboard, Resume Analyzer, Resume Builder, Cold Mail, Job Search.
    - Right side: Single gradient pill button for "Sign In" / "Profile".
    """

    # Sync URL query parameters with session state for URL-based navigation
    if hasattr(st, "query_params"):
        qp = st.query_params
        if "page" in qp:
            param_page = qp["page"]
            if param_page and param_page != st.session_state.get("page"):
                st.session_state.page = param_page

    current_page = active_page or st.session_state.get("page", "home")

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
    /* Reset Streamlit default container padding */
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

    /* ── Header: w-full bg-[#0a0a0f] border-b border-white/10 ── */
    header.arm-site-header {{
        position: sticky !important;
        top: 0 !important;
        left: 0 !important;
        right: 0 !important;
        z-index: 999999 !important;
        width: 100% !important;
        height: 56px !important;
        background-color: rgba(10,13,18,.92) !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1) !important;
        margin-bottom: 0 !important;
    }}

    /* ── Container: mx-auto max-w-7xl px-6 h-14 flex items-center justify-between ── */
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

    /* ── Logo: flex items-center gap-2 shrink-0 ── */
    a.arm-brand-logo {{
        display: flex !important;
        align-items: center !important;
        gap: 8px !important;
        text-decoration: none !important;
        flex-shrink: 0 !important;
        cursor: pointer !important;
        background: transparent !important;
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
        padding: 0 !important;
        margin: 0 !important;
    }}
    a.arm-brand-logo:hover {{
        opacity: 0.9 !important;
    }}

    /* Logo Icon: w-6 h-6 rounded-md bg-gradient-to-br from-blue-500 to-purple-600 */
    div.arm-brand-icon {{
        width: 24px !important;
        height: 24px !important;
        border-radius: 6px !important;
        background: linear-gradient(135deg, #ff6b4a 0%, #e7b85a 100%) !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        font-size: 11px !important;
        color: #ffffff !important;
    }}

    /* Logo Text: text-white font-semibold text-[15px] tracking-tight */
    span.arm-brand-title {{
        font-family: 'Fraunces', Georgia, serif !important;
        font-size: 15px !important;
        font-weight: 600 !important;
        color: #ffffff !important;
        letter-spacing: -0.025em !important;
        white-space: nowrap !important;
    }}

    /* ── Nav Links: flex items-center gap-7 ml-10 mr-auto ── */
    nav.arm-main-nav {{
        display: flex !important;
        align-items: center !important;
        margin-left: 28px !important;
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
        gap: 22px !important;
        background: transparent !important;
        border: none !important;
    }}

    li.arm-nav-li {{
        display: inline-flex !important;
        align-items: center !important;
        height: 56px !important;
        margin: 0 !important;
        padding: 0 !important;
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }}

    /* Plain Text Links: ABSOLUTE OVERRIDE — NO BORDERS, NO BOXES, NO BACKGROUNDS */
    a.arm-nav-a {{
        font-family: -apple-system, BlinkMacSystemFont, 'Inter', sans-serif !important;
        font-size: 14px !important;
        font-weight: 500 !important;
        color: #9ca3af !important; /* text-gray-400 */
        text-decoration: none !important;
        background: transparent !important;
        background-color: transparent !important;
        border: 0 !important;
        border-style: none !important;
        border-radius: 0 !important;
        box-shadow: none !important;
        outline: none !important;
        padding: 0 !important;
        margin: 0 !important;
        height: auto !important;
        width: auto !important;
        white-space: nowrap !important;
        transition: color 150ms ease, transform 150ms ease !important;
    }}

    a.arm-nav-a:hover {{
        color: #ffffff !important; /* hover:text-white */
        background: transparent !important;
        background-color: transparent !important;
        border: 0 !important;
        box-shadow: none !important;
        transform: translateY(-1px) !important;
    }}

    a.arm-nav-a.active {{
        color: #ffffff !important;
        font-weight: 600 !important;
        background: transparent !important;
        border: 0 !important;
        box-shadow: none !important;
    }}

    /* ── Right side: Sign In only ── */
    div.arm-header-right {{
        display: flex !important;
        align-items: center !important;
        flex-shrink: 0 !important;
        background: transparent !important;
        border: none !important;
    }}

    /* Sign In: text-[14px] font-medium text-white bg-gradient-to-r from-blue-500 to-purple-600 hover:opacity-90 transition-opacity duration-150 rounded-full px-4 py-[7px] */
    a.arm-auth-btn {{
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        font-family: -apple-system, BlinkMacSystemFont, 'Inter', sans-serif !important;
        font-size: 14px !important;
        font-weight: 500 !important;
        color: #ffffff !important;
        text-decoration: none !important;
        background: #ff6b4a !important;
        border-radius: 9999px !important;
        padding: 7px 16px !important;
        white-space: nowrap !important;
        border: none !important;
        box-shadow: 0 6px 18px rgba(255, 107, 74, 0.22) !important;
        transition: transform 150ms ease, background 150ms ease !important;
    }}

    a.arm-auth-btn:hover {{
        background: #ff8066 !important;
        transform: translateY(-1px) !important;
    }}

    /* Responsive */
    @media (max-width: 1024px) {{
        div.arm-header-inner {{
            padding: 0 16px !important;
        }}
        nav.arm-main-nav {{
            margin-left: 20px !important;
        }}
        ul.arm-nav-ul {{
            gap: 18px !important;
        }}
    }}

    @media (max-width: 768px) {{
        header.arm-site-header {{ height: auto !important; }}
        div.arm-header-inner {{ min-height: 56px !important; height: auto !important; gap: 14px !important; }}
        nav.arm-main-nav {{ order: 3 !important; width: 100% !important; margin: 0 !important; overflow-x: auto !important; }}
        ul.arm-nav-ul {{
            overflow-x: auto !important;
            scrollbar-width: none !important;
            gap: 16px !important;
            padding-bottom: 10px !important;
        }}
    }}
    </style>

    <header class="arm-site-header">
      <div class="arm-header-inner">
        <!-- Logo -->
        <a href="?page=home" target="_self" class="arm-brand-logo">
          <div class="arm-brand-icon">
            <i class="fa-solid fa-sparkles" style="font-size:11px;"></i>
          </div>
          <span class="arm-brand-title">AiResuMind</span>
        </a>

        <!-- Nav links: Dashboard, Resume Analyzer, Resume Builder, Cold Mail, Job Search -->
        <nav class="arm-main-nav">
          <ul class="arm-nav-ul">
            {nav_links_html}
          </ul>
        </nav>

        <!-- Right side: Sign In only -->
        <div class="arm-header-right">
          <a href="?page={auth_target}" target="_self" class="arm-auth-btn">{auth_label}</a>
        </div>
      </div>
    </header>
    """
    render_clean_html(html_str)
