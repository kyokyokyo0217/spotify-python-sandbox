import requests
from dotenv import dotenv_values
import base64
import json

class Slack():

    def __init__(self, url=""):
        self.url = url

    def post(self, payload):
        headers = {
            "Content-type": "application/json"
        }

        data = json.dumps(payload)

        res = requests.post(
            self.url,
            headers=headers,
            data=data
        ) 

        if res.status_code == 200:
            return res
        else:
            print(res.status_code, res.reason)
            raise SystemExit()
