import streamlit as st

from database import questionnaire_completed, save_questionnaire
from research_utils import require_consent, research_sidebar

participant_id = require_consent()
research_sidebar()

st.title("1. Pre-Training Questionnaire")
st.write(
    "Please answer based on your current knowledge and confidence before using the training modules. "
    "There are no right or wrong answers in this questionnaire."
)

likert = [
    "Strongly disagree", "Disagree", "Neither agree nor disagree", "Agree", "Strongly agree"
]
confidence = ["1 – Not confident", "2", "3 – Moderately confident", "4", "5 – Very confident"]
frequency = ["Never", "Rarely", "Sometimes", "Often", "Very frequently"]

questions = {
    "pre_phishing": "I can identify common warning signs of a phishing email.",
    "pre_password": "I understand how to create and manage a strong password.",
    "pre_social": "I understand how social engineering attackers manipulate users.",
    "pre_response": "I know what action to take after receiving a suspicious message.",
    "pre_mfa": "I understand the purpose of multi-factor authentication.",
}

with st.form("pre_questionnaire"):
    answers = {}
    for key, text in questions.items():
        answers[key] = st.radio(text, likert, key=key, index=None)
    answers["pre_confidence"] = st.radio(
        "How confident are you in recognising cybersecurity threats?",
        confidence,
        index=None,
    )
    answers["pre_frequency"] = st.radio(
        "How frequently do you receive suspicious emails, messages or calls?",
        frequency,
        index=None,
    )
    submitted = st.form_submit_button("Submit pre-training questionnaire", use_container_width=True)

if submitted:
    missing = [key for key, value in answers.items() if value is None]
    if missing:
        st.error("Please answer every question before submitting.")
    else:
        response_map = {key: (questions[key], answers[key]) for key in questions}
        response_map["pre_confidence"] = (
            "How confident are you in recognising cybersecurity threats?", answers["pre_confidence"]
        )
        response_map["pre_frequency"] = (
            "How frequently do you receive suspicious emails, messages or calls?", answers["pre_frequency"]
        )
        save_questionnaire(participant_id, "pre", response_map)
        st.success("Your pre-training responses have been recorded. Continue to the training modules.")

if questionnaire_completed(participant_id, "pre"):
    st.info("This questionnaire has already been submitted. Submitting again will update your previous responses.")
