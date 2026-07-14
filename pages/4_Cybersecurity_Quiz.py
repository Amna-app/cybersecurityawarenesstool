import streamlit as st
from auth import require_login
from certificate import get_or_create_certificate
from database import save_quiz_attempt

user = require_login()
st.title("📝 Cybersecurity Quiz")
st.write("Pass mark: **80%**. A successful attempt automatically creates your certificate.")

questions = [
    ("What is phishing?", ["A hardware failure", "A social engineering attack", "An antivirus tool"], "A social engineering attack"),
    ("What is the safest response to an unexpected sign-in link?", ["Click quickly", "Open the service directly using a trusted address", "Forward it to everyone"], "Open the service directly using a trusted address"),
    ("Which password practice is strongest?", ["Reuse one complex password", "Use unique passwords with a password manager", "Write passwords in email drafts"], "Use unique passwords with a password manager"),
    ("What should you do if a caller asks for your password?", ["Share it if they sound professional", "Verify through the official helpdesk and never disclose it", "Disable antivirus"], "Verify through the official helpdesk and never disclose it"),
    ("Why is multi-factor authentication useful?", ["It adds another verification step", "It makes passwords public", "It removes the need for account security"], "It adds another verification step"),
    ("What is tailgating?", ["Following a social media page", "Unauthorised entry by following an authorised person", "Backing up a file"], "Unauthorised entry by following an authorised person"),
    ("What is a warning sign of social engineering?", ["Unusual urgency or secrecy", "A normal scheduled meeting", "Using an approved internal portal"], "Unusual urgency or secrecy"),
    ("What should you do with a suspicious attachment?", ["Open it in a hurry", "Report it and verify the sender", "Rename and run it"], "Report it and verify the sender"),
    ("Which action protects sensitive information?", ["Share only on a need-to-know basis", "Post it in public chat", "Use personal email for work data"], "Share only on a need-to-know basis"),
    ("What should happen after suspected account compromise?", ["Ignore it", "Report it promptly and change credentials through trusted channels", "Delete all evidence"], "Report it promptly and change credentials through trusted channels"),
]

with st.form("final_quiz"):
    answers = []
    for i, (question, options, correct) in enumerate(questions, 1):
        answers.append(
            st.radio(
                f"{i}. {question}",
                options,
                key=f"quiz_q_{i}",
                index=None,
            )
        )
    submitted = st.form_submit_button("Submit final assessment", use_container_width=True)

if submitted:
    unanswered = sum(answer is None for answer in answers)
    if unanswered:
        st.error(f"Answer all questions before submitting. Unanswered: {unanswered}")
    else:
        score = sum(answer == questions[i][2] for i, answer in enumerate(answers))
        total = len(questions)
        percentage = (score / total) * 100
        passed = percentage >= 80
        save_quiz_attempt(user["id"], score, total, passed)

        st.metric("Assessment result", f"{score}/{total} ({percentage:.0f}%)")
        if passed:
            certificate = get_or_create_certificate(user, score, total, percentage)
            st.success(
                f"Congratulations — you passed. Certificate {certificate['certificate_id']} "
                "has been generated automatically. Open the Certificate page to download it."
            )
            st.balloons()
        else:
            st.error("You did not reach the 80% pass mark. Review the training modules and try again.")
