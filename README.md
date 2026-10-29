# 🚀 CareerTrack AI

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/Framework-Flask-green.svg)](https://flask.palletsprojects.com/)
[![Database](https://img.shields.io/badge/Database-SQLite-lightgrey.svg)](https://www.sqlite.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**CareerTrack AI** is an intelligent web application designed to help job seekers track, organize, and manage their job applications efficiently. Featuring automated resume/job description parsing via PDF processing, CareerTrack AI simplifies your career search pipeline.

---

## ✨ Features

- 📊 **Interactive Dashboard**: View, filter, and track all your job applications at a glance.
- 📄 **PDF Parsing Engine**: Automatically extract key details from resumes and job postings.
- 🔐 **User Authentication**: Secure user registration, login, and session management.
- ✏️ **Full Application Management (CRUD)**: Create, view, update, and delete application records seamlessly.
- 🎨 **Responsive UI**: Clean, user-friendly interface built with modern templates.

---

## 📁 Repository Structure

```text
careertrack-ai/
├── app/
│   ├── routes/
│   │   └── auth.py              # Authentication routes & session logic
│   ├── services/
│   │   └── pdf_parser.py        # PDF text parsing & extraction service
│   ├── templates/               # Jinja2 HTML templates
│   │   ├── add_application.html
│   │   ├── base.html
│   │   ├── dashboard.html
│   │   ├── edit_application.html
│   │   ├── login.html
│   │   └── register.html
│   ├── __init__.py              # Application factory & initialization
│   └── models.py                # Database models (SQLAlchemy)
├── instance/
│   └── career.db                # SQLite database instance
├── README.md                    # Project documentation
├── requirements.txt             # Project dependencies
└── run.py                       # Application entry point
