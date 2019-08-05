# Scrapy + Selenium
Script file @ `scrapy_selenium_example/comments/spiders/comments_spider.py`

## How to run
```
cd scrapy_selenium_example
scrapy crawl comments -o comments.jsonlines
```

*Comment-out this line for standard Chrome Browser*

`options.binary_location = "/opt/brave.com/brave/brave-browser"`
