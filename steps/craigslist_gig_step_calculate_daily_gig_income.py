from steps.craigslist_gig_step import Step
from steps.craigslist_gig_step_close_driver import CloseDriverStep
import re
import datetime
import pandas as pd


class CalculateDailyGigIncomeStep(Step):
    def __init__(self, driver, logger, gig_object):
        Step.__init__(self, driver, logger, gig_object)
        self.new_gig_page_found = False
        self.complete = False

    def run(self):

        try:
            self.logger.info("Calculating daily income")

            df = self.gig_object.gigs
            df.to_csv(f'../data/CraigslistBostonGigs{datetime.datetime.now().strftime("%m%d%Y")}.csv')

            df['day'] = df['post_datetime'].apply(
                lambda x: datetime.datetime.strptime(x.split(".")[0], "%Y-%m-%dT%H:%M:%S").strftime("%m-%d-%Y"))

            pay_listed = df[pd.notna(df['pay_from_post'])]

            hourly_pay = pay_listed[pay_listed['pay_rate'] == 'hourly']
            lump_sums = pay_listed[pay_listed['pay_rate'] == 'lump']
            daily = pay_listed[pay_listed['pay_rate'] == 'daily']
            weekly = pay_listed[pay_listed['pay_rate'] == 'weekly']

            # Remove outliers
            hourly_pay = hourly_pay[(hourly_pay['pay_from_post'] < hourly_pay['pay_from_post'].quantile(0.98))]
            lump_sums = lump_sums[lump_sums['pay_from_post'] < lump_sums['pay_from_post'].quantile(0.98)]
            daily = daily[daily['pay_from_post'] < daily['pay_from_post'].quantile(0.98)]
            weekly = weekly[weekly['pay_from_post'] < weekly['pay_from_post'].quantile(0.98)]

            # Calculate average max hourly rate income by day
            max_hourly_rate = hourly_pay.groupby("day")['pay_from_post'].max().mean()
            self.logger.info(f"Average max hourly rate per day: ${max_hourly_rate}")

            # Calculate average lump sum total per day
            average_lump_sum_total_per_day = lump_sums.groupby('day')['pay_from_post'].sum().mean()
            self.logger.info(f"Average lump sum total per day: ${average_lump_sum_total_per_day}")

            # Calculate average daily sum per day
            average_daily_sum_per_day = daily.groupby("day")["pay_from_post"].sum().mean()
            self.logger.info(f"Average daily pay per day: ${average_daily_sum_per_day}")

            # Calculate average weekly sum per day
            average_weekly_sum_per_day = weekly.groupby("day")['pay_from_post'].sum().mean()
            self.logger.info(f"Average weekly pay per day: ${average_weekly_sum_per_day}")

            # Calculate average total for max hourly rate * 8 hours +
            #                             average lump sum per day +
            #                             average daily pay +
            #                             average weekly pay / 5 work days

            total_possible_income_per_day = (max_hourly_rate * 8) + \
                                            average_lump_sum_total_per_day + \
                                            average_daily_sum_per_day + \
                                            (average_weekly_sum_per_day / 5)

            self.logger.info(f"Total possible income per day if one did all the jobs: ${total_possible_income_per_day}")

        except Exception as e:
            self.logger.exception(e)
            self.logger.exception("Failed to calculate daily income")

    def next_step(self):
        return CloseDriverStep(self.driver, self.logger, self.gig_object)
