# Cybersecurity Awareness Training Tool

A professional Streamlit application with participant registration, secure login/logout, learning modules, final assessment, saved results and automatic PDF certificate generation.

## Main features

- Participant registration with full name, email, organisation, job title/course, country and optional employee/student ID
- Passwords protected using PBKDF2-HMAC-SHA256 with individual random salts
- Login, session control and logout
- Phishing, password and social-engineering training modules
- Ten-question final assessment with an 80% pass mark
- Automatic certificate creation after the first successful attempt
- Downloadable landscape A4 PDF certificate with unique certificate ID
- SQLite storage for participants, attempts and certificates

## Installation

1. Open Command Prompt or PowerShell inside the extracted folder.
1. Create and activate a virtual environment:

```bash
python -m venv venv
venv\Scripts\activate
```

4. Install dependencies:

```bash
pip install -r requirements.txt
```

5. Start the application:

```bash
streamlit run app.py
```

Streamlit will display a local address, normally `http://localhost:8501`.

## First use

1. Open the **Register** tab.
2. Complete all required participant details.
3. Sign in.
4. Review the three training modules.
5. Complete the quiz.
6. Score at least 80%.
7. Open **Professional Certificate** and download the PDF.

## Important deployment note

This application is suitable for coursework, demonstrations and small internal training deployments. For a public production deployment, add HTTPS, managed secrets, email verification, rate limiting, password-reset functionality, privacy notices, database backups and administrator access controls.

## Existing database

A new `database.db` file is created automatically. To begin with an empty system, delete `database.db` while the application is stopped, then restart it.
