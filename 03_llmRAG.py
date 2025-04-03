import requests

OLLAMA_API_URL = "http://127.0.0.1:11434/v1/chat/completions"

def query_api_schema(query):
    response = requests.get(f"http://localhost:5086/query?query={query}")
    return response.json()

query = input("!! Ask a question about the API (use the path ONLY for best results, such as /login): ")
api_results = query_api_schema(query)

context = "\n".join(
    [f"- {item['method']} {item['path']}: {item['description']}" for item in api_results]
) if api_results else "No relevant API information found."

# Send request to Ollama
modelx = "mistral:7b"
payload = {
    "model": modelx,
    "messages": [
        {"role": "system", "content": "You are an AI assistant that answers API-related questions."},
        {"role": "user", "content": f"Using the following API schema, answer this question: {query}\n\n{context}"}
    ]
}

response = requests.post(OLLAMA_API_URL, json=payload)
llm_reply = response.json()["choices"][0]["message"]["content"]

print(f"\n{modelx}'s Response:\n", llm_reply)
