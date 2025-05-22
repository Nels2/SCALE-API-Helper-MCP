import requests
import urllib3
import time
import json
import pickle

api_headers = pickle.load( open( "session/aisys_sessionLogin.p", "rb"))
print(api_headers)
print("AI Systems is Logged in still!..")
host="172.18.33.216"
logout_url = f"https://{host}/rest/v1/logout"
logout_response = requests.request("POST",
                                   logout_url,
                                   headers=api_headers,
                                   verify=False
)
print("Closing Session!")
print(logout_response)
print(">> Development Session is closed.")

