# SCALE API Helper (LLM)

This project was created to teach myself the SCALE API.
I hope this serves useful to someone else in the near future.

I've included scripts 01-02, the full API schema as `scale_api_full_schema.json`, and api_schema.db to show how I set this up and how it works.

## How To use this project (as-is)
1. Git Clone this project.
2. Install the requirements via `latest_requirements.txt`
3. Make sure you have ollama installed & running, then make sure you have `mistral:7b` downloaded as well. 

  Other models probably will work fine for this, but I have found this model to be the most consistent.

3. open two separate terminal windows, or a split terminal, even `screen` works for this.
4. in one window run: `python 03_flaskapi.py`
5. in the other window run: `python 03_llmRAG.py`
6. Have fun!


## Example output
Question Example 0, Straight Path: 
``` 
python 03_llmRAG.py
Ask a question about the API: /Node
```
Answer:
```
mistral:7b's Response:
  Based on the API schema provided, to get a list of all nodes in the system using this API, you would use the GET request: `/Node`. There is no specific endpoint (such as `/Nodes` or plural form) for listing multiple nodes, and since it's not explicitly mentioned, `/Node` appears to be the correct endpoint following RESTful API principles.

To retrieve information about a single node using its unique UUID, you would use the GET request: `/Node/{uuid}`. Replace `{uuid}` with the specific ID or unique identifier of the desired node in the URL. Note that this does not return a list of nodes but only details for one specific node. If you need to retrieve multiple nodes based on their UUIDs, consider creating a new endpoint (such as `/Nodes`) that accepts multiple requests for different UUIDs, if the current schema does not offer this functionality.
```

Question Example 1, Straight Path 2:
```
Ask a question about the API: /User
```
Answer:
```
mistral:7b's Response:
  Based on the provided API schema, the `/User` endpoint has two main operations: `POST /User:` for creating a user and `GET /User/{uuid}:` for getting a specific user. So when you make a GET request to `/User/{uuid}`, it will return a list of users if the input `{uuid}` is actually an array of user IDs, or it will return a single user if the `{uuid}` is a specific user's unique identifier. If no user with that identified `{uuid}` exists, the API probably would return an error message.
```
