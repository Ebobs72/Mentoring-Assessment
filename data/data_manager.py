"""
Data management for NELFT Mentoring Assessment
Handles storage and retrieval of cohorts and assessments
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Optional
import streamlit as st

# Data directory
DATA_DIR = Path(__file__).parent / "data"
COHORTS_FILE = DATA_DIR / "cohorts.json"
ASSESSMENTS_FILE = DATA_DIR / "assessments.json"

# Ensure data directory exists
DATA_DIR.mkdir(exist_ok=True)


def load_cohorts() -> list[dict]:
    """Load all cohorts from storage"""
    if not COHORTS_FILE.exists():
        # Create default cohorts
        default_cohorts = [
            {
                "id": "cohort-1",
                "name": "March 2025",
                "active": True,
                "start_date": "2025-03-01"
            },
            {
                "id": "cohort-2", 
                "name": "June 2025",
                "active": True,
                "start_date": "2025-06-01"
            },
            {
                "id": "cohort-3",
                "name": "September 2025",
                "active": True,
                "start_date": "2025-09-01"
            }
        ]
        save_cohorts(default_cohorts)
        return default_cohorts
    
    with open(COHORTS_FILE, "r") as f:
        return json.load(f)


def save_cohorts(cohorts: list[dict]) -> None:
    """Save cohorts to storage"""
    with open(COHORTS_FILE, "w") as f:
        json.dump(cohorts, f, indent=2)


def add_cohort(name: str, start_date: str) -> dict:
    """Add a new cohort"""
    cohorts = load_cohorts()
    new_cohort = {
        "id": f"cohort-{len(cohorts) + 1}",
        "name": name,
        "active": True,
        "start_date": start_date
    }
    cohorts.append(new_cohort)
    save_cohorts(cohorts)
    return new_cohort


def get_active_cohorts() -> list[dict]:
    """Get only active cohorts"""
    return [c for c in load_cohorts() if c.get("active", True)]


def load_assessments() -> list[dict]:
    """Load all assessments from storage"""
    if not ASSESSMENTS_FILE.exists():
        save_assessments([])
        return []
    
    with open(ASSESSMENTS_FILE, "r") as f:
        return json.load(f)


def save_assessments(assessments: list[dict]) -> None:
    """Save assessments to storage"""
    with open(ASSESSMENTS_FILE, "w") as f:
        json.dump(assessments, f, indent=2)


def add_assessment(assessment: dict) -> dict:
    """Add a new assessment submission"""
    assessments = load_assessments()
    
    # Add metadata
    assessment["id"] = f"assessment-{len(assessments) + 1}"
    assessment["submitted_at"] = datetime.now().isoformat()
    
    # Calculate average score
    responses = assessment.get("responses", {})
    if responses:
        assessment["average_score"] = sum(responses.values()) / len(responses)
    
    assessments.append(assessment)
    save_assessments(assessments)
    return assessment


def find_pre_assessment(email: str, cohort: str) -> Optional[dict]:
    """Find a pre-assessment for matching"""
    assessments = load_assessments()
    email_lower = email.lower().strip()
    
    for a in assessments:
        if (a.get("email", "").lower().strip() == email_lower and 
            a.get("cohort") == cohort and 
            a.get("assessment_type") == "pre"):
            return a
    
    return None


def get_assessments_by_cohort(cohort_id: str) -> list[dict]:
    """Get all assessments for a specific cohort"""
    return [a for a in load_assessments() if a.get("cohort") == cohort_id]


def get_participant_data() -> list[dict]:
    """Build participant list with pre/post matching"""
    assessments = load_assessments()
    participants = {}
    
    for a in assessments:
        key = f"{a.get('email', '').lower().strip()}-{a.get('cohort')}"
        
        if key not in participants:
            participants[key] = {
                "name": a.get("name"),
                "email": a.get("email"),
                "cohort": a.get("cohort"),
                "pre_assessment": None,
                "post_assessment": None
            }
        
        if a.get("assessment_type") == "pre":
            participants[key]["pre_assessment"] = a
        else:
            participants[key]["post_assessment"] = a
    
    return list(participants.values())


# Questions data
QUESTIONS = [
    {
        "id": 1,
        "text": "I understand the purpose and role of mentoring, and how it differs from coaching, managing or advising.",
        "category": "Foundation"
    },
    {
        "id": 2,
        "text": "I am able to establish clear boundaries and confidentiality within a mentoring relationship.",
        "category": "Contracting"
    },
    {
        "id": 3,
        "text": "I can contract effectively at the start of a mentoring relationship, including agreeing expectations, goals and ways of working.",
        "category": "Contracting"
    },
    {
        "id": 4,
        "text": "I use open, exploratory questions to encourage reflection and insight.",
        "category": "Core Skills"
    },
    {
        "id": 5,
        "text": "I listen actively and am able to summarise and reflect back what I hear to deepen understanding.",
        "category": "Core Skills"
    },
    {
        "id": 6,
        "text": "I can balance support and challenge appropriately to help the mentee think differently.",
        "category": "Core Skills"
    },
    {
        "id": 7,
        "text": "I avoid giving solutions and instead facilitate the mentee to generate their own options.",
        "category": "Core Skills"
    },
    {
        "id": 8,
        "text": "I am able to manage silence and pace in mentoring conversations effectively.",
        "category": "Advanced Skills"
    },
    {
        "id": 9,
        "text": "I can recognise when an issue is outside the scope of mentoring and respond appropriately.",
        "category": "Judgement"
    },
    {
        "id": 10,
        "text": "I am confident in maintaining focus on the mentee's goals and development, even when conversations feel complex.",
        "category": "Advanced Skills"
    },
    {
        "id": 11,
        "text": "I can encourage accountability and follow-through without becoming directive.",
        "category": "Advanced Skills"
    },
    {
        "id": 12,
        "text": "I feel confident in my ability to build trust and rapport within a mentoring relationship.",
        "category": "Relationship"
    }
]

RATING_LABELS = {
    1: "Not confident",
    2: "Slightly confident", 
    3: "Moderately confident",
    4: "Confident",
    5: "Highly confident"
}

DEVELOPMENT_SUGGESTIONS = {
    "Foundation": [
        "Explore the EMCC (European Mentoring and Coaching Council) competency framework for mentoring",
        "Reflect on the differences between mentoring, coaching, and managing in your own experience",
        "Consider how your role as a mentor differs from your day-to-day professional role"
    ],
    "Contracting": [
        "Develop a personal contracting checklist for the start of mentoring relationships",
        "Practice having explicit conversations about confidentiality and its limits",
        "Create a simple agreement template that covers expectations and ways of working"
    ],
    "Core Skills": [
        "Build a bank of powerful open questions to draw on in mentoring conversations",
        "Practice summarising and reflecting back in everyday conversations",
        "Notice when you feel the urge to give advice, and pause to ask a question instead"
    ],
    "Advanced Skills": [
        "Experiment with allowing longer silences in conversations and observe what emerges",
        "Develop strategies for bringing conversations back to the mentee's stated goals",
        "Practice holding people accountable through questions rather than instructions"
    ],
    "Judgement": [
        "Familiarise yourself with available support services and referral pathways",
        "Develop your awareness of the boundaries of your competence and role",
        "Create a personal decision tree for when to refer or signpost"
    ],
    "Relationship": [
        "Reflect on what helps you build trust with others, and how this applies to mentoring",
        "Consider how you demonstrate warmth and positive regard while maintaining boundaries",
        "Seek feedback from mentees on what helps them feel supported"
    ]
}
