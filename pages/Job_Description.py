# Recruiting_App.py
from flask import Blueprint, render_template_string

recruiting_app_bp = Blueprint('recruiting_app', __name__)

@recruiting_app_bp.route('/recruiting_app', methods=['GET', 'POST'])
def recruiting_app():
    job_title = "Software Engineer"
    questions = [
        f"What are the key responsibilities for a {job_title}?",
        f"What skills are absolutely necessary for a {job_title}?",
        f"What benefits can attract top talent for the {job_title} role?",
    ]
    
    # Example placeholder data for answers
    answers = {
        "responsibilities": [
            "Manage team operations",
            "Ensure project deadlines are met",
            "Collaborate with stakeholders"
        ],
        "skills": [
            "Leadership",
            "Time Management",
            "Critical Thinking"
        ],
        "benefits": [
            "Flexible Work Hours",
            "Competitive Salary",
            "Health Insurance"
        ]
    }
    
    return render_template_string('''
    <div class="recruiting-app-content">
        <h1>Recruitment Analysis for {{ job_title }}</h1>
        <h2>Key Questions</h2>
        <ul>
            {% for question in questions %}
                <li>{{ question }}</li>
            {% endfor %}
        </ul>
        <h2>Responsibilities</h2>
        <ul>
            {% for responsibility in answers['responsibilities'] %}
                <li>{{ responsibility }}</li>
            {% endfor %}
        </ul>
        <h2>Skills</h2>
        <ul>
            {% for skill in answers['skills'] %}
                <li>{{ skill }}</li>
            {% endfor %}
        </ul>
        <h2>Benefits</h2>
        <ul>
            {% for benefit in answers['benefits'] %}
                <li>{{ benefit }}</li>
            {% endfor %}
        </ul>
    </div>
    ''', job_title=job_title, questions=questions, answers=answers)
