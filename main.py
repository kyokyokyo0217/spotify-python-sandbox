import json
import datetime
from dotenv import dotenv_values

from spotify import Spotify
from slack import Slack

def main():
    config = dotenv_values(".env")
    slack_url_album_global = config["SLACK_WEBHOOK_URL_ALBUM_GLOBAL"]
    slack_url_single_global = config["SLACK_WEBHOOK_URL_SINGLE_GLOBAL"]
    slack_url_album_japan = config["SLACK_WEBHOOK_URL_ALBUM_JAPAN"]
    slack_url_single_japan = config["SLACK_WEBHOOK_URL_SINGLE_JAPAN"]

    client_id = config["SPOTIFY_CLIENT_ID"]
    client_secret = config["SPOTIFY_CLIENT_SECRET"]

    spotify = Spotify()
    spotify.authorize(client_id, client_secret)

    new_releases_japan = spotify.get_new_releases_by_country("JP")
    albums_japan, singles_japan = separate_releases_into_albums_and_singles(new_releases_japan)
    print(f"released today in Japan: albums: {len(albums_japan)}, singles: {len(singles_japan)}")
    notify_new_releases_album(albums_japan, slack_url_album_japan) 
    notify_new_releases_single(singles_japan, slack_url_single_japan)

    new_releases = spotify.get_new_releases_global()
    albums_global, singles_global = separate_releases_into_albums_and_singles(new_releases)
    print(f"released today in global: albums: {len(albums_global)}, singles: {len(singles_global)}")
    notify_new_releases_album(albums_global, slack_url_album_global)
    notify_new_releases_single(singles_global, slack_url_single_global)

def get_combined_artists_name(artists):
    artists_buff = []
    for i, artist in enumerate(artists):
        artists_buff.append(artist["name"])
    artists = ", ".join(artists_buff)
    return artists

def separate_releases_into_albums_and_singles(items):
    d_today = datetime.date.today()
    # d_today = "2022-03-18"
    print(d_today)
    albums = []
    singles = []

    for item in items:
        # print(item["release_date"])
        if str(d_today) != item["release_date"]:
            continue

        if item["album_type"] == "album":
            albums.append(item)
            continue
        elif item["album_type"] == "single":
            singles.append(item)
            continue
        else:
            print(f"unknown album_type?: {item['album_type']}")
            continue

    return albums, singles

def notify_new_releases_album(items, url):    
    data = {
        "blocks": []
    }

    if len(items) == 0:
        data["blocks"].append(
            {
                "type": "section",
                "text": {
                    "type": "plain_text",
                    "text": "Seems like no releases for today...🥺"
                }
            }
        )
    else:
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

def notify_new_releases_single(items, url):
    data = {
        "blocks": []
    }

    if len(items) == 0:
        data["blocks"].append(
            {
                "type": "section",
                "text": {
                    "type": "plain_text",
                    "text": "Seems like no releases for today...🥺"
                }
            }
        )
    else:
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