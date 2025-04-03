import json

# Load the JSON file
with open("scale_api_full_schema.json", "r", encoding="utf-8") as file:
    schema = json.load(file)

# Example: Print all available API paths - this is for quick exploration....
if "paths" in schema:
    for path, methods in schema["paths"].items():
        print(f"Endpoint: {path}")
        for method in methods.keys():
            print(f"  - {method.upper()}")
