import json
import datetime
from dotenv import dotenv_values

from spotify import Spotify
from slack import Slack


def main():
    config = dotenv_values(".env")
    slack_url = config["SLACK_WEBHOOK_URL"]
    d_today = datetime.date.today()
    spotify = Spotify()
    spotify.authorize()

    new_releases = spotify.get_new_releases()

    for item in new_releases:
        if str(d_today) != item["release_date"]:
            # print(f"not released today: {item['release_date']}")
            continue

        # print(json.dumps(item, indent=2))
        
        if item["album_type"] == "album":
            print(item["artists"][0]["name"], ": ", item["name"])

    slack = Slack(slack_url)
    slack.post({"text": "hi"})





if __name__ == "__main__":
    main()