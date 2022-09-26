from selenium import webdriver
import logging
from steps import craigslist_gig_step_calculate_daily_gig_income
import gig_object
import pandas as pd


def main():
    driver = webdriver.Chrome(executable_path="chromedriver.exe")
    logger = logging.Logger("initial-view")
    stream_h = logging.StreamHandler()
    logger.addHandler(stream_h)
    logger.setLevel(logging.DEBUG)

    gig = gig_object.GigObject()

    gig.gigs = pd.read_csv(r'..\data\CraigslistBostonGigs09262022.csv')

    step = craigslist_gig_step_calculate_daily_gig_income.CalculateDailyGigIncomeStep(driver, logger, gig)
    step.run()


if __name__ == '__main__':
    main()