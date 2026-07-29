import time

import streamlit as st

from src.database.config import supabase
from src.database.db import enroll_student_to_subject


@st.dialog("Enroll in Subject")
def enroll_dialog():
    st.markdown(
        "<p class='page-eyebrow'>Quick Enroll</p>"
        "<h3 style='margin:0 0 0.35rem; font-family:Poppins,sans-serif; font-size:1.1rem; "
        "font-weight:700; color:#111827;'>Enter your subject code</h3>"
        "<p style='margin:0 0 1rem; font-size:0.875rem; color:#6B7280;'>"
        "Ask your teacher for the code and paste it below to instantly join their class.</p>",
        unsafe_allow_html=True,
    )

    join_code = st.text_input("Subject Code", placeholder="CS101")

    if st.button("Enroll Now", type="primary", use_container_width=True):
        if join_code:
            res = (
                supabase.table("subjects")
                .select("subject_id, name, subject_code")
                .eq("subject_code", join_code)
                .execute()
            )
            if res.data:
                subject = res.data[0]
                student_id = st.session_state.student_data["student_id"]
                check = (
                    supabase.table("subject_students")
                    .select("*")
                    .eq("subject_id", subject["subject_id"])
                    .eq("student_id", student_id)
                    .execute()
                )
                if check.data:
                    st.warning("You are already enrolled in this subject.")
                else:
                    enroll_student_to_subject(student_id, subject["subject_id"])
                    st.success(f"Successfully enrolled in **{subject['name']}**!")
                    time.sleep(1)
                    st.rerun()
            else:
                st.error("Subject code not found. Double-check with your teacher.")
        else:
            st.warning("Please enter a subject code.")
