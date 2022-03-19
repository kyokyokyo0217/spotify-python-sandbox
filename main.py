import json
import datetime
from dotenv import dotenv_values

from spotify import Spotify
from slack import Slack


def main():
    config = dotenv_values(".env")
    slack_url = config["SLACK_WEBHOOK_URL"]
    d_today = datetime.date.today()
    # d_today = "2022-03-18"
    spotify = Spotify()
    spotify.authorize()

    new_releases = spotify.get_new_releases()

    for item in new_releases:
        if str(d_today) != item["release_date"]:
            # print(f"not released today: {item['release_date']}")
            continue
        
        if item["album_type"] != "album": 
            continue

        artists = get_combined_artists_name(item["artists"])
        album_title = item["name"]
        spotify_link = item["external_urls"]["spotify"]
        # 用意されているサムネは常に[640x640, 300x300, 64x64]の３種類という前提
        thumbnail_url = item["images"][1]["url"]

        print(artists, album_title, spotify_link, thumbnail_url)

        data = {
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"*{album_title}* \n{artists}\n<{spotify_link}|Listen On Spotify>"
                    },
                    "accessory": {
                        "type": "image",
                        "image_url": thumbnail_url,
                        "alt_text": "alt text for image"
                    }
                },
            ]
        }

        slack = Slack(slack_url)
        slack.post(data)

def get_combined_artists_name(artists):
    artists_buff = []
    for i, artist in enumerate(artists):
        artists_buff.append(artist["name"])
    artists = ", ".join(artists_buff)
    return artists

if __name__ == "__main__":
    main()