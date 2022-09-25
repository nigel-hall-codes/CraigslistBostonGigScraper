from steps.craigslist_gig_step import Step
import re


class CloseDriverStep(Step):
    def __init__(self, driver, logger, gig_object):
        Step.__init__(self, driver, logger, gig_object)

    def run(self):
        """Attempts to scrape Craigslist gigs off current page of webdriver"""

        try:
            self.logger.debug("Closing driver...")
            self.driver.close()

        except Exception as e:
            self.logger.exception("Failed to close driver")
            self.logger.exception(e)

    def next_step(self):
        return None


