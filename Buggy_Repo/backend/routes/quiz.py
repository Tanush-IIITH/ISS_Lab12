from fastapi import APIRouter, Body, FastAPI
import random
import asyncio  # Added for thread-safe game state

# Initialize FastAPI app
app = FastAPI()

# Router for quiz-related endpoints
router = APIRouter(prefix="/quiz", tags=["quiz"])


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


game_state = {"high_score": 0}

# Add a lock for thread-safe access to game_state
game_state_lock = asyncio.Lock()

# Pydantic model for request body in the '/answer' endpoint
from pydantic import BaseModel

class AnswerRequest(BaseModel):
    id: int
    answer: str
    score: int


@router.get("/question")
async def get_question():
    if not questions:  
        return {"error": "No questions available"}
    question = random.choice(questions)
    return {
        "id": question["id"],
        "text": question["text"],
        "options": question["options"]
    }


@router.post("/answer")
async def submit_answer(request: AnswerRequest):
    async with game_state_lock:  
       
        question = next((q for q in questions if q["id"] == request.id), None)
        if not question:
            return {"error": "Invalid question ID"}

        is_correct = request.answer == question["correct"]
        score = request.score 
        if is_correct:
            score += 10
            if score > game_state["high_score"]:
                game_state["high_score"] = score

   
        return {
            "is_correct": is_correct,
            "correct_answer": question["correct"],
            "score": score,
            "high_score": game_state["high_score"]
        }


@router.get("/highscore")
async def get_highscore():
    return {"high_score": game_state["high_score"]}


app.include_router(router)