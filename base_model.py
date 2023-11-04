from dataclasses import dataclass

from pandas import DataFrame


@dataclass
class BaseModel:
    def load_data(self) -> DataFrame:
        pass

    def clean_data(self, df: DataFrame) -> DataFrame:
        pass

    def run_strategy(self, df):
        pass

    def execute(self):
        df = self.load_data()
        df = self.clean_data(df)
        self.run_strategy(df)


# class BandModel(BaseModel):
