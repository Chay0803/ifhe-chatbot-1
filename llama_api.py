import requests
import os

# ✅ You can either set this via environment variable or paste your key directly
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY") or "2da7a11f4b32a4e6fbb54ac8c1f07c81ccc588792a3fbb0e166b9dbb54e2178f"

def ask_llama(prompt):
    url = "https://api.together.xyz/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {TOGETHER_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "mistralai/Mistral-7B-Instruct-v0.1",  # ✅ works on Together API
        "messages": [
            {"role": "system", "content": "You are a helpful assistant for answering college admission queries."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "top_p": 0.9,
        "max_tokens": 512
    }

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()

    return response.json()["choices"][0]["message"]["content"]
