import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement

driver = webdriver.Firefox()
wait = WebDriverWait(driver, 10)

# Opening the Home Page
start = time.time()
driver.get("https://www.amazon.in/")
assert 'Amazon' in driver.title
print("home page loaded in:", time.time() - start, "seconds")
driver.implicitly_wait(10)

# Searching for wireless headphones
start = time.time()
searchBox = driver.find_element(By.ID, "twotabsearchtextbox")
searchBox.send_keys("wireless headphones")
searchBox.send_keys(Keys.RETURN)
results = driver.find_elements(By.CSS_SELECTOR, "div.s-main-slot div[data-component-type='s-search-result']")
assert len(results) > 0
print("search results loaded in:", time.time() - start, "seconds")

start = time.time()
sortDropdown = wait.until(EC.element_to_be_clickable((By.ID, "a-autoid-0-announce")))
sortDropdown.click()
sortDropdown.click()

sortLowtoHigh = wait.until(EC.element_to_be_clickable((By.ID, "s-result-sort-select_1")))
ActionChains(driver).move_to_element(sortLowtoHigh).click().perform()

wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.s-main-slot div[data-component-type='s-search-result'] span.a-price")))
sortedResults = driver.find_elements(By.CSS_SELECTOR, ".s-main-slot .s-result-item[data-component-type='s-search-result']")
assert len(sortedResults) > 0
print("sorted search results loaded in:", time.time() - start, "seconds")

start = time.time()
name = None
price = None
# Retrieving Name and Price of cheapest item
for item in sortedResults:
    # try catch as sometimes the price isn't where you'd expect it to be
    # print(item.get_attribute("outerHTML"))

    try:
        name = item.find_element(By.CSS_SELECTOR, "h2 span").text.strip()[:50]  # Extracting the name
        price = item.find_element(By.CSS_SELECTOR, "span.a-price-whole").text
        break
    except:
        continue
if name and price:
    print("The cheapest item is:", name, "for", price, "rupees")
else:
    print("Couldn't find the name and price")
print("time for retrieval:", time.time() - start, "seconds")