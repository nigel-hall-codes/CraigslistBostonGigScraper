from steps.craigslist_gig_step import Step
import steps.craigslist_gig_step_select_next_gig_for_more_info
from steps.craigslist_gig_step_close_driver import CloseDriverStep
import time


class ScrapeGigDetailPageStep(Step):
    def __init__(self, driver, logger, gig_object):
        Step.__init__(self, driver, logger, gig_object)

    def run(self):
        """
        Scrapes post body for any pay amounts and rates. Then navigates back.
        """

        try:
            self.logger.info("Scraping post for pay and rate")

            time.sleep(4)

            compensation_attribute = self.gigs_detail_page.compensation_attribute()

            if compensation_attribute == None:
                self.logger.info("Compensation attribute not found. Extracting post text")
                text = self.gigs_detail_page.post_text()

            else:
                self.logger.info(f"Compensation attribute found. {compensation_attribute}")
                text = compensation_attribute

            pay_from_post = self.gig_object.pay_from_s(text)
            pay_rate = self.gig_object.pay_rate(text)

            self.logger.info(f"Pay from post identified as {pay_from_post}")
            self.logger.info(f"Pay rate identified as {pay_rate}")

            self.gig_object.gigs._set_value(self.gig_object.current_gig.name, "pay_from_post", pay_from_post)
            self.gig_object.gigs._set_value(self.gig_object.current_gig.name, "pay_rate", pay_rate)
            self.gig_object.gigs._set_value(self.gig_object.current_gig.name, "Completed", True)

            self.driver.back()
            time.sleep(2)

            self.step_success = True

        except Exception as e:
            self.logger.exception("Failed to scrape post for pay and rate")
            self.logger.exception(e)


    def next_step(self):
        if self.step_success:
            return steps.craigslist_gig_step_select_next_gig_for_more_info.SelectNextGigForMoreInfoStep(self.driver, self.logger, self.gig_object)

        else:
            return CloseDriverStep(self.driver, self.logger, self.gig_object)