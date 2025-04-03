# SCALE API Helper (LLM)

This project was created to teach myself the SCALE API.
I hope this serves useful to someone else in the near future.

I've included scripts 01-02, the full API schema as `scale_api_full_schema.json`, and api_schema.db to show how I set this up and how it works.

# How To use this project (as-is)
1. Git Clone this project.
2. Install the requirements via `latest_requirements.txt`
3. Make sure you have ollama installed & running, then make sure you have `mistral:7b` downloaded as well. 

  Other models probably will work fine for this, but I have found this model to be the most consistent.

3. open two separate terminal windows, or a split terminal.
4. in one window run: `python 03_flaskapi.py`
5. in the other window run: `python 03_llmRAG.py`
6. Have fun!
