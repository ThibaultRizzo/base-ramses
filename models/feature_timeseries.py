
class FeatureTimeseries:
    __tablename__ = 'featuretimeseries'


    id: str
    date: datetime
    value: float
    model_id: str
    feature_id: str
