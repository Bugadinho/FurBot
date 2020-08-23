import json
import requests

headers = {"User-Agent":"Project-Luna/1.0 (API Usage by jezzar on E621)"}
Req = requests.get(f"https://e621.net/posts.json?tags=order:random+rating:explicit&limit=1", headers=headers)
ReqJson = Req.json()
Post = ReqJson["posts"][0]["file"]["url"]
print(f"Here is your {type} yiff: {Post}\nURL: <https://e621.net/posts/{ReqJson['posts'][0]['id']}>")

