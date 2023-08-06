import sys
import os
from typing import List, Union
from arelle import ModelXbrl, XbrlConst
import re
from pandas import DataFrame
from arelle import Cntlr
import pandas as pd

from .helper import consolidated_code_to_role_number, get_title
from .util import str_compare
from .xbrl_table import XbrlTable


def arelle_setup():
    if sys.platform == 'win32':
        pass
    elif sys.platform == 'darwin':
        arelle_app_dir = os.path.join(os.path.expanduser('~/Library/Application Support'), 'Arelle')
        if not os.path.exists(arelle_app_dir):
            os.makedirs(arelle_app_dir)
    else:
        arelle_app_dir = os.path.join(os.path.expanduser("~/.config"), "arelle")
        if not os.path.exists(arelle_app_dir):
            os.makedirs(arelle_app_dir)


class Xbrl:
    def __init__(self, file_uri: str):
        arelle_setup()
        self.xbrl: ModelXbrl = Cntlr.Cntlr(
            logFileName='temp.log').modelManager.load(file_uri)
        self._tables = None

    def get_fs(self):
        data = self.get_financial_statement()
        return data[0] if data else None

    def get_is(self):
        data = self.get_income_statement()
        if data:
            data = data[0] if len(data) > 1 else None
        return data

    def get_ci(self):
        data = self.get_income_statement()
        if data:
            data = data[1] if len(data) > 1 else data[0]
        return data

    def get_cf(self):
        data = self.get_cash_flows()
        return data[0] if data else None

    @property
    def tables(self):
        """list of Table: Table 리스트"""
        if self._tables is not None:
            return self._tables

        arcrole = XbrlConst.parentChild
        relationship = self.xbrl.relationshipSet(arcrole)
        tables = None
        if relationship is not None:
            tables = []
            for uri in relationship.linkRoleUris:
                role_types = self.xbrl.roleTypes.get(uri)

                if role_types is not None:
                    definition = (role_types[0].genLabel(lang='ko', strip=True)
                                  or role_types[0].definition or uri)
                else:
                    definition = uri

                role_code = re.search(r"\[(.*?)\]", definition)
                role_code = role_code.group(1) if role_code else None
                tables.append(XbrlTable(self, self.xbrl, role_code, definition, uri))
                
        self._tables = tables
        return tables

    def get_table_by_code(self, code: str) -> Union[XbrlTable, None]:
        for table in self.tables:
            if str_compare(table.code, code):
                return table
        return None

    def _to_info_DataFrame(self, code: str, lang: str = 'ko') -> DataFrame:
        table = self.get_table_by_code(code)
        return table.to_DataFrame(lang=lang, show_class=False, show_concept=False, separator=False)
    
    def get_document_information(self, lang: str = 'ko') -> DataFrame:
        return self._to_info_DataFrame('d999001', lang=lang)

    def get_entity_information(self, lang: str = 'ko') -> DataFrame:
        """
        공시 대상 정보
        """
        return self._to_info_DataFrame('d999004', lang=lang)

    def get_audit_information(self, lang: str = 'ko') -> DataFrame:
        """
        감사 정보
        """
        return self._to_info_DataFrame('d999003', lang=lang)

    def get_entity_address_information(self, lang: str = 'ko') -> DataFrame:
        return self._to_info_DataFrame('d999005', lang=lang)

    def get_author_information(self, lang: str = 'ko') -> DataFrame:
        return self._to_info_DataFrame('d999006', lang=lang)

    def get_financial_statement_information(self, lang: str = 'ko') -> DataFrame:
        """
        재무제표
        """
        return self._to_info_DataFrame('d999007', lang=lang)

    def get_financial_statement(self, separate: bool = False) -> Union[List[XbrlTable], None]:
        return self._get_statement('dart-gcd_StatementOfFinancialPosition', separate=separate)

    def get_income_statement(self, separate: bool = False) -> Union[List[XbrlTable], None]:
        return self._get_statement('dart-gcd_StatementOfComprehensiveIncome', separate=separate)

    def get_changes_in_equity(self, separate: bool = False) -> Union[List[XbrlTable], None]:
        return self._get_statement('dart-gcd_StatementOfChangesInEquity', separate=separate)

    def get_cash_flows(self, separate: bool = False) -> Union[List[XbrlTable], None]:
        return self._get_statement('dart-gcd_StatementOfCashFlows', separate=separate)

    def _get_statement(
        self,
        concept_id: str,
        separate: bool = False
    ) -> Union[List[XbrlTable], None]:
        """ Financial statement information 을 이용하여 제공되는 재무제표를 추출하는 함수

        Parameters
        ----------
        concept_id: str
            dart-gcd_StatementOfFinancialPosition: 재무상태표
            dart-gcd_StatementOfComprehensiveIncome: 포괄손익계산서
            dart-gcd_StatementOfChangesInEquity: 자본변동표
            dart-gcd_StatementOfCashFlows: 현금프름표
        separate: bool, optional
            True: 개별재무제표
            False: 연결재무제표

        Returns
        -------
        Table or None


        """
        table = self.get_table_by_code('d999007')
        if table is None:
            return None
        table_dict = table.get_value_by_concept_id(concept_id)
        compare_name = 'Separate' if separate else 'Consolidated'
        for keys, value in table_dict.items():
            for key in keys:
                title = ''.join(key)
                if re.search(compare_name, title, re.IGNORECASE):
                    code_list = consolidated_code_to_role_number(value, separate=separate)
                    tables = [self.get_table_by_code(code) for code in code_list]
                    return tables
        return None

    def exist_consolidated(self):
        """ 연결 재무제표 존재 여부를 확인하기 위한 함수

        Returns
        -------
        bool
            연결재무제표 존재시 True / 개별재무제표만 존재시 False
        """
        regex = re.compile(r'Consolidated', re.IGNORECASE)
        info_table = self.get_table_by_code('d999007')
        cls_list = info_table.cls
        for cls in cls_list:
            titles = get_title(cls, 'en')
            for title in titles:
                if isinstance(title, str):
                    if regex.search(title):
                        return True
                else:
                    if regex.search(' '.join(title)):
                        return True
        return False
    
    def get_period_information(self, lang: str = 'ko') -> DataFrame:
        """ 공시 문서 기간 정보

        Parameters
        ----------
        lang: str
            표시 언어 설정('ko': 한글, 'en': 영어)

        Returns
        -------
        DataFrame
            공시 문서 기간 정보
        """
        df = self._to_info_DataFrame('d999002', lang=lang)
        data = df[df.columns[2:]].iloc[3]
        data_set = [(key, data[key]) for key in data.keys()]
        new_columns = list(df.columns[:2]) + \
            [data[0] for data in sorted(data_set, key=lambda x: x[1], reverse=True)]
        new_columns = pd.MultiIndex.from_tuples(new_columns)
        return df[new_columns]