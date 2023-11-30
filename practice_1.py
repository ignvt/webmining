import requests
import re
import matplotlib.pyplot as plt


def find_links(current_url):
    html_code = get_html(current_url)
    find_relative = re.findall(r'<a\s+(?:[^>]*?\s+)?href=(["\'])(https://' + current_url.split("://")[1] + r'.*?)\1',
                               html_code)
    links = [link[1] for link in find_relative[:2]]
    return links


def get_html(current_url):
    response = requests.get(current_url)
    return response.text


def go(current_url, current_data, is_next):
    html = get_html(current_url)
    current_data.append({"domain": current_url, "count": html.count(text)})
    if is_next:
        links = find_links(current_url)
        for link in links:
            go(link, current_data, False)


text = "ИТАС"
urls = ["https://59.ru", "https://pstu.ru"]
data = []

for url in urls:
    go(url, data, True)

domains = [d['domain'] for d in data]
counts = [d['count'] for d in data]

plt.barh(domains, counts)
plt.title(f'Упоминания {text} на искомых сайтах')
plt.ylabel('Сайт')
plt.xlabel(f'Количество {text}')
plt.subplots_adjust(left=0.6)
plt.show()
