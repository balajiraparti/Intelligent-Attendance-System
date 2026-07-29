# Smart Attendance System — Product Requirements Document

> **Internal codename:** SNAP CLASS
> **Version:** 1.0 (V1)
> **Framework:** Streamlit 1.58.0 · **Database:** Supabase (PostgreSQL)
> **Status:** In Development

---

## 📋 1. Executive Summary

The **Smart Attendance System** (codename: SNAP CLASS) is a web-based attendance management platform built for educational institutions. It eliminates manual roll-call by leveraging AI-driven **face recognition** and **voice recognition** to automatically identify students from classroom photos or audio recordings.

Teachers take attendance in seconds by uploading a classroom photo or recording audio; the system identifies every recognised student and logs their presence. Students authenticate passively via a face scan and self-register in under a minute. The entire experience runs as a single-page Streamlit application, deployable with zero client-side installation required.

---

## 🔍 2. Problem Statement

Traditional attendance-taking in classrooms suffers from three compounding issues:

| Problem | Impact |
|---|---|
| Manual roll-call is time-consuming | Eats 5–10 minutes of class time per session |
| Paper or spreadsheet logs are error-prone | Mismarks, illegible entries, and proxy attendance |
| Students signing on behalf of absent peers | Academic integrity violations are hard to detect |

Existing digital solutions either require hardware (fingerprint scanners, RFID cards) or complex infrastructure. SNAP CLASS solves this with a software-only approach: teachers use the camera or a photo upload, and the AI handles the rest.

---

## 🎯 3. Goals & Success Metrics

### Primary Goals

- ✅ Reduce attendance-taking time per session to **under 60 seconds** for classes of up to 50 students.
- ✅ Achieve face recognition accuracy sufficient for reliable daily use (euclidean-distance threshold of **0.6**).
- ✅ Provide a frictionless student onboarding path (face scan → self-registration in **under 2 minutes**).
- ✅ Persist all attendance data reliably in Supabase with per-session, per-subject queryability.

### Success Metrics

| Metric | Target |
|---|---|
| Face recognition match rate | ≥ 90% of enrolled students identified per session |
| Voice recognition match rate | ≥ 85% of enrolled students identified per audio clip |
| Student self-registration completion rate | ≥ 95% of students who begin registration finish it |
| Teacher session setup time | ≤ 30 seconds from login to starting attendance |
| System availability | ≥ 99% uptime during class hours |

---

## 👥 4. Target Users

### 👩‍🏫 4.1 Teachers

**Profile:** Instructors at educational institutions who manage one or more class sections.

**Needs:**
- A fast, reliable way to record attendance without interrupting the flow of a lecture.
- The ability to review historical attendance logs grouped by session and subject.
- A simple mechanism to onboard students into their subjects (shareable links and QR codes).

**Technical Comfort:** Moderate. Teachers are assumed to be comfortable with web applications but are not expected to have technical expertise. The UI must be self-explanatory.

**Authentication:** Username + password (bcrypt-hashed). Registration requires a username, display name, and password. Session persists across Streamlit reruns via `st.session_state`.

---

### 🎓 4.2 Students

**Profile:** Enrolled students who attend classes managed by teachers on the platform.

**Needs:**
- Passwordless, frictionless login via face recognition.
- A clear view of their enrolled subjects and their own attendance statistics.
- An easy way to join a new subject using a code or a QR link shared by their teacher.

**Technical Comfort:** Variable. Students may be using the system on a shared classroom computer or their own device. The onboarding flow must require minimal instruction.

**Authentication:** Face recognition only — no username, password, or OTP is required. Unrecognised faces are guided through a self-registration flow.

---

### 🚫 4.3 Out of Scope for V1 (Admins)

No administrative role exists in V1. There is no institution-level management, no bulk user import, no cross-teacher reporting, and no system configuration dashboard. Administrative capabilities are deferred to a future release.

---

## ⚙️ 5. Feature Specifications

### 🔐 5.1 Authentication & Onboarding

#### Teacher Registration & Login

- **Registration fields:** `username` (unique), `display name`, `password`
- Passwords are hashed with **bcrypt** before storage; plaintext is never persisted.
- Credentials are stored in the `teachers` table (`teacher_id`, `username`, `password`, `name`).
- Login accepts `username` + `password`; session is maintained in `st.session_state` and survives Streamlit reruns.

#### Student Login — Face Recognition

1. Student opens the app and is directed to the student entry point.
2. The camera captures a frame or the student uploads a photo.
3. The face recognition pipeline (dlib + sklearn SVC classifier) runs inference against all registered student embeddings.
4. If a match is found (euclidean distance **≤ 0.6**), the student is logged in automatically.
5. If no match is found, the student is routed to the **self-registration flow**.

#### Student Self-Registration

Triggered when face recognition fails to identify a visitor.

1. Student enters their **full name**.
2. Student captures one or more face photos via the browser camera; embeddings are extracted and averaged.
3. Optionally, student records a **voice sample** for voice enrollment (used later for voice-based attendance).
4. Face embedding (128-d float array) and optional voice embedding are stored in the `students` table.
5. The face and voice classifiers are **retrained immediately** after registration to include the new student.
6. Student is logged in upon successful registration.

---

### 📚 5.2 Subject Management (Teacher)

Teachers can create and manage class subjects after logging in.

#### Creating a Subject

- **Required fields:** `subject_code` (unique across the system), `name`, `section`
- Subjects are stored in the `subjects` table with a foreign key linking to the creating teacher (`teacher_id`).

#### Sharing a Subject

- After creation, the teacher can view and share:
  - A **subject join link** in the format `/?join-code=<subject_code>`
  - A **QR code** encoding the same URL, suitable for display on a projector or printed handout
- Students who scan the QR code or visit the link are guided through enrollment automatically (see §5.7).

---

### 📷 5.3 AI Attendance — Face Recognition (Teacher)

The primary attendance-taking mechanism for teachers.

#### Workflow

1. Teacher navigates to the attendance panel for a specific subject.
2. Teacher provides one or more classroom photos via:
   - **File upload** (JPEG/PNG, multiple files accepted)
   - **Live camera capture** within the browser
3. Each image is processed by the face recognition pipeline:
   - dlib detects face bounding boxes.
   - 128-dimensional face embeddings are extracted using `face_recognition_models`.
   - The sklearn SVC classifier matches each embedding against registered students.
   - Matches with euclidean distance **> 0.6** are rejected as unrecognised.
4. Multiple photos from the same session are unioned — a student is marked present if identified in **any** of the uploaded images.
5. Identified students are displayed for teacher review before confirmation.
6. On confirmation, presence records are written to `attendance_logs` with `is_present = true`, `subject_id`, `student_id`, and an ISO-format `timestamp`.

#### Classifier Details

- **Algorithm:** sklearn Support Vector Classifier (SVC)
- **Input features:** 128-d face embeddings from dlib
- **Retraining trigger:** Any new student registration
- **Caching:** Model is loaded via `@st.cache_resource` to avoid redundant retraining across sessions

---

### 🎙️ 5.4 AI Attendance — Voice Recognition (Teacher)

An alternative attendance method using classroom audio.

#### Workflow

1. Teacher initiates a voice attendance session for a specific subject.
2. Teacher records classroom audio (e.g., asks students to say a phrase or answer a question).
3. The audio is processed by the voice recognition pipeline:
   - **librosa** performs audio segmentation to isolate individual speaker segments.
   - **resemblyzer** extracts voice embeddings for each segment.
   - Each embedding is compared against stored student voice embeddings using **cosine similarity**.
   - Segments with cosine similarity **≥ 0.65** are matched to a student.
4. Identified students are displayed for teacher review.
5. On confirmation, presence records are written to `attendance_logs`.

#### Voice Enrollment

- Students may optionally enroll a voice sample during self-registration.
- Voice embeddings are stored as a float array in the `students` table (`voice_embedding`, nullable).
- Students without a voice embedding cannot be identified via voice attendance but are unaffected in face-recognition sessions.

#### Dependency Note

> ⚠️ `resemblyzer` and `librosa` are **not included in `requirements.txt`** and must be installed manually in the deployment environment. Voice attendance will fail at runtime if these packages are absent.

---

### 📊 5.5 Attendance Records (Teacher)

Teachers can review all logged attendance for subjects they own.

#### Record View

- Records are grouped by **session** (timestamp bucket) and by **subject**.
- Each session entry shows:
  - Date and time of the session
  - List of students marked present
  - Total count of enrolled students vs. students present
- Teachers can drill into a specific subject to see per-student attendance history (sessions attended / total sessions).

#### Data Source

- All reads come from the `attendance_logs` table, joined with `students`, `subjects`, and `subject_students`.
- The teacher only sees records for subjects they created (`teacher_id` FK filter enforced).

---

### 🧑‍💻 5.6 Student Dashboard & Enrollment

After a successful face-recognition login, the student lands on their personal dashboard.

#### Dashboard Content

- List of all enrolled subjects, each showing:
  - Subject name, code, and section
  - **Total sessions** held in that subject
  - **Sessions attended** by this student
  - Attendance percentage (derived metric, computed in-app)
- Option to **unenroll** from any subject

#### Subject Enrollment (Manual)

- A dialog allows the student to type a **subject code** directly.
- On submission, a record is inserted into `subject_students` (`subject_id`, `student_id`).
- Duplicate enrollment attempts are rejected gracefully.

---

### 🔗 5.7 QR Code Deep-Link Enrollment

A streamlined path for students to enroll in a subject via a teacher-shared link or QR code.

#### URL Format

```
https://<app-url>/?join-code=<subject_code>
```

#### Enrollment Flow

1. Student scans the QR code or clicks the URL.
2. If **not logged in**: the app redirects to the student face-recognition login screen. The `join-code` query parameter is preserved in session state.
3. After successful **face-recognition login** (or self-registration), the app detects the stored `join-code` in session state.
4. `auto_enroll_dialog(join_code)` is called automatically, opening a pre-filled enrollment confirmation dialog.
5. Student confirms → enrollment record is created in `subject_students`.
6. The student is returned to their dashboard with the new subject visible.

This flow requires zero manual code entry from the student and is the recommended onboarding path for teachers distributing class links.

---

## 🛡️ 6. Non-Functional Requirements

### ⚡ 6.1 Performance

- Face recognition inference on a single image must complete in **≤ 5 seconds** on the deployment server.
- Voice segmentation and embedding extraction must complete in **≤ 15 seconds** for audio clips up to 2 minutes.
- Classifier retraining (triggered on new student registration) must complete in **≤ 10 seconds** for up to 500 enrolled students.
- Supabase queries (reads and writes) must complete in **≤ 2 seconds** under normal load.
- The Streamlit app must load to an interactive state in **≤ 4 seconds** on a standard broadband connection.

---

### 🔒 6.2 Security

- Teacher passwords are hashed with **bcrypt** before storage; plaintext passwords are never written to the database or logged.
- Supabase credentials (`SUPABASE_URL`, `SUPABASE_KEY`) are stored exclusively in `.streamlit/secrets.toml` and must never be committed to version control.
- Face embeddings and voice embeddings are stored as numeric float arrays — raw biometric data (photos, audio) is not persisted beyond the current request.
- Teacher records are scoped by `teacher_id`; a teacher cannot read or modify another teacher's subjects or attendance logs.
- Enrollment records are validated server-side to prevent a student from enrolling in a subject they are already in.
- No session tokens are issued to students; identity is re-confirmed via face recognition on each login.

---

### 🏗️ 6.3 Reliability

- All attendance writes are atomic single-row inserts to `attendance_logs`; partial session writes do not corrupt existing records.
- The face and voice classifiers are cached via `@st.cache_resource`; cache invalidation occurs only on new student registration to avoid unnecessary model churn.
- The application must handle the case where no students are registered (empty classifier) without crashing — an informative UI message is shown instead.
- Supabase is the single source of truth; no local file storage is used for persistent data.

---

### 🖥️ 6.4 Usability

- The app uses Streamlit's `layout="wide"` with the **sidebar collapsed by default** to maximise content area on classroom projectors and standard monitors.
- All primary teacher actions (take attendance, view records, share subject) are reachable in **≤ 2 clicks** from the post-login state.
- Student onboarding (first visit to login → enrolled in first subject) must be completable in **≤ 3 minutes** with no external instruction.
- Error messages must be human-readable and actionable (e.g., "No face detected in the uploaded image — please try a clearer photo").
- The UI must function on any modern desktop browser (Chrome, Firefox, Edge, Safari) without plugins or extensions.

---

## 🔧 7. Technical Constraints & Assumptions

| Constraint | Detail |
|---|---|
| **Framework** | Streamlit 1.58.0 — single-page application, no multi-page routing beyond query-param deep-links |
| **Database** | Supabase (hosted PostgreSQL); accessed via the Supabase Python client |
| **Secrets management** | `.streamlit/secrets.toml` for `SUPABASE_URL` and `SUPABASE_KEY` |
| **Face recognition stack** | dlib + `face_recognition_models` (128-d embeddings) + sklearn SVC |
| **Face match threshold** | Euclidean distance **≤ 0.6** for a positive identification |
| **Voice recognition stack** | resemblyzer (embeddings) + librosa (segmentation) |
| **Voice match threshold** | Cosine similarity **≥ 0.65** for a positive identification |
| **Voice dependencies** | `resemblyzer` and `librosa` must be installed manually; absent from `requirements.txt` |
| **Model caching** | `@st.cache_resource` used for both face and voice classifiers |
| **Retraining trigger** | Both classifiers are retrained on every new student registration |
| **Session state** | `st.session_state` used for all cross-rerun state (login, pending join-code, etc.) |
| **Deployment target** | Web-only; no mobile-native or desktop application |
| **Browser camera** | Browser's `getUserMedia` API used for live capture; requires HTTPS in production |
| **Student auth** | Face recognition only — no username/password, email, or OTP for students |
| **Multiple images** | Face attendance supports multiple images per session; union of all detections |

---

## ⚠️ 8. Known Limitations (V1)

1. **No admin role.** There is no institution-level dashboard, no bulk user management, and no cross-teacher analytics. All data access is scoped to individual teachers.

2. **Voice dependencies not packaged.** `resemblyzer` and `librosa` are excluded from `requirements.txt`. Voice attendance will fail silently or with an import error if the deployment environment has not had these packages installed manually.

3. **No real-time notifications.** Students are not notified when attendance is taken. Teachers receive no alerts when new students register or enroll in their subjects.

4. **No mobile-native app.** The platform is web-only. Camera capture depends on browser support for `getUserMedia` and may be degraded on some mobile browsers, particularly Safari on iOS.

5. **No email or OTP authentication for students.** Students have no fallback login method. If a student's face cannot be recognised (e.g., due to significant appearance change, occlusion, or poor lighting), they must re-register.

6. **Classifier accuracy degrades without retraining.** The SVC classifier is retrained only when a new student registers. It does not improve over time from additional images unless a new student registration occurs.

7. **Single-teacher subject ownership.** Subjects are owned by a single teacher. There is no co-teacher or shared-subject functionality.

8. **No attendance correction mechanism.** Teachers cannot retroactively edit or delete attendance records through the UI in V1. Manual correction requires direct database access.

9. **Subject code is globally unique.** Subject codes must be unique across all teachers, not just within a teacher's scope. This may cause conflicts in large deployments.

10. **No pagination on attendance records.** Large attendance histories are loaded in full; this may degrade performance for subjects with many sessions or many students.

---

## 🚀 9. Future Roadmap (V2+)

The following capabilities are explicitly deferred from V1 and represent the most frequently anticipated needs for a mature release.

| Priority | Feature | Description |
|---|---|---|
| 🔴 High | **Admin dashboard** | Institution-level user management, cross-teacher reporting, bulk student import |
| 🔴 High | **Voice dependency packaging** | Include `resemblyzer` and `librosa` in `requirements.txt`; document system-level dependencies (e.g., `ffmpeg`) |
| 🔴 High | **Attendance correction UI** | Allow teachers to manually mark, unmark, or adjust attendance records |
| 🟠 Medium | **Real-time notifications** | Notify students (via email or in-app) when attendance is recorded |
| 🟠 Medium | **Multi-teacher subject ownership** | Allow subjects to have co-owners or shared edit access |
| 🟠 Medium | **Improved face recognition** | Continuous learning from new face captures to improve match accuracy over time |
| 🟠 Medium | **Student photo update** | Allow students to retake their registration photo to handle appearance changes |
| 🟡 Low | **Export / reporting** | CSV and PDF export of attendance records per subject or student |
| 🟡 Low | **Mobile-optimised UI** | Responsive layout improvements for smaller screens and mobile browsers |
| 🟡 Low | **Multi-page Streamlit routing** | Migrate from query-param deep-links to Streamlit's native multi-page support |
| 🟡 Low | **Scoped subject codes** | Allow subject codes to be unique per teacher rather than globally, to reduce conflicts |
| 🟡 Low | **Session-level analytics** | Attendance trends, absentee alerts, and session-over-session comparisons for teachers |

---

*Document maintained by the SNAP CLASS development team. For architecture diagrams and system design, see `architecture.md`.*
