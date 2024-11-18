# main_rec_need_app.py

from flask import Flask
from pages.Home import home_bp
from pages.Job_Description import job_description_bp
from pages.Impressum import impressum_bp
from pages.Our_Mission import mission_bp
from pages.Recruiting_App import recruiting_app_bp

# Instantiate the Flask application
app = Flask(__name__)

# Register blueprints from different parts of the web app
app.register_blueprint(home_bp)
app.register_blueprint(job_description_bp)
app.register_blueprint(impressum_bp)
app.register_blueprint(mission_bp)
app.register_blueprint(recruiting_app_bp)

if __name__ == "__main__":
    app.run(debug=True)
