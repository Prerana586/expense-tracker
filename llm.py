from groq import Groq
import json, re, os
from datetime import date
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

# Works both locally and on Streamlit Cloud
api_key = os.getenv("GROQ_API_KEY") or st.secrets.get("GROQ_API_KEY", "")
client = Groq(api_key=api_key)

PARSE_PROMPT = """You are an expense parser. Extract expense data from natural language.
Return ONLY valid JSON — no markdown, no explanation — matching this schema:
{{
  "amount": float,
  "currency": "USD",
  "category": one of ["food","transport","housing","health","entertainment","shopping","utilities","other"],
  "description": str,
  "date": "YYYY-MM-DD"
}}
If the date is missing, use today. If anything is ambiguous, make a reasonable guess.
Today is {today}. Parse: {text}"""

def parse_expense(text: str) -> dict:
    today = date.today().isoformat()
    prompt = PARSE_PROMPT.format(today=today, text=text)
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300,
    )
    raw = response.choices[0].message.content.strip()
    raw = re.sub(r"```json|```", "", raw).strip()
    return json.loads(raw)

INSIGHTS_PROMPT = """You are a personal finance advisor. Given this JSON summary of a user's expenses:
{summary}
Write 3-5 concise bullet-point insights (plain text, no markdown headers).
Be specific with numbers. Suggest one actionable saving tip."""

def generate_insights(summary: dict) -> str:
    prompt = INSIGHTS_PROMPT.format(summary=json.dumps(summary, indent=2))
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500,
    )
    return response.choices[0].message.content.strip()