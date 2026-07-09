import streamlit as st
from database import save_user

st.title("Certificate Generator")

name = st.text_input("Enter Your Name")

if st.button("Generate Certificate"):

    if name:

        save_user(name)

        st.success("Certificate Generated")

        st.markdown("# Certificate of Completion")

        st.write(
            f"This certifies that **{name}** has successfully completed the Cybersecurity Awareness Training Program."
        )

    else:
        st.error("Please enter your name.")