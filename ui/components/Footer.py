import streamlit as st
import textwrap

def render_clean_html(html_str):
    """Cleanly render HTML by stripping multiline indentation to prevent Markdown code block bugs."""
    if not html_str:
        return
    lines = [line.strip() for line in html_str.splitlines() if line.strip()]
    cleaned = chr(10).join(lines)
    st.markdown(cleaned, unsafe_allow_html=True)

def render_footer():
    """Render Minimal Apple-style footer."""
    render_clean_html("""
        <div style="border-top: 1px solid rgba(255, 255, 255, 0.08); padding-top: 56px; padding-bottom: 56px; margin-top: 96px; text-align: center;">
            <div style="font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', sans-serif; font-size: 20px; font-weight: 700; color: #F5F5F7; letter-spacing: -0.02em; margin-bottom: 8px;">
                AiResuMind
            </div>
            <div style="font-size: 14px; color: #86868B; margin-bottom: 24px; font-weight: 400;">
                AI Career Intelligence Platform
            </div>
            <div style="font-size: 12.5px; color: #6E6E73;">
                &copy; 2026 AiResuMind. All rights reserved. Precision candidate engineering.
            </div>
        </div>
    """)
