import streamlit as st

st.title("Cybersecurity Quiz")

score = 0

q1 = st.radio(
    "1. What is phishing?",
    [
        "A type of malware",
        "A social engineering attack",
        "An antivirus tool"
    ]
)

q2 = st.radio(
    "2. Which password is strongest?",
    [
        "123456",
        "password",
        "M@ster#2026!"
    ]
)

q3 = st.radio(
    "3. Should you click unknown links in emails?",
    [
        "Yes",
        "No"
    ]
)

if st.button("Submit Quiz"):

    if q1 == "A social engineering attack":
        score += 1

    if q2 == "M@ster#2026!":
        score += 1

    if q3 == "No":
        score += 1

    st.success(f"Your Score: {score}/3")

    if score == 3:
        st.balloons()