import streamlit as st
from auth import require_login
from certificate import generate_certificate_pdf
from database import get_best_attempt, get_certificate

user = require_login()
st.title("🏅 Professional Certificate")

certificate = get_certificate(user["id"])
best_attempt = get_best_attempt(user["id"])

if not certificate:
    st.warning(
        "No certificate is available yet. Complete the final assessment with a score of 80% or higher."
    )
    if best_attempt:
        st.write(f"Best recorded score: **{best_attempt['percentage']:.0f}%**")
    st.stop()

pdf_bytes = generate_certificate_pdf(user, certificate)

st.success("Your certificate is ready.")
col1, col2, col3 = st.columns(3)
col1.metric("Participant", user["full_name"])
col2.metric("Score", f"{certificate['percentage']:.0f}%")
col3.metric("Certificate ID", certificate["certificate_id"])

st.download_button(
    label="Download professional certificate (PDF)",
    data=pdf_bytes,
    file_name=f"Cybersecurity_Certificate_{user['full_name'].replace(' ', '_')}.pdf",
    mime="application/pdf",
    use_container_width=True,
)

st.info(
    "The PDF includes the participant's registered name, organisation, assessment score, issue date "
    "and a unique certificate ID."
)
