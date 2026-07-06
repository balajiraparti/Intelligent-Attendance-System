import streamlit as st


def header_home():
    st.markdown(
        """
        <div class="top-nav">
            <div class="top-nav__brand">
                <div class="brand-mark"><span class="material-symbols-rounded">face</span></div>
                <div>
                    <span class="brand-title">Smart Attendance</span>
                    <span class="brand-subtitle">AI Face Recognition Attendance Platform</span>
                </div>
            </div>
            <div class="top-nav__links">
                <span class="nav-link active">Overview</span>
                <span class="nav-link">Teacher Portal</span>
                <span class="nav-link">Student Portal</span>
                <span class="nav-link hide-mobile">Analytics</span>
            </div>
            <div class="top-nav__actions">
                <div class="nav-icon" title="Notifications"><span class="material-symbols-rounded">notifications</span></div>
                <div class="nav-icon" title="Settings"><span class="material-symbols-rounded">settings</span></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
