import re
import statistics
import numpy as np
import pandas as pd

class GigObject:

    def __init__(self):
        self.hourly_identifiers = ["hr", "hour", "hrly"]
        self.daily_identifiers = ["daily", "per day", "day"]

        self.gigs = pd.DataFrame()

    def pay_from_s(self, s):

        s = s.lower()

        possible_pay = re.findall("\$\d+(?:\.\d+)?", s.replace(",", ""))
        possible_pay = [float(s.replace("$", "")) for s in possible_pay]
        if possible_pay == []:
            return np.NAN

        else:
            return statistics.mean([float(pay) for pay in possible_pay])

    def pay_rate(self, s):

        s = s.lower()

        if any([hourly_id in s for hourly_id in self.hourly_identifiers]):
            return "hourly"

        elif any([daily_id in s for daily_id in self.daily_identifiers]):
            return "daily"

        else:
            return "lump"