import time

import streamlit as st

from src.database.db import create_attendance


@st.dialog("Attendance Result")
def show_attendance_result(df, logs):
    present = (
        int(df["Status"].str.contains("Present").sum()) if "Status" in df.columns else 0
    )
    total = len(df)

    st.markdown(
        f"<p style='font-size:0.875rem; color:#6B7280; margin:0 0 1rem;'>"
        f"Review the detected attendance before saving. "
        f"<strong style='color:#10B981;'>{present} present</strong> / "
        f"<strong style='color:#111827;'>{total} total</strong>.</p>",
        unsafe_allow_html=True,
    )

    st.dataframe(df, hide_index=True, use_container_width=True)

    st.markdown("<div class='section-gap-xs'></div>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        if st.button(
            "Discard",
            use_container_width=True,
            type="tertiary",
            icon=":material/delete:",
        ):
            st.session_state.attendance_images = []
            st.session_state.voice_attendance_results = None
            st.rerun()
    with col2:
        if st.button(
            "Confirm & Save",
            use_container_width=True,
            type="primary",
            icon=":material/save:",
        ):
            try:
                create_attendance(logs)
                st.toast("Attendance saved successfully! ✅")
                st.session_state.attendance_images = []
                st.session_state.voice_attendance_results = None
                st.rerun()
            except Exception as e:
                st.error("Failed to save attendance. Please try again.")


def attendance_result_dialog(df, logs):
    show_attendance_result(df, logs)
