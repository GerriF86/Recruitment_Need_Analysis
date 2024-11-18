# About_Us.py
from flask import Blueprint, render_template_string

about_us_bp = Blueprint('about_us', __name__)

@about_us_bp.route('/about_us')
def about_us():
    return render_template_string('''
    <div class="about-us-content">
        <h1>About Us</h1>
        <p>We are dedicated to providing innovative solutions for recruitment needs, ensuring the best job-to-candidate matches with efficient and thorough requirement analysis.</p>
        <p>Our team is committed to helping organizations streamline their hiring processes, making sure that every detail is analyzed and addressed for the perfect recruitment experience.</p>
    </div>
    ''')
