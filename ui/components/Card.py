import textwrap

def render_clean_html(html_str):
    """Cleanly render HTML by stripping multiline indentation to prevent Markdown code block bugs."""
    if not html_str:
        return
    lines = [line.strip() for line in html_str.splitlines() if line.strip()]
    cleaned = chr(10).join(lines)
    st.markdown(cleaned, unsafe_allow_html=True)

import streamlit as st

def render_card(title, description, icon_class=None):
    """Render single reusable card component variant"""
    icon_html = f'<div class="editorial-card-icon"><i class="{icon_class}"></i></div>' if icon_class else ''
    render_clean_html(f"""
        <div class="editorial-card">
            <div class="editorial-card-header">
                {icon_html}
                <h3 class="editorial-card-title">{title}</h3>
            </div>
            <p class="editorial-card-desc">{description}</p>
        </div>
    """)
