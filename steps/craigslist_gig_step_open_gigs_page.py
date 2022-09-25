import time

from steps.craigslist_gig_step import Step
from steps.craigslist_gig_step_scrape_gigs import ScrapeGigsStep
from steps.craigslist_gig_step_close_driver import CloseDriverStep

class OpenGigsPageStep(Step):
    def __init__(self, driver, logger, gig_object):
        Step.__init__(self, driver, logger, gig_object)

    def run(self):
        """Attempts to open Craigslist Boston gig page and validates gig count"""

        try:
            self.logger.debug("Opening gigs page")
            self.gigs_page.open_page_no_duplicates()
            time.sleep(4)

        except Exception as e:
            self.logger.exception("Failed to open gigs page")
            self.logger.exception(e)

        try:
            self.logger.debug("Validating gigs...")
            gigs = self.gigs_page.gigs()

            assert not gigs.empty

            self.step_success = True

        except Exception as e:
            self.logger.exception("Failed to validate gigs")
            self.logger.exception(e)


    def next_step(self):
        if self.step_success:
            return ScrapeGigsStep(self.driver, self.logger, self.gig_object)

        else:
            return CloseDriverStep(self.driver, self.logger, self.gig_object)