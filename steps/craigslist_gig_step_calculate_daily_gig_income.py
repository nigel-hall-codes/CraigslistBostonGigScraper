from steps.craigslist_gig_step import Step
from steps.craigslist_gig_step_close_driver import CloseDriverStep
import re


class CalculateDailyGigIncomeStep(Step):
    def __init__(self, driver, logger, gig_object):
        Step.__init__(self, driver, logger, gig_object)
        self.new_gig_page_found = False
        self.complete = False

    def run(self):

        self.logger.info("Calculating daily income")

        pass

    def next_step(self):
        return CloseDriverStep(self.driver, self.logger, self.gig_object)