from pandas import DataFrame

from consts import THAM_GIA, NOP


class MemberParser:
    dataframe: DataFrame

    def __init__(self, df: DataFrame):
        self.dataframe = df

    def parse(self):
        self.dataframe=self.dataframe[self.dataframe[THAM_GIA].notnull()]
        self.dataframe.reindex(self.dataframe[THAM_GIA])
        return self.dataframe.to_dict(orient='records')

