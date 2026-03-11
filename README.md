# Adaptive Diagnostic Engine

An AI-powered adaptive testing system that dynamically adjusts question difficulty based on student performance and generates personalized learning recommendations.

This project combines **FastAPI, MongoDB, and AI models** to create a smart assessment platform similar to adaptive exams like GRE.

---

## Features

- Adaptive question selection based on ability level
- Dynamic difficulty adjustment
- Session-based test tracking
- Topic-wise performance analysis
- AI-generated learning plan using Google Gemini
- Simple frontend interface for taking the test
- REST API built with FastAPI
- MongoDB database for storing sessions and questions

---

## Tech Stack

### Backend
- Python
- FastAPI
- MongoDB
- Motor (Async MongoDB Driver)

### AI Integration
- Google Gemini API

### Frontend
- HTML
- JavaScript

### Tools
- Uvicorn
- Pydantic
- VS Code

---

## Project Structure


adaptive-diagnostic-engine
│
├── app
│ ├── routers
│ │ ├── questions.py
│ │ └── sessions.py
│ │
│ ├── services
│ │ ├── adaptive.py
│ │ └── ai_insights.py
│ │
│ ├── models
│ │ └── schemas.py
│ │
│ ├── seed
│ │ └── questions.py
│ │
│ ├── database.py
│ ├── config.py
│ └── main.py
│
├── frontend
│ └── index.html
│
├── run.py
├── requirements.txt
├── .gitignore
└── README.md


---

## How It Works

1. A student starts a test session.
2. The system selects a question based on the student's ability level.
3. The student submits an answer.
4. The system updates the ability score using an adaptive algorithm.
5. A new question is selected with adjusted difficulty.
6. After completing the test, the system generates a personalized learning plan using AI.

git clone https://github.com/yourusername/adaptive-diagnostic-engine.git

cd adaptive-diagnostic-engine


---

### 2. Create Virtual Environment


python -m venv venv


Activate environment:

**Windows**


venv\Scripts\activate


**Mac/Linux**


source venv/bin/activate


---

### 3. Install Dependencies


pip install -r requirements.txt


---

### 4. Configure Environment Variables

Create a `.env` file in the root directory.


MONGODB_URI=mongodb://localhost:27017
DB_NAME=adaptive_engine
GEMINI_API_KEY=your_api_key_here
INITIAL_ABILITY=0.5
MAX_QUESTIONS=10


---

### 5. Run the Application


python run.py


Server will start at:


http://localhost:8000


---

## API Documentation

FastAPI automatically generates interactive API documentation.

Open:


http://localhost:8000/docs


---

## Seed Questions

To insert the question dataset into MongoDB:


POST /api/v1/questions/seed


Use the FastAPI docs interface to run the endpoint.

---

## Frontend

To take the test, open the frontend page:


frontend/index.html


in your browser.

---

## Example Flow


Start Test
↓
Answer Questions
↓
Adaptive Difficulty Adjustment
↓
Ability Score Updated
↓
AI Learning Plan Generated


---

## Future Improvements

- Interactive dashboard with ability progression graphs
- Topic-wise analytics
- User authentication system
- Test history tracking
- Advanced IRT-based adaptive algorithms
- Modern frontend using React

---

## Author

**Jino J**

B.Tech Artificial Intelligence and Data Science
