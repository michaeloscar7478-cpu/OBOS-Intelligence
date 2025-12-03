from fastapi import APIRouter
from vector_store import search
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

router = APIRouter()
client = OpenAI()

MODEL = "gpt-4o-mini"  # We will upgrade later if needed

@router.post("/ask")
def ask_agent(query: str):
    # Search vector DB
    results = search(query, n_results=3)

    # Prepare retrieved context
    context = ""
    if "documents" in results:
        for doc in results["documents"]:
            context += doc[0] + "\n\n"

    # AI prompt
    prompt = f"""
    You are OBOS Intelligence, an AI system designed to analyze business
    documents using the O-BOS framework.

    Use the following context extracted from uploaded documents:
    {context}

    Now answer this query clearly and intelligently:
    {query}
    """

    # Call OpenAI
    completion = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}]
    )

    answer = completion.choices[0].message["content"]

    return {
        "query": query,
        "answer": answer,
        "context_used": context
    }
