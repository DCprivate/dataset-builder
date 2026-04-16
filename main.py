from scrapy.crawler import CrawlerProcess
import scrapy


class Spooder(scrapy.Spider):
    name = "test"
    start_urls = ["https://www.scrapethissite.com/pages/"]

    def parse(self, response):
        text_chunks = response.css("body ::text").getall()
        clean_text = " ".join(t.strip() for t in text_chunks if t.strip())

        yield {
            "url": response.url,
            "title": response.css("title::text").get(),
            "text": clean_text,
        }


def main():
    process = CrawlerProcess(settings={
        "FEEDS": {
            "output.json": {"format": "json"},
        }
    })

    process.crawl(Spooder)
    process.start()  # blocks until finished


if __name__ == "__main__":
    main()