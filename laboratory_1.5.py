import wikipedia
import json

search = "Ежик в тумане"
response = wikipedia.search(search)
main_content = wikipedia.page(response[0])

data_to_json = {
    "href": main_content.url,
    "mainTitle": main_content.title,
    "content": main_content.content,
    "images": main_content.images,
    "links": main_content.links,
    "references": main_content.references
}
with open("data.json", "w") as f:
    json.dump(data_to_json, f)
