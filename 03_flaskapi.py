from flask import Flask, request, jsonify
import sqlite3
import json

app = Flask(__name__)

def search_endpoint(query):
    conn = sqlite3.connect("api_schema.db")
    cursor = conn.cursor()
    cursor.execute("SELECT path, method, description, request_body, responses FROM api_endpoints WHERE path LIKE ?", (f"%{query}%",))
    results = cursor.fetchall()
    conn.close()

    return [{"path": path, "method": method, "description": description,
             "request_body": json.loads(request_body) if request_body != "None" else None,
             "responses": json.loads(responses)} for path, method, description, request_body, responses in results]

@app.route('/query', methods=['GET'])
def query_api():
    query = request.args.get("query", "")
    results = search_endpoint(query)
    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True, port=5086)
