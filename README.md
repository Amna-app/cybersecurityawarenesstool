# Cybersecurity Awareness Questionnaire

This Streamlit application is an anonymous academic questionnaire and research study. It is not an instructional course or professional qualification.

## Main features

- Research-focused title and participant-information page
- Informed consent before access
- Anonymous participant ID
- No participant login, name or email collection
- Initial cybersecurity-awareness questionnaire
- Interactive phishing, password-security and social-engineering sections
- Knowledge assessment
- Final questionnaire and open-text feedback
- SQLite storage of anonymous responses
- Restricted researcher results and CSV export page

## Research details

- Researcher: Amna Rashid
- Supervisor: Dr. Maria Alvanou
- Institution: University of Essex

## Local installation

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

For macOS or Linux:

```bash
source venv/bin/activate
```

## Streamlit Community Cloud deployment

1. Upload the project files to a GitHub repository.
2. Deploy `app.py` through Streamlit Community Cloud.
3. Open **Manage app → Settings → Secrets** and add:

```toml
RESEARCHER_PASSWORD = "replace-with-a-strong-private-password"
```

4. Reboot the application after saving the secret.

## Research data

Open **Researcher Results and Feedback Export** from the sidebar and enter the researcher password. Anonymous questionnaire responses, assessment results and section-progress records can be downloaded as CSV files.

Before collecting responses, confirm that the participant information, consent wording, data-retention period and withdrawal procedure match the approved ethics documents. SQLite storage on Streamlit Community Cloud may not persist through every restart or redeployment, so an approved persistent database or regular secure exports may be required.
