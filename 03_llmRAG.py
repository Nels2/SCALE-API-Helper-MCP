import requests

API_URL = "http://172.18.33.152:8001/v1/chat/completions"

def query_api_schema(query):
    response = requests.get(f"http://localhost:5086/query?query={query}")
    return response.json()

query = input("💡 Ask a question about the API: ")
api_results = query_api_schema(query)

context = "\n".join(
    [f"- {item['methods']} {item['path']}: {item['description']}" for item in api_results]
) if api_results else "No relevant API information found."

# Send request to Ollama
modelx = "openai/gpt-oss-20b"
payload = {
    "model": modelx,
    "messages": [
        {"role": "system", "content": "You are an AI assistant that answers API-related questions."},
        {"role": "user", "content": f"Using the following API schema, answer this question: {query}\n\n{context}"}
    ]
}

response = requests.post(API_URL, json=payload)
llm_reply = response.json()["choices"][0]["message"]["content"]

print(f"\n{modelx}'s Response:\n", llm_reply)
