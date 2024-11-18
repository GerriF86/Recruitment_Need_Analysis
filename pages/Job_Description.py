# Job_Description.py
from flask import Blueprint, render_template_string

job_description_bp = Blueprint('job_description', __name__)

@job_description_bp.route('/job_description')
def job_description():
    # Placeholder data for demonstration
    role = "Software Engineer"
    skills = ["Python", "Machine Learning", "APIs"]
    benefits = ["Health Insurance", "Flexible Work Hours", "Gym Membership"]
    
    return render_template_string('''
    <div class="job-description-content">
        <h1>Job Description for {{ role }}</h1>
        <h2>Key Skills</h2>
        <ul>
            {% for skill in skills %}
                <li>{{ skill }}</li>
            {% endfor %}
        </ul>
        <h2>Benefits</h2>
        <ul>
            {% for benefit in benefits %}
                <li>{{ benefit }}</li>
            {% endfor %}
        </ul>
    </div>
    ''', role=role, skills=skills, benefits=benefits)
