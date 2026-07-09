import streamlit as st

st.title("Social Engineering Awareness")

st.subheader("Scenario")

st.write("""
You receive a phone call from someone claiming to be from your company's IT department.
They ask for your password to fix a security issue.
""")

answer = st.radio(
    "What should you do?",
    [
        "Give them your password",
        "Verify their identity first",
        "Ignore all future IT calls"
    ]
)

if st.button("Submit"):
    if answer == "Verify their identity first":
        st.success("Correct! Always verify identity before sharing information.")
    else:
        st.error("Incorrect. Never share passwords without verification.")