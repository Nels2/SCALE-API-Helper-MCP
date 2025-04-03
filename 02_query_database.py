import sqlite3

def search_endpoint(query):
    """Search for API endpoints containing the query string."""
    conn = sqlite3.connect("api_schema.db")
    cursor = conn.cursor()

    # Search for an endpoint that matches the query
    cursor.execute("SELECT path, methods, description FROM api_endpoints WHERE path LIKE ?", (f"%{query}%",))
    results = cursor.fetchall()

    conn.close()
    
    return results

if __name__ == "__main__":
    query = input("Enter an API path keyword to search: ")  # User input for dynamic search
    endpoints = search_endpoint(query)

    if endpoints:
        for path, methods, description in endpoints:
            print(f"\n🔹 Endpoint: {path}\nMethods: {methods}\nDescription: {description}\n")
    else:
        print(">> No matching endpoints found.")
