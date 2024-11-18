# Our_Mission.py
from flask import Blueprint, render_template_string

mission_bp = Blueprint('mission', __name__)

@mission_bp.route('/our_mission')
def our_mission():
    return render_template_string('''
    <div class="mission-content">
        <h1>Our Mission</h1>
        <p>We aim to revolutionize the recruitment process by providing innovative tools that
           ensure the right candidates are matched with the right roles.</p>
        <p>Our commitment lies in innovation, efficiency, and inclusivity to create a better future for recruitment.</p>
    </div>
    ''')
