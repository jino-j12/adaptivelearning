from fastapi import APIRouter, HTTPException
from uuid import uuid4
from bson import ObjectId

from app.database import get_db
from app.config import settings
from app.services.adaptive import update_ability, select_next_question
from app.services.ai_insights import generate_learning_plan
from app.models.schemas import SessionCreate
from app.models.schemas import SubmitAnswerRequest

router = APIRouter()


# START TEST



@router.post("/sessions")
async def start_session(data: SessionCreate):

    student_name = data.student_name

    db = get_db()

    session_id = str(uuid4())

    session = {
        "session_id": session_id,
        "student_name": student_name,
        "ability": settings.INITIAL_ABILITY,
        "questions_asked": [],
        "answers": [],
        "is_complete": False,
        "learning_plan": None
    }

    await db.user_sessions.insert_one(session)

    first_question = await select_next_question(db, settings.INITIAL_ABILITY, [])

    if not first_question:
        raise HTTPException(status_code=500, detail="No questions available")

    await db.user_sessions.update_one(
        {"session_id": session_id},
        {"$push": {"questions_asked": first_question["id"]}}
    )

    return {
        "session_id": session_id,
        "first_question": first_question
    }


# SUBMIT ANSWER



@router.post("/sessions/submit")
async def submit_answer(data: SubmitAnswerRequest):

    session_id = data.session_id
    question_id = data.question_id
    selected_option = data.selected_option

    db = get_db()

    session = await db.user_sessions.find_one({"session_id": session_id})

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    if session["is_complete"]:
        raise HTTPException(status_code=400, detail="Test already finished")

    question = await db.questions.find_one({"_id": ObjectId(question_id)})

    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    is_correct = selected_option.upper() == question["correct_answer"].upper()

    new_ability = update_ability(
        session["ability"],
        question["difficulty"],
        is_correct
    )

    answer_record = {
        "question_id": question_id,
        "topic": question["topic"],
        "difficulty": question["difficulty"],
        "is_correct": is_correct
    }

    answers_count = len(session["answers"]) + 1

    is_complete = answers_count >= settings.MAX_QUESTIONS

    update_data = {
        "$push": {"answers": answer_record},
        "$set": {
            "ability": new_ability,
            "is_complete": is_complete
        }
    }

    await db.user_sessions.update_one(
        {"session_id": session_id},
        update_data
    )

    # IF TEST FINISHED → GENERATE AI LEARNING PLAN
    if is_complete:

        answers = session["answers"] + [answer_record]

        topic_stats = {}

        for a in answers:
            topic = a["topic"]

            if topic not in topic_stats:
                topic_stats[topic] = {"correct": 0, "total": 0}

            topic_stats[topic]["total"] += 1

            if a["is_correct"]:
                topic_stats[topic]["correct"] += 1

        summary = f"""
Student performance summary:
Ability score: {new_ability}

Topic stats:
{topic_stats}
"""

        learning_plan = await generate_learning_plan(summary)

        await db.user_sessions.update_one(
            {"session_id": session_id},
            {"$set": {"learning_plan": learning_plan}}
        )

        return {
            "is_correct": is_correct,
            "updated_ability": new_ability,
            "is_complete": True,
            "learning_plan": learning_plan
        }

    next_question = await select_next_question(
        db,
        new_ability,
        session["questions_asked"]
    )

    if next_question:
        await db.user_sessions.update_one(
            {"session_id": session_id},
            {"$push": {"questions_asked": next_question["id"]}}
        )

    return {
        "is_correct": is_correct,
        "updated_ability": new_ability,
        "next_question": next_question,
        "is_complete": False
    }


# FINAL REPORT
@router.get("/sessions/{session_id}/report")
async def session_report(session_id: str):

    db = get_db()

    session = await db.user_sessions.find_one({"session_id": session_id})

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    answers = session.get("answers", [])

    total = len(answers)

    correct = sum(1 for a in answers if a["is_correct"])

    accuracy = (correct / total) * 100 if total > 0 else 0

    topic_stats = {}

    for a in answers:
        topic = a["topic"]

        if topic not in topic_stats:
            topic_stats[topic] = {"correct": 0, "total": 0}

        topic_stats[topic]["total"] += 1

        if a["is_correct"]:
            topic_stats[topic]["correct"] += 1

    return {
        "session_id": session_id,
        "student_name": session["student_name"],
        "final_ability": session["ability"],
        "total_questions": total,
        "correct_answers": correct,
        "accuracy_percent": round(accuracy, 2),
        "topic_breakdown": topic_stats,
        "learning_plan": session.get("learning_plan")
    }


# GET SESSION
@router.get("/sessions/{session_id}")
async def get_session(session_id: str):

    db = get_db()

    session = await db.user_sessions.find_one({"session_id": session_id})

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    session["_id"] = str(session["_id"])

    return session