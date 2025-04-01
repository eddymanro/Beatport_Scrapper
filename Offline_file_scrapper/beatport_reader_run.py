from bs4 import BeautifulSoup

# Open the local HTML file
with open("Offline_file_scrapper/beatport_html_files/DeepHouse_TOP_100.html", "r", encoding="utf-8") as file:
    soup = BeautifulSoup(file, "html.parser")

# Find all rows (adjust selector if needed)
rows = soup.find_all("div", {"data-testid": "tracks-table-row"})

# Iterate over rows and extract track info
for index, row in enumerate(rows, start=1):  # Start numbering from 1
    # Extract track title
    title_element = row.select_one("div.container a[title]")
    track_title = title_element["title"].strip() if title_element else "Unknown Title"

    # Extract remix info (if available)
    remix_element = row.select_one("div.container span span")
    remix = remix_element.text.strip() if remix_element else "Original Mix"

    # Extract artist names
    artist_elements = row.select("div.ArtistNames-sc-72fc6023-0 a")
    all_artists = [artist.text.strip() for artist in artist_elements if artist.text.strip()] if artist_elements else []

    # Handle missing artist cases
    if not all_artists:
        all_artists = ["Unknown Artist"]

    # If there's a remix, assume the last artist is the remixer
    if remix != "Original Mix" and len(all_artists) > 1:
        remixer = all_artists[-1]  # Last artist is usually the remixer
        main_artists = ", ".join(all_artists[:-1])  # Exclude last artist from main list
    else:
        remixer = None
        main_artists = ", ".join(all_artists)

    # Prevent duplicate remixer names
    if remixer and remix.startswith(remixer):
        remix_text = remix  # Already contains remixer info, no need to repeat
    else:
        remix_text = f"{remixer} {remix}" if remixer else remix

    # Print the formatted result
    print(f"{index} | {main_artists} | {track_title} | {remix_text}")
