import requests
from bs4 import BeautifulSoup
import zipfile


def images_from_url(url):
    response = requests.get(url)
    if response.status_code == 200 or response.status_code == 304:
        soup = BeautifulSoup(response.content, "html.parser")
        images_img = soup.find_all("img")
        images_source = soup.find_all("source")
        img_urls = []
        for img in images_img:
            if "src" in img.attrs:
                if img["src"][0] == "/":
                    img_urls.append(url + img["src"])
                else:
                    img_urls.append(img["src"])
        for source in images_source:
            if "srcset" in source.attrs:
                src_sets = source["srcset"].split(",")
                for srcset in src_sets:
                    if source["srcset"][0] == "/":
                        img_urls.append(url + srcset.strip().split(" ")[0])
                    else:
                        img_urls.append(srcset.strip().split(" ")[0])
        with zipfile.ZipFile("images.zip", "w") as myZip:
            for index, current_url in enumerate(img_urls):
                file = requests.get(current_url)
                myZip.writestr(f'picture_{index + 1}.{current_url.split("/")[-1].split(".")[-1]}', file.content)
    else:
        print("Error:", response.status_code)


domain = "https://drom.ru"
images_from_url(domain)
