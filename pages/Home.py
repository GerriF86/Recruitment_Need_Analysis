# Home.py
from flask import Flask

app = Flask(__name__)

def render_home_page():
    return '''
    <div class="home-content">
        <h1>Welcome to the Recruitment Need Analysis Web App</h1>
        <p>Discover the innovation that transforms recruitment processes.</p>
        <form method="POST" action="/recruiting_app">
            <input type="text" name="job_title" placeholder="Enter Job Title" required>
            <button type="submit">Start Need Analysis</button>
        </form>
    </div>
    '''

@app.route('/')
def home():
    return render_home_page()

if __name__ == "__main__":
    app.run(debug=True)
