from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

from app.database import connect_db, close_db
from app.routers import questions, sessions


# LIFESPAN HANDLER (runs when server starts and stops)
@asynccontextmanager
async def lifespan(app: FastAPI):

    # connect to MongoDB
    await connect_db()

    yield

    # close MongoDB connection
    await close_db()


# CREATE FASTAPI APP
app = FastAPI(
    title="Adaptive Diagnostic Engine",
    description="Adaptive testing system using IRT and AI learning insights",
    version="1.0.0",
    lifespan=lifespan
)


# ENABLE CORS (for frontend later)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change to frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# INCLUDE ROUTERS
app.include_router(questions.router, prefix="/api/v1", tags=["Questions"])
app.include_router(sessions.router, prefix="/api/v1", tags=["Sessions"])


# HEALTH CHECK ENDPOINT
@app.get("/health")
async def health():
    return {"status": "ok"}