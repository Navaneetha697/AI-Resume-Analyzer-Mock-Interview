from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.resume import router as resume_router
from app.routes.interview import router as interview_router

app = FastAPI(
    title="AI Resume Analyzer & Mock Interview",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(resume_router)
app.include_router(interview_router)


@app.get("/")
def home():
    return {
        "message": "Welcome to AI Resume Analyzer & Mock Interview API"
    }