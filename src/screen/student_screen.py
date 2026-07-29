import html
import time

import numpy as np
import streamlit as st
from PIL import Image

from src.components.dialog_enroll import enroll_dialog
from src.components.header import header_home
from src.components.subject_card import subject_card
from src.database.db import (
    create_student,
    get_all_students,
    get_student_attendance,
    get_student_subject,
    unenroll_student_to_subject,
)
from src.pipeline.face_pipeline import (
    get_face_embedding,
    predict_attendance,
    train_classifier,
)
from src.pipeline.voice_pipeline import get_voice_embedding
from src.ui.base_layout import style_base_layout


def _kpi_card(
    icon,
    value,
    label,
    sub="",
    accent="#2563EB",
    bg="#EFF6FF",
    icon_color="#2563EB",
    sub_class="neutral",
):
    sub_html = f'<div class="kpi-sub {sub_class}">{sub}</div>' if sub else ""
    return f"""
<div class="kpi-card" style="--kpi-accent:{accent};">
    <div class="kpi-icon" style="background:{bg}; color:{icon_color};">
        <span class="material-symbols-rounded">{icon}</span>
    </div>
    <div class="kpi-value">{value}</div>
    <div class="kpi-label">{label}</div>
    {sub_html}
</div>"""


def student_dashboard():
    student_data = st.session_state.get("student_data", {})
    student_id = student_data["student_id"]
    safe_name = html.escape(str(student_data.get("name", "Student")))
    safe_student_id = html.escape(str(student_data.get("student_id", "N/A")))

    # ── Gradient header ──────────────────────────────────────────────────────
    st.markdown(
        f"""
<div class="dash-header">
    <div class="dash-role-badge">
        <span class="material-symbols-rounded" style="font-size:0.8rem;">person</span>
        Student Portal
    </div>
    <h1 class="dash-name">Welcome back, {safe_name}</h1>
    <p class="dash-meta">Student ID: {safe_student_id}</p>
</div>""",
        unsafe_allow_html=True,
    )

    st.markdown("<div class='section-gap-sm'></div>", unsafe_allow_html=True)

    # ── Data loading ─────────────────────────────────────────────────────────
    with st.spinner("Loading your enrolled subjects.."):
        subjects = get_student_subject(student_id)
        logs = get_student_attendance(student_id)

    stats_map = {}
    for log in logs:
        sid = log["subject_id"]
        if sid not in stats_map:
            stats_map[sid] = {"total": 0, "attended": 0}
        stats_map[sid]["total"] += 1
        if log.get("is_present"):
            stats_map[sid]["attended"] += 1

    # ── Compute KPI values ───────────────────────────────────────────────────
    enrolled_count = len(subjects)
    total_attended = sum(stats_map[sid]["attended"] for sid in stats_map)
    total_sessions = sum(stats_map[sid]["total"] for sid in stats_map)
    rate = (total_attended / total_sessions * 100) if total_sessions > 0 else 0
    rate_accent = "#10B981" if rate >= 75 else "#F59E0B"
    rate_bg = "#ECFDF5" if rate >= 75 else "#FFFBEB"
    rate_sub_class = "positive" if rate >= 75 else "negative"

    # ── KPI row ───────────────────────────────────────────────────────────────
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.markdown(
            _kpi_card(
                icon="book",
                value=str(enrolled_count),
                label="Enrolled Subjects",
                sub="Active enrollments",
                accent="#2563EB",
                bg="#EFF6FF",
                icon_color="#2563EB",
                sub_class="neutral",
            ),
            unsafe_allow_html=True,
        )
    with k2:
        st.markdown(
            _kpi_card(
                icon="event_available",
                value=str(total_attended),
                label="Sessions Attended",
                sub="Across all subjects",
                accent="#10B981",
                bg="#ECFDF5",
                icon_color="#10B981",
                sub_class="positive",
            ),
            unsafe_allow_html=True,
        )
    with k3:
        st.markdown(
            _kpi_card(
                icon="calendar_month",
                value=str(total_sessions),
                label="Total Sessions",
                sub="Cumulative sessions",
                accent="#8B5CF6",
                bg="#F5F3FF",
                icon_color="#8B5CF6",
                sub_class="neutral",
            ),
            unsafe_allow_html=True,
        )
    with k4:
        st.markdown(
            _kpi_card(
                icon="percent",
                value=f"{rate:.1f}%",
                label="Attendance Rate",
                sub="≥75% required",
                accent=rate_accent,
                bg=rate_bg,
                icon_color=rate_accent,
                sub_class=rate_sub_class,
            ),
            unsafe_allow_html=True,
        )

    st.markdown("<div class='section-gap'></div>", unsafe_allow_html=True)

    # ── Section header row ───────────────────────────────────────────────────
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(
            "<h2 class='section-heading'>Your Enrolled Subjects</h2>",
            unsafe_allow_html=True,
        )
    with col2:
        if st.button("Enroll in Subject", type="primary", width="stretch"):
            enroll_dialog()

    st.markdown("<div class='section-gap-xs'></div>", unsafe_allow_html=True)

    # ── Subject grid ─────────────────────────────────────────────────────────
    cols = st.columns(2)
    for i, sub_node in enumerate(subjects):
        sub = sub_node["subjects"]
        sid = sub["subject_id"]
        stats = stats_map.get(sid, {"total": 0, "attended": 0})

        def unenroll_button():
            if st.button(
                ":material/exit_to_app: Unenroll", type="tertiary", width="stretch"
            ):
                unenroll_student_to_subject(student_id, sid)

        with cols[i % 2]:
            subject_card(
                name=sub["name"],
                code=sub["subject_code"],
                section=sub["section"],
                stats=[
                    ("🗓️", "Total", stats["total"]),
                    ("✅", "Attended", stats["attended"]),
                ],
                footer_callback=unenroll_button,
                index=i,
            )


def student_page():
    show_registration = False
    style_base_layout()
    if "student_data" in st.session_state:
        student_dashboard()
        return
    header_home()

    # ── Instruction card ─────────────────────────────────────────────────────
    st.markdown(
        """
<div style="background:#EFF6FF; border:1px solid #DBEAFE; border-radius:14px; padding:1.25rem 1.5rem; margin-bottom:1rem;">
    <p style="margin:0; font-size:0.78rem; font-weight:700; letter-spacing:0.08em; text-transform:uppercase; color:#2563EB;">Face Recognition Login</p>
    <p style="margin:0.35rem 0 0; font-size:0.9rem; color:#374151; line-height:1.6;">Position your face clearly in the camera. The AI will identify you automatically and log you in.</p>
</div>""",
        unsafe_allow_html=True,
    )

    if st.button(
        ":material/arrow_back: Back to Home", key="student_back", type="tertiary"
    ):
        st.session_state["login_type"] = None
        st.rerun()

    photo_source = st.camera_input("Position your face in the centre")

    if photo_source:
        img = np.array(Image.open(photo_source))
        with st.spinner("AI is scanning"):
            detected, all_ids, num_faces = predict_attendance(img)
            if num_faces == 0:
                st.warning("face not found")
            elif num_faces > 1:
                st.warning("multiple faces found")
            else:
                if detected:
                    student_id = list(detected.keys())[0]
                    all_students = get_all_students()
                    student = next(
                        (s for s in all_students if s["student_id"] == student_id), None
                    )
                    if student:
                        st.session_state.is_logged_in = True
                        st.session_state.user_role = "student"
                        st.session_state["login_type"] = "student"
                        st.session_state.student_data = student
                        st.toast(f"Welcome Back{student['name']}")
                        time.sleep(3)
                        st.rerun()
                else:
                    st.info("Face not recognized! You might be a new student!")
                    show_registration = True

    # ── Registration form ─────────────────────────────────────────────────────
    if show_registration:
        with st.container(border=True):
            st.markdown(
                "<p class='page-eyebrow'>New Student</p>", unsafe_allow_html=True
            )
            st.markdown(
                "<h3 class='section-heading'>Register New Profile</h3>",
                unsafe_allow_html=True,
            )
            new_name = st.text_input("Enter your name", placeholder="Rahul Yadav")
            st.markdown("<div class='section-gap-xs'></div>", unsafe_allow_html=True)
            st.markdown(
                "<p style='margin:0 0 0.35rem; font-size:0.78rem; font-weight:700; "
                "letter-spacing:0.08em; text-transform:uppercase; color:#6B7280;'>"
                "Optional: Voice Enrollment</p>",
                unsafe_allow_html=True,
            )
            st.info("Enroll your voice for voice-only attendance")
            audio_data = None
            try:
                audio_data = st.audio_input(
                    "Record a short Phrase like i am present, My name is Rahul."
                )
            except Exception as e:
                st.error("Audio Data Failed!")
            if st.button("create account", type="primary"):
                if new_name:
                    with st.spinner("creating profile..."):
                        img = np.array(Image.open(photo_source))
                        encoding = get_face_embedding(img)
                        if encoding:
                            face_emb = encoding[0].tolist()
                            voice_emb = None
                            if audio_data:
                                voice_emb = get_voice_embedding(audio_data.read())
                            response_data = create_student(
                                new_name,
                                face_embedding=face_emb,
                                voice_embedding=voice_emb,
                            )
                            if response_data:
                                t = train_classifier()
                                st.session_state.is_logged_in = True
                                st.session_state.user_role = "student"
                                st.session_state["login_type"] = "student"
                                st.session_state.student_data = response_data[0]
                                st.toast(f"Profile Created! Hi {new_name}!")
                                time.sleep(1)
                                st.rerun()
                        else:
                            st.warning(
                                "couldn't capture your facial features for registration"
                            )
                else:
                    st.warning("Please enter your name!")
