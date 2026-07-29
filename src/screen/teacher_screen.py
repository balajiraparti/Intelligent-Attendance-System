import html as _html
import time
from datetime import datetime

import numpy as np
import pandas as pd
import streamlit as st

from src.components.dialog_add_photo import add_photos_dialog
from src.components.dialog_attendance_result import attendance_result_dialog
from src.components.dialog_create_subject import create_subject_dialog
from src.components.dialog_voice_attenadance import voice_attendance_dialog
from src.components.share_subject_dialog import share_subject_dialog
from src.components.subject_card import subject_card
from src.database.config import supabase
from src.database.db import (
    check_username_exsit,
    create_teacher,
    get_attendance_for_teacher,
    get_teacher_subjects,
    teacher_login,
)
from src.pipeline.face_pipeline import predict_attendance
from src.ui.base_layout import style_base_layout

# ---------------------------------------------------------------------------
# KPI card helper
# ---------------------------------------------------------------------------


def _kpi_card(
    icon: str,
    value: str,
    label: str,
    sub: str,
    accent: str,
    bg: str,
    icon_color: str,
    sub_class: str = "neutral",
) -> None:
    sub_html = (
        f'<div class="kpi-sub {sub_class}">{_html.escape(sub)}</div>' if sub else ""
    )
    st.markdown(
        f"""
        <div class="kpi-card" style="--kpi-accent:{accent};">
            <div class="kpi-icon" style="background:{bg}; color:{icon_color};">
                <span class="material-symbols-rounded">{icon}</span>
            </div>
            <div class="kpi-value">{_html.escape(str(value))}</div>
            <div class="kpi-label">{_html.escape(label)}</div>
            {sub_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------------
# Tab: Take AI Attendance
# ---------------------------------------------------------------------------


def teacher_tab_take_attendance():
    teacher_id = st.session_state.teacher_data["teacher_id"]

    st.markdown(
        "<p class='page-eyebrow'>AI-Powered</p>"
        "<h2 class='section-heading'>Take Attendance</h2>",
        unsafe_allow_html=True,
    )
    st.markdown("<div class='section-gap-xs'></div>", unsafe_allow_html=True)

    if "attendance_images" not in st.session_state:
        st.session_state.attendance_images = []

    subjects = get_teacher_subjects(teacher_id)

    if not subjects:
        st.warning("You havent created any subjects yet! Please create one to begin!")
        return

    subject_options = {
        f"{s['name']} - {s['subject_code']}": s["subject_id"] for s in subjects
    }

    col1, col2 = st.columns([3, 1], vertical_alignment="bottom")
    with col1:
        selected_subject_label = st.selectbox(
            "Select Subject", options=list(subject_options.keys())
        )
    with col2:
        if st.button(
            "Add Photos",
            type="primary",
            icon=":material/photo_prints:",
            width="stretch",
        ):
            add_photos_dialog()

    selected_subject_id = subject_options[selected_subject_label]

    st.divider()

    if st.session_state.attendance_images:
        st.header("Added Photos")
        gallery_cols = st.columns(4)
        for idx, img in enumerate(st.session_state.attendance_images):
            with gallery_cols[idx % 4]:
                st.image(img, width="stretch", caption=f"Photo {idx + 1}")

    has_photos = bool(st.session_state.attendance_images)
    c1, c2, c3 = st.columns(3)

    with c1:
        if st.button(
            "Clear all photos",
            width="stretch",
            type="tertiary",
            icon=":material/delete:",
            disabled=not has_photos,
        ):
            st.session_state.attendance_images = []
            st.rerun()

    with c2:
        if st.button(
            "Run Face Analysis",
            width="stretch",
            type="secondary",
            icon=":material/analytics:",
            disabled=not has_photos,
        ):
            with st.spinner("Deep scanning classroom photos..."):
                all_detected_ids = {}
                for idx, img in enumerate(st.session_state.attendance_images):
                    img_np = np.array(img.convert("RGB"))
                    detected, _, _ = predict_attendance(img_np)
                    if detected:
                        for sid in detected.keys():
                            student_id = int(sid)
                            all_detected_ids.setdefault(student_id, []).append(
                                f"Photo {idx + 1}"
                            )

                enrolled_res = (
                    supabase.table("subject_students")
                    .select("*, students(*)")
                    .eq("subject_id", selected_subject_id)
                    .execute()
                )
                enrolled_students = enrolled_res.data

                if not enrolled_students:
                    st.warning("No students enrolled in this course")
                else:
                    results, attendance_to_log = [], []
                    current_timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
                    for node in enrolled_students:
                        student = node["students"]
                        sources = all_detected_ids.get(int(student["student_id"]), [])
                        is_present = len(sources) > 0
                        results.append(
                            {
                                "Name": student["name"],
                                "ID": student["student_id"],
                                "Source": ", ".join(sources) if is_present else "-",
                                "Status": "✅ Present" if is_present else "❌ Absent",
                            }
                        )
                        attendance_to_log.append(
                            {
                                "student_id": student["student_id"],
                                "subject_id": selected_subject_id,
                                "timestamp": current_timestamp,
                                "is_present": bool(is_present),
                            }
                        )
                    attendance_result_dialog(pd.DataFrame(results), attendance_to_log)

    with c3:
        if st.button(
            "Use Voice Attendance",
            type="primary",
            width="stretch",
            icon=":material/mic:",
        ):
            voice_attendance_dialog(selected_subject_id)


# ---------------------------------------------------------------------------
# Dashboard (main shell)
# ---------------------------------------------------------------------------


def teacher_dashboard():
    teacher_data = st.session_state.teacher_data
    teacher_id = teacher_data["teacher_id"]
    safe_name = _html.escape(teacher_data["name"])

    if "teacher_active_tab" not in st.session_state:
        st.session_state["teacher_active_tab"] = "overview"

    # ── Fetch data once ──────────────────────────────────────────────────────
    subjects = get_teacher_subjects(teacher_id)
    records = get_attendance_for_teacher(teacher_id)

    # ── Gradient header card ─────────────────────────────────────────────────
    left, right = st.columns([0.72, 0.28], gap="large")
    with left:
        st.markdown(
            f"""
            <div class="dash-header">
                <div class="dash-role-badge">
                    <span class="material-symbols-rounded" style="font-size:0.8rem;">school</span>
                    Teacher Portal
                </div>
                <h1 class="dash-name">Welcome back, {safe_name}</h1>
                <p class="dash-meta">Manage your subjects, take attendance, and review records.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with right:
        st.markdown("<div class='section-gap'></div>", unsafe_allow_html=True)
        st.button(
            "Logout",
            key="teacher_logout_action",
            icon=":material/logout:",
            use_container_width=True,
            on_click=logout_teacher,
        )
        st.markdown(
            "<p class='hint-text'>Ctrl+Backspace to log out</p>", unsafe_allow_html=True
        )

    st.markdown("<div class='section-gap-sm'></div>", unsafe_allow_html=True)

    # ── KPI row ──────────────────────────────────────────────────────────────
    total_subjects = len(subjects) if subjects else 0
    total_students = (
        sum(s.get("total_students", 0) for s in subjects) if subjects else 0
    )
    sessions_taken = sum(s.get("total_classes", 0) for s in subjects) if subjects else 0

    if records:
        present_count = sum(1 for r in records if r.get("is_present", False))
        avg_pct = round(present_count / len(records) * 100, 1)
    else:
        avg_pct = 0.0

    if avg_pct >= 75:
        avg_accent, avg_bg, avg_icon_color, avg_sub_class = (
            "#10B981",
            "#ECFDF5",
            "#10B981",
            "positive",
        )
        avg_sub_text = "On track"
    elif avg_pct >= 50:
        avg_accent, avg_bg, avg_icon_color, avg_sub_class = (
            "#F59E0B",
            "#FFFBEB",
            "#F59E0B",
            "neutral",
        )
        avg_sub_text = "Needs attention"
    else:
        avg_accent, avg_bg, avg_icon_color, avg_sub_class = (
            "#EF4444",
            "#FEF2F2",
            "#EF4444",
            "negative",
        )
        avg_sub_text = "Critical" if records else "No data yet"

    k1, k2, k3, k4 = st.columns(4, gap="medium")
    with k1:
        _kpi_card(
            "book_2",
            str(total_subjects),
            "Total Subjects",
            "Active subjects",
            "#2563EB",
            "#EFF6FF",
            "#2563EB",
        )
    with k2:
        _kpi_card(
            "group",
            str(total_students),
            "Total Students",
            "Across all subjects",
            "#14B8A6",
            "#F0FDFA",
            "#14B8A6",
        )
    with k3:
        _kpi_card(
            "event_available",
            str(sessions_taken),
            "Sessions Taken",
            "Total classes logged",
            "#8B5CF6",
            "#F5F3FF",
            "#8B5CF6",
        )
    with k4:
        _kpi_card(
            "analytics",
            f"{avg_pct}%",
            "Avg Attendance",
            avg_sub_text,
            avg_accent,
            avg_bg,
            avg_icon_color,
            avg_sub_class,
        )

    st.markdown("<div class='section-gap-sm'></div>", unsafe_allow_html=True)

    # ── Tab bar (visual only) ────────────────────────────────────────────────
    tab = st.session_state["teacher_active_tab"]
    tab_defs = [
        ("overview", "Overview", "home"),
        ("attendance", "Take Attendance", "camera_alt"),
        ("subjects", "Subjects", "book_2"),
        ("records", "Records", "analytics"),
    ]
    tabs_html = '<div class="tab-bar">'
    for key, label, icon in tab_defs:
        active_cls = " active" if tab == key else ""
        tabs_html += (
            f'<span class="tab-item{active_cls}">'
            f'<span class="material-symbols-rounded" '
            f'style="font-size:1rem;vertical-align:-3px;margin-right:4px;">{icon}</span>'
            f"{label}</span>"
        )
    tabs_html += "</div>"
    st.markdown(tabs_html, unsafe_allow_html=True)

    # Navigation buttons (below the visual tab bar)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button(
            "🏠 Overview",
            use_container_width=True,
            type="primary" if tab == "overview" else "tertiary",
            key="tab_btn_overview",
        ):
            st.session_state["teacher_active_tab"] = "overview"
            st.rerun()
    with col2:
        if st.button(
            "📷 Take Attendance",
            use_container_width=True,
            type="primary" if tab == "attendance" else "tertiary",
            key="tab_btn_attendance",
        ):
            st.session_state["teacher_active_tab"] = "attendance"
            st.rerun()
    with col3:
        if st.button(
            "📚 Subjects",
            use_container_width=True,
            type="primary" if tab == "subjects" else "tertiary",
            key="tab_btn_subjects",
        ):
            st.session_state["teacher_active_tab"] = "subjects"
            st.rerun()
    with col4:
        if st.button(
            "📊 Records",
            use_container_width=True,
            type="primary" if tab == "records" else "tertiary",
            key="tab_btn_records",
        ):
            st.session_state["teacher_active_tab"] = "records"
            st.rerun()

    st.markdown("<div class='section-gap-sm'></div>", unsafe_allow_html=True)

    # ── Content area ─────────────────────────────────────────────────────────
    if tab == "attendance":
        teacher_tab_take_attendance()
    elif tab == "subjects":
        teacher_tab_manage_subjects()
    elif tab == "records":
        teacher_tab_attendance_records()
    else:
        # Overview tab — pleasant landing state
        st.markdown(
            """
            <div style="text-align:center; padding:3rem 1rem 2rem;">
                <span class="material-symbols-rounded"
                      style="font-size:4rem; color:#2563EB; display:block; margin-bottom:1rem;">
                    dashboard
                </span>
                <h2 style="color:#111827; margin-bottom:0.5rem;">Your Teaching Dashboard</h2>
                <p style="color:#6B7280; max-width:480px; margin:0 auto 1rem;">
                    Use the tabs above to take AI-powered attendance, manage your subjects,
                    and review historical session records.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        qa1, qa2, qa3 = st.columns(3, gap="medium")
        with qa1:
            if st.button(
                "📷  Take Attendance",
                key="ov_attendance",
                use_container_width=True,
                type="secondary",
            ):
                st.session_state["teacher_active_tab"] = "attendance"
                st.rerun()
        with qa2:
            if st.button(
                "📚  Manage Subjects",
                key="ov_subjects",
                use_container_width=True,
                type="secondary",
            ):
                st.session_state["teacher_active_tab"] = "subjects"
                st.rerun()
        with qa3:
            if st.button(
                "📊  View Records",
                key="ov_records",
                use_container_width=True,
                type="secondary",
            ):
                st.session_state["teacher_active_tab"] = "records"
                st.rerun()


# ---------------------------------------------------------------------------
# Tab: Attendance Records
# ---------------------------------------------------------------------------


def teacher_tab_attendance_records():
    st.markdown(
        "<p class='page-eyebrow'>Session History</p>"
        "<h2 class='section-heading'>Attendance Records</h2>"
        "<p class='dashboard-subtitle'>A complete log of all attendance sessions taken across your subjects.</p>",
        unsafe_allow_html=True,
    )
    st.markdown("<div class='section-gap-xs'></div>", unsafe_allow_html=True)

    teacher_id = st.session_state.teacher_data["teacher_id"]
    records = get_attendance_for_teacher(teacher_id)

    if not records:
        return

    data = []
    for r in records:
        ts = r.get("timestamp")
        data.append(
            {
                "ts_group": ts.split(".")[0] if ts else None,
                "Time": datetime.fromisoformat(ts).strftime("%Y-%m-%d %I:%M %p")
                if ts
                else "N'A",
                "Subject": r["subjects"]["name"],
                "Subject Code": r["subjects"]["subject_code"],
                "is_present": bool(r.get("is_present", False)),
            }
        )

    df = pd.DataFrame(data)

    summary = (
        df.groupby(["ts_group", "Time", "Subject", "Subject Code"])
        .agg(Present_Count=("is_present", "sum"), Total_Count=("is_present", "count"))
        .reset_index()
    )

    summary["Attendance Stats"] = (
        "✅ "
        + summary["Present_Count"].astype(str)
        + " /"
        + summary["Total_Count"].astype(str)
        + " Students"
    )

    display_df = summary.sort_values(by="ts_group", ascending=False)[
        ["Time", "Subject", "Subject Code", "Attendance Stats"]
    ]

    st.dataframe(display_df, width="stretch", hide_index=True)


# ---------------------------------------------------------------------------
# Tab: Manage Subjects
# ---------------------------------------------------------------------------


def teacher_tab_manage_subjects():
    teacher_id = st.session_state.teacher_data["teacher_id"]

    col1, col2 = st.columns([0.6, 0.4], vertical_alignment="bottom")
    with col1:
        st.markdown(
            "<p class='page-eyebrow'>Curriculum</p>"
            "<h2 class='section-heading' style='margin:0;'>Manage Subjects</h2>",
            unsafe_allow_html=True,
        )
    with col2:
        if st.button(
            "Create New Subject",
            use_container_width=True,
            type="primary",
            icon=":material/add:",
        ):
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
                ("👥", "students", sub["total_students"]),
                ("🤷‍♂️", "Classes", sub["total_classes"]),
            ]

            def share_btn():
                if st.button(
                    f"Share Code:{sub['name']}",
                    key=f"share{sub['subject_code']}",
                    icon=":material/share:",
                ):
                    share_subject_dialog(sub["name"], sub["subject_code"])
                st.markdown(
                    "<div class='section-gap-xs'></div>", unsafe_allow_html=True
                )

            subject_card(
                name=sub["name"],
                code=sub["subject_code"],
                section=sub["section"],
                stats=stats,
                footer_callback=share_btn,
            )
    else:
        st.warning("NO SUBJECTS FOUND. CREATE ONE ABOVE")


# ---------------------------------------------------------------------------
# Auth helpers
# ---------------------------------------------------------------------------


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
    st.markdown(
        "<p class='dashboard-subtitle'>Sign in with your teacher credentials to access your dashboard.</p>",
        unsafe_allow_html=True,
    )
    st.markdown("<div class='section-gap-xs'></div>", unsafe_allow_html=True)

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
            if login_teacher(username, password):
                st.toast("Welcome back", icon="😊")
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
    st.markdown(
        "<p class='dashboard-subtitle'>Create your teacher account to get started with AI-powered attendance.</p>",
        unsafe_allow_html=True,
    )
    st.markdown("<div class='section-gap-xs'></div>", unsafe_allow_html=True)

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

    if register_clicked:
        success, message = register_teacher(username, name, password, confirm_password)
        if success:
            st.success(message)
            time.sleep(2)
            st.session_state.teacher_auth_mode = "login"
            st.rerun()
        else:
            st.error(message)

    if login_clicked:
        st.session_state["teacher_auth_mode"] = "login"
        st.rerun()


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


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
            "Go back to Home",
            key="teacher_back_home",
            use_container_width=True,
            type="tertiary",
            icon=":material/arrow_back:",
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
