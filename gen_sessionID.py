import requests
import urllib3
import time
import json
import pickle


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) #ignore cert stuff. this is an internal job so its ok.
host = ""


## New login method ----

api_login = f'https://{host}/rest/v1/login'

api_headers = {
    'Content-Type': 'application/json'
    }

login_payload = json.dumps({
    "username": username,
    "password": userpass,
    "useOIDC": False
})

login_response = requests.request("POST",
                                  api_login,
                                  headers=api_headers,
                                  data=login_payload,
                                  verify=False
                                  )

api_headers['Cookie'] = 'sessionID={0}'.format(
    login_response.cookies.get('sessionID'))

print(api_headers)
print("Logged in..")

pickle.dump( api_headers, open( "session/aisys_sessionLogin.p", "wb"))
print("AI Systems Session Saved, you do not need to auth for another 12 hours!")
