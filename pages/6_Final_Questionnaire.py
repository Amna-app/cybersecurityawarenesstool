import streamlit as st

from database import latest_quiz_result, mark_study_complete, questionnaire_completed, save_questionnaire
from research_utils import require_initial_questionnaire, research_sidebar

participant_id = require_initial_questionnaire()
research_sidebar()

if latest_quiz_result(participant_id) is None:
    st.warning("Please complete the Knowledge Assessment before submitting final feedback.")
    st.stop()

st.title("6. Final Questionnaire and Feedback")
st.write(
    "This questionnaire collects the research feedback requested for evaluating awareness, usability and participant experience."
)

likert = [
    "Strongly disagree", "Disagree", "Neither agree nor disagree", "Agree", "Strongly agree"
]
questions = {
    "final_phishing": "The questionnaire section improved my ability to recognise phishing attempts.",
    "final_password": "The password activity improved my understanding of secure password practices.",
    "final_social": "The social engineering scenarios were realistic and relevant.",
    "final_navigation": "The research application was easy to navigate.",
    "final_clarity": "The instructions were clear and understandable.",
    "final_feedback": "The feedback provided after each activity was useful.",
    "final_confidence": "I feel more confident responding to cybersecurity threats after the questionnaire activity.",
    "final_recommend": "I would recommend this questionnaire format to other users.",
}

with st.form("final_questionnaire"):
    answers = {key: st.radio(text, likert, key=key, index=None) for key, text in questions.items()}
    most_useful = st.selectbox(
        "Which questionnaire activity was most useful?",
        ["Select...", "Phishing Simulation", "Password Security", "Social Engineering", "Knowledge Assessment"],
    )
    improvement = st.text_area(
        "What could be improved in the research questionnaire?",
        placeholder="Please provide constructive feedback. Enter 'No suggestion' if none.",
    )
    additional = st.text_area(
        "Any additional comments?",
        placeholder="Optional",
    )
    submitted = st.form_submit_button("Submit final research feedback", use_container_width=True)

if submitted:
    missing = [key for key, value in answers.items() if value is None]
    if most_useful == "Select...": missing.append("most useful activity")
    if not improvement.strip(): missing.append("improvement feedback")
    if missing:
        st.error("Please complete all required questions before submitting.")
    else:
        response_map = {key: (questions[key], answers[key]) for key in questions}
        response_map["final_most_useful"] = ("Which questionnaire activity was most useful?", most_useful)
        response_map["final_improvement"] = ("What could be improved in the research questionnaire?", improvement.strip())
        response_map["final_additional"] = ("Any additional comments?", additional.strip() or "No additional comments")
        save_questionnaire(participant_id, "final", response_map)
        mark_study_complete(participant_id)
        st.success(
            "Thank you. Your final questionnaire and feedback have been recorded. "
            "Your participation in the research study is now complete."
        )
        st.balloons()

if questionnaire_completed(participant_id, "final"):
    st.info("Your final questionnaire has already been submitted. Resubmission will update the saved responses.")
