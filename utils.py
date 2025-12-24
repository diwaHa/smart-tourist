def format_places(results):
    if not results["results"]:
        return "No results found."

    output = []
    for place in results["results"][:5]:
        name = place.get("name")
        rating = place.get("rating", "NA")
        address = place.get("formatted_address", "")
        output.append(f"🏞️ {name}\n⭐ {rating}/5\n📍 {address}\n")

    return "\n".join(output)
