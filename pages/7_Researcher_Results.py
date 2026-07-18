import csv
import io
import os

import streamlit as st

from database import fetch_table, summary_counts
from research_utils import research_sidebar

research_sidebar()
st.title("7. Researcher Results and Feedback Export")
st.write(
    "This page allows the researcher to view the number of collected responses and download anonymous data for analysis. "
    "Participants do not need an account."
)

try:
    configured_password = st.secrets.get("RESEARCHER_PASSWORD", "")
except Exception:
    configured_password = os.getenv("RESEARCHER_PASSWORD", "")

if not configured_password:
    st.error(
        "Researcher access is not configured. Add RESEARCHER_PASSWORD to Streamlit secrets before deployment."
    )
    st.code('RESEARCHER_PASSWORD = "replace-with-a-strong-private-password"')
    st.stop()

entered = st.text_input("Researcher password", type="password")
if entered != configured_password:
    st.info("Enter the researcher password to view or export data.")
    st.stop()

st.success("Researcher access granted.")
counts = summary_counts()
cols = st.columns(5)
for col, (label, value) in zip(
    cols,
    [
        ("Participants", counts["participants"]),
        ("Completed", counts["completed"]),
        ("Pre questionnaires", counts["pre_responses"]),
        ("Quiz attempts", counts["quiz_attempts"]),
        ("Post feedback", counts["post_responses"]),
    ],
):
    col.metric(label, value)


def to_csv_bytes(rows):
    if not rows:
        return b""
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=list(rows[0].keys()))
    writer.writeheader()
    writer.writerows(rows)
    return output.getvalue().encode("utf-8-sig")

for table, title, filename in [
    ("participants", "Anonymous participant data", "participants.csv"),
    ("questionnaire_responses", "Pre/post questionnaire responses and feedback", "questionnaire_responses.csv"),
    ("quiz_results", "Knowledge assessment results", "quiz_results.csv"),
    ("module_progress", "Module completion data", "module_progress.csv"),
]:
    rows = fetch_table(table)
    with st.expander(title, expanded=(table == "questionnaire_responses")):
        st.write(f"Records: **{len(rows)}**")
        if rows:
            st.dataframe(rows, use_container_width=True)
            st.download_button(
                f"Download {filename}",
                data=to_csv_bytes(rows),
                file_name=filename,
                mime="text/csv",
                key=f"download_{table}",
            )
        else:
            st.info("No data collected yet.")

st.warning(
    "Store exported files securely, restrict access to the research team, and follow the approved retention and deletion schedule."
)
