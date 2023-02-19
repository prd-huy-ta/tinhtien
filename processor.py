from parsers import PayerParser, MemberParser
from readers.reader import ExcelReader
import pandas
from consts import FILE_PATH, PAYER_SHEET_NAME, TEMPLATE_SHEET_NAME, THAM_GIA, NOP, EVENT, PAYER
import unidecode


class Processor:
    reader: ExcelReader = None
    members = dict()
    payers = dict()

    def __init__(self):
        self.reader = ExcelReader(FILE_PATH)
        self.members = self.get_member_list()
        self.payers = self.get_payers()

    def process(self):
        sheet_names = self.reader.get_sheet_names()

        filter_out_sheet_names = [PAYER_SHEET_NAME, TEMPLATE_SHEET_NAME]
        sheet_names = [sheet_name for sheet_name in sheet_names if sheet_name not in filter_out_sheet_names]
        for sheet_name in sheet_names:
            self.calculate_member_sheet(sheet_name)
        self.to_file()

    def get_payers(self):
        payer_reader = ExcelReader(FILE_PATH)
        payer_reader.read_sheet(PAYER_SHEET_NAME)
        payer_sheet = payer_reader.read_sheet(PAYER_SHEET_NAME)
        return payer_sheet

    def calculate_member_sheet(self, sheet_name):
        sheet_data, payer = self.parse_member_sheet(sheet_name)
        for member in sheet_data:
            if member[THAM_GIA] not in self.members.keys():
                continue
            member_dict = self.members.get(member[THAM_GIA])
            member_events = member_dict.get(EVENT) or []
            member_events.append(sheet_name)
            member_nop = member_dict.get(NOP) or []
            member_nop.append(member[NOP])
            member_payer = member_dict.get(PAYER) or []
            member_payer.append(payer)
            member_dict.update({EVENT: member_events,
                                NOP: member_nop,
                                PAYER:member_payer})

    def parse_member_sheet(self, sheet_name: str):
        member_reader = ExcelReader(FILE_PATH)
        df = member_reader.read_sheet(sheet_name)
        member_parser = MemberParser(df)
        return member_parser.parse(), member_reader.get_payer(sheet_name)

    def get_member_list(self):
        member_reader = ExcelReader(FILE_PATH)
        df = member_reader.read_sheet(TEMPLATE_SHEET_NAME)
        member_parser = MemberParser(df)
        data = member_parser.parse()
        names = [item[THAM_GIA] for item in data]
        member_dict = dict()
        for name in names:
            member_dict.update({
                name: dict()
            })
        return member_dict

    def to_file(self):
        from datetime import datetime
        output = f"Sheet {datetime.now().year}-{datetime.now().month}.xlsx"
        with pandas.ExcelWriter(output) as writer:
            for member_name, member_value in self.members.items():
                member_df = pandas.DataFrame.from_dict(member_value)
                member_df.to_excel(writer, sheet_name=member_name)
