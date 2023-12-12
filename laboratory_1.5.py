import requests
import json
from bs4 import BeautifulSoup

search = "Ёжик в тумане"
urlAPI = "https://ru.wikipedia.org/w/api.php"
domain = "https://ru.wikipedia.org"


def get_json(search_page):
    params = {
        "action": "parse",
        "format": "json",
        "page": search_page,
        "prop": "text|images|links"
    }
    response = requests.get(urlAPI, params=params)
    response_json = response.json()
    if "error" in response:
        print("error: missing title")
    else:
        html = response_json["parse"]["text"]["*"]
        soup = BeautifulSoup(html, "html.parser")
        links = []
        references = soup.find("ol", {"class": "references"}).get_text()
        for link in response_json["parse"]["links"]:
            if link["ns"] == 0:
                links.append(domain + "/wiki/" + link["*"])
        data_to_json = {
            "href": response.request.url,
            "mainTitle": response_json["parse"]["title"],
            "content": response_json["parse"]["text"]["*"],
            "images": response_json["parse"]["images"],
            "links": links,
            "references": references
        }
        with open("data.json", "w", encoding="utf-8") as f:
            json.dump(data_to_json, f, ensure_ascii=False)


get_json(search)
