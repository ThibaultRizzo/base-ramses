from datetime import datetime

from models import HourlyPriceTimeseries

from .base_crud import BaseCrud


class HourlyPriceTimeseriesCrud(BaseCrud):
    base_cls = HourlyPriceTimeseries
