import streamlit as st

st.title("Phishing Simulation")

st.subheader("Question 1")

st.write(
    "Your bank account has been suspended. "
    "Click the link below immediately to verify your account."
)

answer = st.radio(
    "Is this email:",
    ["Legitimate", "Phishing"]
)

if st.button("Check Answer"):
    if answer == "Phishing":
        st.success("Correct! This is a phishing email.")
    else:
        st.error("Incorrect. This is a phishing email.")