"""
NELFT Mentoring Skills Assessment
Main participant assessment application
"""

import streamlit as st
from data_manager import (
    QUESTIONS, RATING_LABELS, DEVELOPMENT_SUGGESTIONS,
    get_active_cohorts, add_assessment, find_pre_assessment
)

# Page configuration
st.set_page_config(
    page_title="Mentoring Skills Assessment",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for Progress International aesthetic
st.markdown("""
<style>
    /* Constrain main content width for readability while using wide layout */
    .block-container {
        max-width: 1000px;
        padding-left: 2rem;
        padding-right: 2rem;
    }
    
    /* Make radio buttons more compact */
    .stRadio > div {
        gap: 0.5rem;
    }
    
    /* Main styling */
    .main-header {
        text-align: center;
        padding: 2rem 0;
        border-bottom: 3px solid #2c5282;
        margin-bottom: 2rem;
    }
    
    .main-header h1 {
        color: #1a3a5c;
        font-size: 2rem;
        margin-bottom: 0.5rem;
    }
    
    .main-header p {
        color: #64748b;
        font-size: 1.1rem;
    }
    
    /* Info box */
    .info-box {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 1.5rem;
        margin: 1.5rem 0;
    }
    
    .info-box h4 {
        color: #1a3a5c;
        margin-bottom: 1rem;
    }
    
    /* Question cards */
    .question-card {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 1.25rem;
        margin-bottom: 1rem;
        transition: all 0.2s;
    }
    
    .question-card:hover {
        border-color: #cbd5e1;
    }
    
    .question-number {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 28px;
        height: 28px;
        background: #2c5282;
        color: white;
        border-radius: 50%;
        font-size: 0.875rem;
        font-weight: 600;
        margin-right: 0.75rem;
    }
    
    .question-text {
        color: #334155;
        font-weight: 500;
        line-height: 1.5;
    }
    
    /* Rating scale legend */
    .rating-legend {
        background: #e6f5f3;
        border-radius: 8px;
        padding: 1rem;
        margin: 1.5rem 0;
        display: flex;
        flex-wrap: wrap;
        gap: 1rem;
        justify-content: center;
    }
    
    .legend-item {
        font-size: 0.875rem;
        color: #475569;
    }
    
    .legend-number {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 22px;
        height: 22px;
        background: #2a9d8f;
        color: white;
        border-radius: 50%;
        font-size: 0.75rem;
        font-weight: 600;
        margin-right: 0.25rem;
    }
    
    /* Comparison table */
    .comparison-header {
        text-align: center;
        margin: 2rem 0 1rem;
    }
    
    .score-improved {
        color: #22c55e;
        font-weight: 600;
    }
    
    .score-declined {
        color: #ef4444;
        font-weight: 600;
    }
    
    .score-same {
        color: #64748b;
    }
    
    /* Summary stats */
    .stats-row {
        display: flex;
        justify-content: space-around;
        margin: 1.5rem 0;
        gap: 1rem;
    }
    
    .stat-box {
        text-align: center;
        background: #f8fafc;
        border-radius: 8px;
        padding: 1.25rem;
        flex: 1;
    }
    
    .stat-value {
        font-size: 1.75rem;
        font-weight: 700;
        color: #2c5282;
    }
    
    .stat-label {
        font-size: 0.875rem;
        color: #64748b;
        margin-top: 0.25rem;
    }
    
    /* Suggestions box */
    .suggestions-box {
        background: #e6f5f3;
        border-radius: 8px;
        padding: 1.5rem;
        margin: 1.5rem 0;
    }
    
    .suggestions-box h4 {
        color: #2a9d8f;
        margin-bottom: 1rem;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem 0;
        color: #64748b;
        font-size: 0.875rem;
        border-top: 1px solid #e2e8f0;
        margin-top: 3rem;
    }
    
    /* Success message */
    .success-box {
        background: #dcfce7;
        border: 1px solid #22c55e;
        border-radius: 8px;
        padding: 2rem;
        text-align: center;
        margin: 2rem 0;
    }
    
    .success-box h2 {
        color: #22c55e;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)


def show_welcome():
    """Display welcome screen"""
    st.markdown("""
    <div class="main-header">
        <h1>📋 Mentoring Skills Assessment</h1>
        <p>Pre and Post Programme Self-Assessment</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("""
    Welcome to the mentoring skills assessment. This short questionnaire will help 
    evaluate your development over the course of the mentoring programme.
    """)
    
    st.markdown("""
    <div class="info-box">
        <h4>Before you begin</h4>
        <ul>
            <li>There are no right or wrong answers</li>
            <li>Rate your current level of confidence and capability</li>
            <li>The assessment takes approximately 5-7 minutes</li>
            <li>Your responses help measure programme effectiveness</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("Begin Assessment", type="primary", use_container_width=True):
        st.session_state.step = "details"
        st.rerun()


def show_participant_details():
    """Collect participant details"""
    st.markdown("""
    <div class="main-header">
        <h1>📋 Your Details</h1>
        <p>Step 1 of 3</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("Please enter your information below. This allows us to match your pre and post programme assessments.")
    
    with st.form("participant_details"):
        name = st.text_input("Full Name", placeholder="Enter your full name")
        email = st.text_input("Email Address", placeholder="Enter your email address")
        
        cohorts = get_active_cohorts()
        cohort_options = {c["name"]: c["id"] for c in cohorts}
        selected_cohort_name = st.selectbox(
            "Programme Cohort",
            options=["Select your cohort..."] + list(cohort_options.keys())
        )
        
        assessment_type = st.radio(
            "Assessment Type",
            options=["Pre-Programme", "Post-Programme"],
            captions=[
                "Complete this before your first session",
                "Complete this after your final session"
            ]
        )
        
        col1, col2 = st.columns(2)
        with col1:
            back = st.form_submit_button("Back", use_container_width=True)
        with col2:
            submit = st.form_submit_button("Continue to Assessment", type="primary", use_container_width=True)
        
        if back:
            st.session_state.step = "welcome"
            st.rerun()
        
        if submit:
            # Validation
            if not name.strip():
                st.error("Please enter your name.")
            elif not email.strip() or "@" not in email:
                st.error("Please enter a valid email address.")
            elif selected_cohort_name == "Select your cohort...":
                st.error("Please select your cohort.")
            else:
                # Store in session
                st.session_state.participant = {
                    "name": name.strip(),
                    "email": email.strip().lower(),
                    "cohort": cohort_options[selected_cohort_name],
                    "cohort_name": selected_cohort_name,
                    "assessment_type": "pre" if assessment_type == "Pre-Programme" else "post"
                }
                
                # Check for pre-assessment if doing post
                if st.session_state.participant["assessment_type"] == "post":
                    pre = find_pre_assessment(
                        st.session_state.participant["email"],
                        st.session_state.participant["cohort"]
                    )
                    if pre:
                        st.session_state.pre_assessment = pre
                    else:
                        st.warning("We couldn't find a pre-programme assessment for this email and cohort. You can continue, but comparison data won't be available.")
                        st.session_state.pre_assessment = None
                
                st.session_state.step = "assessment"
                st.rerun()


def show_assessment():
    """Display the assessment questions"""
    st.markdown("""
    <div class="main-header">
        <h1>📋 Core Mentoring Capabilities</h1>
        <p>Step 2 of 3</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("Please rate your current level of confidence and capability for each statement below.")
    
    # Rating scale legend
    st.markdown("""
    <div class="rating-legend">
        <span class="legend-item"><span class="legend-number">1</span> Not confident</span>
        <span class="legend-item"><span class="legend-number">2</span> Slightly confident</span>
        <span class="legend-item"><span class="legend-number">3</span> Moderately confident</span>
        <span class="legend-item"><span class="legend-number">4</span> Confident</span>
        <span class="legend-item"><span class="legend-number">5</span> Highly confident</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize responses in session state
    if "responses" not in st.session_state:
        st.session_state.responses = {}
    
    with st.form("assessment_form"):
        responses = {}
        
        for q in QUESTIONS:
            st.markdown(f"""
            <div class="question-card">
                <span class="question-number">{q['id']}</span>
                <span class="question-text">{q['text']}</span>
            </div>
            """, unsafe_allow_html=True)
            
            responses[q["id"]] = st.radio(
                f"Q{q['id']} Rating",
                options=[1, 2, 3, 4, 5],
                format_func=lambda x: str(x),
                horizontal=True,
                key=f"q_{q['id']}",
                label_visibility="collapsed"
            )
        
        # Reflective questions for post-programme
        if st.session_state.participant.get("assessment_type") == "post":
            st.markdown("---")
            st.subheader("Reflective Questions")
            st.write("Please take a moment to reflect on your learning journey.")
            
            reflection1 = st.text_area(
                "What mentoring skills do you feel you have developed most through this programme?",
                placeholder="Share your thoughts...",
                key="reflection_1"
            )
            
            reflection2 = st.text_area(
                "What specific mentoring behaviours will you apply in your role going forward?",
                placeholder="Share your thoughts...",
                key="reflection_2"
            )
        else:
            reflection1 = ""
            reflection2 = ""
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        with col1:
            back = st.form_submit_button("Back", use_container_width=True)
        with col2:
            submit = st.form_submit_button("Submit Assessment", type="primary", use_container_width=True)
        
        if back:
            st.session_state.step = "details"
            st.rerun()
        
        if submit:
            # Build assessment record
            assessment = {
                "name": st.session_state.participant["name"],
                "email": st.session_state.participant["email"],
                "cohort": st.session_state.participant["cohort"],
                "assessment_type": st.session_state.participant["assessment_type"],
                "responses": responses,
                "reflections": {
                    "reflection1": reflection1,
                    "reflection2": reflection2
                }
            }
            
            # Save assessment
            saved = add_assessment(assessment)
            st.session_state.submitted_assessment = saved
            st.session_state.step = "confirmation"
            st.rerun()


def show_confirmation():
    """Show confirmation and comparison (for post-assessment)"""
    assessment = st.session_state.submitted_assessment
    is_post = assessment.get("assessment_type") == "post"
    pre_assessment = st.session_state.get("pre_assessment")
    
    st.markdown("""
    <div class="success-box">
        <h2>✓ Assessment Complete</h2>
        <p>Thank you for completing your assessment.</p>
    </div>
    """, unsafe_allow_html=True)
    
    if is_post and pre_assessment:
        # Show comparison
        st.markdown("<h3 class='comparison-header'>Your Development Journey</h3>", unsafe_allow_html=True)
        
        # Calculate stats
        pre_avg = pre_assessment.get("average_score", 0)
        post_avg = assessment.get("average_score", 0)
        improvement = post_avg - pre_avg
        
        # Count improved questions
        improved_count = 0
        for q in QUESTIONS:
            pre_score = pre_assessment.get("responses", {}).get(q["id"], 0)
            post_score = assessment.get("responses", {}).get(q["id"], 0)
            if post_score > pre_score:
                improved_count += 1
        
        # Summary stats
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Pre-Programme Average", f"{pre_avg:.2f}")
        with col2:
            st.metric("Post-Programme Average", f"{post_avg:.2f}")
        with col3:
            st.metric("Average Improvement", f"{improvement:+.2f}")
        
        # Detailed comparison table
        st.markdown("#### Score Comparison by Question")
        
        comparison_data = []
        for q in QUESTIONS:
            pre_score = pre_assessment.get("responses", {}).get(q["id"], 0)
            post_score = assessment.get("responses", {}).get(q["id"], 0)
            change = post_score - pre_score
            
            comparison_data.append({
                "Question": f"Q{q['id']}",
                "Statement": q["text"][:60] + "..." if len(q["text"]) > 60 else q["text"],
                "Pre": pre_score,
                "Post": post_score,
                "Change": f"+{change}" if change > 0 else str(change) if change < 0 else "—"
            })
        
        import pandas as pd
        df = pd.DataFrame(comparison_data)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # Development suggestions
        category_scores = {}
        for q in QUESTIONS:
            cat = q["category"]
            if cat not in category_scores:
                category_scores[cat] = {"total": 0, "count": 0}
            category_scores[cat]["total"] += assessment.get("responses", {}).get(q["id"], 0)
            category_scores[cat]["count"] += 1
        
        # Find lowest scoring categories
        category_averages = [
            (cat, data["total"] / data["count"]) 
            for cat, data in category_scores.items()
        ]
        category_averages.sort(key=lambda x: x[1])
        lowest_categories = category_averages[:2]
        
        st.markdown("""
        <div class="suggestions-box">
            <h4>💡 Continued Development Suggestions</h4>
            <p>Based on your responses, here are some areas for continued focus:</p>
        </div>
        """, unsafe_allow_html=True)
        
        for cat, _ in lowest_categories:
            suggestions = DEVELOPMENT_SUGGESTIONS.get(cat, [])
            for suggestion in suggestions[:2]:
                st.markdown(f"→ {suggestion}")
    
    elif is_post:
        st.info("Pre-programme comparison not available. Your post-programme scores have been recorded.")
        st.metric("Your Average Score", f"{assessment.get('average_score', 0):.2f}")
    
    else:
        st.write("""
        Your responses have been recorded. You will be asked to complete a post-programme 
        assessment after your final session, which will allow us to measure your development.
        """)
    
    st.markdown("""
    <div class="footer">
        <p>Delivered in partnership with Progress International</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("Start New Assessment", use_container_width=True):
        # Clear session state
        for key in ["step", "participant", "responses", "pre_assessment", "submitted_assessment"]:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()


# Main application flow
def main():
    # Initialize session state
    if "step" not in st.session_state:
        st.session_state.step = "welcome"
    
    # Route to appropriate screen
    if st.session_state.step == "welcome":
        show_welcome()
    elif st.session_state.step == "details":
        show_participant_details()
    elif st.session_state.step == "assessment":
        show_assessment()
    elif st.session_state.step == "confirmation":
        show_confirmation()


if __name__ == "__main__":
    main()
