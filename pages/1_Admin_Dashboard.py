"""
NELFT Mentoring Skills Assessment
Admin Dashboard
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from data_manager import (
    QUESTIONS, load_cohorts, save_cohorts, add_cohort,
    load_assessments, get_participant_data
)

# Page configuration
st.set_page_config(
    page_title="Admin Dashboard | Mentoring Assessment",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Simple password protection
def check_password():
    """Simple password check for admin access"""
    if "admin_authenticated" not in st.session_state:
        st.session_state.admin_authenticated = False
    
    if not st.session_state.admin_authenticated:
        st.title("🔐 Admin Login")
        st.write("Please enter the administrator password to access the dashboard.")
        
        password = st.text_input("Password", type="password")
        
        if st.button("Login", type="primary"):
            # Default password - should be changed in production
            if password == "progress2025":
                st.session_state.admin_authenticated = True
                st.rerun()
            else:
                st.error("Incorrect password")
        
        st.info("For demo purposes, use password: `progress2025`")
        return False
    
    return True


def calculate_kpis(participants, selected_cohort=None):
    """Calculate key performance indicators"""
    if selected_cohort:
        participants = [p for p in participants if p["cohort"] == selected_cohort]
    
    total = len(participants)
    complete = len([p for p in participants if p["pre_assessment"] and p["post_assessment"]])
    pre_only = len([p for p in participants if p["pre_assessment"] and not p["post_assessment"]])
    
    completion_rate = (complete / total * 100) if total > 0 else 0
    
    # Calculate improvement
    total_improvement = 0
    improved_count = 0
    
    for p in participants:
        if p["pre_assessment"] and p["post_assessment"]:
            pre_avg = p["pre_assessment"].get("average_score", 0)
            post_avg = p["post_assessment"].get("average_score", 0)
            total_improvement += post_avg - pre_avg
            
            # Check if majority of questions improved
            questions_improved = 0
            for q in QUESTIONS:
                pre_score = p["pre_assessment"].get("responses", {}).get(q["id"], 0)
                post_score = p["post_assessment"].get("responses", {}).get(q["id"], 0)
                if post_score > pre_score:
                    questions_improved += 1
            
            if questions_improved >= 7:
                improved_count += 1
    
    avg_improvement = total_improvement / complete if complete > 0 else 0
    kpi_achievement = (improved_count / complete * 100) if complete > 0 else 0
    
    return {
        "total_participants": total,
        "complete": complete,
        "pre_only": pre_only,
        "completion_rate": completion_rate,
        "avg_improvement": avg_improvement,
        "kpi_achievement": kpi_achievement,
        "improved_count": improved_count
    }


def show_overview(participants, cohorts, selected_cohort):
    """Display overview dashboard"""
    st.header("📊 Overview")
    
    kpis = calculate_kpis(participants, selected_cohort)
    
    # KPI Cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total Participants",
            kpis["total_participants"]
        )
    
    with col2:
        st.metric(
            "Completion Rate",
            f"{kpis['completion_rate']:.0f}%",
            help="Participants who completed both pre and post assessments"
        )
    
    with col3:
        st.metric(
            "Avg. Score Improvement",
            f"{kpis['avg_improvement']:+.2f}",
            help="Average change in score from pre to post"
        )
    
    with col4:
        kpi_color = "normal" if kpis["kpi_achievement"] >= 80 else "off"
        st.metric(
            "KPI Achievement",
            f"{kpis['kpi_achievement']:.0f}%",
            delta=f"{'✓ Target met' if kpis['kpi_achievement'] >= 80 else '✗ Below 80% target'}",
            delta_color=kpi_color,
            help="% of participants showing improvement in majority of questions"
        )
    
    st.markdown("---")
    
    # Charts
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Score Distribution by Question")
        
        # Filter assessments by cohort
        assessments = load_assessments()
        if selected_cohort:
            assessments = [a for a in assessments if a["cohort"] == selected_cohort]
        
        # Calculate averages per question
        chart_data = []
        for q in QUESTIONS:
            pre_scores = [a["responses"].get(q["id"], 0) for a in assessments if a["assessment_type"] == "pre"]
            post_scores = [a["responses"].get(q["id"], 0) for a in assessments if a["assessment_type"] == "post"]
            
            pre_avg = sum(pre_scores) / len(pre_scores) if pre_scores else 0
            post_avg = sum(post_scores) / len(post_scores) if post_scores else 0
            
            chart_data.append({"Question": f"Q{q['id']}", "Pre-Programme": pre_avg, "Post-Programme": post_avg})
        
        df_chart = pd.DataFrame(chart_data)
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            name='Pre-Programme',
            x=df_chart['Question'],
            y=df_chart['Pre-Programme'],
            marker_color='#4a7ab0'
        ))
        fig.add_trace(go.Bar(
            name='Post-Programme',
            x=df_chart['Question'],
            y=df_chart['Post-Programme'],
            marker_color='#2a9d8f'
        ))
        
        fig.update_layout(
            barmode='group',
            yaxis_title='Average Score',
            yaxis_range=[0, 5],
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            margin=dict(l=0, r=0, t=30, b=0),
            height=350
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Completion Status")
        
        status_data = pd.DataFrame({
            'Status': ['Complete', 'Pre Only'],
            'Count': [kpis['complete'], kpis['pre_only']]
        })
        
        fig = px.pie(
            status_data,
            values='Count',
            names='Status',
            color='Status',
            color_discrete_map={'Complete': '#22c55e', 'Pre Only': '#94a3b8'},
            hole=0.4
        )
        fig.update_layout(
            margin=dict(l=0, r=0, t=30, b=0),
            height=350,
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=-0.2)
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Recent submissions
    st.markdown("---")
    st.subheader("Recent Submissions")
    
    assessments = load_assessments()
    if selected_cohort:
        assessments = [a for a in assessments if a["cohort"] == selected_cohort]
    
    # Sort by date and take most recent
    assessments_sorted = sorted(assessments, key=lambda x: x.get("submitted_at", ""), reverse=True)[:10]
    
    if assessments_sorted:
        recent_data = []
        for a in assessments_sorted:
            cohort = next((c["name"] for c in cohorts if c["id"] == a["cohort"]), a["cohort"])
            cohort_short = cohort.split(" - ")[1] if " - " in cohort else cohort
            
            recent_data.append({
                "Name": a.get("name", ""),
                "Cohort": cohort_short,
                "Type": a.get("assessment_type", "").upper(),
                "Avg Score": f"{a.get('average_score', 0):.2f}",
                "Submitted": datetime.fromisoformat(a.get("submitted_at", "")).strftime("%d %b %Y") if a.get("submitted_at") else ""
            })
        
        st.dataframe(pd.DataFrame(recent_data), use_container_width=True, hide_index=True)
    else:
        st.info("No submissions yet.")


def show_cohorts(cohorts, participants):
    """Display cohort management"""
    st.header("👥 Cohort Management")
    
    # Add new cohort
    with st.expander("➕ Add New Cohort"):
        with st.form("add_cohort"):
            new_name = st.text_input("Cohort Name", placeholder="e.g., NELFT Mentoring Programme - Cohort 4 (January 2026)")
            new_date = st.date_input("Start Date")
            
            if st.form_submit_button("Add Cohort", type="primary"):
                if new_name.strip():
                    add_cohort(new_name.strip(), new_date.isoformat())
                    st.success(f"Added cohort: {new_name}")
                    st.rerun()
                else:
                    st.error("Please enter a cohort name")
    
    # Display cohorts
    st.markdown("---")
    
    cols = st.columns(3)
    
    for i, cohort in enumerate(cohorts):
        cohort_participants = [p for p in participants if p["cohort"] == cohort["id"]]
        complete = len([p for p in cohort_participants if p["pre_assessment"] and p["post_assessment"]])
        pre_only = len([p for p in cohort_participants if p["pre_assessment"] and not p["post_assessment"]])
        
        with cols[i % 3]:
            with st.container(border=True):
                st.markdown(f"**{cohort['name']}**")
                st.caption(f"{'Active' if cohort.get('active', True) else 'Inactive'}")
                
                col1, col2, col3 = st.columns(3)
                col1.metric("Total", len(cohort_participants))
                col2.metric("Complete", complete)
                col3.metric("Pending", pre_only)


def show_participants(participants, cohorts, selected_cohort):
    """Display participant list"""
    st.header("👤 Participants")
    
    # Filters
    col1, col2 = st.columns(2)
    with col2:
        status_filter = st.selectbox(
            "Filter by Status",
            options=["All", "Complete", "Pre Only"],
            key="participant_status_filter"
        )
    
    # Filter data
    filtered = participants
    if selected_cohort:
        filtered = [p for p in filtered if p["cohort"] == selected_cohort]
    
    if status_filter == "Complete":
        filtered = [p for p in filtered if p["pre_assessment"] and p["post_assessment"]]
    elif status_filter == "Pre Only":
        filtered = [p for p in filtered if p["pre_assessment"] and not p["post_assessment"]]
    
    # Build table data
    table_data = []
    for p in filtered:
        cohort = next((c["name"] for c in cohorts if c["id"] == p["cohort"]), p["cohort"])
        cohort_short = cohort.split(" - ")[1] if " - " in cohort else cohort
        
        pre_score = p["pre_assessment"].get("average_score", 0) if p["pre_assessment"] else None
        post_score = p["post_assessment"].get("average_score", 0) if p["post_assessment"] else None
        
        change = None
        if pre_score is not None and post_score is not None:
            change = post_score - pre_score
        
        table_data.append({
            "Name": p.get("name", ""),
            "Email": p.get("email", ""),
            "Cohort": cohort_short,
            "Pre Score": f"{pre_score:.2f}" if pre_score else "—",
            "Post Score": f"{post_score:.2f}" if post_score else "—",
            "Change": f"{change:+.2f}" if change is not None else "—"
        })
    
    if table_data:
        df = pd.DataFrame(table_data)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # Export button
        csv = df.to_csv(index=False)
        st.download_button(
            "📥 Export to CSV",
            csv,
            "participants_export.csv",
            "text/csv",
            use_container_width=False
        )
    else:
        st.info("No participants match the current filters.")


def show_reports(participants, cohorts, selected_cohort):
    """Display reports section"""
    st.header("📈 Reports")
    
    kpis = calculate_kpis(participants, selected_cohort)
    
    col1, col2 = st.columns(2)
    
    with col1:
        with st.container(border=True):
            st.subheader("📋 KPI Summary Report")
            st.write("Programme effectiveness metrics for governance and procurement reporting.")
            
            st.markdown(f"""
            **Programme Statistics:**
            - Total Participants: {kpis['total_participants']}
            - Completed Both Assessments: {kpis['complete']}
            - Completion Rate: {kpis['completion_rate']:.1f}%
            
            **Improvement Metrics:**
            - Average Score Improvement: {kpis['avg_improvement']:+.2f}
            - Participants Showing Improvement: {kpis['improved_count']}
            - KPI Achievement: {kpis['kpi_achievement']:.1f}%
            
            **Target:** 80% of participants show improvement in majority of questions
            
            **Status:** {'✅ TARGET MET' if kpis['kpi_achievement'] >= 80 else '⚠️ BELOW TARGET'}
            """)
    
    with col2:
        with st.container(border=True):
            st.subheader("📊 Question Analysis")
            st.write("Detailed breakdown of responses by capability statement.")
            
            assessments = load_assessments()
            if selected_cohort:
                assessments = [a for a in assessments if a["cohort"] == selected_cohort]
            
            analysis_data = []
            for q in QUESTIONS:
                pre_scores = [a["responses"].get(q["id"], 0) for a in assessments if a["assessment_type"] == "pre"]
                post_scores = [a["responses"].get(q["id"], 0) for a in assessments if a["assessment_type"] == "post"]
                
                pre_avg = sum(pre_scores) / len(pre_scores) if pre_scores else 0
                post_avg = sum(post_scores) / len(post_scores) if post_scores else 0
                
                analysis_data.append({
                    "Q": q["id"],
                    "Category": q["category"],
                    "Pre": f"{pre_avg:.2f}",
                    "Post": f"{post_avg:.2f}",
                    "Δ": f"{post_avg - pre_avg:+.2f}"
                })
            
            st.dataframe(pd.DataFrame(analysis_data), use_container_width=True, hide_index=True)


def main():
    """Main admin dashboard"""
    if not check_password():
        return
    
    st.title("📊 Assessment Dashboard")
    
    # Load data
    cohorts = load_cohorts()
    participants = get_participant_data()
    
    # Sidebar
    st.sidebar.header("Filters")
    
    cohort_options = {"All Cohorts": None}
    cohort_options.update({c["name"]: c["id"] for c in cohorts})
    
    selected_cohort_name = st.sidebar.selectbox(
        "Cohort",
        options=list(cohort_options.keys())
    )
    selected_cohort = cohort_options[selected_cohort_name]
    
    st.sidebar.markdown("---")
    
    # Navigation
    page = st.sidebar.radio(
        "Navigation",
        options=["Overview", "Cohorts", "Participants", "Reports"]
    )
    
    st.sidebar.markdown("---")
    
    if st.sidebar.button("🔄 Refresh Data"):
        st.rerun()
    
    if st.sidebar.button("🚪 Logout"):
        st.session_state.admin_authenticated = False
        st.rerun()
    
    st.sidebar.markdown("---")
    st.sidebar.caption("Progress International")
    
    # Route to page
    if page == "Overview":
        show_overview(participants, cohorts, selected_cohort)
    elif page == "Cohorts":
        show_cohorts(cohorts, participants)
    elif page == "Participants":
        show_participants(participants, cohorts, selected_cohort)
    elif page == "Reports":
        show_reports(participants, cohorts, selected_cohort)


if __name__ == "__main__":
    main()
