import streamlit as st
from src.database.db import create_subject

@st.dialog('Create New Subject')
def create_subject_dialog(teacher_id):
    st.markdown("<h3 style='margin:0;'>Enter Details of New Subject</h3>", unsafe_allow_html=True)
    st.markdown("<div style='height: 0.75rem;'></div>", unsafe_allow_html=True)
    sub_id = st.text_input("Subject Code", placeholder="CS101")
    sub_name = st.text_input('Subject Name', placeholder='Introduction to Computer Science')
    sub_section = st.text_input('Section', placeholder='A')

    st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)
    if st.button("Create Subject Now", type='primary', use_container_width=True):
        if sub_id and sub_name and sub_section:
            try:
                create_subject(sub_id, sub_name, sub_section, teacher_id)
                st.toast("Subject Created Succesfully!")
                st.rerun()
            except Exception as e:
                st.error(f"Error: {str(e)}")
        else:
            st.warning("Please fill all the fields")