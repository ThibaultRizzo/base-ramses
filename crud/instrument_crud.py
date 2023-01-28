from .base_crud import BaseCrud
from models import Instrument, HourlyPriceTimeseries
from .timeseries_crud import HourlyPriceTimeseriesCrud
from datetime import datetime, time, timedelta
from models.model_enums import PriceFrequency
from models.instrument import MARKET_TIMEFRAMES

class InstrumentCrud(BaseCrud[Instrument]):
    base_cls = Instrument

    @classmethod
    def pull(cls, session, id: str, end_date: datetime, start_date: datetime = None, frequency: PriceFrequency=PriceFrequency.DAILY):
        instrument = cls.get_by_id(session, id)
        extraction_cls = instrument.get_extract_cls()
        return extraction_cls.pull(instrument, end_date, start_date - timedelta(days=1) , frequency)

    @classmethod
    def get_timeseries(cls, session, code: str, start_date: datetime, end_date: datetime):
        # Get all timeseries persisted in database
        instrument = cls.get_one(session, (
            Instrument.code == code,
        ))
        if not instrument:
            raise Exception(f'No instrument found for code {code}')

        timeseries = HourlyPriceTimeseriesCrud.get_all(session, (
            HourlyPriceTimeseries.instrument_id == instrument.id,
            HourlyPriceTimeseries.date >= start_date,
            HourlyPriceTimeseries.date <= end_date,
        ))

        # Check if some are missing
        persisted_dates = [ts.date for ts in timeseries]
        datetime_delta = end_date - start_date
        expected_start_time, expected_end_time = MARKET_TIMEFRAMES[(instrument.type, instrument.country_code)]
        needed_dates = [
            datetime.combine(
                start_date.date(),
                expected_start_time
            ) + timedelta(days=day, hours=hour) 
            for day in range(datetime_delta.days + 1) for hour in range(
                expected_end_time.hour + 1 - expected_start_time.hour
            )
        ]
        missing_dates = [date for date in needed_dates if date not in persisted_dates]
    
        # Pull data for all missing
        if missing_dates:
            pulled_timeseries_dict = cls.pull(
                session=session,
                id=instrument.id,
                end_date=missing_dates[-1]+ timedelta(days=1),
                start_date=missing_dates[0],
                frequency=PriceFrequency.HOURLY
            )
            new_timeseries = []

            for ts in pulled_timeseries_dict:
                if ts.date not in persisted_dates:
                    _dict = pulled_timeseries_dict[ts]
                    new_timeseries.append(
                        HourlyPriceTimeseries(
                            date=ts.isoformat(),
                            open=_dict.get('Open'),
                            high=_dict.get('High'),
                            low=_dict.get('Low'),
                            close=_dict.get('Close'),
                            volume=_dict.get('Volume'),
                            frequency=PriceFrequency.HOURLY,
                            instrument_id=instrument.id,
                        )
                    )

            session.add_all(new_timeseries)
            session.commit()
            timeseries.extend(new_timeseries)
            
            return sorted(timeseries, key=lambda ts: ts.date, reverse=True)
    
    # @classmethod
    # def get_time_interval(cls, instrument):
    #     instrument_type = instrument.type
    #     if 
    # # def pull_and_save(cls, instrument: Instrument, end_date: datetime, start_date: datetime = None):
    #     data_dict = cls.pull(instrument, end_date, start_date, PriceFrequency.HOURLY)
    #     db = next(get_db())
    #     timeseries = []
    #     for ts in data_dict:
    #         _dict = data_dict[ts]
    #         timeseries.append(
    #             HourlyPriceTimeseries(
    #                 date=ts,
    #                 open=_dict.get('Open'),
    #                 high=_dict.get('High'),
    #                 low=_dict.get('Low'),
    #                 close=_dict.get('Close'),
    #                 volume=_dict.get('Volume'),
    #                 frequency=PriceFrequency.HOURLY,
    #                 instrument_id=instrument.id,
    #             )
    #         )
    #     db.add_all(timeseries)
    #     db.commit()
