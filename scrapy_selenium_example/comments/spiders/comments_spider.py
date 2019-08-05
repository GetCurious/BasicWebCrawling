import scrapy
from scrapy import Selector
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys as Keyboard
from selenium.webdriver.support import expected_conditions as Expects
from selenium.webdriver.support.ui import WebDriverWait


class QuotesSpider(scrapy.Spider):
    name = "comments"
    start_urls = [
        'https://www.scmp.com/week-asia/politics/article/3014355/malaysias-azmin-ali-sex-scandal-ministers-aide-asked-me-lie-says']

    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        options.binary_location = "/opt/brave.com/brave/brave-browser"
        self.driver = webdriver.Chrome(options=options)

    def parse(self, response):
        self.driver.get(response.url)
        body = self.driver.find_element_by_tag_name('body')
        body.click()
        found_button = None

        while not found_button:
            try:
                found_button = self.driver.find_element_by_xpath(
                    '//*[@id="articleDetails-1"]//a[contains(@class, "comment btn-comment")]')
                print("Found Comment Button")
                actions = ActionChains(self.driver)
                actions.move_to_element(found_button)
                actions.click(found_button)
                actions.perform()
                break
            except NoSuchElementException:
                print("Scrolling...")
                body.send_keys(Keyboard.PAGE_DOWN)

        wait = WebDriverWait(self.driver, 10)
        frame = wait.until(
            Expects.presence_of_element_located((By.XPATH, '//iframe[contains(@class, "comment-iframe")]')))

        self.driver.switch_to.frame(frame)

        body = Selector(text=self.driver.page_source)

        # Helper function
        def xp(query) -> str:
            return quote.xpath(query).get(default='').strip()

        # Selector
        for quote in body.xpath('//*[contains(@id, "comment-item-")]/div/div[2]'):
            yield {
                'author': xp('div[1]/text()'),
                'comment': xp('div[2]/text()[normalize-space()]'),
            }

        response.css('div[id*="comment-item"] div div').xpath('div[1]/text()[normalize-space()]').getall()

        # Search for next page
        for a in response.css('li.next a'):
            yield response.follow(a, callback=self.parse)
