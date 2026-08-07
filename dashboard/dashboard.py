import streamlit as st
import textwrap
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from config.database import get_database_connection
import io
import uuid
from plotly.subplots import make_subplots

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
            'primary': '#F5F5F7',
            'secondary': '#86868B',
            'warning': '#F59E0B',
            'danger': '#FF453A',
            'info': '#64D2FF',
            'success': '#30D158',
            'purple': '#BF5AF2',
            'background': 'rgba(0,0,0,0)',
            'card': '#121215',
            'text': '#F5F5F7',
            'subtext': '#86868B'
        }

    def create_trajectory_chart(self):
        """Create 5-Year Career Trajectory Chart with Apple Monochrome styling"""
        years = ['2024', '2025', '2026', '2027', '2028', '2029']
        y_positions = [1, 2, 3, 4, 4.8, 5]
        
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=years,
            y=y_positions,
            mode='lines+markers',
            line=dict(color='#F5F5F7', width=3, shape='spline'),
            marker=dict(size=8, color='#30D158', symbol='circle'),
            name='Trajectory'
        ))

        fig.add_annotation(x='2024', y=1, text="Current Role", showarrow=True, arrowhead=2, arrowcolor="#F5F5F7", ax=0, ay=25, bgcolor="#121215", bordercolor="#F5F5F7", font=dict(color="#F5F5F7", size=11))
        fig.add_annotation(x='2028', y=4.8, text="Executive Target", showarrow=True, arrowhead=2, arrowcolor="#30D158", ax=0, ay=-30, bgcolor="#121215", bordercolor="#30D158", font=dict(color="#F5F5F7", size=11))

        fig.update_layout(
            title={'text': 'Career Trajectory: Next 5 Years', 'font': {'size': 17, 'color': '#F5F5F7', 'family': '-apple-system'}},
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font={'color': '#86868B', 'family': '-apple-system'},
            height=320,
            margin=dict(l=40, r=40, t=50, b=40),
            yaxis=dict(
                tickvals=[1, 2, 3, 4, 5],
                ticktext=['Lead Analyst', 'Manager', 'Director', 'VP', 'C-Suite'],
                showgrid=True, gridcolor='rgba(255,255,255,0.06)'
            ),
            xaxis=dict(showgrid=False, showline=True, linecolor='rgba(255,255,255,0.1)')
        )
        return fig

    def create_radar_competency_chart(self):
        """Create Radar Skill Competency Chart with Apple styling"""
        categories = ['Strategic Thinking', 'Leadership', 'Financial Acumen', 'Tech Mastery', 'EQ', 'Innovation']
        values = [9.5, 9.2, 8.8, 9.1, 8.5, 8.9]

        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=values + [values[0]],
            theta=categories + [categories[0]],
            fill='toself',
            fillcolor='rgba(255, 255, 255, 0.1)',
            line=dict(color='#F5F5F7', width=2),
            marker=dict(color='#30D158', size=6)
        ))

        fig.update_layout(
            title={'text': 'Skill Competency Breakdown', 'font': {'size': 17, 'color': '#F5F5F7', 'family': '-apple-system'}},
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 10], showticklabels=False, linecolor='rgba(255,255,255,0.1)', gridcolor='rgba(255,255,255,0.08)'),
                angularaxis=dict(tickfont=dict(size=11, color='#F5F5F7'))
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font={'color': '#86868B', 'family': '-apple-system'},
            height=320,
            margin=dict(l=40, r=40, t=50, b=40)
        )
        return fig

    def create_peer_benchmark_chart(self):
        """Create Peer Benchmark Bar Chart"""
        cohorts = ['Strategic', 'Analytics', 'Leadership', 'Domain', 'Execution']
        candidate_vals = [24, 40, 25, 20, 22]
        top5_vals = [14, 30, 12, 11, 10]
        industry_vals = [18, 25, 16, 14, 15]

        fig = go.Figure()
        fig.add_trace(go.Bar(x=cohorts, y=candidate_vals, name='You (Candidate)', marker_color='#F5F5F7'))
        fig.add_trace(go.Bar(x=cohorts, y=top5_vals, name='Top 5% Cohort', marker_color='#30D158'))
        fig.add_trace(go.Bar(x=cohorts, y=industry_vals, name='Industry Avg', marker_color='#3A3A3C'))

        fig.update_layout(
            title={'text': 'Peer Benchmark: Executive Competencies', 'font': {'size': 17, 'color': '#F5F5F7', 'family': '-apple-system'}},
            barmode='group',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font={'color': '#86868B', 'family': '-apple-system'},
            height=280,
            margin=dict(l=30, r=30, t=50, b=30),
            legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1, font=dict(color='#F5F5F7')),
            yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.06)'),
            xaxis=dict(showgrid=False)
        )
        return fig

    def render_dashboard(self):
        """Render AI Career Analytics | Executive Dashboard with dynamic candidate personalization."""
        # Dynamic Session State Identification
        default_name = st.session_state.get('parsed_name') or st.session_state.get('user_name') or 'Executive Candidate'
        default_role = st.session_state.get('parsed_role') or st.session_state.get('user_role') or 'Product & Tech Leader'

        if 'candidate_name' not in st.session_state:
            st.session_state.candidate_name = default_name
        if 'candidate_role' not in st.session_state:
            st.session_state.candidate_role = default_role

        user_name = st.session_state.candidate_name
        user_role = st.session_state.candidate_role
        clean_handle = "".join(e for e in user_name if e.isalnum())
        handle_tag = "@" + (clean_handle if clean_handle else "Executive")

        render_clean_html(f"""
            <div style="margin-top: 4px; margin-bottom: 16px;">
                <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(255,255,255,0.08); padding-bottom: 16px;">
                    <div>
                        <h1 style="font-size: 26px !important; font-weight: 800 !important; color: #F5F5F7 !important; margin: 0; display: inline; letter-spacing: -0.02em;">
                            AiResuMind
                        </h1>
                        <span style="font-size: 18px; font-weight: 600; color: #86868B; margin-left: 10px;">AI Career Analytics | Executive Dashboard</span>
                    </div>
                    <div style="display: flex; align-items: center; gap: 12px;">
                        <div style="background: rgba(255, 255, 255, 0.06); border: 1px solid rgba(255, 255, 255, 0.12); padding: 6px 14px; border-radius: 9999px; font-size: 12.5px; color: #F5F5F7;">
                            <strong>{user_name}</strong> <span style="color: #86868B; font-weight: 500;">({user_role} {handle_tag})</span>
                        </div>
                    </div>
                </div>
            </div>
        """)

        # Dynamic Identity Controls
        with st.expander("Edit Candidate Identity Profile", expanded=False):
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

        tab1, tab2, tab3, tab4, tab5 = st.tabs(["Overview", "Progression", "Skills", "Insights", "Performance"])

        with tab1:
            col1, col2, col3 = st.columns(3, gap="medium")

            with col1:
                render_clean_html("""
                    <div class="editorial-card" style="background: #121215; border: 1px solid rgba(255,255,255,0.1); border-radius: 24px; padding: 24px;">
                        <div style="font-size: 12px; font-weight: 700; color: #86868B; text-transform: uppercase; margin-bottom: 8px; letter-spacing: 0.04em;">Leadership Impact Score</div>
                        <div style="font-size: 34px; font-weight: 800; color: #F5F5F7;">8.9/10 <span style="font-size: 13px; color: #30D158; font-weight: 700;">+12% vs. Q3</span></div>
                        <div style="height: 5px; background: rgba(255,255,255,0.08); border-radius: 9999px; margin-top: 16px; overflow: hidden;">
                            <div style="width: 89%; height: 100%; background: #F5F5F7;"></div>
                        </div>
                    </div>
                """)

            with col2:
                render_clean_html("""
                    <div class="editorial-card" style="background: #121215; border: 1px solid rgba(255,255,255,0.1); border-radius: 24px; padding: 24px;">
                        <div style="font-size: 12px; font-weight: 700; color: #86868B; text-transform: uppercase; margin-bottom: 8px; letter-spacing: 0.04em;">Org Velocity Index</div>
                        <div style="font-size: 34px; font-weight: 800; color: #F5F5F7;">74% <span style="font-size: 13px; color: #30D158; font-weight: 700;">+8% YoY</span></div>
                        <div style="height: 5px; background: rgba(255,255,255,0.08); border-radius: 9999px; margin-top: 16px; overflow: hidden; display: flex;">
                            <div style="width: 74%; height: 100%; background: #30D158;"></div>
                            <div style="width: 26%; height: 100%; background: rgba(255,255,255,0.1);"></div>
                        </div>
                    </div>
                """)

            with col3:
                render_clean_html("""
                    <div class="editorial-card" style="background: #121215; border: 1px solid rgba(255,255,255,0.1); border-radius: 24px; padding: 24px;">
                        <div style="font-size: 12px; font-weight: 700; color: #86868B; text-transform: uppercase; margin-bottom: 8px; letter-spacing: 0.04em;">Skill Proficiency</div>
                        <div style="font-size: 34px; font-weight: 800; color: #F5F5F7;">91% <span style="font-size: 13px; color: #86868B; font-weight: 600;">overall</span></div>
                        <div style="height: 5px; background: rgba(255,255,255,0.08); border-radius: 9999px; margin-top: 16px; overflow: hidden;">
                            <div style="width: 91%; height: 100%; background: #F5F5F7;"></div>
                        </div>
                    </div>
                """)

            render_clean_html("<div style='height: 24px;'></div>")

            mid_col1, mid_col2 = st.columns([0.6, 0.4], gap="medium")

            with mid_col1:
                render_clean_html('<div class="editorial-card" style="background: #121215; border: 1px solid rgba(255,255,255,0.1); border-radius: 24px; padding: 22px;">')
                fig_traj = self.create_trajectory_chart()
                st.plotly_chart(fig_traj, use_container_width=True)
                render_clean_html('</div>')

            with mid_col2:
                render_clean_html('<div class="editorial-card" style="background: #121215; border: 1px solid rgba(255,255,255,0.1); border-radius: 24px; padding: 22px;">')
                fig_radar = self.create_radar_competency_chart()
                st.plotly_chart(fig_radar, use_container_width=True)
                render_clean_html('</div>')

            render_clean_html("<div style='height: 24px;'></div>")

            bot_col1, bot_col2 = st.columns([0.55, 0.45], gap="medium")

            with bot_col1:
                render_clean_html("""
                    <div class="editorial-card" style="background: #121215; border: 1px solid rgba(255,255,255,0.1); border-radius: 24px; padding: 26px;">
                        <div style="font-size: 16px; font-weight: 700; color: #F5F5F7; margin-bottom: 20px;">Executive Performance Metrics</div>
                        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px;">
                            <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.06); padding: 18px; border-radius: 16px;">
                                <div style="font-size: 12px; color: #86868B; font-weight: 500;">Revenue Growth</div>
                                <div style="font-size: 26px; font-weight: 800; color: #F5F5F7; margin: 4px 0;">$14.2M</div>
                                <div style="font-size: 12px; color: #30D158; font-weight: 700;">+19%</div>
                            </div>
                            <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.06); padding: 18px; border-radius: 16px;">
                                <div style="font-size: 12px; color: #86868B; font-weight: 500;">Profitability</div>
                                <div style="font-size: 26px; font-weight: 800; color: #F5F5F7; margin: 4px 0;">94%</div>
                                <div style="font-size: 12px; color: #30D158; font-weight: 700;">+5%</div>
                            </div>
                            <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.06); padding: 18px; border-radius: 16px;">
                                <div style="font-size: 12px; color: #86868B; font-weight: 500;">Employee Retention</div>
                                <div style="font-size: 26px; font-weight: 800; color: #F5F5F7; margin: 4px 0;">94%</div>
                                <div style="font-size: 12px; color: #30D158; font-weight: 700;">+5%</div>
                            </div>
                            <div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.06); padding: 18px; border-radius: 16px;">
                                <div style="font-size: 12px; color: #86868B; font-weight: 500;">Market Share</div>
                                <div style="font-size: 26px; font-weight: 800; color: #F5F5F7; margin: 4px 0;">8.6%</div>
                                <div style="font-size: 12px; color: #30D158; font-weight: 700;">+19%</div>
                            </div>
                        </div>
                    </div>
                """)

            with bot_col2:
                render_clean_html('<div class="editorial-card" style="background: #121215; border: 1px solid rgba(255,255,255,0.1); border-radius: 24px; padding: 22px;">')
                fig_peer = self.create_peer_benchmark_chart()
                st.plotly_chart(fig_peer, use_container_width=True)
                render_clean_html('</div>')

        with tab2:
            render_clean_html('<div class="editorial-card" style="background: #121215; padding: 28px; border-radius: 24px;"><h3 style="color: #F5F5F7;">Career Progression Trajectory</h3><p style="color: #86868B;">Quarterly leadership progression and organizational impact milestones.</p></div>')

        with tab3:
            render_clean_html('<div class="editorial-card" style="background: #121215; padding: 28px; border-radius: 24px;"><h3 style="color: #F5F5F7;">Executive Skill Matrix</h3><p style="color: #86868B;">Comprehensive evaluation of strategic, financial, and leadership domain skills.</p></div>')

        with tab4:
            render_clean_html('<div class="editorial-card" style="background: #121215; padding: 28px; border-radius: 24px;"><h3 style="color: #F5F5F7;">AI Career Insights & Recommendations</h3><p style="color: #86868B;">Real-time AI telemetry advice for board-level and C-suite positioning.</p></div>')

        with tab5:
            render_clean_html('<div class="editorial-card" style="background: #121215; padding: 28px; border-radius: 24px;"><h3 style="color: #F5F5F7;">Financial & Organizational Performance</h3><p style="color: #86868B;">Detailed P&L, retention, and market growth benchmarks.</p></div>')