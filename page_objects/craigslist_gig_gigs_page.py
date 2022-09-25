import selenium
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import pandas as pd

class GigsPage:
    def __init__(self, driver):
        self.driver = driver
        self.results_div = (By.ID, 'search-results-page-1')
        self.next_page_button = (By.CLASS_NAME, "cl-next-page")

    def open_page_no_duplicates(self):
        self.driver.get("https://boston.craigslist.org/search/ggg?bundleDuplicates=1#search=1~list~0~0")

    def gigs(self):

        gigs_list = []
        wait = WebDriverWait(self.driver, 5)
        results_div = wait.until(EC.presence_of_element_located(self.results_div))

        for li_element in results_div.find_elements(By.TAG_NAME, "li"):
            data = {}
            data["post_datetime"] = li_element.find_element(By.CLASS_NAME, "post-date").get_attribute("datetime")
            post_title = li_element.find_element(By.CLASS_NAME, "post-title")
            data["post_title_link"] = post_title.get_attribute("href")
            data["post_title_text"] = post_title.text
            data["post_hood"] = li_element.find_element(By.CLASS_NAME, "post-hood").text

            gigs_list.append(data)

        return pd.DataFrame(gigs_list)

    def click_next_page_button(self):
        wait = WebDriverWait(self.driver, 5)
        button = wait.until(EC.presence_of_element_located(self.next_page_button))
        button.click()

    def next_page_button_enabled(self):
        wait = WebDriverWait(self.driver, 5)
        button = wait.until(EC.presence_of_element_located(self.next_page_button))

        return "bd-disabled" not in button.get_attribute("class")




