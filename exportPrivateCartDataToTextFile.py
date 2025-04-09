import requests
import os


def get_cart_private_data(url, auth_token, cart_name):
    # Headers (excluding sensitive info)
    headers = {"accept": "application/json, text/plain, */*",
               "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
               "authorization": f"Bearer {auth_token}"}

    # Update the headers with the provided authorization token

    # Make the request
    response = requests.get(url, headers=headers)

    # Check response
    if response.status_code == 200:
        cart_data = response.json()  # Parse JSON response

        # Get the items list
        items = cart_data.get("results", [])

        # Create the output folder if it doesn't exist
        os.makedirs("output", exist_ok=True)

        # Create filepath
        file_to_write_to_path = "output/" + cart_name + ".txt"

        # Open the file to write data
        with open(file_to_write_to_path, "w") as file:
            # Loop through each item and write the required details into the file
            for index, item in enumerate(items, start=1):
                # Get the artist names and join them with a comma
                artists = ', '.join(artist['name'] for artist in item['item']['artists'])
                title = item['item']['name']  # Get the track title
                mix_name = item['item']['mix_name']  # Get the mix name
                track_length = item['item']['length']  # Get the track length
                file.write(f"{index} | {artists} | {title} | {mix_name} | {track_length}\n")
        print(f"Data exported to {file_to_write_to_path}")  # Confirm success
    else:
        print(f"Error: {response.status_code}, {response.text}")