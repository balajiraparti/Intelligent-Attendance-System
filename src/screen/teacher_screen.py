import streamlit as st
from src.pipeline.face_pipeline import predict_attendance
from src.database.config import supabase
from src.database.db import check_username_exsit, create_teacher, teacher_login
from src.ui.base_layout import style_base_layout
from src.components.dialog_create_subject import create_subject_dialog
from src.database.db import get_teacher_subjects
from src.components.subject_card import subject_card
from src.components.share_subject_dialog import share_subject_dialog
from src.components.dialog_add_photo import add_photos_dialog
import numpy as np
import pandas as pd
from src.components.dialog_attendance_result import attendance_result_dialog
from datetime import datetime
from src.components.dialog_voice_attenadance import voice_attendance_dialog
from src.database.db import get_attendance_for_teacher
def teacher_tab_take_attendance():
    teacher_id = st.session_state.teacher_data['teacher_id']
    st.header('Take AI Attendance')


    if 'attendance_images' not in st.session_state:
        st.session_state.attendance_images = []

    subjects = get_teacher_subjects(teacher_id)

    if not subjects:
        st.warning('You havent created any subjects yet! Please create one to begin!')
        return
    
    subject_options = {f"{s['name']} - {s['subject_code']}": s['subject_id'] for s in subjects}

    col1, col2 = st.columns([3,1], vertical_alignment='bottom')

    with col1:
        selected_subject_label = st.selectbox('Select Subject', options=list(subject_options.keys()))

    with col2:
        if st.button('Add Photos', type='primary', icon=':material/photo_prints:', width='stretch'):
            add_photos_dialog()

    selected_subject_id = subject_options[selected_subject_label]

    st.divider()

    if st.session_state.attendance_images:
        st.header('Added Photos')
        gallery_cols = st.columns(4)

        for idx, img in enumerate(st.session_state.attendance_images):
            with gallery_cols[idx % 4 ]:
                st.image(img, width='stretch', caption=f'Photo {idx+1}')
    has_photos = bool(st.session_state.attendance_images)
    c1, c2, c3 = st.columns(3)

    with c1:
        if st.button('Clear all photos', width='stretch', type='tertiary', icon=':material/delete:', disabled=not has_photos):
            st.session_state.attendance_images = []
            st.rerun()


    with c2:
        
        if st.button('Run Face Analysis', width='stretch', type='secondary', icon=':material/analytics:', disabled=not has_photos):
            with st.spinner('Deep scanning classroom photos...'):
                all_detected_ids = {}

                for idx, img in enumerate(st.session_state.attendance_images):
                    img_np = np.array(img.convert('RGB'))
                    detected, _, _ = predict_attendance(img_np)


                    if detected:
                        for sid in detected.keys():
                            student_id = int(sid)

                            all_detected_ids.setdefault(student_id, []).append(f"Photo {idx+1}")

                enrolled_res = supabase.table('subject_students').select("*, students(*)").eq('subject_id',selected_subject_id ).execute()
                enrolled_students = enrolled_res.data

                if not enrolled_students:
                    st.warning('No students enrolled in this course')
                else:

                    results, attendance_to_log  = [], []

                    current_timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")


                    for node in enrolled_students:
                        student = node['students']
                        sources = all_detected_ids.get(int(student['student_id']), [])
                        is_present= len(sources) > 0

                        results.append({
                            "Name": student['name'],
                            "ID": student['student_id'],
                            "Source": ", ".join(sources) if is_present else "-",
                            "Status": "✅ Present" if is_present else "❌ Absent"
                        })

                        attendance_to_log.append({
                            'student_id': student['student_id'],
                            'subject_id': selected_subject_id,
                            'timestamp': current_timestamp,
                            'is_present': bool(is_present)
                        })

                attendance_result_dialog(pd.DataFrame(results), attendance_to_log)

    with c3:
        if st.button('Use Voice Attendance', type='primary', width='stretch', icon=':material/mic:'):
            voice_attendance_dialog(selected_subject_id)


def teacher_dashboard():
    teacher_data = st.session_state.teacher_data

    if "teacher_active_tab" not in st.session_state:
        st.session_state["teacher_active_tab"] = "overview"

    top_left, top_right = st.columns([0.7, 0.3], gap="large")
    with top_left:
        st.markdown(
            f"<h1 style='margin:0; color:#1f2937;'>Welcome, {teacher_data['name']}</h1>",
            unsafe_allow_html=True,
        )
        st.markdown(
            "<p class='dashboard-subtitle'>Teacher dashboard</p>",
            unsafe_allow_html=True,
        )
    with top_right:
        st.markdown("<div class='section-gap-xs'></div>", unsafe_allow_html=True)
        st.button(
            "Logout",
            key="teacher_logout_action",
            icon=":material/logout:",
            use_container_width=True,
            on_click=logout_teacher,
        )
        st.markdown(
            "<p class='hint-text'>Shortcut: Ctrl + Backspace / Cmd + Backspace</p>",
            unsafe_allow_html=True,
        )

    st.markdown("<div class='section-gap-sm'></div>", unsafe_allow_html=True)
    st.divider()
    st.markdown("<div class='section-gap-sm'></div>", unsafe_allow_html=True)

    action_col_1, action_col_2, action_col_3 = st.columns(3, gap="medium")
    with action_col_1:
        if st.button(
            "Take Attendance",
            key="teacher_take_attendance",
            icon=":material/ar_on_you:",
            type="primary",
            use_container_width=True,
        ):
            st.session_state["teacher_active_tab"] = "attendance"
            st.rerun()
    with action_col_2:
        if st.button(
            "Manage Subjects",
            key="teacher_manage_subjects",
            icon=":material/ar_on_you:",
            type="primary",
            use_container_width=True,
        ):
            st.session_state["teacher_active_tab"] = "subjects"
            st.rerun()
    with action_col_3:
        if st.button(
            "Attendance Records",
            key="teacher_attendance_records",
            icon=":material/ar_on_you:",
            type="primary",
            use_container_width=True,
        ):
              st.session_state["teacher_active_tab"] = "records"
              st.rerun()

    st.markdown("<div class='section-gap-sm'></div>", unsafe_allow_html=True)
    st.divider()
    st.markdown("<div class='section-gap-sm'></div>", unsafe_allow_html=True)

    if st.session_state["teacher_active_tab"] == "attendance":
        teacher_tab_take_attendance()
    elif st.session_state["teacher_active_tab"] == "subjects":
        teacher_tab_manage_subjects()
    elif st.session_state["teacher_active_tab"] == "records":
        teacher_tab_attendance_records()
    else:
        st.markdown(
            "<p class='hint-text'>Choose a dashboard action above to continue.</p>",
            unsafe_allow_html=True,
        )

    # st.markdown(
    #     "<h2 style='margin:0; color:#3b82f6;'>Attendance Records</h2>",
    #     unsafe_allow_html=True,
    # )

def teacher_tab_attendance_records():
    st.header('Attendance Records')

    teacher_id = st.session_state.teacher_data['teacher_id']

    records = get_attendance_for_teacher(teacher_id)

    if not records:
        return
    
    data = []

    for r in records:
        ts = r.get('timestamp')

        data.append({
            "ts_group": ts.split(".")[0] if ts else None,
            "Time": datetime.fromisoformat(ts).strftime("%Y-%m-%d %I:%M %p") if ts else "N'A",
            "Subject": r['subjects']['name'],
            "Subject Code":r['subjects']['subject_code'],
            "is_present": bool(r.get('is_present', False))
        })


    df = pd.DataFrame(data)



    summary = (
        df.groupby(['ts_group', 'Time', 'Subject', 'Subject Code'])
        .agg(
            Present_Count = ('is_present', 'sum'),
            Total_Count =('is_present', 'count')
        ).reset_index()

    )

    summary['Attendance Stats'] = (
        "✅ " + summary['Present_Count'].astype(str) + " /"
        + summary['Total_Count'].astype(str) + ' Students'
    )

    display_df = ( summary.sort_values(by='ts_group' ,ascending=False)
                  [['Time', 'Subject', 'Subject Code', 'Attendance Stats']]
                  )
    
    st.dataframe(display_df, width='stretch', hide_index=True)
def teacher_tab_manage_subjects():
    teacher_id = st.session_state.teacher_data["teacher_id"]
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            "<h2 style='margin:0; color:#1f2937;'>Manage Subjects</h2>",
            unsafe_allow_html=True,
        )
    with col2:
        if st.button("Create New Subject", use_container_width=True):
            st.session_state["open_create_subject_dialog"] = True
            st.rerun()

    if st.session_state.pop("open_create_subject_dialog", False):
        create_subject_dialog(teacher_id)

    st.markdown("<div class='section-gap-sm'></div>", unsafe_allow_html=True)
    st.divider()
    st.markdown("<div class='section-gap-sm'></div>", unsafe_allow_html=True)

    subjects = get_teacher_subjects(teacher_id)
    if subjects:
        for sub in subjects:
            stats = [
                ("👥", "students", sub['total_students']),
                ("🤷‍♂️", "Classes", sub['total_classes']),
            ]

            def share_btn():
                if st.button(
                    f"Share Code:{sub['name']}",
                    key=f"share{sub['subject_code']}",
                    icon=":material/share:",
                ):
                    share_subject_dialog(sub['name'],sub['subject_code'])
                st.markdown("<div class='section-gap-xs'></div>", unsafe_allow_html=True)

            subject_card(
                name=sub['name'],
                code=sub['subject_code'],
                section=sub['section'],
                stats=stats,
                footer_callback=share_btn,
            )
    else:
        st.warning("NO SUBJECTS FOUND. CREATE ONE ABOVE")


def logout_teacher():
    st.session_state.pop("teacher_data", None)
    st.session_state.pop("is_logged_in", None)
    st.session_state.pop("user_role", None)
    st.session_state.pop("teacher_active_tab", None)
    st.session_state.pop("open_create_subject_dialog", None)
    st.session_state.pop("open_add_photos_dialog", None)
    st.session_state["login_type"] = None
    st.session_state["teacher_auth_mode"] = "login"
    st.rerun()


def login_teacher(username, password):
    teacher = teacher_login(username, password)
    if teacher:
        st.session_state.user_role = "teacher"
        st.session_state.teacher_data = teacher
        st.session_state.is_logged_in = True
        st.session_state.is_dashboard = True
        return True
    return False


def _render_teacher_login():
    username = st.text_input(
        "Enter username", placeholder="@abhishek", key="teacher_login_username"
    )
    password = st.text_input(
        "Enter password",
        type="password",
        placeholder="Enter your password",
        key="teacher_login_password",
    )

    st.markdown("<div class='section-gap-sm'></div>", unsafe_allow_html=True)

    action_left, action_right = st.columns(2, gap="medium")
    with action_left:
        login_clicked = st.button(
            "Login",
            key="teacher_login_action",
            type="primary",
            use_container_width=True,
        )
    with action_right:
        register_clicked = st.button(
            "Register Instead",
            key="teacher_register_switch",
            type="secondary",
            use_container_width=True,
        )

    if login_clicked:
        if not username or not password:
            st.error("Please enter your username and password.")
        else:
            # st.success(f"Welcome back, {username}.")
            if login_teacher(username, password):
                st.toast("Welcome back", icon="😊")
                import time

                time.sleep(2)
                st.rerun()
            else:
                st.error("invalid username or password")

    if register_clicked:
        st.session_state["teacher_auth_mode"] = "register"
        st.rerun()


def register_teacher(
    teacher_username, teacher_name, teacher_pass, teacher_pass_coonfirm
):
    if not teacher_username or not teacher_name or not teacher_pass:
        return False, "All Fields are required"
    if check_username_exsit(teacher_username):
        return False, "Username already taken!"
    if teacher_pass != teacher_pass_coonfirm:
        return False, "Password doesn't match!"
    try:
        create_teacher(teacher_username, teacher_pass, teacher_name)
        return True, "Successfully created! Login Now!"
    except Exception as e:
        return False, "Unexpected Error!"


def _render_teacher_register():
    username = st.text_input(
        "Enter username", placeholder="@abhishek", key="teacher_register_username"
    )
    name = st.text_input(
        "Enter name", placeholder="Abhishek Sharma", key="teacher_register_name"
    )
    password = st.text_input(
        "Enter password",
        type="password",
        placeholder="Enter your password",
        key="teacher_register_password",
    )
    confirm_password = st.text_input(
        "Confirm password",
        type="password",
        placeholder="Confirm your password",
        key="teacher_register_confirm_password",
    )

    st.markdown("<div class='section-gap-sm'></div>", unsafe_allow_html=True)

    action_left, action_right = st.columns(2, gap="medium")
    with action_left:
        register_clicked = st.button(
            "Register Now",
            key="teacher_register_action",
            type="primary",
            use_container_width=True,
        )
    with action_right:
        login_clicked = st.button(
            "Login Instead",
            key="teacher_login_switch",
            type="secondary",
            use_container_width=True,
        )

    success, message = register_teacher(username, name, password, confirm_password)
    if success:
        st.success(message)
        import time

        time.sleep(2)
        st.session_state.teacher_auth_mode = "login"
        st.rerun()
    else:
        st.error(message)

    if login_clicked:
        st.session_state["teacher_auth_mode"] = "login"
        st.rerun()


def teacher_page():
    if "is_dashboard" not in st.session_state:
        st.session_state.is_dashboard = False
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
        st.markdown("<div class='section-gap-xs'></div>", unsafe_allow_html=True)
        if st.button(
            "Go back to Home", key="teacher_back_home", use_container_width=True
        ):
            st.session_state["login_type"] = None
            st.session_state["teacher_auth_mode"] = "login"
            st.rerun()

    st.markdown("<div class='section-gap-sm'></div>", unsafe_allow_html=True)
    if not st.session_state["is_dashboard"]:
        st.markdown(
            f"""
                <div class="auth-card">
                    <p class="section-kicker">Teacher portal</p>
                    <h1 class="auth-title">{"Login using password" if st.session_state["teacher_auth_mode"] == "login" else "Register your teacher profile"}</h1>
                </div>
                <div class="section-gap-sm"></div>
                """,
            unsafe_allow_html=True,
        )
    if "teacher_data" in st.session_state:
        teacher_dashboard()
    elif st.session_state["teacher_auth_mode"] == "login":
        _render_teacher_login()
    else:
        _render_teacher_register()
