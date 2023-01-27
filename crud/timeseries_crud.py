from .base_crud import BaseCrud
from models import HourlyPriceTimeseries
from datetime import datetime

class HourlyPriceTimeseriesCrud(BaseCrud):
    base_cls = HourlyPriceTimeseries
