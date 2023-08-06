from enum import Enum
from typing import List


class MarketType(str, Enum):
    KOSPI = 'stockMkt'
    KOSDAQ = 'kosdaqMkt'
    KONEX = 'konexMkt'


class KrxCorp:
    def __init__(
        self,
        sectors: List[str] = [],
        products: List[str] = [],
        market_type: MarketType = MarketType.KOSPI,
        listed_date: str = '',
        name: str = '',
        stock_code: str = '',
        corp_code: str = '',
        update_date: str = ''
    ):
        self.sectors = sectors
        self.products = products
        self.market_type = market_type
        self.listed_date = listed_date
        self.name = name
        self.stock_code = stock_code
        self.halt_reason = ''
        self.is_halt = False
        self.corp_code = corp_code
        self.update_date = update_date

    @property
    def short_market_type(self):
        if self.market_type == MarketType.KOSPI:
            return 'Y'
        elif self.market_type == MarketType.KOSDAQ:
            return 'K'
        elif self.market_type == MarketType.KONEX:
            return 'N'
        return 'E'

    def __str__(self):
        return f'stock code({self.stock_code}) corp code({self.corp_code})' \
               f' name({self.name}) sectors({self.sectors})' \
               f' is_halt({self.is_halt}) reason({self.halt_reason})'
