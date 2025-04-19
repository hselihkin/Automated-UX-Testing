import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

class PythonOrgSearch(unittest.TestCase):

	def setUp(self):
		self.driver = webdriver.Firefox()

	def test_search_in_python_org(self):
		driver = self.driver
		driver.get("http://www.python.org")
		self.assertIn("Python", driver.title)
		elem = driver.find_element(By.NAME, "q")
		elem.send_keys("pycon")
		elem.send_keys(Keys.RETURN)
		self.assertNotIn("No results found.", driver.page_source)

	def test_google(self):
		driver = self.driver
		driver.get("https://google.co.in")
		self.assertIn("Google", driver.title)
		elem = driver.find_element(By.NAME, "q")
		elem.send_keys("BITS Pilani Hyderabad Campus")
		elem.send_keys(Keys.RETURN)
		driver.implicitly_wait
		print(driver.title)


	def tearDown(self):
		# self.driver.close()
		print("Done")

if __name__ == "__main__":
	unittest.main()