import requests
from dotenv import dotenv_values
import base64
import json

class Spotify():
    spotify_access_token_url = "https://accounts.spotify.com/api/token"
    ACCESS_TOKEN = ""

    def authorize(self, client_id, client_secret):
        tmp = client_id + ":" + client_secret
        # TODO 冗長かも？binaryの勉強
        b_tmp = tmp.encode()
        b64encoded = base64.b64encode(b_tmp).decode()

        headers = {
            "Authorization": "Basic " + b64encoded,
            "Content-type": "application/x-www-form-urlencoded"
        }

        data = {
            "grant_type": "client_credentials"
        }

        try:
            res = requests.post(
                self.spotify_access_token_url,
                headers=headers,
                data=data
            ).json()
        except requests.exceptions.HTTPError as err:
            print(err)
            raise SystemExit(err)

        self.ACCESS_TOKEN = res["access_token"]

    def fetch(self, url: str):
        headers = {
            "Authorization": "Bearer " + self.ACCESS_TOKEN,
            "Content-Type": "application/json"
        }

        result = requests.get(
            url=url,
            headers=headers
        )

        return result

    def get_new_releases(self):
        url = f"https://api.spotify.com/v1/browse/new-releases?offset=0&limit=50"

        try:
            result_first_half = self.fetch(url)
        except requests.exceptions.HTTPError as err:
            print(err)
            return None

        url_next = result_first_half.json()["albums"]["next"]

        try:
            result_second_half = self.fetch(url_next)
        except requests.exceptions.HTTPError as err:
            print(err)
            return None

        combined = result_first_half.json()["albums"]["items"] + result_second_half.json()["albums"]["items"]

        return combined