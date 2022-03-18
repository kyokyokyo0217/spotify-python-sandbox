import json
import datetime

from spotify import Spotify


def main():
    d_today = datetime.date.today()
    print(d_today)
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





if __name__ == "__main__":
    main()