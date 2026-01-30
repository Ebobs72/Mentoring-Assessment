# NELFT Mentoring Skills Assessment

A Streamlit-based pre/post programme assessment tool for evaluating mentoring capability development.

## Overview

This application allows participants to complete self-assessments before and after a mentoring development programme, with automatic matching and comparison of results.

### Features

**For Participants:**
- Simple, mobile-friendly assessment form
- 12 capability statements rated on a 1-5 scale
- Post-programme reflective questions
- Immediate comparison feedback after completing post-assessment
- Personalised development suggestions

**For Administrators:**
- Dashboard with KPI metrics
- Cohort management
- Participant tracking (pre/post completion status)
- Score comparison and improvement analysis
- CSV export functionality

## File Structure

```
nelft-mentoring-streamlit/
├── app.py                      # Main participant assessment
├── data_manager.py             # Data storage and retrieval
├── requirements.txt            # Python dependencies
├── pages/
│   └── 1_Admin_Dashboard.py    # Admin dashboard
├── data/
│   ├── cohorts.json            # Cohort data (auto-created)
│   └── assessments.json        # Assessment submissions (auto-created)
├── .streamlit/
│   └── config.toml             # Streamlit configuration
└── README.md                   # This file
```

## Local Development

### Prerequisites
- Python 3.9 or higher
- pip

### Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/nelft-mentoring-assessment.git
cd nelft-mentoring-assessment
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
streamlit run app.py
```

5. Open your browser to `http://localhost:8501`

## Deployment to Streamlit Community Cloud

### Step 1: Push to GitHub

1. Create a new GitHub repository
2. Push all files to the repository:
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/yourusername/nelft-mentoring-assessment.git
git push -u origin main
```

### Step 2: Deploy on Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io/)
2. Sign in with your GitHub account
3. Click "New app"
4. Select your repository, branch (main), and main file (app.py)
5. Click "Deploy"

Your app will be available at: `https://yourusername-nelft-mentoring-assessment-app-xxxxx.streamlit.app`

### Step 3: Configure Admin Access

The default admin password is `progress2025`. To change this:

1. In Streamlit Cloud, go to your app's settings
2. Add a secret called `ADMIN_PASSWORD` with your new password
3. Update `pages/1_Admin_Dashboard.py` to read from secrets:

```python
# Replace the hardcoded password check with:
if password == st.secrets.get("ADMIN_PASSWORD", "progress2025"):
```

## Usage

### For Programme Coordinators

1. **Before Programme Starts:**
   - Access the admin dashboard (click "Admin Dashboard" in sidebar)
   - Login with the admin password
   - Create a cohort if needed (Cohorts > Add New Cohort)
   - Share the main app URL with participants
   - Instruct them to select "Pre-Programme" assessment

2. **After Programme Ends:**
   - Share the same URL
   - Instruct participants to select "Post-Programme" assessment
   - The system automatically matches using their email

3. **Reporting:**
   - View completion status in the admin dashboard
   - Export data via the Participants page
   - View KPI summary in Reports

### For Participants

1. Click the assessment link provided by your programme coordinator
2. Enter your name and email (use the same email for both assessments)
3. Select your cohort and whether this is pre or post programme
4. Rate each statement honestly - there are no right or wrong answers
5. Submit your assessment
6. After completing the post-programme assessment, you'll see a comparison

## KPI Measurement

**Improvement Definition:**
- A participant shows improvement when the majority (7 or more) of the 12 capability statements increase by at least 1 point

**KPI Target:**
- 80% or more of participants demonstrate improvement

## Data Storage

Data is stored in JSON files in the `data/` directory:
- `cohorts.json` - Programme cohorts
- `assessments.json` - All assessment submissions

**Note:** On Streamlit Community Cloud, data persists only within a session. For production use with persistent data, consider:
- Connecting to a Google Sheet
- Using a database (PostgreSQL, MongoDB)
- Using Streamlit's built-in data connections

## Customisation

### Modifying Questions

Edit the `QUESTIONS` list in `data_manager.py` to change capability statements.

### Modifying Development Suggestions

Edit the `DEVELOPMENT_SUGGESTIONS` dict in `data_manager.py`.

### Styling

Edit `.streamlit/config.toml` to change colours and theme.

## Support

For technical issues, contact the development team.
For programme-related queries, contact Progress International.

---

Delivered in partnership with Progress International
