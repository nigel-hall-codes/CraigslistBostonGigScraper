import pandas as pd

from steps.craigslist_gig_step import Step
from steps.craigslist_gig_step_select_next_gig_for_more_info import SelectNextGigForMoreInfoStep
from steps.craigslist_gig_step_close_driver import CloseDriverStep
import re
import time

class ScrapeGigsStep(Step):
    def __init__(self, driver, logger, gig_object):
        Step.__init__(self, driver, logger, gig_object)

    def run(self):

        """Attempts to scrape Craigslist gigs off current page of webdriver"""

        try:
            time.sleep(5)
            self.logger.debug("Scraping gigs...")
            gigs = self.gigs_page.gigs()
            gigs['detail_body'] = None
            gigs['Completed'] = False

            self.logger.info(f"{gigs.shape[0]} gigs found.")

        except Exception as e:
            self.logger.exception("Failed to scrape gigs")
            self.logger.exception(e)
            return

        try:
            self.logger.debug("Extracting any dollar amounts from post title")
            gigs['pay_from_post'] = gigs['post_title_text'].apply(self.gig_object.pay_from_s)
            gigs['pay_rate'] = gigs['post_title_text'].apply(self.gig_object.pay_rate)

            # gigs that have a $ amount listed in post title are marked as completed
            gigs.loc[pd.notna(gigs['pay_from_post']), "Completed"] = True

        except Exception as e:
            self.logger.exception("Failed to extract dollar amounts")
            self.logger.exception(e)

        try:
            self.logger.info("Concatenating gigs to existing gig df if exists")

            if self.gig_object.gigs.empty:
                self.gig_object.gigs = gigs

            else:
                self.gig_object.gigs = pd.concat([self.gig_object.gigs, gigs])

            self.step_success = True

        except Exception as e:
            self.logger.exception(e)
            self.logger.exception("Failed to concatenate gigs")

    def next_step(self):
        if self.step_success:
            return SelectNextGigForMoreInfoStep(self.driver, self.logger, self.gig_object)

        else:
            return CloseDriverStep(self.driver, self.logger, self.gig_object)