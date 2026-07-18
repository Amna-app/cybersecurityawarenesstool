import re
import streamlit as st

from database import mark_module_complete
from research_utils import require_pre_questionnaire, research_sidebar

participant_id = require_pre_questionnaire()
research_sidebar()

st.title("3. Password Security Training")
st.write("Use a fictional sample only. The entered text is not saved to the research database.")

password = st.text_input("Enter a sample password", type="password")
if password:
    checks = {
        "At least 12 characters": len(password) >= 12,
        "Contains an uppercase letter": bool(re.search(r"[A-Z]", password)),
        "Contains a lowercase letter": bool(re.search(r"[a-z]", password)),
        "Contains a number": bool(re.search(r"\d", password)),
        "Contains a symbol": bool(re.search(r"[^A-Za-z0-9]", password)),
        "Is not an obvious common password": password.lower() not in {
            "password", "password123", "qwerty", "admin", "letmein"
        },
    }
    score = sum(checks.values())
    st.progress(score / len(checks))
    if score <= 2:
        st.error("Weak sample password")
    elif score <= 4:
        st.warning("Moderate sample password")
    else:
        st.success("Strong sample password")
    for label, passed in checks.items():
        st.write(("✅ " if passed else "❌ ") + label)

st.markdown("### Recommended practices")
st.write(
    "Use a unique passphrase for every account, store passwords in a reputable password manager, "
    "enable multi-factor authentication, and never send a password through email, chat or telephone."
)

with st.form("password_check"):
    q1 = st.radio(
        "Which practice is safest?",
        ["Reuse one complex password", "Use a unique password for each account", "Share passwords with trusted colleagues"],
        index=None,
    )
    q2 = st.radio(
        "What adds an additional verification step?",
        ["Multi-factor authentication", "Public Wi-Fi", "Password reuse"],
        index=None,
    )
    submitted = st.form_submit_button("Complete password module", use_container_width=True)

if submitted:
    if q1 is None or q2 is None:
        st.error("Answer both questions.")
    elif q1 == "Use a unique password for each account" and q2 == "Multi-factor authentication":
        mark_module_complete(participant_id, "password")
        st.success("Password Security module completed.")
    else:
        st.error("Review the recommended practices and try again.")
