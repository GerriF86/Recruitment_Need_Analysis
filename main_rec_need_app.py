# main_rec_need_app.py

from flask import Flask
from pages.Impressum import impressum_bp
from pages.Our_Mission import mission_bp
from pages.Recruiting_App import recruiting_app_bp
from pages.About_Us import about_us_bp

# Instantiate the Flask application
app = Flask(__name__)

# Register blueprints from different parts of the web app
app.register_blueprint(impressum_bp)
app.register_blueprint(mission_bp)
app.register_blueprint(recruiting_app_bp)
app.register_blueprint(about_us_bp)

if __name__ == "__main__":
    # Run the application in production mode without debug for performance optimization
    app.run(host='0.0.0.0', port=5000, debug=False)
