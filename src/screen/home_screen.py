from base64 import b64encode
from pathlib import Path

import streamlit as st

from src.components.header import header_home
from src.ui.base_layout import style_base_layout


def _icon(name: str) -> str:
    return f"<span class='material-symbols-rounded'>{name}</span>"


def _feature_card(title: str, description: str, icon_name: str) -> None:
    st.markdown(
        f"""
        <div class="feature-card">
            <div class="feature-card__icon">{_icon(icon_name)}</div>
            <h3 class="feature-card__title">{title}</h3>
            <p class="feature-card__text">{description}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _metric_card(value: str, label: str, icon_name: str) -> None:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-card__icon">{_icon(icon_name)}</div>
            <div class="metric-card__value">{value}</div>
            <div class="metric-card__label">{label}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _portal_card(
    title: str, description: str, points: list[str], badge: str, icon_name: str
) -> None:
    points_html = "".join(
        f"<li>{_icon('check_circle')}<span>{point}</span></li>" for point in points
    )
    st.markdown(
        f"""
        <div class="portal-card">
            <div class="portal-card__header">
                <div>
                    <div class="portal-badge">{badge}</div>
                    <h3 class="portal-card__title">{title}</h3>
                </div>
                <div class="portal-card__icon">{_icon(icon_name)}</div>
            </div>
            <p class="portal-card__text">{description}</p>
            <ul class="portal-points">{points_html}</ul>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _hero_visual() -> None:
    base_path = Path(__file__).resolve().parents[2]
    face_image = base_path / "assets" / "face_recognition.png"
    face_image_src = ""

    if face_image.exists():
        face_image_src = f"data:image/png;base64,{b64encode(face_image.read_bytes()).decode('ascii')}"

    st.markdown(
        f"""
        <div class="hero-visual">
            <div class="hero-visual__canvas">
                <div class="hero-visual__chips">
                    <span class="chip primary"><span class="material-symbols-rounded">camera</span>Face Recognition</span>
                    <span class="chip"><span class="material-symbols-rounded">school</span>Education</span>
                    <span class="chip"><span class="material-symbols-rounded">cloud</span>Cloud</span>
                    <span class="chip"><span class="material-symbols-rounded">analytics</span>Analytics</span>
                </div>
                <div class="hero-image-wrap">
                    <img src="{face_image_src}" alt="Face recognition preview" style="display:block;width:100%;max-width:240px;height:auto;object-fit:contain;" />
                </div>
                <div class="hero-meta">
                    <span class="hero-meta__item">Secure authentication</span>
                    <span class="hero-meta__item">Attendance analytics</span>
                    <span class="hero-meta__item">Fast onboarding</span>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def home_page():
    style_base_layout()
    header_home()

    left, right = st.columns([1.15, 0.95], gap="large")

    with left:
        st.markdown(
            """
            <div class="hero-section">
                <p class="section-kicker">AI-first attendance workflow</p>
                <h1 class="hero-title">Smart Attendance System</h1>
                <div class="hero-subtitle">AI Powered Face Recognition Attendance Platform</div>
                <p class="hero-description">The interface keeps teacher and student flows distinct while sharing a single, modern system. High contrast, large targets, and clear hierarchy keep the app usable in real classrooms.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        action_left, action_right = st.columns(2, gap="small")
        with action_left:
            if st.button(
                "Teacher Portal",
                key="home_teacher_portal",
                type="primary",
                use_container_width=True,
            ):
                st.session_state["login_type"] = "teacher"
                st.rerun()
        with action_right:
            if st.button(
                "Student Portal",
                key="home_student_portal",
                type="secondary",
                use_container_width=True,
            ):
                st.session_state["login_type"] = "student"
                st.rerun()

    with right:
        _hero_visual()

    st.markdown("<div class='section-gap'></div>", unsafe_allow_html=True)
    st.markdown(
        "<p class='section-kicker'>Core capabilities</p>", unsafe_allow_html=True
    )
    st.markdown(
        "<h2 class='section-title'>Built for fast recognition, secure access, and live analytics.</h2>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p class='section-description'>Every section is designed to reduce friction: faster check-ins for students, less manual work for teachers, and clearer visibility for administrators.</p>",
        unsafe_allow_html=True,
    )

    feature_col_1, feature_col_2, feature_col_3 = st.columns(3, gap="medium")
    with feature_col_1:
        _feature_card(
            "Fast Recognition",
            "Face verification happens in seconds so classrooms can keep moving without manual attendance bottlenecks.",
            "camera",
        )
    with feature_col_2:
        _feature_card(
            "Secure Authentication",
            "Role-based access, accurate identity matching, and a clean workflow help protect attendance data.",
            "security",
        )
    with feature_col_3:
        _feature_card(
            "Attendance Analytics",
            "Track trends, registration health, and daily activity with a clear analytics-first dashboard view.",
            "analytics",
        )

    st.markdown("<div class='section-gap'></div>", unsafe_allow_html=True)
    st.markdown("<p class='section-kicker'>Portal access</p>", unsafe_allow_html=True)
    st.markdown(
        "<h2 class='section-title'>Choose the workspace that matches your role.</h2>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p class='section-description'>Each portal is designed with its own priorities, but both share the same strong visual system and simple navigation.</p>",
        unsafe_allow_html=True,
    )

    portal_col_1, portal_col_2 = st.columns(2, gap="large")
    with portal_col_1:
        _portal_card(
            "Teacher Portal",
            "Manage classes, review records, and oversee attendance with a focused dashboard built for daily teaching workflows.",
            [
                "Daily attendance controls",
                "Classroom management tools",
                "Reports and history at a glance",
            ],
            "For staff",
            "school",
        )
        if st.button(
            "Open Teacher Portal",
            key="teacher_portal",
            type="primary",
            use_container_width=True,
        ):
            st.session_state["login_type"] = "teacher"
            st.rerun()

    with portal_col_2:
        _portal_card(
            "Student Portal",
            "Check attendance status, review participation, and stay aligned with your class schedule in a simple interface.",
            [
                "Quick attendance review",
                "Student-first navigation",
                "Mobile-friendly experience",
            ],
            "For students",
            "person",
        )
        if st.button(
            "Open Student Portal",
            key="student_portal",
            type="primary",
            use_container_width=True,
        ):
            st.session_state["login_type"] = "student"
            st.rerun()

    st.markdown("<div class='section-gap'></div>", unsafe_allow_html=True)
    st.markdown("<p class='section-kicker'>Live metrics</p>", unsafe_allow_html=True)
    st.markdown(
        "<h2 class='section-title'>Operational overview in one glance.</h2>",
        unsafe_allow_html=True,
    )

    metric_col_1, metric_col_2, metric_col_3, metric_col_4 = st.columns(4, gap="medium")
    with metric_col_1:
        _metric_card("99.2%", "Recognition Accuracy", "check_circle")
    with metric_col_2:
        _metric_card("1,248", "Attendance Today", "dashboard")
    with metric_col_3:
        _metric_card("3,420", "Registered Students", "groups")
    with metric_col_4:
        _metric_card("0.4s", "Recognition Speed", "bolt")
