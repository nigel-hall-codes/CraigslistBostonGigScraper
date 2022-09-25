from page_objects import craigslist_gig_gigs_page, craigslist_gig_gigs_detail_page


class Step:
    def __init__(self, driver, logger, gig_object):
        self.driver = driver
        self.logger = logger
        self.gig_object = gig_object
        self.gigs_page = craigslist_gig_gigs_page.GigsPage(self.driver)
        self.gigs_detail_page = craigslist_gig_gigs_detail_page.GigsDetailPage(self.driver)
        self.step_success = False

