from selenium import webdriver
import logging
from steps import craigslist_gig_step_open_gigs_page, craigslist_gig_step_scrape_gigs
import gig_object

def main():
    driver = webdriver.Chrome(executable_path="chromedriver.exe")
    logger = logging.Logger("initial-view")
    stream_h = logging.StreamHandler()
    logger.addHandler(stream_h)
    logger.setLevel(logging.DEBUG)

    gig = gig_object.GigObject()

    open_page = craigslist_gig_step_open_gigs_page.OpenGigsPageStep(driver, logger, gig)
    open_page.run()

    if open_page.step_success:
        step = craigslist_gig_step_scrape_gigs.ScrapeGigsStep(driver, logger, gig)
        step.run()


if __name__ == '__main__':
    main()