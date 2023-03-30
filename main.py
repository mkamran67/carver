from selenium import webdriver
from selenium.webdriver.common.by import By

url = "https://www.amazon.com/deals?ref_=nav_cs_gb"

driver = webdriver.Firefox()
driver.get(url)


element_list = driver.find_element(By.CSS_SELECTOR, "div.a-row:nth-child(4)")

print(element_list)

driver.close()