import json
import datetime
from dotenv import dotenv_values

from spotify import Spotify
from slack import Slack

def main():
    spotify = Spotify()
    spotify.authorize()

    config = dotenv_values(".env")
    slack_url_album = config["SLACK_WEBHOOK_URL_ALBUM"]
    slack_url_single = config["SLACK_WEBHOOK_URL_SINGLE"]

    new_releases = spotify.get_new_releases()

    albums, singles = separate_releases_into_albums_and_singles(new_releases)

    notify_new_released_album(albums, slack_url_album)
    notify_new_released_single(singles, slack_url_single)

def get_combined_artists_name(artists):
    artists_buff = []
    for i, artist in enumerate(artists):
        artists_buff.append(artist["name"])
    artists = ", ".join(artists_buff)
    return artists

def separate_releases_into_albums_and_singles(items):
    d_today = datetime.date.today()
    albums = []
    singles = []

    for item in items:
        if str(d_today) != item["release_date"]:
            continue

        if item["album_type"] != "album":
            albums.append(item)
            continue
        elif item["album_type"] != "single":
            singles.append(item)
            continue
        else:
            print(f"unknown album_type?: {item['album_type']}")
            continue

    return albums, singles

def notify_new_released_album(items, url):    
    data = {
        "blocks": []
    }

    for item in items:
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

def notify_new_released_single(items, url):
    data = {
        "blocks": []
    }

    for item in items:
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