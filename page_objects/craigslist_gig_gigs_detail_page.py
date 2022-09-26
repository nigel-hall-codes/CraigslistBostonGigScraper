import selenium
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import pandas as pd
import re

class GigsDetailPage:
    def __init__(self, driver):
        self.driver = driver
        self.post_body = (By.ID, "postingbody")
        self.compensation_attribute_div = (By.CLASS_NAME, "attrgroup")

    def post_text(self):

        """
        :return str:
        """

        wait = WebDriverWait(self.driver, 5)
        post_body_div = wait.until(EC.presence_of_element_located(self.post_body))
        return post_body_div.text

    def compensation_attribute(self):

        """
        :return str:
        """

        try:

            wait = WebDriverWait(self.driver, 5)
            attr_group = wait.until(EC.presence_of_element_located(self.compensation_attribute_div))

            for item in attr_group.find_elements(By.TAG_NAME, "span"):
                if "compensation" in item.text:
                    compensation = item.text.split("compensation: ")[-1]

                    if any(chr.isdigit() for chr in compensation):

                        # Some compensation attributes don't have $ symbol. The next code adds it next to any number
                        # for compatibility with gigs_object.pay_from_s

                        numbers = re.findall("\d+(?:\.\d+)?", compensation)

                        if "$" not in compensation:
                            for n in numbers:
                                compensation = compensation.replace(n, f"${n}")

                        return compensation

                    else:
                        return None


            return None

        except:
            return None


