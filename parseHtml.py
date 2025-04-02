import os
from bs4 import BeautifulSoup

def parse_html_files(input_folder="beatport_html_files", output_folder="output"):
    # Ensure output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Get all HTML files in the input folder
    html_files = [f for f in os.listdir(input_folder) if f.endswith(".html")]

    for html_file in html_files:
        input_file_path = os.path.join(input_folder, html_file)
        output_file_path = os.path.join(output_folder, f"{os.path.splitext(html_file)[0]}_export.txt")

        with open(input_file_path, "r", encoding="utf-8") as file:
            soup = BeautifulSoup(file, "html.parser")

        # Find all track rows
        rows = soup.find_all("div", {"data-testid": "tracks-table-row"})

        # Open output file for writing
        with open(output_file_path, "w", encoding="utf-8") as output:
            for index, row in enumerate(rows, start=1):
                # Extract track title
                title_element = row.select_one("div.container a[title]")
                track_title = title_element["title"].strip() if title_element else "Unknown Title"

                # Extract remix info
                remix_element = row.select_one("div.container span span")
                remix = remix_element.text.strip() if remix_element else "Original Mix"

                # Extract all artists
                artist_elements = row.select("div.ArtistNames-sc-72fc6023-0 a")
                all_artists = [artist.text.strip() for artist in artist_elements if artist.text.strip()] if artist_elements else []

                # Handle missing artist cases
                main_artists = ", ".join(all_artists) if all_artists else "Unknown Artist"

                # Identify remixer (if their name appears in the remix field)
                possible_remixers = [artist for artist in all_artists if artist in remix]

                # Format remix text correctly
                remix_text = remix if possible_remixers else remix

                # Write to file
                output.write(f"{index} | {main_artists} | {track_title} | {remix_text}\n")

        print(f"✅ Exported: {output_file_path}")
