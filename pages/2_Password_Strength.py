import streamlit as st
import re

st.title("Password Strength Training")

password = st.text_input("Enter a password", type="password")

if password:

    score = 0

    if len(password) >= 8:
        score += 1

    if re.search(r"[A-Z]", password):
        score += 1

    if re.search(r"[a-z]", password):
        score += 1

    if re.search(r"\d", password):
        score += 1

    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        score += 1

    if score <= 2:
        st.error("Weak Password")
    elif score <= 4:
        st.warning("Medium Password")
    else:
        st.success("Strong Password")

st.markdown("### Password Tips")
st.write("• Use at least 8 characters")
st.write("• Include uppercase letters")
st.write("• Include lowercase letters")
st.write("• Include numbers")
st.write("• Include special characters")