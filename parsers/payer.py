from pandas import DataFrame


class PayerParser:
    dataframe: DataFrame

    def __init__(self, df: DataFrame):
        self.dataframe = df

    def parse(self):
        self.dataframe.reindex(self.dataframe['Payer'])
        return self.dataframe.to_dict(orient='records')
