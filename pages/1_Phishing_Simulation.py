import streamlit as st
from auth import require_login

user = require_login()
st.title("🎣 Phishing Simulation")
st.write("Review each message and decide whether it is legitimate or phishing.")

scenarios = [
    {
        "title": "Urgent bank message",
        "message": "Your bank account has been suspended. Click the link below immediately to verify your account.",
        "options": ["Legitimate", "Phishing"],
        "correct": "Phishing",
        "explanation": "The message creates urgency and asks you to use an unsolicited link. Contact the bank through its official app or website instead."
    },
    {
        "title": "Unexpected document share",
        "message": "A colleague has shared 'Salary_Review.zip'. Sign in again using the attached page to view it.",
        "options": ["Legitimate", "Phishing"],
        "correct": "Phishing",
        "explanation": "Unexpected compressed files and sign-in pages can steal credentials or deliver malware. Verify with the colleague through another channel."
    },
    {
        "title": "Known service notification",
        "message": "Your monthly statement is ready. Open your banking app directly to review it. No link or attachment is included.",
        "options": ["Legitimate", "Phishing"],
        "correct": "Legitimate",
        "explanation": "This message does not pressure you to click a link or disclose information, although the sender address should still be checked."
    },
]

for index, scenario in enumerate(scenarios, start=1):
    with st.container(border=True):
        st.subheader(f"{index}. {scenario['title']}")
        st.write(scenario["message"])
        answer = st.radio(
            "Your decision",
            scenario["options"],
            key=f"phishing_{index}",
            index=None,
        )
        if st.button("Check answer", key=f"check_phishing_{index}"):
            if answer is None:
                st.warning("Select an answer first.")
            elif answer == scenario["correct"]:
                st.success(f"Correct. {scenario['explanation']}")
            else:
                st.error(f"Not quite. {scenario['explanation']}")

st.info("Safety rule: pause, inspect the sender and destination, and verify unusual requests through a trusted channel.")
