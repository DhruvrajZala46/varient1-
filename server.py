import os
from fastapi import FastAPI
from recommend_product import recommend_product
from intent_analysis import analyze_intent  # Ensure this module exists

app = FastAPI()

@app.get("/recommend/")
def recommend(query: str):
    query_analysis = analyze_intent(query)
    recommended_products = recommend_product(query)

    response = {
        "intent": query_analysis.get("intent", "unknown"),
        "emotion": query_analysis.get("emotion", "neutral"),
        "category": query_analysis.get("category", "general"),
        "recommended_products": [
            {
                "title": p["title"],
                "description": p["description"],
                "price": p["price"],
                "image": p["image"]  # ✅ Now included in response
            }
            for p in recommended_products
        ],
    }

    return response

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))  # Use Render's assigned port if available
    uvicorn.run(app, host="0.0.0.0", port=port)
