import sqlite3
import json

def search_endpoint(query):
    """Search for API endpoints containing the query string."""
    conn = sqlite3.connect("api_schema.db")
    cursor = conn.cursor()

    cursor.execute("SELECT path, methods, description, request_body, responses FROM api_endpoints WHERE path LIKE ?", (f"%{query}%",))
    results = cursor.fetchall()

    conn.close()
    return results

if __name__ == "__main__":
    query = input("🔍 Enter an API path keyword to search: ")
    endpoints = search_endpoint(query)

    if endpoints:
        for path, methods, description, request_body, responses in endpoints:
            print(f"\n🔹 Endpoint: {path}\nMethods: {methods}\nDescription: {description}")

            # Pretty-print request body
            if request_body and request_body != "None":
                print("\n📥 Request Body Schema:")
                print(json.dumps(json.loads(request_body), indent=2))

            # Pretty-print responses
            print("\n📤 Response Codes:")
            print(json.dumps(json.loads(responses), indent=2))

    else:
        print("❌ No matching endpoints found.")
