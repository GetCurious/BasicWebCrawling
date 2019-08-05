from selenium import webdriver
import pandas as pd

# # Browser Settings
# options = webdriver.ChromeOptions()
# options.binary_location = "/opt/brave.com/brave/brave-browser"
# driver = webdriver.Chrome(options=options)

driver = webdriver.Chrome()

# Target URL
driver.get("https://www.scmp.com/scmp_comments/popup/3014355")

# XPath
authors = driver.find_elements_by_xpath('//*[contains(@id, "comment-item-")]/div/div[2]/div[1]')
comments = driver.find_elements_by_xpath('//*[contains(@id, "comment-item")]/div/div[2]/div[2][normalize-space(.)]')

# ETL
columns = ['Author', 'Comment']
data = [[author.text, comment.text] for author, comment in zip(authors, comments)]

# Store
df = pd.DataFrame(columns=columns, data=data)
df.to_csv('news_comments.csv', index=False)

# Clean up
driver.close()
