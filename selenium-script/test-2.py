import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

driver = webdriver.Firefox()

driver.get("https://www.bits-pilani.ac.in")
driver.implicitly_wait(10)
assert "Birla Institute of Technology And Science, Pilani (BITS Pilani)" in driver.title
search = driver.find_element(By.NAME, "s")
search.clear()
search.send_keys("Hyderabad Campus")
search.send_keys(Keys.RETURN)
# driver.close()

