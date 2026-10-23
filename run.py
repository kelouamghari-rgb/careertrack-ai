import os
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from app import create_app
from app.models import db, Application
from app.services.pdf_parser import extract_text_from_pdf, analyze_keywords

app = create_app()

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
        
        file = request.files.get('resume')
        if file and file.filename.endswith('.pdf'):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            resume_text = extract_text_from_pdf(filepath)
            analysis = analyze_keywords(resume_text, job_description)
            
            match_score = analysis['score']
            missing_skills_str = ', '.join(analysis['missing']) if analysis['missing'] else 'None'
            
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

@app.route('/edit/<int:app_id>', methods=['GET', 'POST'])
@login_required
def edit_application(app_id):
    application = Application.query.get_or_404(app_id)
    if application.user_id != current_user.id:
        flash('Unauthorized action.', 'danger')
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        application.company = request.form.get('company')
        application.role = request.form.get('role')
        application.status = request.form.get('status')
        
        db.session.commit()
        flash('Application updated successfully!')
        return redirect(url_for('dashboard'))

    return render_template('edit_application.html', app=application)

@app.route('/delete/<int:app_id>', methods=['POST'])
@login_required
def delete_application(app_id):
    application = Application.query.get_or_404(app_id)
    if application.user_id == current_user.id:
        db.session.delete(application)
        db.session.commit()
        flash('Application deleted successfully!')
    
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)