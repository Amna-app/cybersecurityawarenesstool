import streamlit as st

from auth import init_session, login_form, logout_button, register_form
from database import get_best_attempt, get_certificate, init_db


st.set_page_config(
    page_title="Cybersecurity Awareness Training",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

init_db()
init_session()

st.markdown(
    """
    <style>
    .block-container {padding-top: 2rem; padding-bottom: 3rem; max-width: 1180px;}
    .hero {
        padding: 2.2rem;
        border-radius: 18px;
        background: linear-gradient(135deg, #102A43 0%, #1769AA 100%);
        color: white;
        margin-bottom: 1.5rem;
    }
    .hero h1 {margin: 0 0 .4rem 0; color: white;}
    .hero p {font-size: 1.08rem; margin: 0; opacity: .95;}
    .feature {
        border: 1px solid #D9E2EC;
        border-radius: 14px;
        padding: 1rem 1.1rem;
        min-height: 155px;
        background: white;
    }
    .small-note {color: #52606D; font-size: .92rem;}
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero">
      <h1>🛡️ Cybersecurity Awareness Training</h1>
      <p>Learn essential security practices, complete the assessment and receive a professional PDF certificate automatically.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

if st.session_state.authenticated:
    user = st.session_state.user
    st.sidebar.success(f"Signed in as\n\n**{user['full_name']}**")
    logout_button()

    best = get_best_attempt(user["id"])
    certificate = get_certificate(user["id"])

    st.subheader(f"Welcome, {user['full_name']}")
    col1, col2, col3 = st.columns(3)
    col1.metric("Training modules", "3")
    col2.metric("Best assessment score", f"{best['percentage']:.0f}%" if best else "Not attempted")
    col3.metric("Certificate", "Issued" if certificate else "Not yet issued")

    st.info(
        "Use the pages in the left menu. Complete the learning modules, then take the final quiz. "
        "A score of 80% or higher automatically unlocks your downloadable certificate."
    )

    cols = st.columns(3)
    features = [
        ("🎣 Phishing Simulation", "Recognise urgency, suspicious links, sender impersonation and credential requests."),
        ("🔑 Password Security", "Test password strength and learn practical controls for safer authentication."),
        ("☎️ Social Engineering", "Practise responding safely to impersonation, pressure and information requests."),
    ]
    for col, (title, text) in zip(cols, features):
        with col:
            st.markdown(f'<div class="feature"><h3>{title}</h3><p>{text}</p></div>', unsafe_allow_html=True)

    st.markdown("### Recommended pathway")
    st.write(
        "1. Complete the Phishing Simulation.  \n"
        "2. Review Password Strength Training.  \n"
        "3. Complete Social Engineering Awareness.  \n"
        "4. Take the Cybersecurity Quiz.  \n"
        "5. Download the PDF certificate from the Certificate page."
    )
else:
    st.write(
        "Participants must register before accessing the training. Registration details are used "
        "to personalise the certificate and retain assessment progress."
    )
    login_tab, register_tab = st.tabs(["Sign in", "Register"])
    with login_tab:
        login_form()
    with register_tab:
        register_form()

st.divider()
st.caption("Cybersecurity Awareness Training Tool • Secure participant records • Automatic assessment certification")
