import streamlit as st

from src.ui.base_layout import style_base_layout

from src.database.db import create_teacher,check_username_exsit,teacher_login
def teacher_dashboard():
    teacher_data=st.session_state.teacher_data
    st.header(f"""welcome {teacher_data['name']}""")
def login_teacher(username,password):
    teacher= teacher_login(username,password)
    if teacher:
        st.session_state.user_role="teacher"
        st.session_state.teacher_data=teacher
        st.session_state.is_logged_in=True
        return True
    return False
def _render_teacher_login():
    username = st.text_input("Enter username", placeholder="@abhishek", key="teacher_login_username")
    password = st.text_input("Enter password", type="password", placeholder="Enter your password", key="teacher_login_password")

    st.markdown("<div style='height: 0.75rem;'></div>", unsafe_allow_html=True)

    action_left, action_right = st.columns(2, gap="medium")
    with action_left:
        login_clicked = st.button("Login", key="teacher_login_action", type="primary", use_container_width=True)
    with action_right:
        register_clicked = st.button("Register Instead", key="teacher_register_switch", type="secondary", use_container_width=True)

    if login_clicked:
        if not username or not password:
            st.error("Please enter your username and password.")
        else:
            # st.success(f"Welcome back, {username}.")
            if login_teacher(username,password):
                st.toast("Welcome back",icon="😊")
                import time
                time.sleep(2)
                st.rerun()
            else:
                st.error("invalid username or password")
    
    if register_clicked:
        st.session_state["teacher_auth_mode"] = "register"
        st.rerun()

def register_teacher(teacher_username,teacher_name,teacher_pass,teacher_pass_coonfirm):
    if not  teacher_username or not teacher_name or not teacher_pass:
        return False,"All Fields are required"
    if check_username_exsit(teacher_username):
        return False,"Username already taken!"
    if teacher_pass != teacher_pass_coonfirm:
        return False,"Password doesn't match!"
    try:
        create_teacher(teacher_username,teacher_pass,teacher_name)
        return True,"Successfully created! Login Now!"
    except Exception as e:
        return False,"Unexpected Error!"
    
def _render_teacher_register():
    username = st.text_input("Enter username", placeholder="@abhishek", key="teacher_register_username")
    name = st.text_input("Enter name", placeholder="Abhishek Sharma", key="teacher_register_name")
    password = st.text_input("Enter password", type="password", placeholder="Enter your password", key="teacher_register_password")
    confirm_password = st.text_input(
        "Confirm password",
        type="password",
        placeholder="Confirm your password",
        key="teacher_register_confirm_password",
    )

    st.markdown("<div style='height: 0.75rem;'></div>", unsafe_allow_html=True)

    action_left, action_right = st.columns(2, gap="medium")
    with action_left:
        register_clicked = st.button("Register Now", key="teacher_register_action", type="primary", use_container_width=True)
    with action_right:
        login_clicked = st.button("Login Instead", key="teacher_login_switch", type="secondary", use_container_width=True)

    success,message = register_teacher(username,name,password,confirm_password)
    if success:
        st.success(message)
        import time
        time.sleep(2)
        st.session_state.teacher_auth_mode="login"
        st.rerun()
    else:
         st.error(message)

    if login_clicked:
        st.session_state["teacher_auth_mode"] = "login"
        st.rerun()


def teacher_page():
    style_base_layout()
    if "teacher_auth_mode" not in st.session_state:
        st.session_state["teacher_auth_mode"] = "login"

    top_left, top_right = st.columns([0.72, 0.28], gap="medium")
    with top_left:
        st.markdown(
            """
            <div class="auth-shell">
                <div class="auth-topbar">
                    <div class="auth-brand">
                        <div class="auth-brand__logo"><span class="material-symbols-rounded">school</span></div>
                        <div>
                            <span class="auth-brand__title">SNAP CLASS</span>
                            <span class="auth-brand__subtitle">Teacher login portal</span>
                        </div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with top_right:
        st.markdown("<div style='height: 0.35rem;'></div>", unsafe_allow_html=True)
        if st.button("Go back to Home", key="teacher_back_home", use_container_width=True):
            st.session_state["login_type"] = None
            st.session_state["teacher_auth_mode"] = "login"
            st.rerun()

    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)

    st.markdown(
        f"""
        <div class="auth-card">
            <p class="section-kicker">Teacher portal</p>
            <h1 class="auth-title">{'Login using password' if st.session_state['teacher_auth_mode'] == 'login' else 'Register your teacher profile'}</h1>
        </div>
        <div style="height: 1rem;"></div>
        """,
        unsafe_allow_html=True,
    )
    if "teacher_data" in st.session_state:
        teacher_dashboard()
    elif st.session_state["teacher_auth_mode"] == "login":
        _render_teacher_login()
    else:
        _render_teacher_register()