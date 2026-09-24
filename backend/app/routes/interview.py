from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os

router = APIRouter(
    prefix="/interview",
    tags=["Mock Interview"]
)


class InterviewRequest(BaseModel):
    role: str
    experience: str = "Fresher"


class InterviewResponse(BaseModel):
    role: str
    experience: str
    message: str


class InterviewAnswerRequest(BaseModel):
    role: str
    experience: str = "Fresher"
    answer: str
    question_number: int = 1


@router.post("/start")
def start_interview(request: InterviewRequest):

    message = (
        f"Hello! Welcome to your {request.role} mock interview. "
        "I will be your AI interviewer today. "
        "Please answer each question naturally, just like you would in a real interview. "
        "Let's begin. Tell me about yourself."
    )

    return {
        "role": request.role,
        "experience": request.experience,
        "message": message,
        "question_number": 1
    }


@router.post("/respond")
def respond_to_answer(request: InterviewAnswerRequest):

    answer = request.answer.strip()

    if not answer:
        raise HTTPException(
            status_code=400,
            detail="Please provide an answer."
        )

    # Temporary AI-style interview logic.
    # We will connect this to an AI model next.

    questions = [
        "Thank you for your introduction. What technical skills do you have that are useful for this role?",
        "Good. Can you tell me about one of your projects and explain what you contributed to it?",
        "That's interesting. What was the biggest challenge you faced while working on that project?",
        "How did you solve that challenge?",
        "Why do you want to work as a software developer?",
        "Where do you see yourself in the next five years?"
    ]

    current = request.question_number

    if current < len(questions):
        next_question = questions[current]
        next_number = current + 1

        message = (
            "Thank you for your answer. "
            + next_question
        )
    else:
        next_number = current + 1

        message = (
            "Thank you for completing the interview. "
            "You did a good job. The mock interview is now finished."
        )

    return {
        "role": request.role,
        "message": message,
        "question_number": next_number,
        "interview_finished": current >= len(questions)
    }