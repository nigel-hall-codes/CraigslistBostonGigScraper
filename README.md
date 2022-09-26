# CraigslistBostonGigScraper

Installation
------------
Run pip install -r requirements.txt

Run
---
Scripts to run tasks are found in /tasks. Set your webdriver path in those files or place your chromedriver.exe in the /driver folder.

Webscraper

`python3 tasks/craigslist_gig_task_run_daily_gig_income.py`

This will start the web scraping process and when complete will run the daily income calculation

Calculation

`python3 tasks/craigslist_gig_task_run_calculate_daily_income_from_csv.py`

Run this to perform last calculation step on already stored csv data
