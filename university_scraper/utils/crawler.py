import time

from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class Crawler():

    def __init__(self, url, headless=True, wait_time=1):
        options = webdriver.ChromeOptions()

        if headless:
            options.add_argument('headless')

        driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        driver.implicitly_wait(wait_time)
        driver.get(url)
        self.driver = driver
        self._wait_time = wait_time

    @property
    def page_source(self):
        return self.driver.page_source

    @property
    def url(self):
        return self.driver.current_url

    def close(self):
        self.driver.close()

    def wait_for_element_to_load_by_id(self, id, max_delay=5):
        WebDriverWait(self.driver, max_delay).until(EC.presence_of_element_located((By.ID, id)))

    def wait_for_element_to_load_by_xpath(self, xpath, max_delay=5):
        WebDriverWait(self.driver, max_delay).until(EC.presence_of_element_located((By.XPATH, xpath)))

    def scroll_to_top(self):
        element = self.driver.find_element_by_tag_name('header')
        element.location_once_scrolled_into_view
        time.sleep(self._wait_time)

    def scroll_to_bottom(self):
        element = self.driver.find_element_by_tag_name('footer')
        element.location_once_scrolled_into_view
        time.sleep(self._wait_time)

    def click_element(self, identifier=None, tag='div', selector='class', custom=None):
        if custom:
            element = self.driver.find_element_by_xpath(custom)
        else:
            element = self.driver.find_element_by_xpath(f"//{tag}[@{selector}='{identifier}']")
        self.driver.execute_script("arguments[0].click();", element)
        time.sleep(self._wait_time)

    def get_element(self, identifier=None, tag='div', selector='class', custom=None):
        if custom:
            element = self.driver.find_element_by_xpath(custom)
        else:
            element = self.driver.find_element_by_xpath(f"//{tag}[@{selector}='{identifier}']")
        time.sleep(self._wait_time)
        return element

    def scroll_to_element(self, identifier=None, tag='div', selector='class', custom=None):
        if custom:
            element = self.driver.find_element_by_xpath(custom)
        else:
            element = self.driver.find_element_by_xpath(f"//{tag}[@{selector}='{identifier}']")
        element.location_once_scrolled_into_view
        time.sleep(self._wait_time)

    def scroll_to_first_visible(self, identifier=None, tag='div', selector='class', custom=None):
        if custom:
            elements = self.driver.find_elements_by_xpath(custom)
        else:
            elements = self.driver.find_elements_by_xpath(f"//{tag}[@{selector}='{identifier}']")
        elements[0].location_once_scrolled_into_view
        time.sleep(self._wait_time)

    def scroll_to_last_visible(self, identifier=None, tag='div', selector='class', custom=None):
        if custom:
            elements = self.driver.find_elements_by_xpath(custom)
        else:
            elements = self.driver.find_elements_by_xpath(f"//{tag}[@{selector}='{identifier}']")
        elements[len(elements) - 1].location_once_scrolled_into_view
        time.sleep(self._wait_time)

    def scroll_through_first_visible(self, identifier, tag='div', selector='class'):
        while True:
            elements = self.driver.find_elements_by_xpath(f"//{tag}[@{selector}='{identifier}']")
            if len(elements) > 0:
                elements[0].location_once_scrolled_into_view
                time.sleep(self._wait_time)
            else:
                break

    def find_elements(self, identifier=None, tag='div', selector='class', custom=None):
        if custom:
            return self.driver.find_elements_by_xpath(custom)
        else:
            return self.driver.find_elements_by_xpath(f"//{tag}[@{selector}='{identifier}']")
