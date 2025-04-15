import time
import unittest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder

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

        start_time = time.time()

        # either of these can be used to click on filter
        try:
            filter_field = self.driver.find_element(
                AppiumBy.XPATH, "//android.widget.Button[@resource-id='s-all-filters-announce']"
            )
            filter_field.click()
            print("Clicked on Filters")
        except Exception as e:
            print(f"Failed to click filter or it wasnt present: {e}")
        
        try:
            filter_field = self.driver.find_element(
                AppiumBy.XPATH, "//android.view.View[@resource-id='s-all-filters']"
            )
            filter_field.click()
            print("Clicked on Filters")
        except Exception as e:
            print(f"Failed to click filter or it wasnt present: {e}")

        time.sleep(2)

        # swipe down x3
        def swipe_vertical(driver, start_x, start_y, end_y):
            actions = ActionChains(driver)
            pointer = PointerInput(interaction.POINTER_TOUCH, 'finger')
            action_builder = ActionBuilder(driver, mouse=pointer)

            action_builder.pointer_action.move_to_location(x=int(start_x), y=int(start_y))
            action_builder.pointer_action.pointer_down()
            action_builder.pointer_action.move_to_location(x=int(start_x), y=int(end_y))
            action_builder.pointer_action.pointer_up()

            actions.w3c_actions = action_builder
            actions.perform()
        
        screen_size = self.driver.get_window_size()
        width = screen_size['width']
        height = screen_size['height']

        start_x = int(width * 0.2)
        start_y = int(height * 0.7)
        end_y = int(height * 0.3)

        for _ in range(3):
            swipe_vertical(self.driver, start_x, start_y, end_y)

        time.sleep(2)

        #goto sortby section
        sort_text_field = self.driver.find_element(
            AppiumBy.XPATH, "//android.view.View[@text='Sort by']"
        )
        sort_text_field.click()
        print("Clicked on sort filter")

        time.sleep(2)

        #descending order of highest customer rating
        highrated_field = self.driver.find_element(
            AppiumBy.XPATH, "//android.widget.CheckBox[@resource-id='sort/review-rank']"
        )
        highrated_field.click()
        print("Clicked on high rating filter")

        time.sleep(2)

        #go to Products page by clicking on cross
        cross_field = self.driver.find_element(
            AppiumBy.XPATH, "//android.widget.Button[@text='close']"
        )
        cross_field.click()
        print("Clicked on sort filter")

        time.sleep(2)

        filter_time = time.time() - start_time

        start_time = time.time()

        # scroll down
        screen_size2 = self.driver.get_window_size()
        width = screen_size2['width']
        height = screen_size2['height']

        start_x2 = int(width * 0.2)
        start_y2 = int(height * 0.6)  
        end_y2 = int(height * 0.4)

        swipe_vertical(self.driver, start_x2, start_y2, end_y2) 

        time.sleep(2)

        product_elements = self.driver.find_elements(
            AppiumBy.XPATH, "//android.widget.TextView[contains(@text, 'Headphone') or contains(@text, 'Headphones') or contains(@text, 'headphone') or contains(@text, 'headphones')]"
        )
        
        title_element = None
        price_element = None
        
        flag = 0
        #taking the 2nd result, because 1st result is "wireless heaphones" text that is present in the search bar
        for element in product_elements:
            try:
                text = element.get_attribute("text")
                if text:
                    title_element = element
                    if flag:
                        break
                    flag += 1
            except:
                continue
        
        price_elements = self.driver.find_elements(
            AppiumBy.XPATH, "//android.view.View[contains(@content-desc, '₹')]"
        )
        if price_elements:
            price_element = price_elements[0]
        
        product_name = title_element.get_attribute("text") if title_element else "Product name not found"
        product_price = price_element.get_attribute("content-desc") if price_element else "Price not found"

        price = ""
        flag = 0
        #only extracting the price, excluding the product rating, MRP etc..
        for c in product_price:
            if c == "₹":
                flag = 1
            if flag:
                price += c
            if c == " " and flag:
                break
        
        print("Highest Rated Headphone: \n")
        print(f"Name: {product_name}")
        print(f"Price: {price}")

        product_time = time.time() - start_time

        start_time = time.time()

        # depending on number of products on screen the text value changes
        try: 
            cart_field = self.driver.find_element(
                AppiumBy.XPATH, "//android.widget.Button[@text='Add to cart']"
            )
            cart_field.click()
            print("Clicked on add to cart")
        except Exception as e:
            print(f"Failed to click add to cart or it wasnt present: {e}")

        try: 
            cart_field = self.driver.find_element(
                AppiumBy.XPATH, "(//android.widget.Button[@text='Add to cart'])[1]"
            )
            cart_field.click()
            print("Clicked on add to cart")
        except Exception as e:
            print(f"Failed to click add to cart or it wasnt present: {e}")
        
        time.sleep(2)
        
        # seeing if the product was successfully added to the cart
        check_cart_field = self.driver.find_element(
            AppiumBy.XPATH, "(//android.widget.ImageView[@resource-id='in.amazon.mShop.android.shopping:id/bottom_tab_button_icon'])[3]"
        )
        check_cart_field.click()
        print("Clicked on cart")

        time.sleep(5)

        cart_time = time.time() - start_time

        total_time = homepage_load_time + search_time + filter_time + product_time + cart_time

        #part e and f
        f = open("partf.txt", "a")
        e = open("parte.txt", "a")

        f.write(f"Amazon homepage load time(Part D): {homepage_load_time:.2f} seconds\n")
        f.write(f"Amazon homepage Effective(excluding Sleep time) load time(Part D): {homepage_load_time-6:.2f} seconds\n")

        e.write(f"Activity1: homepage load time(Part D): {homepage_load_time:.2f} seconds\n")
        e.write(f"Activity1: Effective(excluding Sleep time) homepage load time(Part D): {homepage_load_time-6:.2f} seconds\n")
        e.write(f"Activity2: Search Time(Part D): {search_time:.2f} seconds\n")
        e.write(f"Activity2: Effective(excluding Sleep time) Search time(Part D): {search_time-9:.2f} seconds\n")
        e.write(f"Activity3: filter time(Part D): {filter_time:.2f} seconds\n")
        e.write(f"Activity3: Effective(excluding Sleep time) filter time(Part D): {filter_time-10:.2f} seconds\n")
        e.write(f"Activity4: product retrieval time(Part D): {product_time:.2f} seconds\n")
        e.write(f"Activity4: Effective(excluding Sleep time) product retrieval time(Part D): {product_time-2:.2f} seconds\n")
        e.write(f"Activity5: product retrieval time(Part D): {cart_time:.2f} seconds\n")
        e.write(f"Activity5: Effective(excluding Sleep time) product retrieval time(Part D): {cart_time-7:.2f} seconds\n")
        e.write(f"Total Time Taken: {total_time:.2f} seconds\n")
        e.write(f"Effective(excluding Sleep time) Total Time Taken: {total_time-34:.2f} seconds\n")

        f.close()
        e.close()

        # 34sec sleep
        # Sleep time is given to account for phones with slow processor or bad wifi - which increases screen loading Time
    

if __name__ == '__main__':
    unittest.main()
