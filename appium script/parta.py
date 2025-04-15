import time
import unittest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy

capabilities = dict(
    platformName='Android',
    automationName='uiautomator2',
    deviceName='Android',
    appPackage='in.amazon.mShop.android.shopping',
    appActivity='com.amazon.mShop.home.HomeActivity',
    language='en',
    locale='US',
	uiautomator2ServerInstallTimeout=60000,
	unicodekeyboard='true',
	resetkeyboard='true'
)

appium_server_url = 'http://localhost:4723'

class TestAppium(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Remote(appium_server_url, options=UiAutomator2Options().load_capabilities(capabilities))

    def tearDown(self):
        if self.driver:
            self.driver.quit()
        print("tear down")

    def test_search(self):
        start_time = time.time()

        # Handle system notification
        notification_allow_button = self.driver.find_element(
            AppiumBy.ID, "com.android.permissioncontroller:id/permission_allow_button"
        )
        notification_allow_button.click()
        print("Clicked on notification allow button")

        time.sleep(2)

        # Handle the case when the user isnt signed in
        def checkSignin():
            try:
                english_field = self.driver.find_element(
                    AppiumBy.XPATH, "//android.widget.ImageView[@content-desc='Select English']"
                )
                english_field.click()
                print("Clicked on english")
            except Exception as e:
                print(f"Failed to English button or it wasnt present: {e}")
            
            time.sleep(2)

            try:
                continue_field = self.driver.find_element(
                    AppiumBy.ID, "in.amazon.mShop.android.shopping:id/continue_button"
                )
                continue_field.click()
                print("Clicked on continue button")
            except Exception as e:
                print(f"Failed to continue button or it wasnt present: {e}")
            
            time.sleep(2)

            try:
                signin_field = self.driver.find_element(
                    AppiumBy.ID, "in.amazon.mShop.android.shopping:id/skip_sign_in_button"
                )
                signin_field.click()
                print("Clicked on skip signin button")
            except Exception as e:
                print(f"Failed to click skip signin button or it wasnt present: {e}")
        
        checkSignin()
        homepage_load_time = time.time() - start_time

        start_time = time.time()
        
        time.sleep(2)

        # click search bar
        search_bar = self.driver.find_element(
            AppiumBy.ID, "in.amazon.mShop.android.shopping:id/chrome_search_hint_view"
        )
        search_bar.click()
        print("Clicked on search bar")

        time.sleep(2)

        # Enter search text
        search_text_field = self.driver.find_element(
            AppiumBy.ID, "in.amazon.mShop.android.shopping:id/rs_search_src_text"
        )
        search_text_field.send_keys("wireless headphones")
        print("Entered search text: wireless headphones")
        
        self.driver.press_keycode(66, 0, 0)
        print("Pressed Enter key")

        time.sleep(5)

        search_time = time.time() - start_time

        #part e and f
        f = open("partf.txt", "a")
        e = open("parte.txt", "a")

        f.write(f"Amazon homepage load time(Part A): {homepage_load_time:.2f} seconds\n")
        f.write(f"Amazon homepage Effective(excluding Sleep time) load time(Part A): {homepage_load_time-6:.2f} seconds\n")
        f.write("*********************************************************************************\n")

        e.write(f"Activity1: homepage load time(Part A): {homepage_load_time:.2f} seconds\n")
        e.write(f"Activity1: Effective(excluding Sleep time) homepage load time(Part A): {homepage_load_time-6:.2f} seconds\n")
        e.write(f"Activity2: Search Time(Part A): {search_time:.2f} seconds\n")
        e.write(f"Activity2: Effective(excluding Sleep time) Search time(Part A): {search_time-9:.2f} seconds\n")
        e.write("*********************************************************************************\n")
        
        f.close()
        e.close()

        # 15sec sleep 
        # Sleep time is given to account for phones with slow processor or bad wifi - which increases screen loading Time
       
	


if __name__ == '__main__':
    unittest.main()
