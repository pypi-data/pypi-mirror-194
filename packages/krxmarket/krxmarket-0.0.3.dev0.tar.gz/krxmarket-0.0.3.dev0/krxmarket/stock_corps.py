from typing import Dict
import logging

from .common.types import KrxCorp
from .dart.api import get_corp_code
from .krx.api import get_krx_all


LOGGER = logging.getLogger(__name__)


class StockCorps:
    """
    mixin KRX market and DART info
    """
    def __init__(self):
        self._corps: Dict[str, KrxCorp] = {}
        self.fetch_info()

    def fetch_info(self) -> None:
        krx_corps = get_krx_all()
        for dart_info in get_corp_code():
            stock_code = dart_info['stock_code']
            if stock_code is not None:
                if stock_code not in krx_corps:
                    # 보통 KRX 에서 상장 폐지 종목은 제외로 아래 warning
                    LOGGER.warning('cannot find dart stock code %s in krx(%s)',
                                   stock_code, dart_info)
                    continue
                krx_corps[stock_code].update_date = dart_info['modify_date']
                krx_corps[stock_code].corp_code = dart_info['corp_code']
                self._corps[stock_code] = krx_corps[stock_code]
    
    def search_by_stock_code(self, stock_code: str):
        return self._corps.get(stock_code)
    
    @property
    def corps(self):
        return self._corps
