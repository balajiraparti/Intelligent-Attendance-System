# Development Rules — Smart Attendance System

> This document is the canonical guide for every developer and AI assistant working on this codebase.
> Follow it. Question it by opening a discussion — not by silently ignoring it.

---

## 🏗️ Architecture Rules

### Routing

This app uses **session-state routing**, not Streamlit's native multipage file system. The single
source of truth is `st.session_state["login_type"]`. All routing decisions flow through the
`match` block in `app.py`.

- [ ] **DO** set `st.session_state["login_type"]` and call `st.rerun()` to navigate between pages.
- [ ] **DO** add new role branches to the `match` block in `app.py` when a new role is introduced (e.g., `"admin"`).
- [ ] **DON'T** create files under a `pages/` directory. Streamlit will auto-register them as separate pages and break the routing model entirely.
- [ ] **DON'T** use `st.switch_page()` or `st.page_link()` — these are multipage-architecture APIs.
- [ ] **DON'T** navigate by changing the URL path. Use the `join-code` query param pattern in `app.py` as the only sanctioned exception.

**Correct navigation pattern:**
```python
# In any screen or component
if st.button("Go to Teacher Portal"):
    st.session_state["login_type"] = "teacher"
    st.rerun()
```

**Incorrect — do NOT do this:**
```python
# Never
st.switch_page("pages/teacher.py")
```

---

### File Placement

Every new file must land in the correct module. No exceptions.

| What you're building | Where it goes |
|---|---|
| A new page/screen | `src/screen/` |
| A dialog or reusable UI widget | `src/components/` |
| A database query function | `src/database/db.py` |
| AI/ML inference or training logic | `src/pipeline/` |
| Global CSS or design tokens | `src/ui/base_layout.py` |
| Supabase client init | `src/database/config.py` (already exists — do not duplicate) |

- [ ] **DO** keep each module's responsibility exactly one layer deep. A component calls a db function; it does not contain the query itself.
- [ ] **DON'T** write Supabase queries inside screen files (`teacher_screen.py`, `student_screen.py`, `home_screen.py`).
- [ ] **DON'T** import `supabase` from `src/database/config.py` directly in screen or component files — go through `src/database/db.py` instead.
- [ ] **DON'T** put ML inference logic inside a screen or dialog. It belongs in `src/pipeline/face_pipeline.py` or `src/pipeline/voice_pipeline.py`.

**Correct import chain:**
```
teacher_screen.py → db.get_teacher_subjects() → config.supabase (internal)
```

**Incorrect — do NOT do this:**
```python
# In teacher_screen.py — this bypasses the db module boundary
from src.database.config import supabase
response = supabase.table("subjects").select("*").execute()
```

---

### Page Initialisation

Every page function **must** call `style_base_layout()` as its very first statement before any
other Streamlit call. This injects the design system CSS. Without it, the page will render
unstyled.

- [ ] **DO** call `style_base_layout()` at the top of `home_page()`, `teacher_page()`, and `student_page()`, and any future page function.
- [ ] **DON'T** call `st.set_page_config()` anywhere except `app.py`. It must remain the first Streamlit call in the entire app execution.

**Correct:**
```python
# src/screen/teacher_screen.py
def teacher_page():
    style_base_layout()   # <-- always first
    header_teacher()
    # ... rest of page
```

---

## 🗄️ Database Rules

### All Queries Live in `db.py`

`src/database/db.py` is the **only** file allowed to call `supabase.table(...)`. Every query,
insert, update, and delete must be wrapped in a named function in that file.

- [ ] **DO** add a new function to `db.py` for every new query pattern, no matter how simple.
- [ ] **DO** return `response.data` from query functions — callers should never see the raw Supabase response object.
- [ ] **DON'T** write one-off `.select()` or `.insert()` calls in screens, components, or pipeline files.
- [ ] **DON'T** catch exceptions inside `db.py` and silently swallow them — let them propagate so the UI layer can show a meaningful error with `st.error()`.

**Correct:**
```python
# src/database/db.py
def get_enrolled_students(subject_id):
    response = supabase.table("subject_students") \
        .select("*, students(*)") \
        .eq("subject_id", subject_id) \
        .execute()
    return response.data
```

**Incorrect — do NOT do this:**
```python
# Inside dialog_enroll.py
from src.database.config import supabase
response = supabase.table("subject_students").select("*").eq("subject_id", sid).execute()
```

---

### Supabase-Specific Gotchas

- [ ] **DO** use `.select("*, related_table(count)")` for cheap aggregate counts rather than fetching full related rows just to call `len()`.
- [ ] **DO** use inner joins (`.select("*, related!inner(*)")`) when you need to filter by a related table's column, as done in `get_attendance_for_teacher()`.
- [ ] **DON'T** use raw SQL strings. The PostgREST query builder in the Supabase Python client is the only sanctioned query interface.
- [ ] **DON'T** store embeddings as anything other than a plain Python list before writing to Supabase. NumPy arrays are not JSON-serialisable. Convert with `.tolist()` before any insert — see `get_voice_embedding()` in `voice_pipeline.py` for the correct pattern.
- [ ] **DON'T** assume Supabase returns rows in insertion order. Always sort explicitly if order matters.
- [ ] **DON'T** store derived/computed values in the database when they can be calculated from raw data (e.g., `total_classes` is computed in `get_teacher_subjects()`, not stored as a column).

---

### Table & Column Names

The Supabase schema is the contract. These names are **frozen** — do not rename, alias, or shadow them in application code.

| Table | Key columns |
|---|---|
| `teachers` | `username`, `password`, `name` |
| `students` | `student_id`, `name`, `face_embedding`, `voice_embedding` |
| `subjects` | `subject_code`, `name`, `section`, `teacher_id` |
| `subject_students` | `student_id`, `subject_id` |
| `attendance_logs` | `student_id`, `subject_id`, `timestamp` |

- [ ] **DON'T** rename table or column names in any query, ORM mapping, or variable without a corresponding verified migration on the Supabase side.

---

## 🤖 AI / ML Rules

### Model Caching

Both pipelines cache their heavy models with `@st.cache_resource`. This is non-negotiable — dlib
models and the `VoiceEncoder` are expensive to load and must not be re-initialised on every rerun.

Cached functions:
- `load_dflib_models()` — dlib detector, shape predictor, face recognition model (`face_pipeline.py`)
- `get_trained_model()` — the sklearn SVC classifier trained on student face embeddings (`face_pipeline.py`)
- `load_voice_encoder()` — resemblyzer `VoiceEncoder` (`voice_pipeline.py`)

- [ ] **DO** preserve every `@st.cache_resource` decorator on these functions. Removing one will make the app unusably slow.
- [ ] **DO** call `train_classifier()` after every new student registration. It calls `st.cache_resource.clear()` and immediately warms the cache back up by calling `get_trained_model()`.
- [ ] **DON'T** call `st.cache_resource.clear()` anywhere except inside `train_classifier()`. Clearing the cache indiscriminately evicts the dlib models and voice encoder, not just the SVC.
- [ ] **DON'T** add `@st.cache_data` to functions that return NumPy arrays or mutable ML objects — use `@st.cache_resource`.

**Retraining trigger (correct pattern):**
```python
# After a student's face embedding is saved to the DB:
from src.pipeline.face_pipeline import train_classifier
train_classifier()  # clears cache, retrains SVC, re-warms cache
```

---

### Thresholds

| Modality | Metric | Threshold | File |
|---|---|---|---|
| Face | Euclidean distance (lower = more similar) | `0.6` | `face_pipeline.py` → `predict_attendance()` |
| Voice | Cosine similarity (higher = more similar) | `0.65` | `voice_pipeline.py` → `identify_speaker()` |

- [ ] **DO** define thresholds as named constants at the top of their respective pipeline file if they need to change, rather than scattering magic numbers.
- [ ] **DON'T** change these thresholds without running a regression test across the enrolled student dataset. They are empirically tuned.
- [ ] **DON'T** invert the comparison direction. Face uses `score <= threshold` (lower distance = match). Voice uses `score >= threshold` (higher similarity = match). Swapping these will break recognition silently.

---

### Embeddings

- [ ] **DO** store face embeddings as a `list[float]` of length 128 (dlib output).
- [ ] **DO** store voice embeddings as a `list[float]` of length 256 (resemblyzer output).
- [ ] **DO** convert NumPy arrays to lists with `.tolist()` before any database write.
- [ ] **DON'T** normalise or post-process embeddings before storage — the pipeline functions consume raw dlib/resemblyzer output directly.
- [ ] **DON'T** attempt to compare face embeddings with voice embeddings, or mix embedding spaces.
- [ ] **DON'T** store embeddings in files, local directories, or any vector database (e.g., FAISS, Chroma). All embeddings live exclusively in the `students` table in Supabase.

---

### What NOT to Do with the SVC

- [ ] **DON'T** call `clf.predict()` when fewer than two distinct student embeddings exist. The pipeline handles this edge case by returning the only known student directly — preserve that branch in `predict_attendance()`.
- [ ] **DON'T** swap the SVC kernel from `"linear"` without benchmarking. The `linear` kernel with `class_weight="balanced"` is intentional for sparse, high-dimensional face embeddings.
- [ ] **DON'T** wrap pipeline calls in `@st.cache_data` — inference results are image/audio-dependent and must not be cached across reruns.

---

## 🔐 Security Rules

### Secrets

Supabase credentials are read exclusively from `.streamlit/secrets.toml` via `st.secrets`. This
file is already in `.gitignore` and must never be committed.

- [ ] **DO** verify `.streamlit/secrets.toml` is listed in `.gitignore` before every commit that touches the `.streamlit/` directory.
- [ ] **DO** provide a `.streamlit/secrets.toml.example` file (with placeholder values) for new developers to copy.
- [ ] **DON'T** hardcode `SUPABASE_URL` or `SUPABASE_SECRET_KEY` anywhere in source code.
- [ ] **DON'T** print, log, or display secrets — not even partial values — in `st.write()`, `st.error()`, or `print()`.
- [ ] **DON'T** commit `.env` files containing credentials. The project uses `st.secrets`, not `python-dotenv`.

**Correct secret access (already implemented in `src/database/config.py`):**
```python
supabase = create_client(
    st.secrets["SUPABASE_URL"],
    st.secrets["SUPABASE_SECRET_KEY"],
)
```

---

### Authentication

- [ ] **DO** hash teacher passwords with `bcrypt` via `hash_pass()` in `db.py` before any database write.
- [ ] **DO** verify passwords with `check_pass()` in `db.py` — never compare plain-text passwords directly.
- [ ] **DON'T** store plain-text passwords for any role, under any circumstance.
- [ ] **DON'T** add a password field to the student registration flow. Students are biometric-only by design.
- [ ] **DON'T** expose teacher password hashes to the UI layer. `teacher_login()` returns the full teacher row from Supabase — strip the `password` key before storing the result in session state.

---

### User-Generated Content in HTML

Whenever user-supplied data (names, subject codes, sections) is interpolated into an HTML string
passed to `st.markdown(..., unsafe_allow_html=True)`, it **must** be escaped.

- [ ] **DO** use `html.escape()` (imported as `_html` in `teacher_screen.py`) on every user-controlled value embedded in an HTML string.
- [ ] **DON'T** assume Supabase-returned strings are safe for direct HTML interpolation.

**Correct:**
```python
import html
safe_name = html.escape(student["name"])
st.markdown(f"<p class='student-name'>{safe_name}</p>", unsafe_allow_html=True)
```

**Incorrect:**
```python
# XSS risk if student["name"] contains "<script>..."
st.markdown(f"<p class='student-name'>{student['name']}</p>", unsafe_allow_html=True)
```

---

## 🎨 UI / Design Rules

### CSS Architecture

All CSS lives in **one place only**: `src/ui/base_layout.py` inside the `style_base_layout()`
function. It is injected via `st.markdown(..., unsafe_allow_html=True)` at the start of every
page render.

- [ ] **DO** add new component styles to `src/ui/base_layout.py`. Keep them grouped logically with a comment header.
- [ ] **DO** use CSS variables for all colour values in HTML strings: `var(--primary)`, `var(--success)`, `var(--error)`, etc.
- [ ] **DON'T** scatter `<style>` blocks across screen or component files. If a component needs styles, they go in `base_layout.py`.
- [ ] **DON'T** use hardcoded hex colours in HTML strings passed to `st.markdown()`. Use CSS variables.
- [ ] **DON'T** use `st.markdown()` with inline `style="color: #2563EB"`. Reference a design-system class instead.

**Correct:**
```python
st.markdown(
    "<h2 class='section-title'>Attendance Dashboard</h2>",
    unsafe_allow_html=True,
)
```

**Incorrect:**
```python
# Hardcoded hex — do not do this
st.markdown(
    "<h2 style='color: #2563EB; font-family: Poppins;'>Attendance Dashboard</h2>",
    unsafe_allow_html=True,
)
```

---

### Design Tokens

| Token | Value | Usage |
|---|---|---|
| `--primary` | `#2563EB` | Primary actions, links, active states |
| `--success` | `#10B981` | Confirmed attendance, success toasts |
| Heading font | Poppins | All `h1`–`h3` elements |
| Body font | Inter | All body copy, labels, inputs |

Both fonts are loaded via a Google Fonts import inside `style_base_layout()`. Do not load them
again in component files.

---

### Dialogs

Dialogs are opened with Streamlit's `@st.dialog` decorator. Every dialog function is in
`src/components/`.

- [ ] **DO** decorate every dialog function with `@st.dialog("Dialog Title")`.
- [ ] **DO** call `st.rerun()` after a successful action inside a dialog to close it and refresh the parent page.
- [ ] **DON'T** build modal-like behaviour with `st.empty()`, `st.container()`, or conditional rendering blocks. Use `@st.dialog`.
- [ ] **DON'T** call `style_base_layout()` inside a dialog — CSS is already injected by the parent page.

**Correct:**
```python
# src/components/dialog_create_subject.py
@st.dialog("Create New Subject")
def create_subject_dialog(teacher_id):
    ...
    if st.button("Create Subject", type="primary"):
        create_subject(sub_id, sub_name, sub_section, teacher_id)
        st.rerun()
```

---

### Sidebar

The sidebar is **intentionally collapsed** (`initial_sidebar_state="collapsed"` in `app.py`). This
is a deliberate UX decision — the app uses in-page navigation via session state, not sidebar nav.

- [ ] **DON'T** add `st.sidebar.*` widgets anywhere in the codebase.
- [ ] **DON'T** change `initial_sidebar_state` to `"expanded"` or `"auto"`.

---

## ✅ What To Do

- [ ] Always call `style_base_layout()` as the first line of every page function.
- [ ] Always use the existing `db.py` functions before writing a new query — check if one already exists.
- [ ] Always convert NumPy arrays to `.tolist()` before writing embeddings to Supabase.
- [ ] Always call `train_classifier()` after saving a new face embedding so the SVC reflects the new student immediately.
- [ ] Always use `@st.dialog` for overlay interactions and `st.rerun()` to close dialogs after success.
- [ ] Always escape user-generated content with `html.escape()` before interpolating into HTML strings.
- [ ] Always add new pip dependencies to `requirements.txt` with pinned versions and verify they install cleanly.
- [ ] Always keep `SUPABASE_URL` and `SUPABASE_SECRET_KEY` in `.streamlit/secrets.toml` and nowhere else.
- [ ] Always use CSS classes and design-system variables from `base_layout.py` for colours and typography.
- [ ] Always give Streamlit widgets a unique `key=` argument when the same widget type appears more than once on a page.
- [ ] Always keep the `@st.cache_resource` decorator on `load_dflib_models()`, `get_trained_model()`, and `load_voice_encoder()`.

---

## ❌ What To Avoid

- [ ] **Never** create a `pages/` directory or use Streamlit's multipage architecture.
- [ ] **Never** call `st.set_page_config()` anywhere except `app.py`.
- [ ] **Never** write a Supabase query outside of `src/database/db.py`.
- [ ] **Never** import `supabase` from `src/database/config.py` in screen, component, or pipeline files.
- [ ] **Never** hardcode `SUPABASE_URL` or `SUPABASE_SECRET_KEY` in source code.
- [ ] **Never** store embeddings as NumPy arrays in Supabase — always `.tolist()` first.
- [ ] **Never** store face/voice embeddings in local files or a vector database; Supabase is the only store.
- [ ] **Never** change the face threshold (`0.6`) or voice threshold (`0.65`) without empirical validation.
- [ ] **Never** remove `@st.cache_resource` from model-loading functions.
- [ ] **Never** call `st.cache_resource.clear()` outside of `train_classifier()`.
- [ ] **Never** add `st.sidebar.*` widgets — the sidebar is intentionally hidden.
- [ ] **Never** give a student a password during registration — students authenticate via biometrics only.
- [ ] **Never** interpolate unescaped user data into HTML strings passed to `st.markdown(..., unsafe_allow_html=True)`.
- [ ] **Never** use hardcoded hex colour values in inline styles — use CSS variables.
- [ ] **Never** scatter `<style>` blocks across component or screen files — CSS belongs in `base_layout.py`.
- [ ] **Never** rename database table or column names in application code without a verified schema migration.
- [ ] **Never** add a new role (e.g., Admin) by duplicating the Teacher screen — add it as a new branch in `app.py` and a new file in `src/screen/`.
- [ ] **Never** use raw SQL strings in any database call — use the PostgREST query builder.

---

## 🤖 AI Assistant Boundaries

These rules apply specifically to LLMs and AI coding assistants (Copilot, Claude, Cursor, etc.)
working on this repository. They exist to prevent silent regressions in routing, security, and
ML behaviour.

- [ ] **Never rewrite business logic in `src/database/db.py` or pipeline files.** Refactoring the function signatures or internal logic of `get_trained_model()`, `predict_attendance()`, `identify_speaker()`, or any `db.py` function is out of scope unless the user explicitly requests it and describes the exact desired change.
- [ ] **Never remove session state keys.** Every key in `st.session_state` (`login_type`, `is_logged_in`, `user_role`, etc.) is load-bearing. Removing or renaming one will silently break routing or auth state.
- [ ] **Never change the routing mechanism.** The `match st.session_state["login_type"]` block in `app.py` is the router. Do not replace it with `st.navigation()`, `st.page_link()`, or any multipage API.
- [ ] **Always call `style_base_layout()` at the start of every page function.** If you generate a new page or scaffold a new screen, the first line of the function body must be `style_base_layout()`.
- [ ] **Never add hardcoded secrets.** If a feature requires a new credential, instruct the developer to add it to `.streamlit/secrets.toml` and access it via `st.secrets["KEY_NAME"]`.
- [ ] **Never switch to Streamlit multipage architecture.** Do not create a `pages/` directory. Do not use `st.navigation()` or `st.Page()`.
- [ ] **Preserve all `@st.cache_resource` decorators.** Do not remove, replace with `@st.cache_data`, or add arguments that would disable caching on `load_dflib_models()`, `get_trained_model()`, or `load_voice_encoder()`.
- [ ] **Never change DB table names or column names** in query strings. The names in `db.py` match the live Supabase schema exactly.
- [ ] **Always use `html.escape()` for user-generated content in HTML strings.** Any value that originates from a database row or a form input must be escaped before being placed inside an `st.markdown()` HTML string.
- [ ] **Never install new ML libraries without updating `requirements.txt`.** If a suggestion requires a new import, provide the pinned `pip install` line and the `requirements.txt` addition explicitly.
- [ ] **`resemblyzer` and `librosa` must be present in `requirements.txt`.** These are runtime dependencies of `src/pipeline/voice_pipeline.py` and are currently missing from the pinned list — add them with pinned versions before any voice pipeline changes.
- [ ] **Always preserve the `@st.dialog` decorator on dialog functions.** Do not refactor dialogs into `st.expander`, `st.container`, or conditional rendering patterns.
- [ ] **Do not add `st.sidebar.*` widgets.** The sidebar is intentionally collapsed. Any suggestion that adds sidebar content is incorrect for this codebase.
- [ ] **Do not use `st.set_page_config()` anywhere except `app.py`.** Calling it in any other file will raise a Streamlit runtime error.
- [ ] **Do not bypass `db.py` when writing database queries.** All Supabase calls must be wrapped in a named function in `src/database/db.py` and called from there.
- [ ] **Do not generate a `pages/` directory** under any circumstances, even if asked to "add a new page."

---

## 📦 Dependency Rules

Before adding any new package:

1. **Check if the functionality already exists** in the current stack. `scikit-learn`, `numpy`, `scipy`, `pandas`, `pillow`, and `librosa` cover a large surface area.
2. **Verify compatibility** with Python and with existing pinned versions (especially `numpy`, `scikit-learn`, and `streamlit`).
3. **Pin the exact version** in `requirements.txt`. Use `pip show <package>` after installing to get the installed version, then pin it.
4. **Test the full install** from a clean virtual environment before committing: `pip install -r requirements.txt`.
5. **Document why** the new package is needed in the PR description or commit message.

- [ ] **DO** add `resemblyzer` and `librosa` to `requirements.txt` immediately — they are already used in `voice_pipeline.py` but are missing from the pinned list.
- [ ] **DON'T** add a new ML framework (PyTorch, TensorFlow, ONNX Runtime) without explicit discussion. The dlib + sklearn + resemblyzer stack is intentional and lightweight.
- [ ] **DON'T** add packages that duplicate existing ones (e.g., `face_recognition` when `dlib-bin` and `face-recognition-models` are already present and used directly).
- [ ] **DON'T** leave transitive dependencies unlisted. Run `pip freeze` and merge any new transitive entries into `requirements.txt`.

---

## 🧪 Testing Considerations

There is no formal test suite. All verification is manual. Before merging any change, walk through
the following checklist depending on what was modified:

### After any change to `src/database/db.py`
- [ ] Verify the affected query returns the expected data structure by printing the result in a temporary `st.write()` and removing it before commit.
- [ ] Check that embeddings read from Supabase are plain Python lists, not strings or None, for any student with a registered biometric.

### After any change to `src/pipeline/face_pipeline.py`
- [ ] Register a test student with a known face embedding and verify `predict_attendance()` returns their `student_id` for a matching image.
- [ ] Verify the single-student edge case: only one student enrolled, recognition still works.
- [ ] Confirm `train_classifier()` completes without error and that `get_trained_model()` returns a non-None result after retraining.

### After any change to `src/pipeline/voice_pipeline.py`
- [ ] Verify `get_voice_embedding()` returns a list of 256 floats for a valid audio input.
- [ ] Verify `identify_speaker()` returns `None` when similarity is below `0.65`.
- [ ] Verify `process_bulk_audio()` correctly segments and identifies multiple speakers.

### After any change to `src/ui/base_layout.py`
- [ ] Reload all three pages (`home_page`, `teacher_page`, `student_page`) and visually check for regressions in layout, typography, and colour.
- [ ] Check on both a wide and a narrow browser window.

### After any change to routing in `app.py`
- [ ] Test the full login → dashboard → logout flow for both Teacher and Student roles.
- [ ] Test the `?join-code=` query param flow: paste a join link, verify the student auto-enroll dialog opens.
- [ ] Verify that navigating directly to `http://localhost:8501` (no query params) lands on `home_page`.

### After adding a new dependency
- [ ] Delete the `venv/` directory, recreate it, and run `pip install -r requirements.txt` from scratch to confirm the install is clean.

### General
- [ ] No `st.write()` or `print()` debug statements in committed code.
- [ ] No credentials, even test credentials, committed to source control.
- [ ] Run `streamlit run app.py` and confirm zero import errors on a clean start.
