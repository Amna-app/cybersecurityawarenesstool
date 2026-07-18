from __future__ import annotations

import secrets
import string
import streamlit as st

from database import (
    completed_modules,
    latest_quiz_result,
    questionnaire_completed,
)


CONSENT_VERSION = "1.0"
REQUIRED_MODULES = {"phishing", "password", "social_engineering"}


def init_session() -> None:
    defaults = {
        "participant_id": None,
        "consent_given": False,
        "study_started": False,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def generate_participant_id() -> str:
    alphabet = string.ascii_uppercase + string.digits
    return "P-" + "".join(secrets.choice(alphabet) for _ in range(8))


def require_consent() -> str:
    init_session()
    participant_id = st.session_state.get("participant_id")
    if not st.session_state.get("consent_given") or not participant_id:
        st.warning(
            "Please read the participant information and provide consent on the Home page before continuing."
        )
        st.stop()
    return str(participant_id)


def require_pre_questionnaire() -> str:
    participant_id = require_consent()
    if not questionnaire_completed(participant_id, "pre"):
        st.warning("Please complete the pre-training questionnaire before accessing this section.")
        st.stop()
    return participant_id


def study_progress(participant_id: str) -> dict[str, object]:
    modules = completed_modules(participant_id)
    return {
        "pre": questionnaire_completed(participant_id, "pre"),
        "modules": modules,
        "modules_complete": REQUIRED_MODULES.issubset(modules),
        "quiz": latest_quiz_result(participant_id) is not None,
        "post": questionnaire_completed(participant_id, "post"),
    }


def research_sidebar() -> None:
    init_session()
    st.sidebar.markdown("## Research Study")
    if st.session_state.get("participant_id"):
        st.sidebar.caption(f"Anonymous ID: {st.session_state.participant_id}")
        progress = study_progress(st.session_state.participant_id)
        completed = sum(
            [
                bool(progress["pre"]),
                bool(progress["modules_complete"]),
                bool(progress["quiz"]),
                bool(progress["post"]),
            ]
        )
        st.sidebar.progress(completed / 4)
        st.sidebar.caption(f"Study progress: {completed}/4 stages")
    st.sidebar.info(
        "Participation is voluntary. Responses are collected for academic research and analysed anonymously."
    )
