from google import genai
import os
from langdetect import detect, DetectorFactory
import json
import difflib
from dotenv import load_dotenv  # Import load_dotenv

load_dotenv()

DetectorFactory.seed = 0

# Initialize the client once
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Load heritage dataset once
HERITAGE_DATA = []
try:
    base_dir = os.path.dirname(__file__)
    data_path = os.path.join(base_dir, "data", "tamil_nadu_heritage.json")
    with open(data_path, "r", encoding="utf-8") as f:
        HERITAGE_DATA = json.load(f)
except Exception:
    HERITAGE_DATA = []

def _find_heritage_match(query: str):
    """Return the best-matching heritage site dict for a free-text query, or None."""
    if not query or not HERITAGE_DATA:
        return None
    names = [s.get("name", "") for s in HERITAGE_DATA]
    
    # try exact substring match first
    q_lower = query.lower()
    for site in HERITAGE_DATA:
        if site.get("name", "").lower() in q_lower or site.get("city", "").lower() in q_lower:
            return site

    # fallback to fuzzy matching
    match = difflib.get_close_matches(query, names, n=1, cutoff=0.6)
    if match:
        for site in HERITAGE_DATA:
            if site.get("name") == match[0]:
                return site
    return None

def ask_gemini(prompt, context="", user_lang=None):
    """Send a query to Gemini and return a text reply enriched with matched heritage data."""
    
    # detect language if not provided
    lang = user_lang
    if not lang:
        try:
            lang = detect(prompt)
        except Exception:
            lang = "en"

    # try to match a heritage site from the user's query
    matched = _find_heritage_match(prompt + " " + context)
    site_block = ""
    if matched:
        stories = "\n- ".join(matched.get("stories", []))
        site_block = f"""
Matched heritage site:
Name: {matched.get('name')}
Location: {matched.get('city')}, {matched.get('district')}
Coordinates: {matched.get('coords')}
Short description: {matched.get('description')}
Stories:
- {stories}
Audio reference: {matched.get('audio')}
Use this information to provide historical context, visiting tips, and a short narrative for tourists.
"""

    full_prompt = f"""
You are a tourism chatbot for the state of Tamil Nadu, India.
Use Google Maps and Weather API results to give accurate answers across districts and cities in Tamil Nadu.

Context:
{context}

User query:
{prompt}

Detected user language: {lang}
{site_block}
Answer in simple, friendly language, using the same language as the user when possible. Include visiting tips, short narrative, and point to the audio reference if available. If the user's question is not about a specific heritage site, give general guidance across Tamil Nadu.
    """

    # NEW SDK SYNTAX
    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents=full_prompt
    )
    return response.text