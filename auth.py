import hashlib
import hmac
import os
import re
import streamlit as st
from database import authenticate_user, create_user, get_user_by_id


EMAIL_RE = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")


def hash_password(password: str, salt: bytes | None = None) -> tuple[str, str]:
    """Return PBKDF2 password hash and salt as hex strings."""
    salt = salt or os.urandom(16)
    password_hash = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt, 310_000
    )
    return password_hash.hex(), salt.hex()


def verify_password(password: str, stored_hash: str, stored_salt: str) -> bool:
    calculated_hash, _ = hash_password(password, bytes.fromhex(stored_salt))
    return hmac.compare_digest(calculated_hash, stored_hash)


def init_session() -> None:
    defaults = {
        "authenticated": False,
        "user_id": None,
        "user": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

    if st.session_state.get("authenticated") and st.session_state.get("user_id"):
        st.session_state.user = get_user_by_id(st.session_state.user_id)


def register_form() -> None:
    st.subheader("Create participant account")
    with st.form("registration_form", clear_on_submit=False):
        col1, col2 = st.columns(2)
        with col1:
            full_name = st.text_input("Full name *", placeholder="e.g. Alex Morgan")
            email = st.text_input("Email address *", placeholder="alex@example.com")
            organisation = st.text_input("Organisation / institution *")
        with col2:
            job_title = st.text_input("Job title / course *")
            country = st.text_input("Country *")
            employee_id = st.text_input("Employee / student ID (optional)")

        password = st.text_input(
            "Password *",
            type="password",
            help="Use at least 8 characters, including uppercase, lowercase, number and symbol.",
        )
        confirm_password = st.text_input("Confirm password *", type="password")
        consent = st.checkbox(
            "I confirm that these details are accurate and may appear on my training certificate."
        )
        submitted = st.form_submit_button("Register account", use_container_width=True)

    if not submitted:
        return

    errors = []
    if len(full_name.strip()) < 2:
        errors.append("Enter your full name.")
    if not EMAIL_RE.match(email.strip()):
        errors.append("Enter a valid email address.")
    if not organisation.strip():
        errors.append("Enter your organisation or institution.")
    if not job_title.strip():
        errors.append("Enter your job title or course.")
    if not country.strip():
        errors.append("Enter your country.")
    if len(password) < 8:
        errors.append("Password must contain at least 8 characters.")
    if not re.search(r"[A-Z]", password):
        errors.append("Password must include an uppercase letter.")
    if not re.search(r"[a-z]", password):
        errors.append("Password must include a lowercase letter.")
    if not re.search(r"\d", password):
        errors.append("Password must include a number.")
    if not re.search(r"[^A-Za-z0-9]", password):
        errors.append("Password must include a symbol.")
    if password != confirm_password:
        errors.append("Passwords do not match.")
    if not consent:
        errors.append("Confirm that your registration details are accurate.")

    if errors:
        for error in errors:
            st.error(error)
        return

    password_hash, salt = hash_password(password)
    result = create_user(
        full_name=full_name.strip(),
        email=email.strip().lower(),
        organisation=organisation.strip(),
        job_title=job_title.strip(),
        country=country.strip(),
        employee_id=employee_id.strip(),
        password_hash=password_hash,
        password_salt=salt,
    )
    if result["success"]:
        st.success("Registration completed. You can now sign in.")
    else:
        st.error(result["message"])


def login_form() -> None:
    st.subheader("Participant sign in")
    with st.form("login_form"):
        email = st.text_input("Email address")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Sign in", use_container_width=True)

    if submitted:
        user = authenticate_user(email.strip().lower())
        if user and verify_password(password, user["password_hash"], user["password_salt"]):
            st.session_state.authenticated = True
            st.session_state.user_id = user["id"]
            st.session_state.user = get_user_by_id(user["id"])
            st.success("Signed in successfully.")
            st.rerun()
        else:
            st.error("Incorrect email address or password.")


def require_login() -> dict:
    init_session()
    if not st.session_state.authenticated:
        st.warning("Please sign in from the Home page to access this section.")
        st.stop()
    return st.session_state.user


def logout_button() -> None:
    if st.sidebar.button("Log out", use_container_width=True):
        st.session_state.authenticated = False
        st.session_state.user_id = None
        st.session_state.user = None
        st.rerun()
