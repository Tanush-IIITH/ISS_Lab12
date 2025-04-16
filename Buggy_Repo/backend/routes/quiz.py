from fastapi import APIRouter, Body, FastAPI
import random

# Initialize FastAPI app
app = FastAPI()

# Router for quiz-related endpoints
router = APIRouter(prefix="/quiz", tags=["quiz"])

# Questions data
questions = [
    {
        "id": 1,
        "text": "What command lists directory contents?",
        "options": ["ls", "cd", "rm", "pwd"],
        "correct": "ls"
    },
    {
        "id": 2,
        "text": "Which command searches for text in files?",
        "options": ["find", "grep", "locate", "cat"],
        "correct": "grep"
    },
    {
        "id": 3,
        "text": "What changes file permissions?",
        "options": ["chmod", "chown", "mv", "cp"],
        "correct": "chmod"
    },
    {
        "id": 4,
        "text": "Which command displays the current directory?",
        "options": ["dir", "pwd", "path", "where"],
        "correct": "pwd"
    },
    {
        "id": 5,
        "text": "What removes a file?",
        "options": ["rm", "del", "erase", "unlink"],
        "correct": "rm"
    }
]

# Game state to track the high score
game_state = {"high_score": 0}

# Pydantic model for request body in the '/answer' endpoint
from pydantic import BaseModel

class AnswerRequest(BaseModel):
    id: int
    answer: str
    score: int

# Endpoint to get a random question
@router.get("/question")
async def get_question():
    # Randomly select a question instead of always returning the same one
    question = random.choice(questions)
    return {
        "id": question["id"],
        "text": question["text"],
        "options": question["options"]
    }

# Endpoint to submit an answer
@router.post("/answer")
async def submit_answer(request: AnswerRequest):
    # Find the question by ID
    question = next((q for q in questions if q["id"] == request.id), None)
    if not question:
        return {"error": "Invalid question ID"}

    # Check if the answer is correct
    is_correct = request.answer == question["correct"]
    if is_correct:
        request.score += 10
        if request.score > game_state["high_score"]:
            game_state["high_score"] = request.score

    # Return the response with score and high score
    return {
        "is_correct": is_correct,
        "correct_answer": question["correct"],
        "score": request.score,
        "high_score": game_state["high_score"]
    }

# Endpoint to get the current high score
@router.get("/highscore")
async def get_highscore():
    return {"high_score": game_state["high_score"]}

# Include the router in the app
app.include_router(router)
