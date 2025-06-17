import requests
import os

def ask_llama(prompt):
    api_key = os.getenv("TOGETHER_API_KEY")
    url = "https://api.together.xyz/v1/completions"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "meta-llama/Llama-3.1-8B-Instruct",
        "prompt": prompt,
        "max_tokens": 512,
        "temperature": 0.7,
        "stop": ["\n\n"]
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()["choices"][0]["text"].strip()
    except Exception as e:
        return f"❌ Error: {e}"
