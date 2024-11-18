# Job_Description.py
def generate_job_description(role, skills, benefits):
    """
    Generate a job description based on role, skills, and benefits.
    """
    return f'''
    <div class="job-description-content">
        <h1>Job Description for {role}</h1>
        <h2>Key Skills</h2>
        <ul>
            {''.join([f'<li>{skill}</li>' for skill in skills])}
        </ul>
        <h2>Benefits</h2>
        <ul>
            {''.join([f'<li>{benefit}</li>' for benefit in benefits])}
        </ul>
    </div>
    '''