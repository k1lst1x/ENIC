# ENIC Project

A beta-version website developed for the **National Center for Higher Education Development** (Kazakhstan).  
Built with Django, Docker, and PostgreSQL/SQLite support.

🏆 This project was created for a national student competition (July 2025) and proudly won **3rd place** among teams from universities across Kazakhstan.
[Read the official announcement](https://enic-kazakhstan.edu.kz/en/post/266)

## Features
- Multi-language support (Kazakh, Russian, English)
- Secure configuration (XSS/CSRF protection, HTTPS-ready)
- Rich text editing with CKEditor 5
- Admin panel enhanced with Jazzmin
- Dockerized setup for easy deployment

## Local Setup

```bash
# Clone the repository
git clone https://github.com/k1lst1x/ENIC.git
cd ENIC

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r req.txt

# Copy environment variables
cp .env.example .env

# Run migrations and start server
python manage.py migrate
python manage.py runserver
```

## Requirements
- Python 3.10+
- Django 4.2
- PostgreSQL (or SQLite for local use)
- Docker (optional)

---

💡 Developed by the **Almaty University of Power Engineering and Telecommunications team** — awarded **3rd place** in the national competition for educational digital projects, 2025.
