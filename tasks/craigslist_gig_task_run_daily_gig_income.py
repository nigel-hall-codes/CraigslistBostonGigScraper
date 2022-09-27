from selenium import webdriver
import logging
import sys
sys.path.append("..")
from steps import craigslist_gig_step_open_gigs_page, craigslist_gig_step_scrape_gigs
import gig_object


def main():
    driver = webdriver.Chrome(executable_path="../drivers/chromedriver.exe")
    logger = logging.Logger("initial-view")
    stream_h = logging.StreamHandler()
    logger.addHandler(stream_h)
    logger.setLevel(logging.DEBUG)

    gig = gig_object.GigObject()

    step = craigslist_gig_step_open_gigs_page.OpenGigsPageStep(driver, logger, gig)

    while step is not None:
        step.run()
        step = step.next_step()

if __name__ == '__main__':
    main()