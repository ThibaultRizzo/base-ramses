from utils.enums import BaseEnum


class PriceFrequency(BaseEnum):
    HOURLY = "HOURLY"
    DAILY = "DAILY"

    def get_interval(self):
        if self == PriceFrequency.DAILY:
            return "1d"
        if self == PriceFrequency.HOURLY:
            return "1h"
        raise ValueError(f"No interval configured for {self.value}")
