# main_rec_need_app.py

from flask import Flask
from pages.Home import home_bp
from pages.Job_Description import job_description_bp
from pages.Role_Specific_Skills import role_specific_skills_bp
from pages.Role_Benefits import role_benefits_bp
from pages.Summary import summary_bp
from pages.Impressum import impressum_bp
from pages.Our_Mission import mission_bp
from pages.Recruiting_App import recruiting_app_bp
from pages.About_Us import about_us_bp
from pages.Job_Ad_Generator import job_ad_generator_bp  # Import for job ad generation

# Instantiate the Flask application
app = Flask(__name__)

# Register blueprints from different parts of the web app
app.register_blueprint(home_bp)
app.register_blueprint(job_description_bp)
app.register_blueprint(role_specific_skills_bp)
app.register_blueprint(role_benefits_bp)
app.register_blueprint(summary_bp)
app.register_blueprint(impressum_bp)
app.register_blueprint(mission_bp)
app.register_blueprint(recruiting_app_bp)
app.register_blueprint(about_us_bp)
app.register_blueprint(job_ad_generator_bp)
  # Register job ad generation blueprint

if __name__ == "__main__":
    app.run(debug=True)
