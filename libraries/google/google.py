from libraries.common import act_on_element, capture_page_screenshot, log_message
from config import OUTPUT_FOLDER
import random
import time
from selenium.webdriver.common.keys import Keys


class Google():

    def __init__(self, rpa_selenium_instance, credentials: dict):
        self.browser = rpa_selenium_instance
        self.google_url = credentials["url"]

    def access_google(self):
        """
        Access Google from the browser.
        """
        self.browser.go_to(self.google_url)
        #print(self.browser.get_source())
        try:
            act_on_element('//button[child::div[text()="I agree"]]', 'click_element', 2)
        except Exception:
            pass

    def search_movie(self):
        """
        Search movie and click the first result that matches the name.
        """
        search_text = "the lord of the rings the return of the king itunes movie us"
        search_bar = act_on_element('//input[@title="Search"]', 'find_element')
        self.browser.input_text_when_element_is_visible('//input[@title="Search"]', search_text)
        search_bar.send_keys(Keys.ENTER)
        #act_on_element('//div[@class="FPdoLc lJ9FBc"]//input[@value="Google Search"]', "click_element")
        act_on_element('//div[@class="g tF2Cxc"]//a[contains(@href, "itunes.apple.com") and descendant::h3[contains(text(), "The Lord of the Rings: The Return of the King")]]', "click_element")
        

