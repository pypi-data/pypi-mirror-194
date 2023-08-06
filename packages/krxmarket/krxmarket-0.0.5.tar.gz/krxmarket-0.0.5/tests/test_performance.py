from krxmarket.stock_corps import StockCorps
from krxmarket.performance import get_performance


def test_performance_all():
    corps = StockCorps().corps

    for stock_code, corp in corps.items():
        get_performance(corp.corp_code, 2016)