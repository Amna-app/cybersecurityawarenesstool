import streamlit as st

from database import mark_module_complete
from research_utils import require_pre_questionnaire, research_sidebar

participant_id = require_pre_questionnaire()
research_sidebar()

st.title("4. Social Engineering Scenario Training")

scenarios = [
    (
        "IT support call",
        "A caller claiming to be from IT asks for your password to resolve an urgent issue.",
        ["Provide the password", "Verify through the official helpdesk and do not disclose the password", "Install any software requested"],
        "Verify through the official helpdesk and do not disclose the password",
        "Legitimate support staff should not need your password."
    ),
    (
        "Tailgating",
        "An unknown person carrying boxes asks you to hold open a secure office door.",
        ["Allow entry", "Ask them to use their access card or contact reception", "Lend your access card"],
        "Ask them to use their access card or contact reception",
        "Physical access controls are part of cybersecurity."
    ),
    (
        "Unexpected information request",
        "Someone claiming to be a supplier asks for employee contact details and project information.",
        ["Send the information", "Verify identity and authorisation before sharing", "Post it in a group chat"],
        "Verify identity and authorisation before sharing",
        "Share sensitive information only on a verified need-to-know basis."
    ),
]

answers = []
for index, (title, prompt, options, correct, explanation) in enumerate(scenarios, 1):
    with st.container(border=True):
        st.subheader(f"{index}. {title}")
        st.write(prompt)
        answer = st.radio("Best response", options, key=f"se_{index}", index=None)
        answers.append((answer, correct, explanation))
        if st.button("Check response", key=f"se_check_{index}"):
            if answer is None:
                st.warning("Select a response first.")
            elif answer == correct:
                st.success("Correct. " + explanation)
            else:
                st.error("Incorrect. " + explanation)

if st.button("Mark social engineering module as completed", use_container_width=True):
    if any(answer is None for answer, _, _ in answers):
        st.error("Answer all scenarios before completing the module.")
    else:
        mark_module_complete(participant_id, "social_engineering")
        st.success("Social Engineering module completed. Continue to the Knowledge Assessment.")
