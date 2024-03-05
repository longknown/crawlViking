#!/usr/bin/python
import scrapy
from scrapy.crawler import CrawlerProcess


class VikingSpider(scrapy.Spider):
    name = "viking"

    start_urls = ["https://vikingcabin.com"]

    def start_requests(self):
        base_url = 'https://vikingcabin.com/page/'
        max_page = 1162
        for page in range(1, max_page+1):
            yield scrapy.Request(url=base_url+str(page), callback=self.parse)

    def parse(self, response):
        book_list = response.css("h2.entry-title")
        for book in book_list:
            yield {
                "book_name": book.css("::text").get(),
                "url": book.css("a::attr(href)").get(),
            }

        #next_page = response.css('.next').css("a::attr(href)").get()
        #if next_page is not None:
            #yield response.follow(next_page, callback=self.parse)

    def parse_books(self, response):
        book_list = response.css("h2.entry-title")
        for book in book_list:
            yield {
                "book_name": book.css("::text").get(),
                "url": book.css("a::attr(href)").get(),
            }

def main():
    process = CrawlerProcess(
            settings = {
                "FEEDS" : {
                    "items.json" : {
                        "format": "json",
                        "encoding" : "utf8",
                        "overwrite": True,
                        },
                },
                "CONCURRENT_REQUESTS" : 500,
                "LOG_LEVEL": "INFO",
            }
    )

    process.crawl(VikingSpider)
    process.start()

if __name__ == "__main__":
    main()
