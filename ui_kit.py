"""
AiResuMind Pro v5.0 — UI Kit (Streamlit Shared Component Inventory)
Pure Streamlit component utilities following 01_DESIGN_SYSTEM.md
"""

import streamlit as st

def render_clean_html(html_str):
    """Cleanly render HTML by stripping multiline indentation to prevent Markdown code block bugs."""
    if not html_str:
        return
    lines = [line.strip() for line in html_str.splitlines() if line.strip()]
    cleaned = chr(10).join(lines)
    st.markdown(cleaned, unsafe_allow_html=True)

def get_badge_html(text, variant="default"):
    """Return clean status or metadata badge HTML string."""
    colors = {
        "success": ("rgba(16, 185, 129, 0.12)", "#34D399", "rgba(16, 185, 129, 0.25)"),
        "warning": ("rgba(245, 158, 11, 0.12)", "#FBBF24", "rgba(245, 158, 11, 0.25)"),
        "error": ("rgba(239, 68, 68, 0.12)", "#F87171", "rgba(239, 68, 68, 0.25)"),
        "info": ("rgba(96, 165, 250, 0.12)", "#60A5FA", "rgba(96, 165, 250, 0.25)"),
        "default": ("rgba(255, 255, 255, 0.05)", "#86868B", "rgba(255, 255, 255, 0.1)")
    }
    bg, fg, border = colors.get(variant, colors["default"])
    return f'<span style="background: {bg}; color: {fg}; border: 1px solid {border}; font-size: 11.5px; font-weight: 700; padding: 4px 12px; border-radius: 9999px; display: inline-block;">{text}</span>'

def render_badge(text, variant="default"):
    """Render a clean status or metadata badge."""
    render_clean_html(get_badge_html(text, variant))

def render_score(score_val, max_val=100, label="ATS Score"):
    """Render a high-precision score indicator."""
    render_clean_html(f"""
        <div style="background: #141519; border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 24px; padding: 32px; text-align: center;">
            <div style="font-size: 11px; font-weight: 700; color: #5F6368; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 8px;">{label}</div>
            <div style="font-size: 64px; font-weight: 800; color: #F5F5F7; line-height: 1; letter-spacing: -0.04em;">{score_val}<span style="font-size: 24px; color: #5F6368;"> / {max_val}</span></div>
        </div>
    """)

def render_empty_state(title, description, cta_label, cta_key, on_click_page="resume_analyzer"):
    """
    Render 3-question empty state pattern:
    1. What's missing?
    2. Why does it matter?
    3. What should I do?
    """
    render_clean_html(f"""
        <div style="background: #141519; border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 24px; padding: 48px 32px; text-align: center;">
            <h4 style="font-size: 22px; font-weight: 700; color: #F5F5F7; margin: 0 0 12px 0;">{title}</h4>
            <p style="font-size: 15px; color: #86868B; max-width: 480px; margin: 0 auto 28px auto; line-height: 1.6;">
                {description}
            </p>
        </div>
    """)
    if st.button(cta_label, type="primary", use_container_width=True, key=cta_key):
        st.session_state.page = on_click_page
        if hasattr(st, "query_params"):
            st.query_params["page"] = on_click_page
        st.rerun()

def render_signed_out_state(title="Sign in to view your career workspace", description="The dashboard requires your resume and analysis history to display your career intelligence scores, target match insights, and application progress.", cta_label="Sign In", cta_key="dash_signed_out_cta", on_click_page="signin"):
    """
    Render 01_DESIGN_SYSTEM.md compliant signed-out state card using dark surface tokens.
    Replaces unstyled Streamlit warning boxes.
    """
    render_clean_html(f"""
        <div style="background: #141519; border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 24px; padding: 48px 32px; text-align: center; margin-bottom: 32px;">
            <div style="font-size: 11px; font-weight: 700; color: #60A5FA; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 12px;">AUTHENTICATION REQUIRED</div>
            <h4 style="font-size: 22px; font-weight: 700; color: #F5F5F7; margin: 0 0 12px 0;">{title}</h4>
            <p style="font-size: 15px; color: #86868B; max-width: 520px; margin: 0 auto 28px auto; line-height: 1.6;">
                {description}
            </p>
        </div>
    """)
    if st.button(cta_label, type="primary", use_container_width=True, key=cta_key):
        st.session_state.page = on_click_page
        if hasattr(st, "query_params"):
            st.query_params["page"] = on_click_page
        st.rerun()

def render_ai_insight(observation, why_it_matters, recommendation, action_label, action_key, action_page="resume_builder"):
    """
    Render signature v5.0 AI response pattern:
    OBSERVATION -> WHY IT MATTERS -> RECOMMENDATION -> ACTION
    """
    render_clean_html(f"""
        <div style="background: #141519; border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 24px; padding: 28px; margin-bottom: 24px;">
            <div style="font-size: 11px; font-weight: 700; color: #3B82F6; text-transform: uppercase; letter-spacing: 0.12em; margin-bottom: 12px;">
                OBSERVATION
            </div>
            <div style="font-size: 15px; font-weight: 600; color: #F5F5F7; margin-bottom: 20px; line-height: 1.5;">
                {observation}
            </div>

            <div style="font-size: 11px; font-weight: 700; color: #5F6368; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 6px;">
                WHY IT MATTERS
            </div>
            <div style="font-size: 14px; color: #86868B; margin-bottom: 20px; line-height: 1.6;">
                {why_it_matters}
            </div>

            <div style="font-size: 11px; font-weight: 700; color: #5F6368; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 6px;">
                RECOMMENDATION
            </div>
            <div style="font-size: 14px; font-weight: 600; color: #60A5FA; margin-bottom: 24px; line-height: 1.5;">
                {recommendation}
            </div>
        </div>
    """)
    if st.button(action_label, type="primary", use_container_width=True, key=action_key):
        st.session_state.page = action_page
        if hasattr(st, "query_params"):
            st.query_params["page"] = action_page
        st.rerun()

def render_metric_card(label, value_str, delta_text=None, progress_pct=100):
    """
    Render executive metric card with big value, optional delta indicator, and progress bar underneath.
    Matches the card design in the reference executive dashboard image.
    """
    delta_html = ""
    if delta_text:
        delta_html = f'<span style="font-size: 13px; font-weight: 600; color: #34D399; margin-left: 12px; display: inline-flex; align-items: center;">{delta_text}</span>'
        
    progress_bar_html = f"""
        <div style="width: 100%; height: 4px; background: rgba(255, 255, 255, 0.08); border-radius: 9999px; overflow: hidden; margin-top: 24px;">
            <div style="width: {min(100, max(0, progress_pct))}%; height: 100%; background: linear-gradient(90deg, #3B82F6 0%, #34D399 100%); border-radius: 9999px;"></div>
        </div>
    """

    render_clean_html(f"""
        <div style="background: #141519; border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 20px; padding: 28px 28px 24px 28px; margin-bottom: 16px;">
            <div style="font-size: 11px; font-weight: 700; color: #86868B; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 16px;">{label}</div>
            <div style="display: flex; align-items: baseline; justify-content: flex-start;">
                <span style="font-size: 42px; font-weight: 800; color: #F5F5F7; letter-spacing: -0.03em; line-height: 1;">{value_str}</span>
                {delta_html}
            </div>
            {progress_bar_html}
        </div>
    """)
