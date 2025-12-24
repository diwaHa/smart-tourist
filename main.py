from fastapi import FastAPI, UploadFile
from maps import search_place, get_directions, nearby_places, static_map
from weather import get_weather
from llm import ask_gemini
from utils import format_places
from PIL import Image
import io
import os
from google import genai  # UPDATED IMPORT

app = FastAPI(title="Tourism Chatbot API")

# ---------- Chatbot Endpoint ----------
@app.get("/chat")
def chat(q: str, region: str = "Tamil Nadu", lang: str = ""):
    context = f"Region: {region}"
    response = ask_gemini(q, context=context, user_lang=lang)
    return {"reply": response}

# ---------- Place Search ----------
@app.get("/search")
def search(q: str, region: str = "Tamil Nadu"):
    result = search_place(q, region=region)
    return {
        "places": format_places(result),
        "raw": result
    }

# ---------- Directions ----------
@app.get("/directions")
def directions(origin: str, destination: str):
    result = get_directions(origin, destination)
    # Add error handling in case routes are missing
    if not result.get("routes"):
        return {"error": "No routes found"}
        
    route = result["routes"][0]["legs"][0]
    return {
        "distance": route["distance"]["text"],
        "duration": route["duration"]["text"],
        "raw": result
    }

# ---------- Weather ----------
@app.get("/weather")
def weather(location: str = "Tamil Nadu"):
    return get_weather(location)

# ---------- Nearby Restaurants/Hotels ----------
@app.get("/nearby")
def nearby(lat: float, lng: float, type: str):
    return nearby_places(lat, lng, type)

# ---------- Image-based place recognition ----------
@app.post("/identify_place")
async def identify_place(file: UploadFile):
    img_bytes = await file.read()
    img = Image.open(io.BytesIO(img_bytes))

    # UPDATED LOGIC FOR NEW SDK
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    
    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents=["Identify the place in Tamil Nadu:", img]
    )

    return {"identified_place": response.text}
    
# ---------- Static Map ----------
@app.get("/static_map")
def get_map(lat: float, lng: float):
    return {"url": static_map(lat, lng)}