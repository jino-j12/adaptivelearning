from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings

client = None
db = None


async def connect_db():
    """
    Create MongoDB connection when FastAPI starts
    """

    global client, db

    client = AsyncIOMotorClient(settings.MONGODB_URI)

    db = client[settings.DB_NAME]

    # Create indexes for better performance
    await db.questions.create_index([("difficulty", 1), ("topic", 1)])
    await db.questions.create_index("tags")

    await db.user_sessions.create_index("session_id", unique=True)


async def close_db():
    """
    Close MongoDB connection when FastAPI shuts down
    """

    global client

    if client:
        client.close()


def get_db():
    """
    Return database instance
    """

    return db