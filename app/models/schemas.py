from pydantic import BaseModel, Field
from datetime import datetime
from typing import Dict, List, Optional
from pydantic import BaseModel

class SessionCreate(BaseModel):
    student_name: str

class QuestionBase(BaseModel):

    text: str
    options: Dict[str, str]
    correct_answer: str
    difficulty: float = Field(ge=0.1, le=1.0)
    topic: str
    tags: List[str]
    explanation: str


class QuestionOut(BaseModel):

    id: str
    text: str
    options: Dict[str, str]
    difficulty: float
    topic: str
    tags: List[str]


class AnswerRecord(BaseModel):

    question_id: str
    topic: str
    difficulty: float
    is_correct: bool
    answered_at: datetime = datetime.utcnow()


class UserSession(BaseModel):

    session_id: str
    student_name: str
    ability: float = 0.5
    questions_asked: List[str] = []
    answers: List[AnswerRecord] = []
    is_complete: bool = False
    learning_plan: Optional[str] = None
    started_at: datetime = datetime.utcnow()
    completed_at: Optional[datetime] = None


class SessionCreate(BaseModel):
    student_name: str


class SubmitAnswerRequest(BaseModel):

    session_id: str
    question_id: str
    selected_option: str