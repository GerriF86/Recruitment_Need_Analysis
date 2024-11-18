# Summary.py
from flask import Blueprint, render_template_string, request, redirect, url_for

summary_bp = Blueprint('summary', __name__)

@summary_bp.route('/summary', methods=['GET', 'POST'])
def summary():
    # Placeholder content to summarize collected information
    role = "Software Engineer"
    skills = ["Python", "Machine Learning", "APIs"]
    responsibilities = ["Manage team operations", "Ensure project deadlines are met", "Collaborate with stakeholders"]
    benefits = ["Flexible Work Hours", "Competitive Salary", "Health Insurance"]

    if request.method == 'POST':
        # Redirect to generate the job ad using collected data
        return redirect(url_for('job_ad_generator.generate_job_ad'))

    return render_template_string('''
    <div class="summary-content">
        <h1>Summary for {{ role }}</h1>
        <h2>Responsibilities</h2>
        <ul>
            {% for responsibility in responsibilities %}
                <li>{{ responsibility }}</li>
            {% endfor %}
        </ul>
        <h2>Skills</h2>
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
        <form method="post">
            <button type="submit">Generate Job Ad</button>
        </form>
    </div>
    ''', role=role, skills=skills, responsibilities=responsibilities, benefits=benefits)