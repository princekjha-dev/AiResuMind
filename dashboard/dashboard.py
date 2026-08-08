import datetime
import streamlit as st
import plotly.graph_objects as go
from config.database import get_database_connection, get_dashboard_analytics
from ui_kit import render_clean_html, render_ai_insight


# ─── colour palette (spec-compliant) ────────────────────────────────────────
BG       = "#0B0C0F"
SURFACE  = "#15171A"
ELEVATED = "#1B1D21"
PRIMARY  = "#F5F5F7"
SECONDARY= "#9CA3AF"
MUTED    = "#6B7280"
ACCENT   = "#4F8CFF"
SUCCESS  = "#34D399"
WARNING  = "#FBBF24"
ERROR    = "#F87171"
BORDER   = "rgba(255,255,255,0.08)"

CHART_LAYOUT = dict(
    paper_bgcolor=SURFACE,
    plot_bgcolor=SURFACE,
    font=dict(color=SECONDARY, family="-apple-system, BlinkMacSystemFont, 'Inter', sans-serif", size=12),
    margin=dict(l=8, r=8, t=8, b=8),
    showlegend=False,
)

AXIS_STYLE = dict(showgrid=True, gridcolor="rgba(255,255,255,0.05)", zeroline=False)


def _nav(page_key):
    st.session_state.page = page_key
    if hasattr(st, "query_params"):
        st.query_params["page"] = page_key
    st.rerun()


def _score_color(score):
    if score is None:
        return MUTED
    if score >= 80:
        return SUCCESS
    if score >= 60:
        return WARNING
    return ERROR


def _section_header(title):
    render_clean_html(f"""
        <div style="display:flex;align-items:center;gap:12px;margin:40px 0 20px 0;">
            <span style="font-size:18px;font-weight:700;color:{PRIMARY};letter-spacing:-0.01em;">{title}</span>
            <div style="flex:1;height:1px;background:{BORDER};"></div>
        </div>
    """)


def _kpi_card(label, value, sub, accent_color=None, delta=None):
    color = accent_color or PRIMARY
    delta_html = ""
    if delta:
        d_color = SUCCESS if "+" in str(delta) else MUTED
        delta_html = f'<span style="font-size:11px;font-weight:600;color:{d_color};margin-left:8px;">{delta}</span>'
    render_clean_html(f"""
        <div style="background:{SURFACE};border:1px solid {BORDER};border-radius:16px;padding:22px 20px 18px 20px;height:100%;box-sizing:border-box;position:relative;overflow:hidden;">
            <div style="position:absolute;top:0;left:0;width:3px;height:100%;background:{color};border-radius:3px 0 0 3px;"></div>
            <div style="font-size:10.5px;font-weight:700;color:{MUTED};text-transform:uppercase;letter-spacing:0.1em;margin-bottom:14px;">{label}</div>
            <div style="display:flex;align-items:baseline;gap:4px;margin-bottom:6px;">
                <span style="font-size:34px;font-weight:800;color:{PRIMARY};line-height:1;letter-spacing:-0.03em;">{value}</span>
                {delta_html}
            </div>
            <div style="font-size:12px;color:{SECONDARY};">{sub}</div>
        </div>
    """)


def _chart_card(title, body_fn, height=300):
    render_clean_html(f"""
        <div style="background:{SURFACE};border:1px solid {BORDER};border-radius:16px;padding:20px 20px 4px 20px;height:100%;box-sizing:border-box;">
            <div style="font-size:13px;font-weight:700;color:{PRIMARY};letter-spacing:-0.01em;margin-bottom:12px;">{title}</div>
    """)
    body_fn()
    render_clean_html("</div>")


def _empty_chart(msg):
    render_clean_html(f"""
        <div style="padding:48px 16px;text-align:center;color:{MUTED};font-size:13px;line-height:1.6;">{msg}</div>
    """)


class DashboardManager:
    def __init__(self):
        self.conn = get_database_connection()

    # ─── main entry ─────────────────────────────────────────────────────────
    def render_dashboard(self):
        analytics   = get_dashboard_analytics()
        ctx         = st.session_state.get("career_context", {})

        total       = analytics.get("total_resumes", 0)
        avg_ats     = analytics.get("avg_ats_score")
        high_perf   = analytics.get("high_performing_count", 0)
        success_rt  = analytics.get("success_rate")
        last_date   = analytics.get("last_analysis_date")
        skills_dist = analytics.get("skill_distribution", [])
        role_perf   = analytics.get("role_performance", [])
        top_role    = analytics.get("top_performing_role")
        recent      = analytics.get("recent_analyses", [])
        weekly_act  = analytics.get("weekly_activity", [])

        # session fallback
        sess_score = st.session_state.get("overall_score") or ctx.get("atsScore")
        if avg_ats is None and sess_score:
            try:
                avg_ats   = round(float(sess_score), 1)
                last_date = datetime.datetime.now().strftime("%b %d, %Y")
                if total == 0:
                    total = 1
            except Exception:
                pass

        render_clean_html(f'<div style="max-width:1320px;margin:0 auto;padding:20px 8px 72px 8px;">')

        # ── 1. HEADER ────────────────────────────────────────────────────────
        last_str = last_date or "—"
        render_clean_html(f"""
            <div style="background:linear-gradient(135deg,rgba(79,140,255,0.09) 0%,rgba(30,58,138,0.18) 100%);
                        border:1px solid rgba(79,140,255,0.15);border-radius:20px;
                        padding:28px 32px;margin-bottom:28px;
                        display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:16px;">
                <div>
                    <div style="font-size:10.5px;font-weight:700;color:{ACCENT};text-transform:uppercase;
                                letter-spacing:0.14em;margin-bottom:6px;">AiResuMind</div>
                    <h1 style="font-size:28px!important;font-weight:800!important;color:{PRIMARY}!important;
                               margin:0 0 8px 0;letter-spacing:-0.025em;">Career Intelligence Dashboard</h1>
                    <div style="font-size:14px;color:{SECONDARY};">
                        Understand your resume performance, ATS readiness, and application progress.
                    </div>
                </div>
                <div style="background:rgba(0,0,0,0.35);border:1px solid {BORDER};border-radius:12px;padding:12px 20px;text-align:right;">
                    <div style="font-size:10px;font-weight:700;color:{MUTED};text-transform:uppercase;
                                letter-spacing:0.1em;margin-bottom:4px;">Last Analyzed</div>
                    <div style="font-size:14px;font-weight:600;color:{PRIMARY};">{last_str}</div>
                </div>
            </div>
        """)

        # ── 2. KPI ROW ───────────────────────────────────────────────────────
        k1, k2, k3, k4 = st.columns(4, gap="medium")
        with k1:
            _kpi_card("Total Resumes",
                      str(total) if total > 0 else "—",
                      "Resumes analyzed" if total > 0 else "No data yet",
                      ACCENT)
        with k2:
            v = f"{avg_ats}" if avg_ats is not None else "—"
            _kpi_card("Avg ATS Score", v,
                      "ATS readiness score" if avg_ats is not None else "No data yet",
                      _score_color(avg_ats))
        with k3:
            _kpi_card("High Performing",
                      str(high_perf) if high_perf > 0 else "—",
                      "Score 80 or above" if high_perf > 0 else "No data yet",
                      SUCCESS)
        with k4:
            v = f"{success_rt}%" if success_rt is not None else "—"
            _kpi_card("Application Match Rate", v,
                      "Resumes scoring 70+" if success_rt is not None else "No data yet",
                      WARNING)

        # ── 3. PERFORMANCE ANALYTICS ─────────────────────────────────────────
        _section_header("Performance Analytics")
        g1l, g1r = st.columns(2, gap="medium")

        # LEFT — ATS gauge
        with g1l:
            def _gauge_body():
                if avg_ats is not None and avg_ats > 0:
                    fig = go.Figure(go.Indicator(
                        mode="gauge+number",
                        value=avg_ats,
                        number={"font": {"size": 48, "color": PRIMARY, "family": "Inter, sans-serif"},
                                "suffix": ""},
                        domain={"x": [0, 1], "y": [0, 1]},
                        gauge={
                            "axis": {"range": [0, 100], "tickwidth": 1, "tickcolor": MUTED,
                                     "tickfont": {"color": MUTED, "size": 11}},
                            "bar": {"color": _score_color(avg_ats), "thickness": 0.22},
                            "bgcolor": ELEVATED,
                            "borderwidth": 0,
                            "steps": [
                                {"range": [0, 40],  "color": "rgba(248,113,113,0.12)"},
                                {"range": [40, 75], "color": "rgba(251,191,36,0.12)"},
                                {"range": [75, 100],"color": "rgba(52,211,153,0.12)"},
                            ],
                        }
                    ))
                    fig.update_layout(**CHART_LAYOUT, height=280)
                    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
                    # score label
                    lbl = ("Excellent" if avg_ats >= 80 else
                           "Good" if avg_ats >= 60 else "Needs Work")
                    render_clean_html(f"""
                        <div style="text-align:center;margin-top:-8px;margin-bottom:12px;">
                            <span style="background:rgba(79,140,255,0.12);color:{ACCENT};
                                         font-size:11.5px;font-weight:700;padding:4px 14px;
                                         border-radius:9999px;">{lbl}</span>
                        </div>
                    """)
                else:
                    _empty_chart("ATS score will appear<br>after your first analysis.")
            _chart_card("ATS Score Performance", _gauge_body)

        # RIGHT — Skill Distribution
        with g1r:
            def _skills_body():
                if skills_dist:
                    cats   = [s[0] for s in skills_dist[:8]]
                    counts = [s[1] for s in skills_dist[:8]]
                else:
                    cats, counts = [], []

                if cats:
                    fig = go.Figure(go.Bar(
                        y=cats, x=counts, orientation="h",
                        marker=dict(
                            color=counts,
                            colorscale=[[0, "rgba(79,140,255,0.5)"], [1, "#4F8CFF"]],
                            showscale=False
                        ),
                        text=counts, textposition="auto",
                        textfont=dict(color=PRIMARY, size=11),
                    ))
                    fig.update_layout(**CHART_LAYOUT, height=280,
                        xaxis=dict(**AXIS_STYLE, tickfont=dict(color=MUTED)),
                        yaxis=dict(showgrid=False, tickfont=dict(color=PRIMARY, size=11)),
                    )
                    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
                else:
                    _empty_chart("Analyze your first resume<br>to view skill distribution.")
            _chart_card("Skill Distribution", _skills_body)

        render_clean_html('<div style="height:24px;"></div>')

        # ── 4. SECOND ANALYTICS ROW ──────────────────────────────────────────
        g2l, g2r = st.columns(2, gap="medium")

        # LEFT — Weekly Activity line chart
        with g2l:
            def _weekly_body():
                if weekly_act:
                    labels = [x[0] for x in weekly_act]
                    values = [x[1] for x in weekly_act]
                else:
                    labels = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
                    values = [0] * 7

                has_data = any(v > 0 for v in values)
                line_color = ACCENT if has_data else MUTED
                fill_color = "rgba(79,140,255,0.08)" if has_data else "rgba(107,114,128,0.04)"

                fig = go.Figure(go.Scatter(
                    x=labels, y=values,
                    mode="lines+markers",
                    line=dict(color=line_color, width=2.5, shape="spline"),
                    marker=dict(size=7, color=line_color,
                                line=dict(color=SURFACE, width=2)),
                    fill="tozeroy", fillcolor=fill_color,
                ))
                ymax = max(2, max(values) + 1) if values else 2
                fig.update_layout(**CHART_LAYOUT, height=250,
                    xaxis=dict(**AXIS_STYLE, tickfont=dict(color=MUTED)),
                    yaxis=dict(**AXIS_STYLE, tickfont=dict(color=MUTED),
                               range=[0, ymax], dtick=1),
                )
                st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
                if not has_data:
                    render_clean_html(f"""
                        <div style="text-align:center;font-size:12px;color:{MUTED};margin-top:-8px;margin-bottom:12px;">
                            No activity in the last 7 days.
                        </div>
                    """)
            _chart_card("Weekly Analysis Activity", _weekly_body)

        # RIGHT — ATS by Target Role
        with g2r:
            def _roles_body():
                if role_perf:
                    roles  = [r[0][:22] for r in role_perf[:6]]
                    scores = [r[1] for r in role_perf[:6]]
                    colors = [_score_color(s) for s in scores]
                    fig = go.Figure(go.Bar(
                        x=roles, y=scores,
                        marker=dict(color=colors, opacity=0.85),
                        text=[f"{s}" for s in scores],
                        textposition="auto",
                        textfont=dict(color=PRIMARY, size=11),
                    ))
                    fig.update_layout(**CHART_LAYOUT, height=250,
                        xaxis=dict(showgrid=False, tickfont=dict(color=PRIMARY, size=10)),
                        yaxis=dict(**AXIS_STYLE, tickfont=dict(color=MUTED), range=[0, 105]),
                    )
                    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
                else:
                    _empty_chart("No role performance data yet.<br>Target specific roles when analyzing.")
            _chart_card("ATS Performance by Target Role", _roles_body)

        # ── 5. KEY INSIGHTS ──────────────────────────────────────────────────
        _section_header("Key Insights")
        ins1, ins2 = st.columns(2, gap="medium")

        with ins1:
            if top_role:
                rname, rscore, rcount = top_role
                sc = _score_color(rscore)
                render_clean_html(f"""
                    <div style="background:{SURFACE};border:1px solid {BORDER};border-radius:16px;padding:24px;height:100%;box-sizing:border-box;">
                        <div style="font-size:10px;font-weight:700;color:{ACCENT};text-transform:uppercase;letter-spacing:0.12em;margin-bottom:10px;">Top Performing Role</div>
                        <div style="font-size:20px;font-weight:700;color:{PRIMARY};margin-bottom:8px;">{rname}</div>
                        <div style="font-size:13.5px;color:{SECONDARY};margin-bottom:18px;line-height:1.55;">
                            Your resumes targeting <strong style="color:{PRIMARY};">{rname}</strong> have the strongest ATS performance
                            across {rcount} evaluation{"s" if rcount != 1 else ""}.
                        </div>
                        <div style="display:flex;align-items:center;gap:10px;">
                            <span style="background:rgba(52,211,153,0.12);color:{sc};font-size:12px;
                                         font-weight:700;padding:5px 14px;border-radius:9999px;">{rscore} avg ATS</span>
                            <div style="flex:1;height:4px;background:{BORDER};border-radius:9999px;">
                                <div style="width:{min(100,rscore)}%;height:100%;background:{sc};border-radius:9999px;"></div>
                            </div>
                        </div>
                    </div>
                """)
            else:
                render_clean_html(f"""
                    <div style="background:{SURFACE};border:1px solid {BORDER};border-radius:16px;padding:24px;height:100%;box-sizing:border-box;">
                        <div style="font-size:10px;font-weight:700;color:{MUTED};text-transform:uppercase;letter-spacing:0.12em;margin-bottom:10px;">Top Performing Role</div>
                        <div style="font-size:16px;font-weight:600;color:{PRIMARY};margin-bottom:8px;">No data yet</div>
                        <div style="font-size:13.5px;color:{SECONDARY};line-height:1.55;">
                            Analyze resumes targeting different roles to see which category performs best.
                        </div>
                    </div>
                """)

        with ins2:
            if avg_ats is not None:
                render_clean_html(f"""
                    <div style="background:{SURFACE};border:1px solid {BORDER};border-radius:16px;padding:24px;height:100%;box-sizing:border-box;">
                        <div style="font-size:10px;font-weight:700;color:{SUCCESS};text-transform:uppercase;letter-spacing:0.12em;margin-bottom:10px;">Weekly Trend</div>
                        <div style="font-size:20px;font-weight:700;color:{PRIMARY};margin-bottom:8px;">Active Baseline</div>
                        <div style="font-size:13.5px;color:{SECONDARY};margin-bottom:18px;line-height:1.55;">
                            Your current average ATS score is <strong style="color:{PRIMARY};">{avg_ats}</strong>.
                            Complete more analyses to track weekly improvement trends.
                        </div>
                        <span style="background:rgba(79,140,255,0.12);color:{ACCENT};font-size:12px;
                                     font-weight:700;padding:5px 14px;border-radius:9999px;">Baseline Established</span>
                    </div>
                """)
            else:
                render_clean_html(f"""
                    <div style="background:{SURFACE};border:1px solid {BORDER};border-radius:16px;padding:24px;height:100%;box-sizing:border-box;">
                        <div style="font-size:10px;font-weight:700;color:{MUTED};text-transform:uppercase;letter-spacing:0.12em;margin-bottom:10px;">Weekly Trend</div>
                        <div style="font-size:16px;font-weight:600;color:{PRIMARY};margin-bottom:8px;">Insufficient Data</div>
                        <div style="font-size:13.5px;color:{SECONDARY};line-height:1.55;">
                            Not enough historical data to calculate a trend. Complete your first resume evaluation to begin tracking.
                        </div>
                    </div>
                """)

        # ── 6. AI CAREER INSIGHT ─────────────────────────────────────────────
        _section_header("AI Career Insight")

        target_role_name = ctx.get("targetRole") or (top_role[0] if top_role else "your target role")
        gaps_list = ctx.get("identifiedGaps") or []
        gaps_text = ", ".join(gaps_list) if gaps_list else "key technical keywords"

        render_ai_insight(
            observation=(
                f"Resume performance for {target_role_name} shows a solid baseline structure, "
                f"but keyword evidence for {gaps_text} is underrepresented relative to top ATS benchmarks."
                if avg_ats is not None else
                "Upload and analyze your resume to receive personalized career intelligence observations."
            ),
            why_it_matters=(
                f"Roles targeting {target_role_name} weight explicit keyword alignment heavily in initial ATS parsing rounds. "
                "Missing terminology reduces match probability before a human ever reviews the document."
                if avg_ats is not None else
                "ATS systems score resumes before a recruiter sees them. "
                "Understanding your gap areas is the first step to improving your match rate."
            ),
            recommendation=(
                f"Incorporate measurable, specific achievements highlighting {gaps_text} "
                "in the experience and projects sections to increase ATS keyword density."
                if avg_ats is not None else
                "Start by uploading your resume to the Resume Analyzer. "
                "Your first analysis will generate a personalized recommendation set."
            ),
            action_label="Optimize Resume",
            action_key="dash_ai_insight_cta",
            action_page="resume_builder",
        )

        # ── 7. RECENT ANALYSIS ───────────────────────────────────────────────
        _section_header("Recent Analysis")

        if recent:
            rows_html = ""
            for item in recent:
                sc    = item["ats_score"]
                sc_color = _score_color(sc)
                rows_html += f"""
                    <tr style="border-bottom:1px solid rgba(255,255,255,0.04);">
                        <td style="padding:14px 20px;font-weight:600;color:{PRIMARY};font-size:13.5px;">{item['name']}</td>
                        <td style="padding:14px 20px;color:{SECONDARY};font-size:13px;">{item['target_role']}</td>
                        <td style="padding:14px 20px;">
                            <div style="display:inline-flex;align-items:center;gap:8px;">
                                <span style="font-size:14px;font-weight:700;color:{sc_color};">{sc}</span>
                                <div style="width:56px;height:4px;background:{BORDER};border-radius:9999px;">
                                    <div style="width:{min(100,sc)}%;height:100%;background:{sc_color};border-radius:9999px;"></div>
                                </div>
                            </div>
                        </td>
                        <td style="padding:14px 20px;color:{MUTED};font-size:12.5px;">{item['created_at']}</td>
                    </tr>
                """
            render_clean_html(f"""
                <div style="background:{SURFACE};border:1px solid {BORDER};border-radius:16px;overflow:hidden;margin-bottom:32px;">
                    <table style="width:100%;border-collapse:collapse;font-size:13.5px;">
                        <thead>
                            <tr style="background:rgba(255,255,255,0.025);border-bottom:1px solid {BORDER};">
                                <th style="padding:12px 20px;font-size:10.5px;font-weight:700;color:{MUTED};text-transform:uppercase;letter-spacing:0.09em;text-align:left;">Resume</th>
                                <th style="padding:12px 20px;font-size:10.5px;font-weight:700;color:{MUTED};text-transform:uppercase;letter-spacing:0.09em;text-align:left;">Target Role</th>
                                <th style="padding:12px 20px;font-size:10.5px;font-weight:700;color:{MUTED};text-transform:uppercase;letter-spacing:0.09em;text-align:left;">ATS Score</th>
                                <th style="padding:12px 20px;font-size:10.5px;font-weight:700;color:{MUTED};text-transform:uppercase;letter-spacing:0.09em;text-align:left;">Date</th>
                            </tr>
                        </thead>
                        <tbody>{rows_html}</tbody>
                    </table>
                </div>
            """)
        else:
            render_clean_html(f"""
                <div style="background:{SURFACE};border:1px solid {BORDER};border-radius:16px;
                            padding:48px 24px;text-align:center;margin-bottom:24px;">
                    <div style="font-size:15px;font-weight:600;color:{PRIMARY};margin-bottom:8px;">No resume analyses yet</div>
                    <div style="font-size:13.5px;color:{SECONDARY};max-width:460px;margin:0 auto 24px auto;line-height:1.55;">
                        Upload your resume to measure ATS compatibility, identify skill gaps, and unlock career intelligence.
                    </div>
                </div>
            """)
            c1, c2, c3 = st.columns([1, 1.4, 1])
            with c2:
                if st.button("Analyze Resume", type="primary", use_container_width=True, key="dash_recent_empty_cta"):
                    _nav("resume_analyzer")

        # ── 8. FOOTER ────────────────────────────────────────────────────────
        render_clean_html(f"""
            <div style="margin-top:48px;padding-top:20px;border-top:1px solid {BORDER};
                        display:flex;justify-content:space-between;align-items:center;
                        font-size:11.5px;color:{MUTED};flex-wrap:wrap;gap:8px;">
                <div>AiResuMind Pro v5.0 · Career Intelligence Dashboard</div>
                <div>All analytics operational</div>
            </div>
        """)

        render_clean_html("</div>")
