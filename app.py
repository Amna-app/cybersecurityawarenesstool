import sqlite3

import streamlit as st

from database import create_participant, init_db, participant_exists
from research_utils import (
    CONSENT_VERSION,
    generate_participant_id,
    init_session,
    research_sidebar,
)


st.set_page_config(
    page_title="Cybersecurity Awareness Research Study",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

init_db()
init_session()
research_sidebar()

st.markdown(
    """
    <style>
      .block-container {max-width: 1100px; padding-top: 2rem; padding-bottom: 3rem;}
      .hero {
        padding: 2rem 2.2rem; border-radius: 18px;
        background: linear-gradient(135deg, #102A43, #1769AA);
        color: white; margin-bottom: 1.5rem;
      }
      .hero h1 {color: white; margin: 0 0 .5rem 0;}
      .hero p {margin: 0; font-size: 1.08rem; opacity: .96;}
      .research-card {
        border: 1px solid #D9E2EC; border-radius: 14px;
        padding: 1.1rem 1.25rem; background: white; height: 100%;
      }
      .required {color: #B42318; font-weight: 700;}
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero">
      <h1>🛡️ Cybersecurity Awareness Research Study</h1>
      <p>An academic research project evaluating whether interactive training improves awareness of phishing, password security and social engineering.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

if st.session_state.consent_given:
    st.success(
        f"Thank you for joining the study. Your anonymous participant ID is "
        f"**{st.session_state.participant_id}**. Use the pages in the left menu to continue."
    )
    cols = st.columns(4)
    stages = [
        ("1", "Pre-training questionnaire"),
        ("2", "Training modules"),
        ("3", "Knowledge assessment"),
        ("4", "Post-training feedback"),
    ]
    for col, (number, label) in zip(cols, stages):
        with col:
            st.markdown(
                f'<div class="research-card"><h3>{number}</h3><p>{label}</p></div>',
                unsafe_allow_html=True,
            )
    st.info(
        "No login, name, email address or certificate is required. Your responses are linked only to the anonymous participant ID shown above."
    )
    st.stop()

st.header("Participant Information")
st.write(
    "You are invited to take part in a research study that evaluates an interactive web-based "
    "cybersecurity awareness intervention. Please read the information below before deciding whether to participate."
)

with st.expander("Purpose of the research", expanded=True):
    st.write(
        "The study investigates whether short interactive activities improve participants’ awareness "
        "and confidence in recognising phishing, creating secure passwords and responding to social engineering."
    )

with st.expander("What participation involves", expanded=True):
    st.write(
        "Participation involves: (1) completing a short pre-training questionnaire; "
        "(2) using three interactive learning modules; (3) completing a knowledge assessment; "
        "and (4) completing a post-training questionnaire and feedback form. The full activity is expected to take approximately 15–20 minutes."
    )

col1, col2 = st.columns(2)
with col1:
    with st.expander("Voluntary participation and withdrawal", expanded=True):
        st.write(
            "Participation is voluntary. You may stop using the application at any time before final submission. "
            "Choosing not to participate will not result in any penalty or disadvantage."
        )
    with st.expander("Potential risks and benefits", expanded=True):
        st.write(
            "The study presents ordinary cybersecurity scenarios and is considered low risk. Some users may find "
            "examples of scams or suspicious messages mildly uncomfortable. A possible benefit is improved awareness of common online threats."
        )
with col2:
    with st.expander("Data collection and confidentiality", expanded=True):
        st.write(
            "The application does not request your name, email address, password or account registration. "
            "It records an anonymous participant ID, broad demographic categories, questionnaire responses, module progress and assessment score. "
            "Results should be reported in aggregated or anonymised form."
        )
    with st.expander("Research use and contact details", expanded=True):
        st.write(
            "The collected information will be used only for the stated academic research project and related dissertation. "
            "Replace the placeholders below with the approved researcher and supervisor contact details before recruitment begins."
        )
        st.code(
            "Researcher: [Insert researcher name and university email]\n"
            "Supervisor: [Insert supervisor name and university email]\n"
            "Institution: University of Essex Online"
        )

st.warning(
    "Before deployment to real participants, ensure that this wording, the data collected, retention period, "
    "contact details and withdrawal procedure exactly match the approved ethics documents."
)

st.header("Consent and anonymous study details")
with st.form("consent_form"):
    age_group = st.selectbox(
        "Age group *",
        ["Select...", "18–24", "25–34", "35–44", "45–54", "55–64", "65 or above", "Prefer not to say"],
    )
    gender = st.selectbox(
        "Gender *",
        ["Select...", "Female", "Male", "Non-binary", "Self-describe", "Prefer not to say"],
    )
    education = st.selectbox(
        "Highest level of education *",
        [
            "Select...", "Secondary school", "College / vocational qualification",
            "Undergraduate degree", "Postgraduate degree", "Other", "Prefer not to say"
        ],
    )
    employment = st.selectbox(
        "Current employment status *",
        [
            "Select...", "Employed full-time", "Employed part-time", "Self-employed",
            "Student", "Unemployed", "Retired", "Other", "Prefer not to say"
        ],
    )
    previous_training = st.radio(
        "Have you previously completed cybersecurity awareness training? *",
        ["Yes", "No", "Not sure"],
        index=None,
    )
    computer_use = st.select_slider(
        "How frequently do you use a computer, smartphone or tablet? *",
        options=["Rarely", "A few times a month", "A few times a week", "Daily", "Several hours each day"],
        value="Daily",
    )
    understood = st.checkbox("I have read and understood the participant information above.")
    voluntary = st.checkbox("I understand that participation is voluntary and that I may stop before final submission.")
    research_use = st.checkbox("I consent to my anonymous responses being used for this academic research study.")
    adult = st.checkbox("I confirm that I am aged 18 or above.")
    submitted = st.form_submit_button("Give consent and begin study", use_container_width=True)

if submitted:
    missing = []
    if age_group == "Select...": missing.append("age group")
    if gender == "Select...": missing.append("gender")
    if education == "Select...": missing.append("education level")
    if employment == "Select...": missing.append("employment status")
    if previous_training is None: missing.append("previous training")
    if not all([understood, voluntary, research_use, adult]):
        missing.append("all consent confirmations")

    if missing:
        st.error("Please complete: " + ", ".join(missing) + ".")
    else:
        for _ in range(10):
            participant_id = generate_participant_id()
            if not participant_exists(participant_id):
                break
        try:
            create_participant(
                {
                    "participant_id": participant_id,
                    "age_group": age_group,
                    "gender": gender,
                    "education_level": education,
                    "employment_status": employment,
                    "previous_training": previous_training,
                    "computer_use": computer_use,
                    "consent_version": CONSENT_VERSION,
                }
            )
        except sqlite3.IntegrityError:
            st.error("A participant ID collision occurred. Please submit the form again.")
        else:
            st.session_state.participant_id = participant_id
            st.session_state.consent_given = True
            st.session_state.study_started = True
            st.rerun()
