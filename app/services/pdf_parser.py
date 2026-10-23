import fitz  # PyMuPDF
import re

def extract_text_from_pdf(pdf_file_path):
    """Extracts raw text content from a PDF file using PyMuPDF."""
    text = ""
    with fitz.open(pdf_file_path) as doc:
        for page in doc:
            text += page.get_text()
    return text

def analyze_keywords(resume_text, job_description):
    """
    Compares resume text against a target job description 
    and returns a match percentage alongside matched/missing skills.
    """
    # Standard tech/IT keywords to track
    common_keywords = [
        'python', 'flask', 'django', 'sql', 'sqlite', 'postgresql', 
        'git', 'github', 'api', 'rest', 'docker', 'linux', 'aws', 
        'html', 'css', 'javascript', 'bootstrap', 'json', 'ci/cd'
    ]
    
    # Clean text to lower case and isolate words
    resume_words = set(re.findall(r'\b\w+\b', resume_text.lower()))
    job_words = set(re.findall(r'\b\w+\b', job_description.lower()))
    
    # Identify key technologies present in the job description
    target_skills = [kw for kw in common_keywords if kw in job_words or kw in job_description.lower()]
    
    if not target_skills:
        return {'score': 100, 'matched': [], 'missing': []}
        
    matched_skills = [skill for skill in target_skills if skill in resume_words]
    missing_skills = [skill for skill in target_skills if skill not in resume_words]
    
    score = int((len(matched_skills) / len(target_skills)) * 100)
    
    return {
        'score': score,
        'matched': matched_skills,
        'missing': missing_skills
    }