import pandas as pd
import openpyxl


class ExcelReader:
    file_path: str = ''
    data: pd.DataFrame

    def __init__(self, file_path: str):
        self.file_path = file_path

    def read_sheet(self, sheet_name: str):
        return pd.read_excel(self.file_path, sheet_name=sheet_name, header=0)

    def get_sheet_names(self) -> [str]:
        workbook = openpyxl.load_workbook(self.file_path, read_only=True)
        sheets = workbook.worksheets
        sheet_names = [sheet.title for sheet in sheets if sheet.sheet_state != 'hidden']
        workbook.close()
        return sheet_names

    def get_payer(self,sheet_name):
        data = pd.read_excel(self.file_path, sheet_name=sheet_name, index_col=None, usecols="K", header=0, nrows=0)
        return data.columns.values[0]
