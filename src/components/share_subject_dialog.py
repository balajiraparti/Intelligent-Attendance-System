import io

import segno
import streamlit as st


@st.dialog("Share Class Code")
def share_subject_dialog(subject_name, subject_code):
    app_domain = "http://localhost:8501"
    join_url = f"{app_domain}/?join-code={subject_code}"

    st.markdown(
        f"<p style='font-size:0.875rem; color:#6B7280; margin:0 0 1rem;'>"
        f"Share the QR code or copy the link below to let students join "
        f"<strong style='color:#111827;'>{subject_name}</strong>.</p>",
        unsafe_allow_html=True,
    )

    qr = segno.make(join_url)
    out = io.BytesIO()
    qr.save(out, kind="png", scale=10, border=2)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            "<p style='font-size:0.8rem; font-weight:700; letter-spacing:0.06em; "
            "text-transform:uppercase; color:#6B7280; margin:0 0 0.5rem;'>Join Link</p>",
            unsafe_allow_html=True,
        )
        st.code(join_url, language="text")
        st.markdown(
            "<p style='font-size:0.8rem; font-weight:700; letter-spacing:0.06em; "
            "text-transform:uppercase; color:#6B7280; margin:0.75rem 0 0.5rem;'>Subject Code</p>",
            unsafe_allow_html=True,
        )
        st.code(subject_code, language="text")
        st.info(
            "Copy the link or code and share it via WhatsApp, email, or any messaging app."
        )

    with col2:
        st.markdown(
            "<p style='font-size:0.8rem; font-weight:700; letter-spacing:0.06em; "
            "text-transform:uppercase; color:#6B7280; margin:0 0 0.5rem;'>Scan to Join</p>",
            unsafe_allow_html=True,
        )
        st.image(
            out.getvalue(),
            caption=f"QR code · {subject_code}",
            use_container_width=True,
        )
