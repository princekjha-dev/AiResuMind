import streamlit as st

def render_clean_html(html_str):
    """Cleanly render HTML by stripping multiline indentation to prevent Markdown code block bugs."""
    if not html_str:
        return
    lines = [line.strip() for line in html_str.splitlines() if line.strip()]
    cleaned = chr(10).join(lines)
    st.markdown(cleaned, unsafe_allow_html=True)

def render_auth_page():
    """Renders Apple & Linear inspired authentication experience for AiResuMind."""
    
    # 1. AUTH HERO SECTION
    render_clean_html("""
        <div style="max-width: 1200px; margin: 0 auto; padding: 48px 24px 32px 24px; text-align: center;">
            <div style="font-size: 11.5px; font-weight: 700; color: #60A5FA; letter-spacing: 0.12em; text-transform: uppercase; margin-bottom: 16px;">
                AI CAREER INTELLIGENCE
            </div>
            
            <h1 style="font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', sans-serif !important; font-size: 60px !important; font-weight: 800 !important; color: #F5F5F7 !important; letter-spacing: -0.04em !important; max-width: 600px; margin: 0 auto 16px auto; line-height: 1.08;">
                Welcome back.
            </h1>
            
            <p style="font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', sans-serif; font-size: 17px; color: #86868B; max-width: 500px; margin: 0 auto; line-height: 1.5; font-weight: 400;">
                Continue building a stronger career story.
            </p>
        </div>
    """)

    # 2. AUTHENTICATION CONTAINER (MAX-WIDTH 440PX)
    render_clean_html("""
        <style>
        .auth-card-container {
            max-width: 440px;
            margin: 0 auto 64px auto;
            padding: 0 16px;
        }
        
        [data-testid="stTabs"] {
            max-width: 440px !important;
            margin: 0 auto 20px auto !important;
        }
        
        [data-testid="stTabs"] [data-baseweb="tab-list"] {
            display: flex !important;
            justify-content: center !important;
            gap: 24px !important;
            border-bottom: 1px solid rgba(255, 255, 255, 0.08) !important;
            background: transparent !important;
        }

        [data-testid="stTabs"] [data-baseweb="tab"] {
            font-size: 14.5px !important;
            font-weight: 600 !important;
            color: #86868B !important;
            padding-bottom: 12px !important;
            background: transparent !important;
            border: none !important;
        }

        [data-testid="stTabs"] [aria-selected="true"] {
            color: #F5F5F7 !important;
            border-bottom: 2px solid #3B82F6 !important;
        }

        [data-testid="stForm"] {
            background: rgba(255, 255, 255, 0.035) !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            border-radius: 20px !important;
            padding: 32px 28px 24px 28px !important;
            box-shadow: 0 40px 100px rgba(0, 0, 0, 0.6) !important;
            max-width: 440px !important;
            margin: 0 auto !important;
        }
        
        .social-auth-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 12px;
            margin-top: 24px;
            margin-bottom: 24px;
        }

        .social-btn {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 12px;
            height: 44px;
            color: #F5F5F7;
            font-size: 13.5px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s ease;
        }

        .social-btn:hover {
            background: rgba(255, 255, 255, 0.08);
            border-color: rgba(255, 255, 255, 0.16);
            transform: translateY(-1px);
        }

        .auth-divider-line {
            display: flex;
            align-items: center;
            margin: 24px 0 16px 0;
            color: #6E6E73;
            font-size: 11px;
            font-weight: 700;
            letter-spacing: 0.08em;
            text-transform: uppercase;
        }

        .auth-divider-line::before, .auth-divider-line::after {
            content: "";
            flex: 1;
            border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        }

        .auth-divider-line span {
            padding: 0 12px;
        }
        </style>
    """)

    auth_tab1, auth_tab2 = st.tabs(["Sign In", "Create Account"])

    with auth_tab1:
        with st.form("signin_form"):
            email_val = st.text_input("Email address", placeholder="you@example.com", key="auth_signin_email")
            pass_val = st.text_input("Password", type="password", placeholder="••••••••", key="auth_signin_pass")
            
            render_clean_html("""
                <div style="display: flex; justify-content: space-between; align-items: center; margin-top: -10px; margin-bottom: 16px; font-size: 12.5px;">
                    <a href="#" onclick="return false;" style="color: #60A5FA; text-decoration: none; font-weight: 500;">Forgot password?</a>
                </div>
            """)

            remember_me = st.checkbox("Remember me", value=True)
            
            render_clean_html("""<div style="height: 12px;"></div>""")
            submit_signin = st.form_submit_button("Sign In", type="primary", use_container_width=True)

        if submit_signin:
            em_clean = email_val.strip().lower()
            if em_clean and pass_val.strip():
                st.session_state.user_authenticated = True
                st.session_state.user_email = email_val.strip()
                if em_clean == "prince@airesumind.com":
                    st.session_state.candidate_name = "Prince Kumar Jha"
                else:
                    st.session_state.candidate_name = email_val.strip().split("@")[0].replace('.', ' ').replace('_', ' ').title()
                st.session_state.page = "dashboard"
                st.success("Authentication successful! Redirecting to Dashboard...")
                st.rerun()
            else:
                st.error("Please enter your email address and password.")

        # SOCIAL AUTHENTICATION
        render_clean_html("""
            <div style="max-width: 440px; margin: 0 auto;">
                <div class="auth-divider-line">
                    <span>OR CONTINUE WITH</span>
                </div>
                <div class="social-auth-grid">
                    <div class="social-btn">
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none"><path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4"/><path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"/><path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z" fill="#FBBC05"/><path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z" fill="#EA4335"/></svg>
                        Google
                    </div>
                    <div class="social-btn">
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="#0A66C2"><path d="M19 3a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h14m-.5 15.5v-5.3a3.26 3.26 0 0 0-3.26-3.26c-.85 0-1.84.52-2.28 1.3v-1.11h-2.79v8.37h2.79v-4.93c0-.77.62-1.4 1.39-1.4a1.4 1.4 0 0 1 1.4 1.4v4.93h2.75M6.88 8.56a1.68 1.68 0 0 0 1.68-1.68c0-.93-.75-1.69-1.68-1.69a1.69 1.69 0 0 0-1.69 1.69c0 .93.76 1.68 1.69 1.68m1.39 9.94v-8.37H5.5v8.37h2.77z"/></svg>
                        LinkedIn
                    </div>
                </div>
            </div>
        """)

        # QUICK DEMO LOGIN TRIGGER
        if st.button("Explore Demo Account", key="btn_quick_demo_login", type="secondary", use_container_width=True):
            st.session_state.candidate_name = "Prince Kumar Jha"
            st.session_state.candidate_role = "Software Engineer"
            st.session_state.user_authenticated = True
            st.session_state.user_email = "pkjha2028@gmail.com"
            st.session_state.page = "dashboard"
            st.success("Logged in with candidate demo profile...")
            st.rerun()

        render_clean_html("""
            <div style="text-align: center; margin-top: 24px; font-size: 13.5px; color: #86868B;">
                New to AiResuMind? <span style="color: #60A5FA; cursor: pointer; font-weight: 500;">Create account</span>
            </div>
        """)

    with auth_tab2:
        with st.form("signup_form"):
            new_name = st.text_input("Full name", placeholder="Prince Kumar Jha", key="auth_signup_name")
            new_email = st.text_input("Email address", placeholder="you@example.com", key="auth_signup_email")
            new_pass = st.text_input("Password", type="password", placeholder="••••••••", key="auth_signup_pass")
            confirm_pass = st.text_input("Confirm password", type="password", placeholder="••••••••", key="auth_signup_confirm")
            
            render_clean_html("""<div style="height: 12px;"></div>""")
            submit_signup = st.form_submit_button("Create Account", type="primary", use_container_width=True)

        if submit_signup:
            if new_email.strip() and new_pass.strip():
                if new_pass != confirm_pass:
                    st.error("Passwords do not match.")
                else:
                    st.session_state.candidate_name = new_name if new_name.strip() else "Prince Kumar Jha"
                    st.session_state.user_email = new_email
                    st.session_state.user_authenticated = True
                    st.session_state.page = "dashboard"
                    st.success("Account created successfully! Welcome to AiResuMind.")
                    st.rerun()
            else:
                st.error("Please fill out all required fields.")
