import streamlit as st

def render_clean_html(html_str):
    """Cleanly render HTML by stripping multiline indentation to prevent Markdown code block bugs."""
    if not html_str:
        return
    lines = [line.strip() for line in html_str.splitlines() if line.strip()]
    cleaned = chr(10).join(lines)
    st.markdown(cleaned, unsafe_allow_html=True)

def render_auth_page():
    """Render Executive Dark Glassmorphic Sign In / Sign Up Page for AiResuMind Pro v4.0."""
    
    # Global CSS for Auth Page
    render_clean_html("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@600;700;800&family=Inter:wght@400;500;600;700&display=swap');

        .auth-wrapper {
            max-width: 520px;
            margin: 42px auto 24px auto;
            padding: 0 16px;
        }

        /* Streamlit widgets sit outside the HTML heading block.  Constrain each
           generated section so the authentication flow remains one focused panel. */
        [data-testid="stTabs"], [data-testid="stForm"],
        div[data-testid="stElementContainer"]:has(.auth-divider),
        div[data-testid="stElementContainer"]:has(.social-btn) {
            max-width: 520px !important;
            margin-left: auto !important;
            margin-right: auto !important;
        }
        [data-testid="stTabs"] { margin-bottom: 16px !important; }
        [data-testid="stTabs"] [data-baseweb="tab-list"] { gap: 20px !important; border-bottom-color: rgba(255,255,255,.1) !important; }
        [data-testid="stForm"] {
            background: rgba(21,28,38,.78) !important;
            border: 1px solid rgba(255,255,255,.1) !important;
            border-radius: 18px !important;
            padding: 22px 20px 14px !important;
            box-shadow: 0 18px 42px rgba(0,0,0,.22) !important;
        }
        [data-testid="stTextInput"] input {
            background: rgba(255,255,255,.055) !important;
            border: 1px solid rgba(255,255,255,.1) !important;
            border-radius: 10px !important;
            color: #f6f1e8 !important;
        }
        [data-testid="stTextInput"] input:focus { border-color: #ff6b4a !important; box-shadow: 0 0 0 3px rgba(255,107,74,.12) !important; }
        @media (max-width: 620px) {
            .auth-wrapper { margin-top: 28px; padding: 0 4px; }
            [data-testid="stForm"] { border-radius: 14px !important; padding: 18px 14px 10px !important; }
        }

        .auth-glass-card {
            background: rgba(18, 22, 31, 0.85) !important;
            backdrop-filter: blur(25px) !important;
            -webkit-backdrop-filter: blur(25px) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 24px !important;
            padding: 36px 32px !important;
            box-shadow: 0 20px 50px rgba(0, 0, 0, 0.5), 0 0 30px rgba(108, 92, 231, 0.12) !important;
        }

        .auth-title {
            font-family: 'Space Grotesk', -apple-system, sans-serif !important;
            font-size: 26px !important;
            font-weight: 800 !important;
            color: #FFFFFF !important;
            letter-spacing: -0.03em !important;
            margin: 0 0 6px 0;
            text-align: center;
        }

        .auth-subtitle {
            font-family: 'Inter', sans-serif !important;
            font-size: 13.5px !important;
            color: #8A8F9E !important;
            text-align: center;
            margin-bottom: 28px;
            line-height: 1.5;
        }

        .social-btn {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 12px;
            padding: 10px 16px;
            color: #FFFFFF;
            font-size: 13.5px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s ease;
            width: 100%;
            margin-bottom: 10px;
        }

        .social-btn:hover {
            background: rgba(255, 255, 255, 0.08);
            border-color: rgba(255, 255, 255, 0.18);
            transform: translateY(-1px);
        }

        .auth-divider {
            display: flex;
            align-items: center;
            margin: 24px 0;
            color: #8A8F9E;
            font-size: 12px;
        }

        .auth-divider::before, .auth-divider::after {
            content: "";
            flex: 1;
            border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        }

        .auth-divider span {
            padding: 0 12px;
        }
        .demo-credential-card {
            display:flex; align-items:center; gap:12px; padding:13px 14px;
            margin:16px 0 12px; border:1px solid rgba(97,215,178,.2);
            background:rgba(97,215,178,.055); border-radius:12px;
        }
        .demo-credential-icon {
            width:30px; height:30px; flex:0 0 30px; display:grid; place-items:center;
            border-radius:9px; background:rgba(97,215,178,.15); color:#61d7b2;
            font:700 12px 'DM Mono', monospace;
        }
        .demo-credential-copy { color:#b6becb; font-size:11.5px; line-height:1.55; }
        .demo-credential-copy strong { display:block; color:#f6f1e8; font-size:12px; }
        .demo-credential-copy code { color:#61d7b2; font-family:'DM Mono',monospace; font-size:10.5px; }
        </style>
    """)

    render_clean_html("""
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
        <div class="auth-wrapper">
            <div style="text-align: center; margin-bottom: 8px;">
                <div style="display: inline-flex; align-items: center; justify-content: center; width: 50px; height: 50px; background: linear-gradient(135deg, #ff6b4a 0%, #e7b85a 100%); border-radius: 14px; font-family: 'Space Grotesk', sans-serif; font-weight: 900; font-size: 22px; color: #FFFFFF; box-shadow: 0 0 25px rgba(255,107,74,.28); margin-bottom: 12px;">
                    <i class="fa-solid fa-circle-user"></i>
                </div>
                <h1 class="auth-title">Welcome back</h1>
                <p class="auth-subtitle">Continue building a stronger career story.</p>
            </div>
        </div>
    """)

    auth_tab1, auth_tab2 = st.tabs(["Sign In", "Create Account"])

    with auth_tab1:
        with st.form("signin_form"):
            email_val = st.text_input("Work Email Address", placeholder="name@company.com", key="auth_signin_email")
            pass_val = st.text_input("Password", type="password", placeholder="••••••••", key="auth_signin_pass")
            remember_me = st.checkbox("Remember this device for 30 days", value=True)
            
            submit_signin = st.form_submit_button("Sign In to Dashboard", type="primary", use_container_width=True)

        if submit_signin:
            if email_val.strip() and pass_val.strip():
                st.session_state.user_authenticated = True
                st.session_state.user_email = email_val
                st.session_state.page = "dashboard"
                st.success("Authentication Successful! Loading Executive Dashboard...")
                st.rerun()
            else:
                st.error("Please enter your email address and password.")

        render_clean_html("""
            <div class="auth-divider">
                <span>OR CONTINUE WITH</span>
            </div>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 16px;">
                <div class="social-btn">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none"><path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4"/><path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"/><path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z" fill="#FBBC05"/><path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z" fill="#EA4335"/></svg>
                    Google
                </div>
                <div class="social-btn">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="#0A66C2"><path d="M19 3a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h14m-.5 15.5v-5.3a3.26 3.26 0 0 0-3.26-3.26c-.85 0-1.84.52-2.28 1.3v-1.11h-2.79v8.37h2.79v-4.93c0-.77.62-1.4 1.39-1.4a1.4 1.4 0 0 1 1.4 1.4v4.93h2.75M6.88 8.56a1.68 1.68 0 0 0 1.68-1.68c0-.93-.75-1.69-1.68-1.69a1.69 1.69 0 0 0-1.69 1.69c0 .93.76 1.68 1.69 1.68m1.39 9.94v-8.37H5.5v8.37h2.77z"/></svg>
                    LinkedIn
                </div>
            </div>
        """)

        render_clean_html("""
            <div class="demo-credential-card" role="note" aria-label="Demo account credentials">
                <div class="demo-credential-icon">DEMO</div>
                <div class="demo-credential-copy">
                    <strong>Candidate preview account</strong>
                    Use <code>demo@airesumind.com</code> · <code>demo1234</code> to explore the dashboard.
                </div>
            </div>
        """)

        # One-Click Executive Demo Login
        if st.button("🚀 Quick Demo Login as Executive Candidate", key="btn_quick_demo_login", type="secondary", use_container_width=True):
            st.session_state.candidate_name = "Executive Candidate"
            st.session_state.candidate_role = "Product & Tech Leader"
            st.session_state.user_authenticated = True
            st.session_state.page = "dashboard"
            st.success("Logging in with Executive Demo Profile...")
            st.rerun()

    with auth_tab2:
        with st.form("signup_form"):
            new_name = st.text_input("Full Name", placeholder="Alex Sharma", key="auth_signup_name")
            new_email = st.text_input("Work Email", placeholder="alex@company.com", key="auth_signup_email")
            new_role = st.text_input("Target Career Role", placeholder="Vice President of Engineering", key="auth_signup_role")
            new_pass = st.text_input("Create Password", type="password", placeholder="••••••••", key="auth_signup_pass")
            
            submit_signup = st.form_submit_button("Create Free Candidate Account", type="primary", use_container_width=True)

        if submit_signup:
            if new_email.strip() and new_pass.strip():
                st.session_state.candidate_name = new_name if new_name.strip() else "Executive Candidate"
                st.session_state.candidate_role = new_role if new_role.strip() else "Product & Tech Leader"
                st.session_state.user_authenticated = True
                st.session_state.page = "dashboard"
                st.success("Account Created Successfully! Welcome to AiResuMind Pro v4.0.")
                st.rerun()
            else:
                st.error("Please fill out all required fields to create your account.")
