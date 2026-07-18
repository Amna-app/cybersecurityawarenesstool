import json
import streamlit as st

from database import save_quiz_result
from research_utils import REQUIRED_MODULES, require_pre_questionnaire, research_sidebar, study_progress

participant_id = require_pre_questionnaire()
research_sidebar()
progress = study_progress(participant_id)

st.title("5. Post-Training Knowledge Assessment")
if not REQUIRED_MODULES.issubset(progress["modules"]):
    missing = sorted(REQUIRED_MODULES - progress["modules"])
    st.warning("Complete all three training modules first. Missing: " + ", ".join(missing))
    st.stop()

st.write(
    "This assessment measures cybersecurity knowledge after the training intervention. "
    "It is for research evaluation; no certificate or pass/fail award is issued."
)

questions = [
    ("What is phishing?", ["A hardware failure", "A social engineering attack", "An antivirus tool"], "A social engineering attack"),
    ("What is the safest response to an unexpected sign-in link?", ["Click quickly", "Open the service directly using a trusted address", "Forward it"], "Open the service directly using a trusted address"),
    ("Which password practice is strongest?", ["Reuse one complex password", "Use unique passwords with a password manager", "Store passwords in email drafts"], "Use unique passwords with a password manager"),
    ("What should you do if a caller asks for your password?", ["Share it if they sound professional", "Verify through the official helpdesk and never disclose it", "Disable antivirus"], "Verify through the official helpdesk and never disclose it"),
    ("Why is multi-factor authentication useful?", ["It adds another verification step", "It publishes passwords", "It removes the need for security"], "It adds another verification step"),
    ("What is tailgating?", ["Following a social-media page", "Unauthorised entry by following an authorised person", "Backing up a file"], "Unauthorised entry by following an authorised person"),
    ("Which is a warning sign of social engineering?", ["Unusual urgency or secrecy", "A scheduled meeting", "An approved internal portal"], "Unusual urgency or secrecy"),
    ("What should you do with a suspicious attachment?", ["Open it immediately", "Report it and verify the sender", "Rename and run it"], "Report it and verify the sender"),
    ("Which action protects sensitive information?", ["Share only on a need-to-know basis", "Post it publicly", "Use personal email for work data"], "Share only on a need-to-know basis"),
    ("What should happen after suspected account compromise?", ["Ignore it", "Report it promptly and change credentials through trusted channels", "Delete all evidence"], "Report it promptly and change credentials through trusted channels"),
]

with st.form("knowledge_assessment"):
    answers = []
    for index, (question, options, _) in enumerate(questions, 1):
        answers.append(st.radio(f"{index}. {question}", options, key=f"quiz_{index}", index=None))
    submitted = st.form_submit_button("Submit knowledge assessment", use_container_width=True)

if submitted:
    if any(answer is None for answer in answers):
        st.error("Answer all questions before submitting.")
    else:
        score = sum(answer == questions[i][2] for i, answer in enumerate(answers))
        total = len(questions)
        percentage = (score / total) * 100
        payload = {
            str(i + 1): {
                "question": questions[i][0],
                "answer": answers[i],
                "correct": answers[i] == questions[i][2],
            }
            for i in range(total)
        }
        save_quiz_result(participant_id, score, total, json.dumps(payload, ensure_ascii=False))
        st.metric("Knowledge assessment score", f"{score}/{total} ({percentage:.0f}%)")
        st.success(
            "Your assessment response has been recorded for research analysis. "
            "Please complete the Post-Training Questionnaire and Feedback page."
        )
