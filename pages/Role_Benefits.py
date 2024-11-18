# Role_Benefits.py
from flask import Blueprint, render_template_string

role_benefits_bp = Blueprint('role_benefits', __name__)

@role_benefits_bp.route('/role_benefits')
def role_benefits():
    # Placeholder content for role-specific benefits
    role = "Software Engineer"
    benefits = ["Flexible Work Hours", "Remote Work Option", "Health Insurance", "Stock Options"]

    return render_template_string('''
    <div class="role-benefits-content">
        <h1>Benefits for {{ role }}</h1>
        <ul>
            {% for benefit in benefits %}
                <li>{{ benefit }}</li>
            {% endfor %}
        </ul>
    </div>
    ''', role=role, benefits=benefits)
