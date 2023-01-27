from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from models import Instrument

@dataclass
class BaseExtractor:
    ticker_column: str

    def pull(cls, instrument: Instrument, end_date: datetime, start_date: datetime = None):
        '''
        Download timeseries from a datasource
        '''
        raise Exception('Not implemented')
