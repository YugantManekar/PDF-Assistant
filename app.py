import os
import uuid
import requests
import streamlit as st
from dotenv import load_dotenv

# Load env
load_dotenv()
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

LANGUAGES = [
    "English", "Hindi", "Bengali", "Telugu", "Marathi", "Tamil"
]

st.set_page_config(page_title="Gemini PDF Assistant", layout="wide")
st.title("📄 Gemini PDF Assistant")

# ---------- Session Init ----------
if "session_id" not in st.session_state:
    res = requests.post(f"{BACKEND_URL}/create_session")
    st.session_state.session_id = res.json()["session_id"]

if "messages" not in st.session_state:
    st.session_state.messages = []

if "tts_language" not in st.session_state:
    st.session_state.tts_language = "English"

# ---------- Sidebar ----------
st.sidebar.header("⚙️ Settings")

language = st.sidebar.selectbox(
    "TTS Language",
    LANGUAGES,
    index=LANGUAGES.index(st.session_state.tts_language)
)

if language != st.session_state.tts_language:
    requests.post(
        f"{BACKEND_URL}/update_tts_language",
        params={
            "session_id": st.session_state.session_id,
            "language": language
        }
    )
    st.session_state.tts_language = language

uploaded_file = st.sidebar.file_uploader("Upload PDF", type="pdf")

if uploaded_file:
    files = {
        "file": (
            uploaded_file.name,
            uploaded_file.getvalue(),
            "application/pdf"
        )
    }
    res = requests.post(
        f"{BACKEND_URL}/upload_pdf",
        files=files,
        params={"session_id": st.session_state.session_id}
    )
    if res.status_code == 200:
        st.sidebar.success("PDF processed successfully")
        st.session_state.messages = []
    else:
        st.sidebar.error("PDF upload failed")

# ---------- Chat History ----------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---------- Chat Input ----------
if prompt := st.chat_input("Ask something about the PDF..."):
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            res = requests.post(
                f"{BACKEND_URL}/chat",
                json={
                    "session_id": st.session_state.session_id,
                    "question": prompt
                }
            )

            if res.status_code == 200:
                data = res.json()
                answer = data["answer"]
                translated = data.get("translated_answer") or answer

                st.markdown(answer)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })

                # Auto TTS
                tts = requests.post(
                    f"{BACKEND_URL}/generate_tts",
                    json={
                        "text": translated,
                        "language": st.session_state.tts_language
                    }
                )
                if tts.status_code == 200:
                    st.audio(tts.json()["audio"], format="audio/mpeg", autoplay=True)

            else:
                st.error(res.text)

        except Exception as e:
            st.error(str(e))

# ---------- Footer ----------
st.sidebar.button(
    "🗑 Clear Chat",
    on_click=lambda: st.session_state.update({"messages": []})
)

if not uploaded_file:
    st.info("⬅ Upload a PDF to start chatting")
