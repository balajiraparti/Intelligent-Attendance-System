import streamlit as st
from src.components.dialog_auto_enroll import auto_enroll_dialog
st.set_page_config(
    page_title="Smart Attendance System",
    page_icon="SA",
    layout="wide",
    initial_sidebar_state="collapsed",
)

from src.screen.home_screen import home_page
from src.screen.student_screen import student_page
from src.screen.teacher_screen import teacher_page


def main():
    if "login_type" not in st.session_state:
        st.session_state['login_type']=None
    match st.session_state['login_type']:
        case "teacher":
            teacher_page()
        case "student":
            student_page()
        case None:
            home_page()
    join_code=st.query_params.get('join-code')
    if join_code:
        if st.session_state.login_type!='student':
            st.session_state.login_type='student'
            st.rerun()
        if st.session_state.get('is_logged_in') and st.session_state.get('user_role')=='student':
            auto_enroll_dialog(join_code)

main()