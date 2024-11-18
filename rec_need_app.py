from multiapp import MultiApp
from pages.Impressum import impressum_content
from pages.Our_Mission import mission_content
from pages.Recruiting_App import recruiting_app_content
from pages.About_Us import about_us_content

app = MultiApp()

# Add pages
app.add_app("Recruiting App", recruiting_app_content)
app.add_app("Our Mission", mission_content)
app.add_app("About Us", about_us_content)
app.add_app("Impressum", impressum_content)

# Run the app
app.run()
