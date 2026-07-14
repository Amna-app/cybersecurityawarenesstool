import streamlit as st
from auth import require_login

require_login()
st.title("☎️ Social Engineering Awareness")

scenarios = [
    (
        "IT support call",
        "A caller claiming to be from IT asks for your password to fix an urgent issue.",
        ["Give the password", "Verify identity through the official helpdesk", "Install any tool they request"],
        "Verify identity through the official helpdesk",
        "Legitimate support staff should not need your password."
    ),
    (
        "Executive payment request",
        "You receive an unusual message apparently from a senior manager asking for an immediate confidential payment.",
        ["Process it immediately", "Reply with bank details", "Confirm through an approved independent channel"],
        "Confirm through an approved independent channel",
        "Attackers often impersonate authority figures and use secrecy or urgency."
    ),
    (
        "Tailgating",
        "An unknown person carrying boxes asks you to hold a secure office door open.",
        ["Allow entry to be polite", "Ask them to use their access card or contact reception", "Lend them your access card"],
        "Ask them to use their access card or contact reception",
        "Physical access controls are part of cybersecurity."
    ),
]

for i, (title, prompt, options, correct, explanation) in enumerate(scenarios, 1):
    with st.container(border=True):
        st.subheader(f"{i}. {title}")
        st.write(prompt)
        answer = st.radio("Best response", options, key=f"se_{i}", index=None)
        if st.button("Submit response", key=f"se_btn_{i}"):
            if answer is None:
                st.warning("Select a response.")
            elif answer == correct:
                st.success(f"Correct. {explanation}")
            else:
                st.error(f"Incorrect. {explanation}")
