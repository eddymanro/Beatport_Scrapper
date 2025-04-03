from parseHtml import parse_html_files
from extractFromUrl import extract_using_request
from extractPrivateCartData import get_cart_private_data

def __main__():
    # uses downloaded html files
    # parse_html_files()

    # give publicly accessible url as param
    # extract_using_request("https://www.beatport.com/genre/organic-house/93/top-100")

    # Private authorization token, edit manually
    token = "REPLACE WITH YOUR OWN"
    # param1 is API url
    get_cart_private_data("https://api.beatport.com/v4/my/carts/284486641/items/tracks/?page=1&per_page=150", token)
__main__()