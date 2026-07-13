import streamlit as st
import numpy as np
import html
from src.components.header import header_home
from src.ui.base_layout import style_base_layout
from src.pipeline.face_pipeline import predict_attendance,get_face_embedding,train_classifier
from src.database.db import get_all_students,create_student,get_student_subject,get_student_attendance,unenroll_student_to_subject
from src.pipeline.voice_pipeline import get_voice_embedding
from PIL import Image
from src.components.dialog_enroll import enroll_dialog
from src.components.subject_card import subject_card
import time

def student_dashboard():
    student_data = st.session_state.get("student_data", {})
    student_id=student_data['student_id']
    safe_name = html.escape(str(student_data.get('name', 'Student')))
    safe_student_id = html.escape(str(student_data.get('student_id', 'N/A')))

    st.markdown(
        """
        <style>
            .student-hero {
                background: linear-gradient(135deg, #ecfeff 0%, #eff6ff 55%, #f8fafc 100%);
                border: 1px solid #dbeafe;
                border-radius: 16px;
                padding: 20px 24px;
                box-shadow: 0 8px 24px rgba(15, 23, 42, 0.06);
                margin-bottom: 12px;
            }
            .student-hero-tag {
                color: #0f766e;
                font-size: 0.8rem;
                text-transform: uppercase;
                letter-spacing: 0.08em;
                font-weight: 700;
                margin: 0;
            }
            .student-hero-title {
                color: #0f172a;
                font-size: 1.9rem;
                font-weight: 800;
                line-height: 1.25;
                margin: 0.2rem 0 0.35rem;
            }
            .student-hero-meta {
                color: #334155;
                margin: 0;
                font-size: 0.98rem;
            }
            .student-section-title {
                margin: 0.25rem 0;
                font-size: 1.05rem;
                font-weight: 700;
                color: #0f172a;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="student-hero">
            <p class="student-hero-tag">Student Dashboard</p>
            <h1 class="student-hero-title">Welcome, {safe_name}</h1>
            <p class="student-hero-meta"><strong>Student ID:</strong> {safe_student_id}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.space()

    col1,col2=st.columns(2)
    with col1:
            st.markdown("<p class='student-section-title'>Your Enrolled Subjects</p>", unsafe_allow_html=True)
    with col2:
        if st.button('Enroll in Subject',type='primary',width='stretch'):
            enroll_dialog()
    
    st.divider()
    with st.spinner('Loading your enrolled subjects..'):
        subjects=get_student_subject(student_id)
        logs=get_student_attendance(student_id)
    stats_map={
    }
    for log in logs:
        sid= log['subject_id']
        if sid not in stats_map:
            stats_map[sid]={"total":0,"attended":0}
        stats_map[sid]['total']+=1
        if logs.get('is_present'):
            stats_map[sid]['attended']+=1

    cols=st.columns(2)
    for i,sub_node in enumerate(subjects):
        sub=sub_node['subjects']
        sid=sub['subject_id']
        stats=stats_map.get(sid,{"total":0,"attended":0})
        def unenroll_button():
            if st.button("Unenroll from this coures",type='tertiary',width='stretch'):
                unenroll_student_to_subject(student_id,sid)
        with cols[i%2]:
            subject_card(name=sub['name'],code=sub['subject_code'],section=sub['section'],stats=[('🗓️','Total',stats['total']),('✅','Attended',stats['attended'])],footer_callback=unenroll_button)



def student_page():
    show_registration=False
    style_base_layout()
    if "student_data" in st.session_state:
        student_dashboard()
        return
    header_home()
    st.markdown("<div class='page-section'>", unsafe_allow_html=True)

    if st.button("Back to Home", key="student_back", use_container_width=True):
        st.session_state["login_type"] = None
        st.rerun()

    photo_source=st.camera_input("position your face in center")
    if photo_source:
        img=np.array(Image.open(photo_source))
        with st.spinner('AI is scanning'):
           detected,all_ids,num_faces=predict_attendance(img) 
           if num_faces == 0:
               st.warning("face not found")
           elif(num_faces>1):
               st.warning("multiple faces found")
           else:
               if detected:
                   student_id=list(detected.keys())[0]
                   all_students= get_all_students()
                   student=next((s for s in all_students if s['student_id']== student_id),None)
                   if student:
                       st.session_state.is_logged_in=True
                       st.session_state.user_role='student'
                       st.session_state["login_type"] = "student"
                       st.session_state.student_data=student
                       st.toast(f"Welcome Back{student['name']}")
            
                       time.sleep(3)
                       st.rerun()            
               else:
                   st.info("Face not recognized! You might be a new student!")
                   show_registration=True
    if show_registration:
        with st.container(border=True):
            st.header('Register new profile')
            new_name=st.text_input("Enter your name",placeholder="Rahul Yadav")
            st.subheader("optional: voice enrollment")
            st.info("enroll your for voice only attendance")
            audio_data=None
            try:
                audio_data=st.audio_input('Record a short Phrase like i am present, My name is Rahul.')

            except Exception as e:
                st.error('Audio Data Failed!')
            if st.button('create account',type='primary'):
                if new_name:
                    with st.spinner('creating profile...'):
                        img=np.array(Image.open(photo_source))
                        encoding=get_face_embedding(img)
                        if encoding:
                            face_emb=encoding[0].tolist()
                            voice_emb=None
                            if audio_data:
                                voice_emb=get_voice_embedding(audio_data.read())
                            response_data=create_student(new_name,face_embedding=face_emb,voice_embedding=voice_emb)
                            if response_data:
                                t=train_classifier()
                                st.session_state.is_logged_in=True
                                st.session_state.user_role='student'
                                st.session_state["login_type"] = "student"
                                st.session_state.student_data=response_data[0]
                                st.toast(f'Profile Created! Hi {new_name}!')
            
                                time.sleep(1)
                                st.rerun()  
                        else:
                            st.warning("couldn't capture your facial features for registration")
                else:
                    st.warning("Please enter your name!")
            
    st.markdown("</div>", unsafe_allow_html=True)