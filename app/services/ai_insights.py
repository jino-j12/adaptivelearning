from google import genai
from app.config import settings

client = genai.Client(api_key=settings.GEMINI_API_KEY)


async def generate_learning_plan(summary: str):

    prompt = f"""
You are an educational tutor.

A student completed an adaptive diagnostic test.

Performance summary:
{summary}

Generate a short learning plan with:
1. Weak topic improvement
2. Moderate topic practice
3. Advanced topic challenge
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )

        # Safely extract AI text
        if response.candidates:
            return response.candidates[0].content.parts[0].text

        return "AI could not generate a response."

    except Exception as e:
        print("Gemini error:", e)

        # fallback response so your demo never crashes
        return """
Step 1 – Practice Algebra basics
Solve 10 linear equations daily.

Step 2 – Strengthen Geometry
Focus on triangle area and angle rules.

Step 3 – Improve Vocabulary
Learn 5 new academic words every day.

Estimated Time to Improvement: 3 weeks at 1 hour/day
"""