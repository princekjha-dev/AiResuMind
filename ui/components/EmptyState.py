import textwrap

def render_clean_html(html_str):
    """Cleanly render HTML by stripping multiline indentation to prevent Markdown code block bugs."""
    if not html_str:
        return
    lines = [line.strip() for line in html_str.splitlines() if line.strip()]
    cleaned = chr(10).join(lines)
    st.markdown(cleaned, unsafe_allow_html=True)

import streamlit as st

def render_empty_state(title="No data found", description="Upload or submit content to view details here."):
    """Render empty state card variant"""
    render_clean_html(f"""
        <div class="empty-card">
            <div class="empty-title">{title}</div>
            <div class="empty-desc">{description}</div>
        </div>
    """)
