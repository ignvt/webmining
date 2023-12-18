import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import requests
from bs4 import BeautifulSoup
import re

menu = [
    "Пицца", "Карбонара", "Болоньезе", "Лазанья", "Ризотто",
    "Чак-чак", "Губадия", "Эчпочмак", "Кыстыбый", "Хворост",
    "Кимчи", "Том-ям", "Рис", "Соба", "Креветки", "Пад-тай",
    "Шаурма", "Пельмени", "Борщ", "Суши", "Стейк", "Рамен",
    "Фалафель", "Хачапури", "Гамбургер", "Сэндвич", "Мясо", "Рыба",
    "Курица", "Суп-пюре", "Салат", "Суп", "Каша"
]
sources = {
    "Perm": "https://59.ru/text?rubric=food",
    "Kazan": "https://116.ru/text?rubric=food",
    "Ekaterinburg": "https://www.e1.ru/text?rubric=food",
    "Moscow": "https://msk1.ru/text?rubric=food",
    "Tyumen": "https://72.ru/text?rubric=food",
    "Vladivostok": "https://vladivostok1.ru/text?rubric=food",
    "Novosibirsk": "https://ngs.ru/text/?rubric=food"
}


def get_links_page(response):
    soup = BeautifulSoup(response.content, "html.parser")
    links = []
    for link in soup.find_all("a", {"class": "qZbm2"}):
        if link["href"].startswith("/text/"):
            links.append(response.url.split("/")[2] + link["href"])
    return links


def load_file(name):
    with open(name, "r", encoding="utf-8") as file:
        return json.load(file)


def processing_pages():
    data = {}
    for source in sources:
        for page_count in range(1, 10):
            response = requests.get(f"{sources.get(source)}&page={page_count}")
            links = get_links_page(response)
            for link in links:
                print(link)
                response_page = requests.get(f"https://{link}")
                soup_page = BeautifulSoup(response_page.content, "html.parser")
                content = soup_page.get_text()
                counts_menu = {}
                for item in menu:
                    counts_menu[item] = len(re.findall(item, content, re.IGNORECASE))
                data[source] = counts_menu
    with open("zzzzzzzzzzzzzz.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)
    return data


df = processing_pages()
# df = load_file("zzzzzzzzzzzzzz.json")
df = pd.DataFrame(df).T
kmeans = KMeans(n_clusters=3, random_state=0, n_init=10).fit(df)
df["KMeans_Cluster"] = kmeans.labels_
pca = PCA(n_components=2)
df_with_pca = pca.fit_transform(df.drop("KMeans_Cluster", axis=1))
df_with_pca = pd.DataFrame(df_with_pca, columns=["PCA_1", "PCA_2"])
df_with_pca["KMeans_Cluster"] = df["KMeans_Cluster"].values
city_names = df.index
df_with_pca["City"] = city_names
plt.figure()
sns.scatterplot(data=df_with_pca, x="PCA_1", y="PCA_2", hue="KMeans_Cluster")
for i in range(len(df_with_pca)):
    plt.text(df_with_pca.PCA_1[i], df_with_pca.PCA_2[i], df_with_pca.City[i])
plt.savefig("KMeans_Clusters.png")
print(df.drop("KMeans_Cluster", axis=1).idxmax(axis=1))
