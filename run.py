import os
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from app import create_app
from app.models import db, Application
from app.services.pdf_parser import extract_text_from_pdf, analyze_keywords

app = create_app()

# Upload configuration
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
@login_required
def dashboard():
    user_apps = Application.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', applications=user_apps)

@app.route('/add', methods=['GET', 'POST'])
@login_required
def add_application():
    if request.method == 'POST':
        company = request.form.get('company')
        role = request.form.get('role')
        status = request.form.get('status')
        job_description = request.form.get('job_description', '')
        
        match_score = 0
        missing_skills_str = ''
        
        # Handle PDF File Upload
        file = request.files.get('resume')
        if file and file.filename.endswith('.pdf'):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Run PDF Parsing and Matcher Service
            resume_text = extract_text_from_pdf(filepath)
            analysis = analyze_keywords(resume_text, job_description)
            
            match_score = analysis['score']
            missing_skills_str = ', '.join(analysis['missing']) if analysis['missing'] else 'None'
            
            # Clean up uploaded file after reading
            if os.path.exists(filepath):
                os.remove(filepath)

        new_app = Application(
            company=company,
            role=role,
            status=status,
            job_description=job_description,
            match_score=match_score,
            missing_skills=missing_skills_str,
            user_id=current_user.id
        )
        
        db.session.add(new_app)
        db.session.commit()
        
        flash('Application analyzed and saved successfully!')
        return redirect(url_for('dashboard'))

    return render_template('add_application.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)