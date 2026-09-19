import feedparser
from bs4 import BeautifulSoup
import pprint

def get_preview_image_url(soup) -> str | None:

    image = soup.find("img")

    if image:
        return image.get("src")

    return None

def get_gallery_url(soup) -> str | None:

    for link in soup.find_all("a"):
        href = link.get("href")

        if href and "/gallery/" in href:
            return href

    return None

def get_body(soup) -> str | None:

    body = soup.find("div", class_="md")

    if body:
        return body.get_text(" ", strip=True)

    return None

RSS_URL = (
    "https://www.reddit.com/r/MechanicalKeyboards/search.rss"
    '?q=flair:"Builds"&restrict_sr=1&sort=new'
)

feed = feedparser.parse(RSS_URL)

print("Feed status:", getattr(feed, "status", None))
print("Entries found:", len(feed.entries))
print("Bozo:", feed.bozo)

posts = []

for entry in feed.entries[:1]:
    html = entry["content"][0]["value"]

    soup = BeautifulSoup(html, "html.parser")

    print(soup)

    raw_post = {
        "source": "r/MechanicalKeyboards",        
        "author": entry["authors"][0]["name"],
        "title": entry["title"],    
        "post_url": entry.get("link"),
        "created_utc": entry.get("published"),

        "preview_image_url": get_preview_image_url(soup),
        "gallery_url": get_gallery_url(soup),
        "body": get_body(soup),
    }

    posts.append(raw_post)

print(posts[0])