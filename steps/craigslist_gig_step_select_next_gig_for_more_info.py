from steps.craigslist_gig_step import Step
# from steps.craigslist_gig_step_scrape_gigs import ScrapeGigsStep
import steps.craigslist_gig_step_scrape_gigs
from steps.craigslist_gig_step_scrape_gig_detail_page import ScrapeGigDetailPageStep
from steps.craigslist_gig_step_calculate_daily_gig_income import CalculateDailyGigIncomeStep
from steps.craigslist_gig_step_close_driver import CloseDriverStep


class SelectNextGigForMoreInfoStep(Step):
    def __init__(self, driver, logger, gig_object):
        Step.__init__(self, driver, logger, gig_object)
        self.new_gig_page_found = False
        self.complete = False

    def run(self):
        """
        Searches gig_object.gigs for any remaining gigs without associated pay and gig detail check.
        If valid gig found, clicks gig and runs ScrapeGigDetailPage
        If zero gigs remains, attempts to click next page, and rerun ScrapeGigsStep
        """

        try:
            self.logger.info("Selecting next incomplete gigs")

            incomplete_gigs = self.gig_object.gigs[self.gig_object.gigs['Completed'] == False]

            if not incomplete_gigs.empty:
                self.gig_object.current_gig = incomplete_gigs.iloc[0]
                self.logger.info(f"Gig found: {self.gig_object.current_gig}. Navigating to detail page")
                self.driver.get(self.gig_object.current_gig["post_title_link"])
                self.step_success = True
                return

            else:
                if self.gigs_page.next_page_button_enabled():
                    self.logger.info("More gig pages available. Clicking next page")
                    self.gigs_page.click_next_page_button()
                    self.new_gig_page_found = True

                else:
                    self.logger.info("No more gig pages found")
                    self.complete = True

                self.step_success = True

        except Exception as e:
            self.logger.exception("Failed to select next incomplete gig")
            self.logger.exception(e)


    def next_step(self):
        if self.step_success:
            if self.new_gig_page_found:
                return steps.craigslist_gig_step_scrape_gigs.ScrapeGigsStep(self.driver, self.logger, self.gig_object)

            elif self.complete:
                return CalculateDailyGigIncomeStep(self.driver, self.logger, self.gig_object)

            else:
                return ScrapeGigDetailPageStep(self.driver, self.logger, self.gig_object)

        else:
            return CloseDriverStep(self.driver, self.logger, self.gig_object)