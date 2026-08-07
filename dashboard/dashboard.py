import streamlit as st
import textwrap
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from config.database import get_database_connection
import io
import uuid

def render_clean_html(html_str):
    """Cleanly render HTML by stripping multiline indentation to prevent Markdown code block bugs."""
    if not html_str:
        return
    lines = [line.strip() for line in html_str.splitlines() if line.strip()]
    cleaned = chr(10).join(lines)
    st.markdown(cleaned, unsafe_allow_html=True)


class DashboardManager:
    def __init__(self):
        self.conn = get_database_connection()
        self.colors = {
            'bg_base': '#0A0D14',
            'panel_glass': '#12161F',
            'indigo': '#6C5CE7',
            'teal': '#22D3EE',
            'amber': '#F5A623',
            'text_white': '#FFFFFF',
            'text_subtle': '#8A8F9E',
            'border_glass': 'rgba(255, 255, 255, 0.08)'
        }

    def inject_dashboard_styles(self):
        """Inject custom CSS for dark glassmorphism, Space Grotesk font, and micro-interactions."""
        render_clean_html("""
            <style>
            @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;700;800&family=Inter:wght@400;500;600;700&display=swap');

            .main .block-container,
            [data-testid="stAppViewBlockContainer"] {
                background: #0A0D14 !important;
                color: #FFFFFF !important;
                font-family: 'Inter', -apple-system, sans-serif !important;
                max-width: 1280px !important;
                padding: 28px 28px 72px !important;
            }

            /* Keep the dashboard a focused command centre at desktop widths. */
            [data-testid="stExpander"] {
                border-color: rgba(255,255,255,.1) !important;
                border-radius: 12px !important;
                margin-bottom: 10px !important;
            }
            [data-testid="stExpander"] summary { font-size: 13px !important; }
            @media (max-width: 760px) {
                .main .block-container, [data-testid="stAppViewBlockContainer"] { padding: 22px 16px 48px !important; }
                [data-testid="stHorizontalBlock"] { gap: 12px !important; }
            }

            /* Custom Typography Classes */
            .space-font {
                font-family: 'Space Grotesk', -apple-system, sans-serif !important;
            }

            /* Glassmorphic Panel Base */
            .glass-card {
                background: rgba(18, 22, 31, 0.75) !important;
                backdrop-filter: blur(20px) !important;
                -webkit-backdrop-filter: blur(20px) !important;
                border: 1px solid rgba(255, 255, 255, 0.08) !important;
                border-radius: 20px !important;
                padding: 24px !important;
                transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1) !important;
                position: relative;
                overflow: hidden;
            }

            .glass-card:hover {
                transform: translateY(-3px) !important;
                border-color: rgba(255, 255, 255, 0.16) !important;
                box-shadow: 0 12px 30px rgba(0, 0, 0, 0.4), 0 0 20px rgba(108, 92, 231, 0.15) !important;
            }

            /* The top metrics intentionally use three distinct readings, not a repeated card. */
            .metric-featured { background:linear-gradient(145deg, rgba(245,166,35,.18), rgba(18,22,31,.9) 60%) !important; border-radius:28px 8px 28px 8px !important; }
            .metric-velocity { background:rgba(108,92,231,.08) !important; border-left:3px solid #6C5CE7 !important; border-radius:8px 20px 20px 8px !important; }
            .metric-skill { background:radial-gradient(circle at 88% 15%, rgba(34,211,238,.18), transparent 32%), rgba(18,22,31,.8) !important; border-radius:50% 20px 20px 20px !important; }

            /* Glow Highlights */
            .glow-amber {
                box-shadow: 0 0 25px rgba(245, 166, 35, 0.18) !important;
                border: 1px solid rgba(245, 166, 35, 0.35) !important;
            }

            .glow-indigo {
                box-shadow: 0 0 25px rgba(108, 92, 231, 0.18) !important;
                border: 1px solid rgba(108, 92, 231, 0.3) !important;
            }

            .glow-teal {
                box-shadow: 0 0 25px rgba(34, 211, 238, 0.18) !important;
                border: 1px solid rgba(34, 211, 238, 0.3) !important;
            }

            /* Metric Chip Badge */
            .delta-chip-teal {
                display: inline-flex;
                align-items: center;
                gap: 4px;
                background: rgba(34, 211, 238, 0.12);
                color: #22D3EE;
                border: 1px solid rgba(34, 211, 238, 0.3);
                padding: 3px 10px;
                border-radius: 9999px;
                font-size: 12px;
                font-weight: 700;
            }

            .delta-chip-amber {
                display: inline-flex;
                align-items: center;
                gap: 4px;
                background: rgba(245, 166, 35, 0.12);
                color: #F5A623;
                border: 1px solid rgba(245, 166, 35, 0.3);
                padding: 3px 10px;
                border-radius: 9999px;
                font-size: 12px;
                font-weight: 700;
            }

            /* Pulsing Status Dot */
            .status-dot-live {
                width: 8px;
                height: 8px;
                background-color: #22D3EE;
                border-radius: 50%;
                display: inline-block;
                box-shadow: 0 0 10px #22D3EE;
                animation: pulse-dot 1.8s infinite ease-in-out;
            }

            @keyframes pulse-dot {
                0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(34, 211, 238, 0.7); }
                70% { transform: scale(1.1); box-shadow: 0 0 0 8px rgba(34, 211, 238, 0); }
                100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(34, 211, 238, 0); }
            }

            @media (prefers-reduced-motion: reduce) {
                .glass-card, .status-dot-live {
                    animation: none !important;
                    transition: none !important;
                    transform: none !important;
                }
            }
            </style>
        """)

    def create_trajectory_chart(self):
        """Create 5-Year Executive Trajectory Chart in Dark Glass style"""
        years = ['2024', '2025', '2026', '2027', '2028', '2029']
        y_positions = [1, 2, 3, 4, 4.8, 5]

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=years,
            y=y_positions,
            mode='lines+markers',
            line=dict(color='#6C5CE7', width=3.5, shape='spline'),
            marker=dict(size=9, color='#22D3EE', symbol='circle', line=dict(color='#FFFFFF', width=1.5)),
            name='Trajectory'
        ))

        fig.add_annotation(
            x='2024', y=1, text="Current Role", showarrow=True, arrowhead=2,
            arrowcolor="#6C5CE7", ax=0, ay=25, bgcolor="#12161F", bordercolor="rgba(255,255,255,0.15)",
            font=dict(color="#FFFFFF", size=11, family='Inter')
        )
        fig.add_annotation(
            x='2028', y=4.8, text="Executive Target", showarrow=True, arrowhead=2,
            arrowcolor="#22D3EE", ax=0, ay=-30, bgcolor="#12161F", bordercolor="#22D3EE",
            font=dict(color="#22D3EE", size=11, family='Inter', weight=700)
        )

        fig.update_layout(
            title={'text': '5-Year Leadership Trajectory', 'font': {'size': 16, 'color': '#FFFFFF', 'family': 'Space Grotesk'}},
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font={'color': '#8A8F9E', 'family': 'Inter'},
            height=320,
            margin=dict(l=40, r=40, t=50, b=40),
            yaxis=dict(
                tickvals=[1, 2, 3, 4, 5],
                ticktext=['Lead Eng', 'Director', 'VP Eng', 'SVP Tech', 'C-Suite'],
                showgrid=True, gridcolor='rgba(255,255,255,0.05)'
            ),
            xaxis=dict(showgrid=False, showline=True, linecolor='rgba(255,255,255,0.1)')
        )
        return fig

    def create_radar_competency_chart(self):
        """Create Radar Skill Competency Chart in Dark Glass style"""
        categories = ['Strategic Thinking', 'Org Velocity', 'Financial Acumen', 'Tech Mastery', 'EQ & Culture', 'Product Scale']
        values = [9.5, 9.2, 8.8, 9.4, 8.7, 9.1]

        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=values + [values[0]],
            theta=categories + [categories[0]],
            fill='toself',
            fillcolor='rgba(108, 92, 231, 0.25)',
            line=dict(color='#6C5CE7', width=2.5),
            marker=dict(color='#22D3EE', size=6)
        ))

        fig.update_layout(
            title={'text': 'Executive Competency Radar', 'font': {'size': 16, 'color': '#FFFFFF', 'family': 'Space Grotesk'}},
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 10], showticklabels=False, linecolor='rgba(255,255,255,0.1)', gridcolor='rgba(255,255,255,0.06)'),
                angularaxis=dict(tickfont=dict(size=11, color='#FFFFFF', family='Inter'))
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font={'color': '#8A8F9E', 'family': 'Inter'},
            height=320,
            margin=dict(l=40, r=40, t=50, b=40)
        )
        return fig

    def create_peer_benchmark_chart(self):
        """Create Peer Benchmark Bar Chart in Dark Glass style"""
        cohorts = ['Strategic Alignment', 'Tech Architecture', 'Team Scale', 'Domain Expertise', 'Execution Speed']
        candidate_vals = [94, 96, 91, 88, 95]
        top5_vals = [88, 90, 85, 84, 87]
        industry_vals = [72, 75, 68, 65, 70]

        fig = go.Figure()
        fig.add_trace(go.Bar(x=cohorts, y=candidate_vals, name='You (Executive)', marker_color='#6C5CE7'))
        fig.add_trace(go.Bar(x=cohorts, y=top5_vals, name='Top 5% Cohort', marker_color='#22D3EE'))
        fig.add_trace(go.Bar(x=cohorts, y=industry_vals, name='Industry Avg', marker_color='rgba(255,255,255,0.12)'))

        fig.update_layout(
            title={'text': 'Executive Peer Benchmark (% Percentile)', 'font': {'size': 16, 'color': '#FFFFFF', 'family': 'Space Grotesk'}},
            barmode='group',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font={'color': '#8A8F9E', 'family': 'Inter'},
            height=290,
            margin=dict(l=30, r=30, t=50, b=30),
            legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1, font=dict(color='#FFFFFF')),
            yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', range=[0, 100]),
            xaxis=dict(showgrid=False)
        )
        return fig

    def render_dashboard(self):
        """Render AiResuMind Pro v4.0 Executive Candidate Dashboard."""
        # Defence in depth for callers outside app.py's primary router.
        if not st.session_state.get("user_authenticated", False):
            st.session_state.page = "signin"
            st.warning("Please sign in to view your career dashboard.")
            return

        self.inject_dashboard_styles()

        # Dynamic Session State
        email_name = st.session_state.get("user_email", "").split("@", 1)[0].replace(".", " ").replace("_", " ").title()
        default_name = st.session_state.get('candidate_name') or st.session_state.get('user_name') or email_name or 'Candidate'
        default_role = st.session_state.get('candidate_role') or st.session_state.get('user_role') or 'Career Explorer'

        if 'candidate_name' not in st.session_state:
            st.session_state.candidate_name = default_name
        if 'candidate_role' not in st.session_state:
            st.session_state.candidate_role = default_role

        user_name = st.session_state.candidate_name
        user_role = st.session_state.candidate_role
        clean_handle = "".join(e for e in user_name if e.isalnum())
        handle_tag = "@" + (clean_handle if clean_handle else "ExecutiveCandidate")

        # Top Header Banner
        render_clean_html(f"""
            <div style="margin-bottom: 20px;">
                <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(255,255,255,0.08); padding-bottom: 18px;">
                    <div>
                        <h1 class="space-font" style="font-size: 30px !important; font-weight: 800 !important; color: #FFFFFF !important; margin: 0; display: inline; letter-spacing: -0.03em;">
                            Career Command Center
                        </h1>
                        <span style="font-size: 16px; font-weight: 600; color: #8A8F9E; margin-left: 12px; font-family: 'Inter', sans-serif;">
                            Live career intelligence for your next move
                        </span>
                    </div>
                    <div>
                        <div style="background: rgba(18, 22, 31, 0.8); border: 1px solid rgba(255, 255, 255, 0.12); padding: 8px 18px; border-radius: 9999px; font-size: 13px; color: #FFFFFF;">
                            <strong style="color: #22D3EE;">{user_name}</strong>
                            <span style="color: #8A8F9E; margin-left: 6px;">({user_role} {handle_tag})</span>
                        </div>
                    </div>
                </div>
            </div>
        """)

        # Candidate Profile Control Panel
        with st.expander("Profile settings", expanded=False):
            col_n, col_r, col_b = st.columns([0.4, 0.4, 0.2])
            with col_n:
                input_name = st.text_input("Candidate Name", value=user_name, key="dash_input_name")
            with col_r:
                input_role = st.text_input("Target Role / Title", value=user_role, key="dash_input_role")
            with col_b:
                st.write("")
                st.write("")
                if st.button("Save Profile", key="save_identity_btn", type="primary", use_container_width=True):
                    st.session_state.candidate_name = input_name
                    st.session_state.candidate_role = input_role
                    st.rerun()

        # Main Navigation Tabs
        tab_overview, tab_progression, tab_skills, tab_insights, tab_performance = st.tabs([
            "Overview", "Progression", "Skills", "Insights", "Performance"
        ])

        with tab_overview:
            # ── HERO METRICS ROW (3 Cards with Signature Warm Amber for Card 1) ──
            col_hero1, col_hero2, col_hero3 = st.columns(3, gap="medium")

            with col_hero1:
                render_clean_html("""
                    <div class="glass-card glow-amber metric-featured">
                        <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                            <div>
                                <div style="font-size: 12px; font-weight: 700; color: #8A8F9E; text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 6px;">
                                    Leadership Impact Score
                                </div>
                                <div class="space-font" style="font-size: 38px; font-weight: 800; color: #F5A623; line-height: 1.1;">
                                    8.9<span style="font-size: 20px; color: #8A8F9E; font-weight: 500;">/10</span>
                                </div>
                            </div>
                            <span class="delta-chip-amber">+12% vs. Q3</span>
                        </div>
                        <div style="margin-top: 18px; display: flex; align-items: center; justify-content: space-between;">
                            <div style="font-size: 12px; color: #8A8F9E;">Target Cohort: Top 1% Tech Executives</div>
                            <!-- Mini Sparkline SVG -->
                            <svg width="60" height="20" viewBox="0 0 60 20" fill="none">
                                <path d="M2 18 L15 14 L30 15 L42 7 L58 2" stroke="#F5A623" stroke-width="2.5" stroke-linecap="round"/>
                            </svg>
                        </div>
                        <div style="height: 4px; background: rgba(255,255,255,0.06); border-radius: 9999px; margin-top: 14px; overflow: hidden;">
                            <div style="width: 89%; height: 100%; background: #F5A623;"></div>
                        </div>
                    </div>
                """)

            with col_hero2:
                render_clean_html("""
                    <div class="glass-card glow-indigo metric-velocity">
                        <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                            <div>
                                <div style="font-size: 12px; font-weight: 700; color: #8A8F9E; text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 6px;">
                                    Org Velocity Index
                                </div>
                                <div class="space-font" style="font-size: 38px; font-weight: 800; color: #FFFFFF; line-height: 1.1;">
                                    74%
                                </div>
                            </div>
                            <span class="delta-chip-teal">+8% YoY</span>
                        </div>
                        <div style="margin-top: 18px; display: flex; align-items: center; justify-content: space-between;">
                            <div style="font-size: 12px; color: #8A8F9E;">Engineered Team Throughput Rate</div>
                            <svg width="60" height="20" viewBox="0 0 60 20" fill="none">
                                <path d="M2 16 L18 12 L32 14 L46 6 L58 3" stroke="#6C5CE7" stroke-width="2.5" stroke-linecap="round"/>
                            </svg>
                        </div>
                        <div style="height: 4px; background: rgba(255,255,255,0.06); border-radius: 9999px; margin-top: 14px; overflow: hidden;">
                            <div style="width: 74%; height: 100%; background: #6C5CE7;"></div>
                        </div>
                    </div>
                """)

            with col_hero3:
                render_clean_html("""
                    <div class="glass-card glow-teal metric-skill">
                        <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                            <div>
                                <div style="font-size: 12px; font-weight: 700; color: #8A8F9E; text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 6px;">
                                    Skill Proficiency
                                </div>
                                <div class="space-font" style="font-size: 38px; font-weight: 800; color: #FFFFFF; line-height: 1.1;">
                                    91%
                                </div>
                            </div>
                            <span style="background: rgba(255,255,255,0.06); color: #8A8F9E; border: 1px solid rgba(255,255,255,0.12); padding: 3px 10px; border-radius: 9999px; font-size: 12px; font-weight: 600;">
                                overall
                            </span>
                        </div>
                        <div style="margin-top: 18px; display: flex; align-items: center; justify-content: space-between;">
                            <div style="font-size: 12px; color: #8A8F9E;">Strategic & Technical Competency</div>
                            <svg width="60" height="20" viewBox="0 0 60 20" fill="none">
                                <path d="M2 17 L14 13 L28 15 L44 8 L58 2" stroke="#22D3EE" stroke-width="2.5" stroke-linecap="round"/>
                            </svg>
                        </div>
                        <div style="height: 4px; background: rgba(255,255,255,0.06); border-radius: 9999px; margin-top: 14px; overflow: hidden;">
                            <div style="width: 91%; height: 100%; background: #22D3EE;"></div>
                        </div>
                    </div>
                """)

            render_clean_html("<div style='height: 24px;'></div>")

            # ── CHARTS ROW ──
            mid_col1, mid_col2 = st.columns([0.58, 0.42], gap="medium")

            with mid_col1:
                render_clean_html('<div class="glass-card">')
                fig_traj = self.create_trajectory_chart()
                st.plotly_chart(fig_traj, use_container_width=True)
                render_clean_html('</div>')

            with mid_col2:
                render_clean_html('<div class="glass-card">')
                fig_radar = self.create_radar_competency_chart()
                st.plotly_chart(fig_radar, use_container_width=True)
                render_clean_html('</div>')

            render_clean_html("<div style='height: 24px;'></div>")

            # ── EXECUTIVE PERFORMANCE METRICS GRID & PEER BENCHMARK ──
            bot_col1, bot_col2 = st.columns([0.55, 0.45], gap="medium")

            with bot_col1:
                render_clean_html("""
                    <div class="glass-card">
                        <div class="space-font" style="font-size: 18px; font-weight: 700; color: #FFFFFF; margin-bottom: 18px; display: flex; align-items: center; gap: 8px;">
                            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#22D3EE" stroke-width="2">
                                <path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/>
                            </svg>
                            Executive Performance Metrics
                        </div>
                        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 14px;">
                            <!-- Card 1: Revenue Growth -->
                            <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.06); padding: 18px; border-radius: 16px;">
                                <div style="font-size: 12px; color: #8A8F9E; font-weight: 500;">Revenue Growth</div>
                                <div class="space-font" style="font-size: 28px; font-weight: 800; color: #FFFFFF; margin: 6px 0;">$14.2M</div>
                                <div style="display: inline-flex; align-items: center; gap: 4px; color: #22D3EE; font-size: 13px; font-weight: 700;">
                                    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3">
                                        <path d="M12 19V5M5 12l7-7 7 7"/>
                                    </svg>
                                    +19%
                                </div>
                            </div>
                            <!-- Card 2: Profitability -->
                            <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.06); padding: 18px; border-radius: 16px;">
                                <div style="font-size: 12px; color: #8A8F9E; font-weight: 500;">Profitability</div>
                                <div class="space-font" style="font-size: 28px; font-weight: 800; color: #FFFFFF; margin: 6px 0;">94%</div>
                                <div style="display: inline-flex; align-items: center; gap: 4px; color: #22D3EE; font-size: 13px; font-weight: 700;">
                                    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3">
                                        <path d="M12 19V5M5 12l7-7 7 7"/>
                                    </svg>
                                    +5%
                                </div>
                            </div>
                            <!-- Card 3: Employee Retention -->
                            <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.06); padding: 18px; border-radius: 16px;">
                                <div style="font-size: 12px; color: #8A8F9E; font-weight: 500;">Employee Retention</div>
                                <div class="space-font" style="font-size: 28px; font-weight: 800; color: #FFFFFF; margin: 6px 0;">94%</div>
                                <div style="display: inline-flex; align-items: center; gap: 4px; color: #22D3EE; font-size: 13px; font-weight: 700;">
                                    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3">
                                        <path d="M12 19V5M5 12l7-7 7 7"/>
                                    </svg>
                                    +5%
                                </div>
                            </div>
                            <!-- Card 4: Market Share -->
                            <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.06); padding: 18px; border-radius: 16px;">
                                <div style="font-size: 12px; color: #8A8F9E; font-weight: 500;">Market Share</div>
                                <div class="space-font" style="font-size: 28px; font-weight: 800; color: #FFFFFF; margin: 6px 0;">8.6%</div>
                                <div style="display: inline-flex; align-items: center; gap: 4px; color: #22D3EE; font-size: 13px; font-weight: 700;">
                                    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3">
                                        <path d="M12 19V5M5 12l7-7 7 7"/>
                                    </svg>
                                    +19%
                                </div>
                            </div>
                        </div>
                    </div>
                """)

            with bot_col2:
                render_clean_html('<div class="glass-card">')
                fig_peer = self.create_peer_benchmark_chart()
                st.plotly_chart(fig_peer, use_container_width=True)
                render_clean_html('</div>')

        with tab_progression:
            render_clean_html("""
                <div class="glass-card" style="margin-top: 10px;">
                    <div class="space-font" style="font-size: 20px; font-weight: 700; color: #FFFFFF; margin-bottom: 8px;">
                        Quarterly Leadership Progression & Impact Milestones
                    </div>
                    <p style="color: #8A8F9E; font-size: 14px; margin-bottom: 24px;">
                        Track your career velocity, organization growth targets, and executive board presentations.
                    </p>
                    <div style="display: flex; flex-direction: column; gap: 16px;">
                        <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.06); padding: 16px 20px; border-radius: 14px; display: flex; justify-content: space-between; align-items: center;">
                            <div>
                                <div style="font-size: 11px; font-weight: 700; color: #6C5CE7; text-transform: uppercase;">Q4 2025 Target</div>
                                <div style="font-size: 16px; font-weight: 700; color: #FFFFFF;">Scaled Engineering Org to 120+ Across 3 Hubs</div>
                            </div>
                            <span class="delta-chip-teal">Completed</span>
                        </div>
                        <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.06); padding: 16px 20px; border-radius: 14px; display: flex; justify-content: space-between; align-items: center;">
                            <div>
                                <div style="font-size: 11px; font-weight: 700; color: #22D3EE; text-transform: uppercase;">Q1 2026 Milestone</div>
                                <div style="font-size: 16px; font-weight: 700; color: #FFFFFF;">Delivered AI Infrastructure Saving $140k Cloud Overhead</div>
                            </div>
                            <span class="delta-chip-teal">Exceeded (+19%)</span>
                        </div>
                        <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.06); padding: 16px 20px; border-radius: 14px; display: flex; justify-content: space-between; align-items: center;">
                            <div>
                                <div style="font-size: 11px; font-weight: 700; color: #F5A623; text-transform: uppercase;">Q2 2026 Objective</div>
                                <div style="font-size: 16px; font-weight: 700; color: #FFFFFF;">C-Suite & SVP Engineering Position Pitching</div>
                            </div>
                            <span class="delta-chip-amber">In Progress</span>
                        </div>
                    </div>
                </div>
            """)

        with tab_skills:
            render_clean_html("""
                <div class="glass-card" style="margin-top: 10px;">
                    <div class="space-font" style="font-size: 20px; font-weight: 700; color: #FFFFFF; margin-bottom: 8px;">
                        Executive Competency & Skill Proficiency Matrix
                    </div>
                    <p style="color: #8A8F9E; font-size: 14px; margin-bottom: 24px;">
                        AI evaluation of your core strategic capabilities verified against top tier tech companies.
                    </p>
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 16px;">
                        <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.06); padding: 18px; border-radius: 14px;">
                            <div style="display: flex; justify-content: space-between; font-size: 14px; font-weight: 700; color: #FFFFFF;">
                                <span>System Design & Architecture</span>
                                <span style="color: #22D3EE;">96%</span>
                            </div>
                            <div style="height: 6px; background: rgba(255,255,255,0.08); border-radius: 999px; margin-top: 10px;">
                                <div style="width: 96%; height: 100%; background: #22D3EE; border-radius: 999px;"></div>
                            </div>
                        </div>
                        <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.06); padding: 18px; border-radius: 14px;">
                            <div style="display: flex; justify-content: space-between; font-size: 14px; font-weight: 700; color: #FFFFFF;">
                                <span>Strategic P&L Management</span>
                                <span style="color: #6C5CE7;">92%</span>
                            </div>
                            <div style="height: 6px; background: rgba(255,255,255,0.08); border-radius: 999px; margin-top: 10px;">
                                <div style="width: 92%; height: 100%; background: #6C5CE7; border-radius: 999px;"></div>
                            </div>
                        </div>
                        <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.06); padding: 18px; border-radius: 14px;">
                            <div style="display: flex; justify-content: space-between; font-size: 14px; font-weight: 700; color: #FFFFFF;">
                                <span>Team Growth & Retention</span>
                                <span style="color: #F5A623;">94%</span>
                            </div>
                            <div style="height: 6px; background: rgba(255,255,255,0.08); border-radius: 999px; margin-top: 10px;">
                                <div style="width: 94%; height: 100%; background: #F5A623; border-radius: 999px;"></div>
                            </div>
                        </div>
                    </div>
                </div>
            """)

        with tab_insights:
            render_clean_html("""
                <div class="glass-card" style="margin-top: 10px;">
                    <div class="space-font" style="font-size: 20px; font-weight: 700; color: #FFFFFF; margin-bottom: 8px;">
                        AI Candidate Telemetry & C-Suite Positioning Insights
                    </div>
                    <p style="color: #8A8F9E; font-size: 14px; margin-bottom: 24px;">
                        Real-time AI recommendations based on 50,000+ executive recruiter searches.
                    </p>
                    <div style="display: flex; flex-direction: column; gap: 16px;">
                        <div style="background: rgba(108, 92, 231, 0.1); border: 1px solid rgba(108, 92, 231, 0.3); padding: 20px; border-radius: 16px;">
                            <div style="font-size: 15px; font-weight: 700; color: #FFFFFF; margin-bottom: 6px;">
                                💡 Executive Resume Optimization Signal
                            </div>
                            <div style="font-size: 13.5px; color: #8A8F9E; line-height: 1.6;">
                                Your quantified metrics ($14.2M Revenue Growth, 94% Retention) put your profile in the top 0.5% for Vice President of Engineering roles at Series C through IPO companies.
                            </div>
                        </div>
                        <div style="background: rgba(34, 211, 238, 0.1); border: 1px solid rgba(34, 211, 238, 0.3); padding: 20px; border-radius: 16px;">
                            <div style="font-size: 15px; font-weight: 700; color: #FFFFFF; margin-bottom: 6px;">
                                🚀 Recruiter Cold Outreach Conversion
                            </div>
                            <div style="font-size: 13.5px; color: #8A8F9E; line-height: 1.6;">
                                Use the Cold Mail generator to highlight your Spring Boot & Cloud Cost Reduction achievements for a 45%+ response rate from Managing Directors.
                            </div>
                        </div>
                    </div>
                </div>
            """)

        with tab_performance:
            render_clean_html("""
                <div class="glass-card" style="margin-top: 10px;">
                    <div class="space-font" style="font-size: 20px; font-weight: 700; color: #FFFFFF; margin-bottom: 8px;">
                        Financial & Organizational Performance Breakdown
                    </div>
                    <p style="color: #8A8F9E; font-size: 14px; margin-bottom: 24px;">
                        Detailed audited P&L metrics, headcount scaling velocity, and market expansion scores.
                    </p>
                    <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px;">
                        <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.06); padding: 20px; border-radius: 16px; text-align: center;">
                            <div style="font-size: 12px; color: #8A8F9E;">Arr Scaled</div>
                            <div class="space-font" style="font-size: 26px; font-weight: 800; color: #22D3EE; margin: 4px 0;">$42M</div>
                            <div style="font-size: 11px; color: #8A8F9E;">+34% YoY</div>
                        </div>
                        <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.06); padding: 20px; border-radius: 16px; text-align: center;">
                            <div style="font-size: 12px; color: #8A8F9E;">Gross Margin</div>
                            <div class="space-font" style="font-size: 26px; font-weight: 800; color: #6C5CE7; margin: 4px 0;">84%</div>
                            <div style="font-size: 11px; color: #8A8F9E;">Top Tier SaaS</div>
                        </div>
                        <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.06); padding: 20px; border-radius: 16px; text-align: center;">
                            <div style="font-size: 12px; color: #8A8F9E;">Org Headcount</div>
                            <div class="space-font" style="font-size: 26px; font-weight: 800; color: #F5A623; margin: 4px 0;">140+</div>
                            <div style="font-size: 11px; color: #8A8F9E;">Engineers & PMs</div>
                        </div>
                        <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.06); padding: 20px; border-radius: 16px; text-align: center;">
                            <div style="font-size: 12px; color: #8A8F9E;">Retention Rate</div>
                            <div class="space-font" style="font-size: 26px; font-weight: 800; color: #22D3EE; margin: 4px 0;">94%</div>
                            <div style="font-size: 11px; color: #8A8F9E;">+5% vs Industry</div>
                        </div>
                    </div>
                </div>
            """)

        # ── FOOTER STATUS & COPYRIGHT ──
        render_clean_html("""
            <div style="margin-top: 40px; border-top: 1px solid rgba(255,255,255,0.08); padding-top: 24px; padding-bottom: 24px;">
                <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 16px;">
                    <!-- Status Pill -->
                    <div style="display: inline-flex; align-items: center; gap: 8px; background: rgba(34, 211, 238, 0.08); border: 1px solid rgba(34, 211, 238, 0.25); padding: 6px 16px; border-radius: 9999px; font-size: 12.5px; font-weight: 600; color: #FFFFFF;">
                        <span class="status-dot-live"></span>
                        All v4.0 AI Candidate Engines Operational
                    </div>
                    <!-- Copyright -->
                    <div style="font-size: 12.5px; color: #8A8F9E; text-align: right;">
                        <strong style="color: #FFFFFF;">AiResuMind Pro v4.0</strong> — Next-Generation AI Candidate Intelligence & Executive Resume Platform<br/>
                        Copyright © 2026 AiResuMind Inc. All rights reserved. Built for candidates aiming for executive tech roles.
                    </div>
                </div>
            </div>
        """)
