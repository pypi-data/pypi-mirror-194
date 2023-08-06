from krxmarket.krx import api


def test_stock_market_list():
    krx_list = api.get_krx_all()
    assert len(krx_list) > 2000