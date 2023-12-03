import requests
from bs4 import BeautifulSoup
from rutermextract import TermExtractor
import graphviz

base_url_wiki = "https://ru.wikipedia.org"
find_category = "Металлургические компании России"


def get_url_with_category(category):
    return f'{base_url_wiki}/wiki/Категория:{category}'


def get_relative_links_on_wiki_page(page_url):
    response = requests.get(page_url)
    if response.status_code != 200 or response.status_code != 304:
        soup = BeautifulSoup(response.content, "html.parser")
        links_div = soup.find("div", {"class": "mw-category mw-category-columns"})
        if not links_div:
            return []
        links_a = soup.find_all("a")
        links_href = []
        for curr_a in links_a:
            if curr_a.get("href") and curr_a.get("href").startswith("/wiki"):
                links_href.append(f'{base_url_wiki}{curr_a.get("href")}')
        return links_href
    else:
        return []


def get_content_text_wiki_page(url):
    response = requests.get(url)
    if response.status_code != 200 or response.status_code != 304:
        soup = BeautifulSoup(response.content, "html.parser")
        text_content_div = soup.find("div", {"id": "mw-content-text"})
        title_div = soup.find("span", {"class": "mw-page-title-main"})
        title = ""
        if title_div:
            title = title_div.text
        if text_content_div:
            return {"title": title, "content": text_content_div.get_text()}
        else:
            return {}
    else:
        return {}


hrefs_page = get_relative_links_on_wiki_page(get_url_with_category(find_category))
extractor = TermExtractor()
list_nodes = {}
for href in hrefs_page[:30]:
    html = get_content_text_wiki_page(href)
    term_nodes = []
    for term in extractor(html["content"])[:15]:
        if term.normalized not in ["дата обращения", "код", "статья", "категория", "источники",
                                   "компания"] and term.count > 4:
            term_nodes.append(term.normalized)
    list_nodes[href] = {
        "title": html["title"],
        "term_nodes": term_nodes
    }

f = graphviz.Digraph("mentions")
for href_in_graph_1, node_1 in list_nodes.items():
    for href_in_graph_2, node_2 in list_nodes.items():
        if node_1["title"] != node_2["title"]:
            nodes_1_linkage = set(node_1["term_nodes"])
            nodes_2_linkage = set(node_2["term_nodes"])
            linkage = nodes_1_linkage.intersection(nodes_2_linkage)
            if linkage:
                f.edge(node_1["title"], node_2["title"], label=", ".join(linkage))
f.view()
