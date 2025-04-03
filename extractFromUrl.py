import os
import requests
from bs4 import BeautifulSoup


def extract_using_request(url):
    # Send a GET request to the URL
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Failed to retrieve page: {response.status_code}")
        return

    soup = BeautifulSoup(response.text, "html.parser")
    rows = soup.find_all("div", {"data-testid": "tracks-table-row"})

    # Extract genre from URL for filename
    genre = url.split("/")[-3] if len(url.split("/")) > 3 else "unknown"
    output_filename = f"output/{genre}_export.txt"

    os.makedirs("output", exist_ok=True)

    with open(output_filename, "w", encoding="utf-8") as file:
        for index, row in enumerate(rows, start=1):
            title_element = row.select_one("div.container a[title]")
            track_title = title_element["title"].strip() if title_element else "Unknown Title"

            remix_element = row.select_one("div.container span span")
            remix = remix_element.text.strip() if remix_element else "Original Mix"

            artist_elements = row.select("div.ArtistNames-sc-72fc6023-0 a")
            all_artists = [artist.text.strip() for artist in artist_elements if
                           artist.text.strip()] if artist_elements else []

            main_artists = ", ".join(all_artists) if all_artists else "Unknown Artist"

            possible_remixers = [artist for artist in all_artists if artist in remix]

            remix_text = remix if possible_remixers else remix

            line = f"{index} | {main_artists} | {track_title} | {remix_text}\n"
            file.write(line)

    print(f"Data written to {output_filename}")
