import math
from bson import ObjectId
from app.config import settings


LEARNING_RATE = 0.15


def rasch_probability(ability, difficulty):

    return 1.0 / (1.0 + math.exp(-(ability - difficulty)))


def update_ability(current_ability, difficulty, is_correct):

    p = rasch_probability(current_ability, difficulty)

    if is_correct:
        new = current_ability + LEARNING_RATE * (1 - p)
    else:
        new = current_ability - LEARNING_RATE * p

    return max(settings.MIN_ABILITY, min(settings.MAX_ABILITY, new))


async def select_next_question(db, ability, asked_ids):

    low = ability - settings.DIFFICULTY_WINDOW
    high = ability + settings.DIFFICULTY_WINDOW

    pipeline = [
        {
            "$match": {
                "difficulty": {"$gte": low, "$lte": high},
                "_id": {"$nin": [ObjectId(i) for i in asked_ids]}
            }
        },
        {
            "$addFields": {
                "distance": {"$abs": {"$subtract": ["$difficulty", ability]}}
            }
        },
        {"$sort": {"distance": 1}},
        {"$limit": 1}
    ]

    result = await db.questions.aggregate(pipeline).to_list(1)

    if not result:
        result = await db.questions.find_one({"_id": {"$nin": [ObjectId(i) for i in asked_ids]}})

    if not result:
        return None

    q = result[0] if isinstance(result, list) else result

    return {
        "id": str(q["_id"]),
        "text": q["text"],
        "options": q["options"],
        "difficulty": q["difficulty"],
        "topic": q["topic"],
        "tags": q["tags"]
    }