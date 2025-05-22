import requests
import urllib3
import time
import json
import pickle

api_headers = pickle.load( open( "session/aisys_sessionLogin.p", "rb"))
print(api_headers)

