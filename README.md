# Cybersecurity Awareness Research Study

This Streamlit application implements an anonymous academic research intervention rather than a participant certification system.

## Included requirements

- Research-focused title and first-page participant information
- Explicit informed consent before access
- No participant login or registration account
- No certificate generation
- Anonymous participant ID
- Broad demographic categories only
- Pre-training research questionnaire
- Phishing, password-security and social-engineering modules
- Post-training knowledge assessment
- Post-training usability and feedback questionnaire
- SQLite storage of anonymous responses
- Password-protected researcher results/export page
- CSV downloads for questionnaire feedback, assessment scores and participant data

## Local installation

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

For macOS/Linux activation:

```bash
source venv/bin/activate
```

## Streamlit Community Cloud deployment

1. Upload all project files to a GitHub repository.
2. Do **not** upload an old `database.db` from the certificate/login version.
3. Deploy `app.py` in Streamlit Community Cloud.
4. Open **Manage app → Settings → Secrets** and add:

```toml
RESEARCHER_PASSWORD = "replace-with-a-strong-private-password"
```

5. Reboot the application after changing secrets.

## Where feedback is found

Open **Researcher Results and Feedback Export** from the Streamlit sidebar. Enter the researcher password. The page displays counts and provides CSV downloads. Open `questionnaire_responses.csv` to find all pre-training responses, post-training ratings and open-text feedback.

## Data and ethics notice

Before recruiting participants, replace the researcher/supervisor placeholders on the Home page and ensure every statement matches the approved participant information sheet, consent form, privacy notice, data-retention schedule and withdrawal procedure.

SQLite files on Streamlit Community Cloud may not be permanent across every redeployment or infrastructure restart. For formal data collection, use an approved persistent database or take secure exports frequently, subject to ethics approval and institutional policy.
