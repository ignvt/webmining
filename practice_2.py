import scrapy


class ScrapySpider(scrapy.Spider):
    name = "pstu web"
    start_urls = ["https://pstu.ru"]

    def parse(self, response):
        links = response.css(f'a[href^="{response.url}"]::attr(href)').getall()
        images_src = response.css("img::attr(src)").getall()
        news = []
        for announcement in response.css("div.news_item"):
            news.append({
                "href": response.url + announcement.css("a::attr(href)").get(),
                "date": {
                    "day": announcement.css("div.date div.day::text").get(),
                    "month": announcement.css("div.date div.month::text").get(),
                    "year": announcement.css("div.date div.year::text").get(),
                },
                "title": announcement.css("div.title::text").get()
            })
        print("News", news)
        print("Relative links:", links)
        print("Images with src:", images_src)
