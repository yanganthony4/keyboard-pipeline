import requests

search_url = "https://www.reddit.com/r/MechanicalKeyboards/search.json"

params = {
    "q": 'flair:"Builds"',
    "restrict_sr": 1,
    "sort": "new",
    "limit": 10
}

headers = {
    "User-Agent": "keyboard-scraper"
}

response = requests.get(search_url, headers=headers, params = params)

search_data = response.json()

for post in search_data["data"]["children"]:
    post_data = post["data"]
    post_url = "https://www.reddit.com" + post_data["permalink"] 
    post_author = post_data["author"]
    if post_data.get("post_hint") == "image":
        image_url = post_data["url"]
    body = post_data["selftext"]

    print(post_url)
    print(post_author)
    print(image_url) 
    print(body)   
