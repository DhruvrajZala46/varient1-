import os
import json
from huggingface_hub import InferenceClient

# Load API token
HUGGINGFACE_API_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")
client = InferenceClient(model="mistralai/Mistral-7B-Instruct-v0.1", token=HUGGINGFACE_API_TOKEN)

# Function to analyze intent
def analyze_intent(user_query):
    prompt = f"""
    You are an intent classifier. Categorize the following query:
    
    Query: "{user_query}"
    
    Respond in JSON format:
    {{
        "intent": "luxury or budget or unknown",
        "emotion": "status or affordability or neutral",
        "category": "headphones, watches, etc. or general"
    }}
    """
    
    try:
        response = client.text_generation(prompt, max_new_tokens=100, return_full_text=False)
        
        # Extract JSON response from AI output
        start_idx = response.find("{")
        end_idx = response.rfind("}") + 1
        result_json = response[start_idx:end_idx]
        parsed_json = json.loads(result_json)  # Convert string to dictionary

        # Ensure all keys exist
        return {
            "intent": parsed_json.get("intent", "unknown"),
            "emotion": parsed_json.get("emotion", "neutral"),
            "category": parsed_json.get("category", "general")
        }
    
    except json.JSONDecodeError:
        return {"intent": "unknown", "emotion": "neutral", "category": "general"}
    except Exception as e:
        return {"intent": "error", "emotion": "neutral", "category": "general", "error": str(e)}

# Test it
if __name__ == "__main__":
    user_input = input("Enter a query: ")
    result = analyze_intent(user_input)
    print(result)
