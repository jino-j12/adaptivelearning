from fastapi import APIRouter, HTTPException
from bson import ObjectId

from app.database import get_db
from app.seed.questions import GRE_QUESTIONS

router = APIRouter()


# SEED QUESTIONS INTO DATABASE
@router.post("/questions/seed")
async def seed_questions():

    db = get_db()

    # remove existing questions
    await db.questions.delete_many({})

    # insert new dataset
    result = await db.questions.insert_many(GRE_QUESTIONS)

    return {
        "message": "Questions seeded successfully",
        "inserted_count": len(result.inserted_ids)
    }


# GET ALL QUESTIONS (without correct answer)
@router.get("/questions")
async def get_questions():

    db = get_db()

    questions = []

    async for q in db.questions.find({}):

        questions.append({
            "id": str(q["_id"]),
            "text": q["text"],
            "options": q["options"],
            "difficulty": q["difficulty"],
            "topic": q["topic"],
            "tags": q.get("tags", [])
        })

    return {"count": len(questions), "questions": questions}


# GET ONE QUESTION (with correct answer for admin/debug)
@router.get("/questions/{question_id}")
async def get_question(question_id: str):

    db = get_db()

    question = await db.questions.find_one({"_id": ObjectId(question_id)})

    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    question["_id"] = str(question["_id"])

    return question