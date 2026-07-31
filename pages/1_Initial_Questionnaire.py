import streamlit as st

from database import questionnaire_completed, save_questionnaire
from research_utils import require_consent, research_sidebar

participant_id = require_consent()
research_sidebar()

st.title("1. Initial Questionnaire")
st.write(
    "Please answer based on your current knowledge and confidence before using the interactive questionnaire sections. "
    "There are no right or wrong answers in this questionnaire."
)

likert = [
    "Strongly disagree", "Disagree", "Neither agree nor disagree", "Agree", "Strongly agree"
]
confidence = ["1 – Not confident", "2", "3 – Moderately confident", "4", "5 – Very confident"]
frequency = ["Never", "Rarely", "Sometimes", "Often", "Very frequently"]

questions = {
    "initial_phishing": "I can identify common warning signs of a phishing email.",
    "initial_password": "I understand how to create and manage a strong password.",
    "initial_social": "I understand how social engineering attackers manipulate users.",
    "initial_response": "I know what action to take after receiving a suspicious message.",
    "initial_mfa": "I understand the purpose of multi-factor authentication.",
}

with st.form("initial_questionnaire"):
    answers = {}
    for key, text in questions.items():
        answers[key] = st.radio(text, likert, key=key, index=None)
    answers["initial_confidence"] = st.radio(
        "How confident are you in recognising cybersecurity threats?",
        confidence,
        index=None,
    )
    answers["initial_frequency"] = st.radio(
        "How frequently do you receive suspicious emails, messages or calls?",
        frequency,
        index=None,
    )
    submitted = st.form_submit_button("Submit initial questionnaire", use_container_width=True)

if submitted:
    missing = [key for key, value in answers.items() if value is None]
    if missing:
        st.error("Please answer every question before submitting.")
    else:
        response_map = {key: (questions[key], answers[key]) for key in questions}
        response_map["initial_confidence"] = (
            "How confident are you in recognising cybersecurity threats?", answers["initial_confidence"]
        )
        response_map["initial_frequency"] = (
            "How frequently do you receive suspicious emails, messages or calls?", answers["initial_frequency"]
        )
        save_questionnaire(participant_id, "initial", response_map)
        st.success("Your initial responses have been recorded. Continue to the interactive questionnaire sections.")

if questionnaire_completed(participant_id, "initial"):
    st.info("This questionnaire has already been submitted. Submitting again will update your previous responses.")
