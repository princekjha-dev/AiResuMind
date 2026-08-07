import streamlit as st

def render_page_header(title, subtitle=None):
    """Render unified editorial page header"""
    subtitle_html = f'<p style="color: var(--color-ink-muted); margin-top: 0.4rem; font-size: 16px;">{subtitle}</p>' if subtitle else ''
    st.markdown(
        f'''
        <div style="padding: 1rem 0; margin-bottom: 1.5rem; border-bottom: 1px solid var(--color-line);">
            <div style="display: inline-flex; align-items: center; gap: 0.4rem; font-size: 13px; font-weight: 600; color: var(--color-accent); letter-spacing: 0.06em; text-transform: uppercase; margin-bottom: 0.4rem;">
                <span style="width: 6px; height: 6px; border-radius: 50%; background: var(--color-accent);"></span>
                AiResuMind Platform
            </div>
            <h1 style="margin: 0; font-family: \'Fraunces\', serif !important; font-size: 42px; font-weight: 700; color: var(--color-ink);">{title}</h1>
            {subtitle_html}
        </div>
        ''',
        unsafe_allow_html=True
    )
