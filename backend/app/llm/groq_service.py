from groq import Groq

from app.config import settings


class GroqService:

    def __init__(self):

        if not settings.GROQ_API_KEY:
            raise ValueError(
                "GROQ_API_KEY is not configured."
            )

        self.client = Groq(
            api_key=settings.GROQ_API_KEY
        )

        self.model = settings.GROQ_MODEL

    def generate_answer(
        self,
        question: str,
        context: str
    ):

        system_prompt = """
You are an AI Engineering Copilot.

You help software developers understand their codebases.

Use the retrieved code context to answer the user's question.

Rules:
- Base your answer on the provided code.
- Do not invent files, functions, classes, or behavior.
- If the retrieved context is insufficient, say so.
- Mention relevant file paths and line numbers.
- Give practical technical explanations.
- Keep answers concise but useful.
"""

        user_prompt = f"""
Retrieved code:

{context}

User question:

{question}
"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ],
            temperature=0.2,
        )

        return response.choices[0].message.content