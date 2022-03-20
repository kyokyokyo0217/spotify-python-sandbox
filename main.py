import json
import datetime
from dotenv import dotenv_values

from spotify import Spotify
from slack import Slack

config = dotenv_values(".env")
slack_url_album = config["SLACK_WEBHOOK_URL_ALBUM"]

def main():
    spotify = Spotify()
    spotify.authorize()

    new_releases = spotify.get_new_releases()

    notify_new_released_album(new_releases, slack_url_album)

def get_combined_artists_name(artists):
    artists_buff = []
    for i, artist in enumerate(artists):
        artists_buff.append(artist["name"])
    artists = ", ".join(artists_buff)
    return artists

def notify_new_released_album(items, url):
    d_today = datetime.date.today()
    d_today = "2022-03-18"
    
    data = {
        "blocks": []
    }

    for item in items:
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

        data["blocks"].append(
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
            }
        )

    slack = Slack(url)
    slack.post(data)

if __name__ == "__main__":
    main()