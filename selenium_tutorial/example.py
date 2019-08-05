from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as Expects
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys as Keyboard

import pandas as pd

# Browser Settings
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.binary_location = "/opt/brave.com/brave/brave-browser"
driver = webdriver.Chrome(options=options)


# Target URL
driver.get("https://www.scmp.com/week-asia/politics/article/3014355/malaysias-azmin-ali-sex-scandal-ministers-aide-asked-me-lie-says")
print("Page is ready!")


# Focus on dynamic element
body = driver.find_element_by_tag_name('body')
body.click()


# Comment Button
found_button = None

while not found_button:
    try:
        found_button = driver.find_element_by_xpath(
            '//*[@id="articleDetails-1"]//a[contains(@class, "comment btn-comment")]')
        print("Found Comment Button")
        actions = ActionChains(driver)
        actions.move_to_element(found_button)
        actions.click(found_button)
        actions.perform()
        break
    except NoSuchElementException:
        print("Scrolling...")
        body.send_keys(Keyboard.PAGE_DOWN)


# Wait Component to load before switching
wait = WebDriverWait(driver, 10)
frame = wait.until(Expects.presence_of_element_located((By.XPATH, '//iframe[contains(@class, "comment-iframe")]')))
driver.switch_to.frame(frame)


# XPath Query
authors = driver.find_elements_by_xpath('//*[contains(@id, "comment-item-")]/div/div[2]/div[1]')
comments = driver.find_elements_by_xpath('//*[contains(@id, "comment-item")]/div/div[2]/div[2][normalize-space(.)]')
assert authors, f"No data : {authors}"


# ETL
if authors and comments:
    columns = ['Author', 'Comment']
    data = [[author.text, comment.text] for author, comment in zip(authors, comments)]

    # Store
    df = pd.DataFrame(columns=columns, data=data)
    df.to_csv('news_comments.csv', index=False)
    print("Comments saved")


# Clean up
driver.close()
