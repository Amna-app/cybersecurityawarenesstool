import re
import streamlit as st
from auth import require_login

require_login()
st.title("🔑 Password Strength Training")
st.write("This checker evaluates patterns locally in the browser session. Passwords are not stored.")

password = st.text_input("Enter a sample password", type="password")
if password:
    checks = {
        "At least 12 characters": len(password) >= 12,
        "Uppercase letter": bool(re.search(r"[A-Z]", password)),
        "Lowercase letter": bool(re.search(r"[a-z]", password)),
        "Number": bool(re.search(r"\d", password)),
        "Symbol": bool(re.search(r"[^A-Za-z0-9]", password)),
        "No obvious common word": password.lower() not in {"password", "password123", "qwerty", "admin123"},
    }
    score = sum(checks.values())
    st.progress(score / len(checks))

    if score <= 2:
        st.error("Weak password")
    elif score <= 4:
        st.warning("Moderate password")
    else:
        st.success("Strong password")

    for label, passed in checks.items():
        st.write(("✅ " if passed else "❌ ") + label)

st.markdown("### Safer authentication")
st.write(
    "Use a unique passphrase for every account, store it in a reputable password manager, "
    "and enable multi-factor authentication. Never reuse a work password on personal websites."
)
