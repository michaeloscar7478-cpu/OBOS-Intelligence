from fastapi import APIRouter
from reasoning import search
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI()
router = APIRouter()

MODEL = "gpt-4o-mini"

O_BOS_PROMPT = """
You are OBOS Intelligence — an AI system trained on the OBOS Framework:
O — Operations
B — Branding & Market Positioning
O — Offer Design & Value Creation
S — Systems & Structure

Your job is to analyze the user's business documents, understand their strengths and weaknesses, and return an OBOS Diagnostic Report.

Your report MUST follow this format:

1. OPERATIONS SCORE (0-10)
2. BRANDING SCORE (0-10)
3. OFFER SCORE (0-10)
4. SYSTEMS SCORE (0-10)

Then:

5. KEY OBSERVATIONS
6. PRIORITY PROBLEMS
7. ACTION PLAN (3 steps only)
8. OBOS SUMMARY — brief and powerful.

Base your answers on the retrieved documents + the user's query.
"""

@router.post("/diagnose")
def diagnose_business(query: str):
    results = search(query, n_results=5)

    context = ""
    if "documents" in results:
        for doc in results["documents"]:
            context += doc[0] + "\n\n"

    prompt = f"""
    {O_BOS_PROMPT}

    CONTEXT FROM BUSINESS DOCUMENTS:
    {context}

    USER QUESTION:
    {query}

    Generate the diagnostic now:
    """

    completion = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}]
    )

    answer = completion.choices[0].message["content"]

    return {
        "query": query,
        "diagnostic": answer
    }
