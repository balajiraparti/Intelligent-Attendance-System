import streamlit as st

from src.database.db import create_subject


@st.dialog("Create New Subject")
def create_subject_dialog(teacher_id):
    st.markdown(
        "<p class='page-eyebrow'>New Subject</p>"
        "<h3 style='margin:0 0 1rem; font-family:Poppins,sans-serif; font-size:1.25rem; "
        "font-weight:700; color:#111827;'>Enter Subject Details</h3>",
        unsafe_allow_html=True,
    )

    sub_id = st.text_input("Subject Code", placeholder="CS101")
    sub_name = st.text_input(
        "Subject Name", placeholder="Introduction to Computer Science"
    )
    sub_section = st.text_input("Section", placeholder="A")

    st.markdown("<div class='section-gap-xs'></div>", unsafe_allow_html=True)

    if st.button("Create Subject", type="primary", use_container_width=True):
        if sub_id and sub_name and sub_section:
            try:
                create_subject(sub_id, sub_name, sub_section, teacher_id)
                st.toast("Subject created successfully! 🎉")
                st.rerun()
            except Exception as e:
                st.error(f"Error: {str(e)}")
        else:
            st.warning("Please fill in all fields before creating the subject.")
