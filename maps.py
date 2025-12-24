import requests
import os

GOOGLE_API = os.getenv("GOOGLE_MAPS_API_KEY")

def _append_region(query: str, region: str) -> str:
    q = query.strip()
    if region and region.lower() not in q.lower():
        return f"{q}, {region}"
    return q

def search_place(query, region="Tamil Nadu"):
    q = _append_region(query, region)
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    params = {"query": q, "key": GOOGLE_API}
    return requests.get(url, params=params).json()

def nearby_places(lat, lng, place_type, radius=5000):
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        "location": f"{lat},{lng}",
        "radius": radius,
        "type": place_type,
        "key": GOOGLE_API
    }
    return requests.get(url, params=params).json()

def get_directions(origin, destination):
    url = "https://maps.googleapis.com/maps/api/directions/json"
    params = {"origin": origin, "destination": destination, "key": GOOGLE_API}
    return requests.get(url, params=params).json()

def static_map(lat, lng, zoom=15, size="400x400"):
    return f"https://maps.googleapis.com/maps/api/staticmap?center={lat},{lng}&zoom={zoom}&size={size}&key={GOOGLE_API}"