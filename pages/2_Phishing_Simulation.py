import streamlit as st

from database import mark_module_complete
from research_utils import require_pre_questionnaire, research_sidebar

participant_id = require_pre_questionnaire()
research_sidebar()

st.title("2. Interactive Phishing Simulation")
st.write("Review each message and select the safest interpretation or response.")

scenarios = [
    {
        "title": "Urgent bank message",
        "message": "Your bank account has been suspended. Click the link below immediately to verify your account.",
        "options": ["Legitimate", "Phishing"],
        "correct": "Phishing",
        "explanation": "The message creates urgency and asks you to use an unsolicited link. Access the bank through its official app or known website instead.",
    },
    {
        "title": "Unexpected document share",
        "message": "A colleague has shared Salary_Review.zip. Sign in again using the attached page to view it.",
        "options": ["Open the attachment", "Verify with the colleague using another channel", "Reply with your password"],
        "correct": "Verify with the colleague using another channel",
        "explanation": "Unexpected compressed files and sign-in pages can steal credentials or install malware.",
    },
    {
        "title": "Payment request",
        "message": "A senior manager requests an urgent confidential payment to a new bank account.",
        "options": ["Pay immediately", "Confirm through an approved independent channel", "Forward bank details by email"],
        "correct": "Confirm through an approved independent channel",
        "explanation": "Authority, urgency and secrecy are common social-engineering techniques. Follow the organisation's payment-verification process.",
    },
]

all_correct = True
answered = True
for index, scenario in enumerate(scenarios, 1):
    with st.container(border=True):
        st.subheader(f"{index}. {scenario['title']}")
        st.write(scenario["message"])
        choice = st.radio(
            "Select your answer",
            scenario["options"],
            key=f"phishing_choice_{index}",
            index=None,
        )
        if choice is None:
            answered = False
            all_correct = False
        elif choice != scenario["correct"]:
            all_correct = False
        if st.button("Check answer", key=f"phishing_check_{index}"):
            if choice is None:
                st.warning("Select an answer first.")
            elif choice == scenario["correct"]:
                st.success("Correct. " + scenario["explanation"])
            else:
                st.error("Not quite. " + scenario["explanation"])

if st.button("Mark phishing module as completed", use_container_width=True):
    if not answered:
        st.error("Answer all scenarios before completing the module.")
    else:
        mark_module_complete(participant_id, "phishing")
        st.success("Phishing module completed. You may continue to Password Security.")
        if not all_correct:
            st.info("Some answers were incorrect. Review the feedback above before continuing.")
