from selenium import webdriver
import logging
from steps import craigslist_gig_step_open_gigs_page, craigslist_gig_step_scrape_gigs
from steps import craigslist_gig_step_scrape_gig_detail_page
import gig_object

def main():
    driver = webdriver.Chrome(executable_path="../drivers/chromedriver.exe")
    logger = logging.Logger("initial-view")
    stream_h = logging.StreamHandler()
    logger.addHandler(stream_h)
    logger.setLevel(logging.DEBUG)

    gig = gig_object.GigObject()

    single_detail_url = "https://boston.craigslist.org/gbs/evg/7527997529.html"

    driver.get(single_detail_url)

    step = craigslist_gig_step_scrape_gig_detail_page.ScrapeGigDetailPageStep(driver, logger, gig_object)
    step.run()

if __name__ == '__main__':
    main()