from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
from dotenv import load_dotenv
import os
import io
from PyPDF2 import PdfReader
from groq import Groq

# ================= LOAD ENV =================
load_dotenv()

app = FastAPI()

# ================= CORS =================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ================= GROQ =================
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise Exception("GROQ_API_KEY not found in environment")

client = Groq(api_key=api_key)

# ================= MODELS =================
class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    message: str
    resume_text: Optional[str] = None
    jd_text: Optional[str] = None
    chat_history: List[ChatMessage] = []

class AnalyzeRequest(BaseModel):
    resume_text: str
    jd_text: str

# ================= GROQ CALL =================
def get_groq_response(messages, model="openai/gpt-oss-20b"):
    try:
        res = client.chat.completions.create(
            messages=messages,
            model=model,
        )
        return res.choices[0].message.content
    except Exception as e:
        print("GROQ ERROR:", e)
        return "Error processing request"

# ================= PDF =================
def extract_text_from_pdf(file: UploadFile):
    try:
        pdf_bytes = file.file.read()
        reader = PdfReader(io.BytesIO(pdf_bytes))

        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""

        file.file.seek(0)
        return text.strip()

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF parsing failed: {str(e)}")

# ================= ROUTES =================

@app.get("/")
def root():
    return {"status": "Backend running"}

# ---------- PDF ----------
@app.post("/api/extract-pdf")
async def extract_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="File must be a PDF")

    text = extract_text_from_pdf(file)
    return {"text": text}


# ---------- ANALYZE ----------
@app.post("/api/analyze")
async def analyze_resume(request: AnalyzeRequest):
    if not request.resume_text or not request.jd_text:
        raise HTTPException(status_code=400, detail="Missing resume or JD")

    prompt = f"""
You are a strict ATS Resume Analyzer.

Step 1: Check for Multiple Job Descriptions
Look carefully at the Job Description (JD) below. Does it contain MULTIPLE distinct job roles (for example, lists both a 'Software Developer' and a 'Chef' description together)? 
If YES, you MUST STOP analysis and output EXACTLY this:
ATS Score: 0/100
Missing Skills:
- Please give a relevant job description
- Don't use multiple job descriptions
Improvements:
- Submit only one job description for accurate analysis
Summary:
- Multiple job descriptions detected. Please provide a single relevant job description.

Step 2: Check for Template/Placeholder Resume
Look carefully at the resume. Does it contain obvious template placeholders (like "Summarise your responsibilities", "To get started", "Your Name Here", etc.)?
If YES, you MUST STOP analysis and output EXACTLY this:
ATS Score: 0/100
Missing Skills:
- Resume contains template/placeholder text
Improvements:
- Remove template text and placeholders
- Fill out the resume with your actual experience
Summary:
- The uploaded resume appears to be a template and cannot be properly evaluated.

Step 3: Normal Analysis (Only if Step 1 and Step 2 do not trigger)
If the JD has ONE role and the resume is NOT a template, analyze the resume strictly.
Calculate the score mathematically:
- Start at 100.
- Deduct 15 points for every core skill missing.
- Deduct 5 points for every secondary skill missing.
- If the resume is completely unrelated to the JD, give a score below 30.
- Do NOT give scores like 90+ unless it is an absolutely perfect match.

Resume:
{request.resume_text}

JD:
{request.jd_text}

Output format EXACTLY (if Step 1 and Step 2 don't trigger):
ATS Score: XX/100
Missing Skills:
- point 1
- point 2
Improvements:
- point 1
- point 2
Summary:
- 2 short lines
"""

    messages = [
        {"role": "system", "content": "You are a strict ATS system."},
        {"role": "user", "content": prompt},
    ]

    analysis = get_groq_response(messages)

    return {"analysis": analysis}


# ---------- CHAT ----------
@app.post("/api/chat")
async def chat(request: ChatRequest):

    if not request.message:
        return {"reply": "Please ask something."}

    system_prompt = """
You are SageAI, an AI resume assistant.

Rules:
- Answer ONLY the user's question
- Max 2-3 lines
- Do NOT repeat ATS analysis
- Be crisp, relevant, and helpful
"""

    messages = [
        {"role": "system", "content": system_prompt}
    ]

    #  ADD CONTEXT (RESUME + JD)
    if request.resume_text and request.jd_text:
        messages.append({
            "role": "system",
            "content": f"""
Resume (short):
{request.resume_text[:400]}

Job Description (short):
{request.jd_text[:400]}
"""
        })

    # ADD CHAT HISTORY
    for msg in request.chat_history:
        messages.append({
            "role": msg.role,
            "content": msg.content
        })

    #  CURRENT QUESTION
    messages.append({
        "role": "user",
        "content": request.message
    })

    reply = get_groq_response(messages)

    return {"reply": reply}