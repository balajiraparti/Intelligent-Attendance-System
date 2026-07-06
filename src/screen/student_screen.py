import streamlit as st
import numpy as np
from src.components.header import header_home
from src.ui.base_layout import style_base_layout
from src.pipeline.face_pipeline import predict_attendance,get_face_embedding,train_classifier
from src.database.db import get_all_students,create_student
from src.pipeline.voice_pipeline import get_voice_embedding
from PIL import Image
import time

def student_dashboard():
    st.write("student dashboard")
    st.header("DASHBOARD HERE")
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
                                st.session_state.student_data=response_data[0]
                                st.toast(f'Profile Created! Hi {new_name}!')
            
                                time.sleep(1)
                                st.rerun()  
                        else:
                            st.warning("couldn't capture your facial features for registration")
                else:
                    st.warning("Please enter your name!")
            
    st.markdown("</div>", unsafe_allow_html=True)