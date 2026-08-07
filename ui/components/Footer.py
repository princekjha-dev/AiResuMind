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
    """Render Apple minimalist dark monochrome footer with zero emojis."""
    render_clean_html("""
        <div style="border-top: 1px solid rgba(255, 255, 255, 0.08); padding-top: 56px; padding-bottom: 56px; margin-top: 96px; text-align: center;">
            <div style="font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', sans-serif; font-size: 22px; font-weight: 800; color: #F5F5F7; letter-spacing: -0.02em; margin-bottom: 10px;">
                AiResuMind Pro v4.0
            </div>
            <div style="font-size: 14px; color: #86868B; margin-bottom: 24px; font-weight: 400;">
                Next-Generation AI Candidate Intelligence & Executive Resume Platform
            </div>
            <div style="display: flex; justify-content: center; align-items: center; gap: 24px; font-size: 13px; font-weight: 500; color: #86868B; margin-bottom: 28px;">
                <span style="display: inline-flex; align-items: center; gap: 8px; background: rgba(255, 255, 255, 0.06); color: #F5F5F7; border: 1px solid rgba(255, 255, 255, 0.12); padding: 5px 16px; border-radius: 9999px; font-size: 12px;">
                    <span style="width: 6px; height: 6px; border-radius: 50%; background: #30D158;"></span> All v4.0 AI Candidate Engines Operational
                </span>
            </div>
            <div style="font-size: 12.5px; color: #6E6E73;">
                Copyright 2026 AiResuMind Inc. All rights reserved. Built for candidates aiming for executive tech roles.
            </div>
        </div>
    """)
