# Role_Specific_Skills.py
from flask import Blueprint, render_template_string

role_specific_skills_bp = Blueprint('role_specific_skills', __name__)

@role_specific_skills_bp.route('/role_specific_skills')
def role_specific_skills():
    # Placeholder content for role-specific skills
    role = "Software Engineer"
    skills = ["Python", "Django", "REST APIs", "Machine Learning"]

    return render_template_string('''
    <div class="role-specific-skills-content">
        <h1>Skills Required for {{ role }}</h1>
        <ul>
            {% for skill in skills %}
                <li>{{ skill }}</li>
            {% endfor %}
        </ul>
    </div>
    ''', role=role, skills=skills)
