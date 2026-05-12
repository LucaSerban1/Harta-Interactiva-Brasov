from fastapi import APIRouter
import logging

router = APIRouter(prefix="/api/ai", tags=["AI Recommendations"])

try:
    from groq import Groq

    # PUNE CHEIA TA AICI:
    client = Groq(api_key="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")
except ImportError:
    client = None


@router.get("/recommend")
def ai_recommend(prompt_user: str):
    if client is None:
        return {"error": "Libraria groq nu este instalata! Ruleaza 'pip install groq' in terminal."}

    try:
        # Folosim date simple pentru test
        date_test = [{"nume": "Hub Cafe", "specific": "Liniste"}]

        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": f"Esti un ghid din Brasov. Date: {date_test}"},
                {"role": "user", "content": prompt_user}
            ]
        )
        return {"recomandare": completion.choices[0].message.content}
    except Exception as e:
        return {"eroare_detaliata": str(e)}