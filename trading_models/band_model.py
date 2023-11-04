class BandModel(BaseTradingModel):
    pass


class BandModels(BaseTradingModel):
    def load_data(self) -> DataFrame:
        super().load_data()
