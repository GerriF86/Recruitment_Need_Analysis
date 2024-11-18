# Home.py
from flask import Blueprint, render_template_string

home_bp = Blueprint('home', __name__)

@home_bp.route('/')
def home():
    return render_template_string('''
    <div class="home-content">
        <h1>Welcome to the Recruitment Need Analysis Web App</h1>
        <p>Discover the innovation that transforms recruitment processes.</p>
        <form method="POST" action="/recruiting_app">
            <input type="text" name="job_title" placeholder="Enter Job Title" required>
            <button type="submit">Start Need Analysis</button>
        </form>
    </div>
    ''')
