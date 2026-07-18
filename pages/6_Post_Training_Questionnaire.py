import streamlit as st

from database import latest_quiz_result, mark_study_complete, questionnaire_completed, save_questionnaire
from research_utils import require_pre_questionnaire, research_sidebar

participant_id = require_pre_questionnaire()
research_sidebar()

if latest_quiz_result(participant_id) is None:
    st.warning("Please complete the Knowledge Assessment before submitting post-training feedback.")
    st.stop()

st.title("6. Post-Training Questionnaire and Feedback")
st.write(
    "This questionnaire collects the research feedback requested for evaluating learning, usability and participant experience."
)

likert = [
    "Strongly disagree", "Disagree", "Neither agree nor disagree", "Agree", "Strongly agree"
]
questions = {
    "post_phishing": "The training improved my ability to recognise phishing attempts.",
    "post_password": "The password activity improved my understanding of secure password practices.",
    "post_social": "The social engineering scenarios were realistic and relevant.",
    "post_navigation": "The research application was easy to navigate.",
    "post_clarity": "The instructions were clear and understandable.",
    "post_feedback": "The feedback provided after each activity was useful.",
    "post_confidence": "I feel more confident responding to cybersecurity threats after the training.",
    "post_recommend": "I would recommend this training approach to other users.",
}

with st.form("post_questionnaire"):
    answers = {key: st.radio(text, likert, key=key, index=None) for key, text in questions.items()}
    most_useful = st.selectbox(
        "Which training activity was most useful?",
        ["Select...", "Phishing Simulation", "Password Security", "Social Engineering", "Knowledge Assessment"],
    )
    improvement = st.text_area(
        "What could be improved in the training tool?",
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
        response_map["post_most_useful"] = ("Which training activity was most useful?", most_useful)
        response_map["post_improvement"] = ("What could be improved in the training tool?", improvement.strip())
        response_map["post_additional"] = ("Any additional comments?", additional.strip() or "No additional comments")
        save_questionnaire(participant_id, "post", response_map)
        mark_study_complete(participant_id)
        st.success(
            "Thank you. Your final questionnaire and feedback have been recorded. "
            "Your participation in the research study is now complete."
        )
        st.balloons()

if questionnaire_completed(participant_id, "post"):
    st.info("Your post-training questionnaire has already been submitted. Resubmission will update the saved responses.")
