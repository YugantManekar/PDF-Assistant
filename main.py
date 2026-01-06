from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uuid
import os
from elevenlabs import ElevenLabs
client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))

from .models import ChatRequest, ChatResponse, TTSRequest
from .utils import clean_text, process_pdf
from .vector_store import vector_store_manager
from .rag_processor import RAGProcessor
from .config import LANGUAGES

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

@app.get("/")
def root():
    return {"status": "Backend is running "}

rag = RAGProcessor()
sessions = {}

@app.post("/create_session")
def create_session():
    sid = str(uuid.uuid4())
    sessions[sid] = "English"
    return {"session_id": sid}

@app.post("/upload_pdf")
async def upload_pdf(file: UploadFile = File(...), session_id: str = None):
    session_id = session_id or str(uuid.uuid4())
    vector_store_manager.add(session_id, process_pdf(await file.read()))
    return {"session_id": session_id}

@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    if not vector_store_manager.exists(req.session_id):
        raise HTTPException(404, "Session not found")

    chain = rag.create_chain(vector_store_manager.retriever(req.session_id))
    answer = clean_text(chain.invoke(req.question))

    lang = sessions.get(req.session_id, "English")
    translated = None if lang == "English" else rag.translate(answer, lang)

    return ChatResponse(answer=answer, translated_answer=translated)

@app.post("/generate_tts")
def generate_tts(request: TTSRequest):
    audio = client.text_to_speech.convert(
        text=request.text,
        model_id="eleven_multilingual_v2",
        voice_id="Rachel"
    )
    return {"audio": audio}
