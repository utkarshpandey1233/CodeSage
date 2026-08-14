CodeSage — AI Resume Analyzer

CodeSage is an AI-powered resume analysis platform that helps users evaluate their resume against a specific Job Description (JD).

It extracts resume content from PDF files, analyzes the resume using AI, identifies missing skills, suggests improvements, provides an ATS-style score, and includes an AI assistant for resume-related questions.

Live Demo

Frontend: https://code-sage-chi.vercel.app

Backend: https://codesage-backend-cspt.onrender.com

⸻

Features

Resume PDF Upload

Users can upload their resume in PDF format.

CodeSage:

* Accepts PDF resumes
* Extracts text from uploaded PDFs
* Uses the extracted resume content for analysis
* Uses the resume content as context for AI chat

PDF text extraction is handled using PyPDF2.

Job Description Analysis

Users can provide a Job Description against which their resume is evaluated.

The system analyzes the relationship between the resume and the provided JD to identify relevant skills and potential gaps.

AI-Powered ATS Analysis

CodeSage uses the Groq API to analyze resumes against Job Descriptions.

The analysis provides:

* ATS Score
* Missing Skills
* Improvements
* Summary

The analyzer follows a structured evaluation process.

Multiple Job Description Detection

The system checks whether the provided Job Description contains multiple distinct job roles.

If multiple roles are detected, the analysis stops and asks the user to provide a single relevant Job Description.

Resume Template Detection

The system checks for obvious resume template or placeholder text such as:

* Your Name Here
* Summarise your responsibilities
* To get started

If placeholder content is detected, the resume receives an ATS score of 0/100 and the user is asked to provide an actual resume.

Skill-Based ATS Scoring

The analyzer uses the following scoring rules:

* Starts with a score of 100
* Deducts 15 points for every missing core skill
* Deducts 5 points for every missing secondary skill
* Completely unrelated resumes receive a score below 30
* Very high scores are reserved for extremely strong matches

SageAI

CodeSage includes an AI resume assistant called SageAI.

Users can ask questions related to their resume and Job Description.

The assistant can use:

* Resume context
* Job Description context
* Previous chat history
* Current user question

Responses are designed to be concise and relevant.

Mock Interview

CodeSage also provides a Mock Interview section to help users prepare for interviews using their resume and Job Description.

⸻

Tech Stack

Frontend

* React
* Vite
* JavaScript
* CSS
* React Hooks

Backend

* Python
* FastAPI
* Pydantic
* PyPDF2
* python-dotenv
* Groq Python SDK

AI

* Groq API
* OpenAI GPT OSS 20B

Deployment

* Vercel — Frontend
* Render — Backend

⸻

Architecture

                    ┌──────────────────────┐
                    │        User          │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │    React Frontend    │
                    │                      │
                    │  Resume Upload       │
                    │  Job Description     │
                    │  ATS Analysis        │
                    │  Mock Interview      │
                    │  SageAI Chat         │
                    └──────────┬───────────┘
                               │
                          HTTP / JSON
                               │
                               ▼
                    ┌──────────────────────┐
                    │   FastAPI Backend    │
                    │                      │
                    │  PDF Extraction      │
                    │  Resume Analysis     │
                    │  AI Chat             │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │      Groq API        │
                    │                      │
                    │    GPT OSS 20B       │
                    └──────────────────────┘

⸻

Project Structure

CodeSage/
│
├── backend/
│   └── main.py
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── AnalysisCard.jsx
│   │   │   └── ...
│   │   │
│   │   ├── App.jsx
│   │   ├── App.css
│   │   ├── index.css
│   │   └── main.jsx
│   │
│   └── ...
│
├── .gitignore
├── package.json
└── README.md

⸻

Backend API

Health Check

GET /

Response:

{
  "status": "Backend running"
}

Extract Resume PDF

POST /api/extract-pdf

Accepts a PDF file and extracts its text.

Response:

{
  "text": "Extracted resume text..."
}

Analyze Resume

POST /api/analyze

Request:

{
  "resume_text": "Resume content...",
  "jd_text": "Job description..."
}

Response:

{
  "analysis": "ATS Score: XX/100 ..."
}

AI Chat

POST /api/chat

Request:

{
  "message": "How can I improve my resume?",
  "resume_text": "Resume content...",
  "jd_text": "Job description...",
  "chat_history": []
}

Response:

{
  "reply": "AI generated response..."
}

⸻

Environment Variables

The backend requires a Groq API key.

Create a .env file:

GROQ_API_KEY=your_groq_api_key

Never commit the .env file to GitHub.

The .gitignore file excludes environment files from version control.

⸻

Running the Backend Locally

Clone the repository:

git clone https://github.com/utkarshpandey1233/CodeSage.git

Navigate to the project:

cd CodeSage

Create a Python virtual environment:

python3 -m venv venv

Activate the virtual environment:

source venv/bin/activate

Install backend dependencies:

pip install fastapi uvicorn python-multipart python-dotenv PyPDF2 groq

Create the environment file:

GROQ_API_KEY=your_groq_api_key

Start the backend:

uvicorn backend.main:app --reload

⸻

Running the Frontend Locally

Navigate to the frontend:

cd frontend

Install dependencies:

npm install

Start the development server:

npm run dev

Open the local URL displayed by Vite.

⸻

Application Flow

1. User opens CodeSage
          ↓
2. User uploads resume PDF
          ↓
3. Backend extracts resume text
          ↓
4. User enters Job Description
          ↓
5. User starts resume analysis
          ↓
6. Resume + JD are sent to FastAPI
          ↓
7. FastAPI sends the request to Groq
          ↓
8. GPT OSS 20B generates the analysis
          ↓
9. ATS results are displayed
          ↓
10. User can ask SageAI questions

⸻

AI Model

CodeSage currently uses:

openai/gpt-oss-20b

through the Groq API.

The project was migrated from:

llama-3.1-8b-instant

to GPT OSS 20B following the decommissioning of the previous model.

⸻

Deployment

Frontend

The frontend is deployed using Vercel.

https://code-sage-chi.vercel.app

Backend

The FastAPI backend is deployed using Render.

https://codesage-backend-cspt.onrender.com

The deployment is connected to the main branch of the GitHub repository.

New commits pushed to main can trigger new deployments.

Note: The backend currently uses a Render free instance. After periods of inactivity, the service may spin down, which can cause the first request to take significantly longer.

⸻

Security

The Groq API key must never be exposed in frontend code.

Use environment variables:

GROQ_API_KEY=your_secret_key

Do not commit .env files or API keys to GitHub.

⸻

Future Improvements

* More detailed ATS scoring
* Resume section-by-section analysis
* Keyword matching visualization
* Resume rewriting suggestions
* Resume version history
* User authentication
* Saved resumes
* Job tracking
* Interview performance scoring
* Improved skill extraction
* More detailed mock interviews
* Resume export
* Additional AI model support
* Streaming AI responses
* Improved Job Description validation

⸻

Project Goal

The goal of CodeSage is to help job seekers understand how well their resume matches a particular Job Description and provide actionable feedback for improvement.

The platform combines:

Resume Parsing
      +
Job Description Analysis
      +
ATS Evaluation
      +
AI Recommendations
      +
AI Resume Assistant
      +
Mock Interview Preparation

⸻

Author

Utkarsh Pandey

GitHub: https://github.com/utkarshpandey1233

⸻

License

This project is currently intended as a personal and academic project.
