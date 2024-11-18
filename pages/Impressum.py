# Impressum.py
from flask import Blueprint, render_template_string

impressum_bp = Blueprint('impressum', __name__)

@impressum_bp.route('/impressum')
def impressum():
    return render_template_string('''
    <div class="impressum-content">
        <h1>Impressum</h1>
        <p>This web application is developed to streamline the recruitment process.</p>
        <p>Contact Information:</p>
        <ul>
            <li>Email: contact@recruitmentapp.com</li>
            <li>Phone: +123456789</li>
            <li>Address: 123 Recruitment Avenue, Innovation City</li>
        </ul>
    </div>
    ''')
