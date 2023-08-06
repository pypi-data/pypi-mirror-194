from krxmarket.stock_corps import StockCorps


def test_samsung_in_stock():
    corps = StockCorps().corps
    assert '005930' in corps
    assert corps['005930'].name == '삼성전자'