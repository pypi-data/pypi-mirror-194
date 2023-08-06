from typing import Dict, List
from bs4 import BeautifulSoup

from ..common.webrequest import request
from ..common.types import KrxCorp, MarketType


def get_stock_market_list(market_type: MarketType) -> List[KrxCorp]:
    """
    return corporation list which listed on KRX
    """
    url = 'https://kind.krx.co.kr/corpgeneral/corpList.do'
    referer = 'https://kind.krx.co.kr/corpgeneral/corpList.do' \
              '?method=loadInitPage'
    
    payload = {
        'method': 'download',
        'pageIndex': 1,
        'currentPageSize': 5000,
        'orderMode': 3,
        'orderStat': 'D',
        'searchType': 13,
        'marketType': market_type.value,
        'fiscalYearEnd': 'all',
        'location': 'all',
    }
    
    stock_market_list = []

    resp = request.post(url=url, payload=payload, referer=referer)
    html = BeautifulSoup(resp.text, 'html.parser')
    rows = html.find_all('tr')

    for row in rows:
        cols = row.find_all('td')
        if len(cols) > 0:
            stock_market_list.append(
                KrxCorp(
                    sectors=cols[2].text.strip(),
                    products=cols[3].text.strip(),
                    market_type=market_type,
                    listed_date=cols[4].text.strip(),
                    name=cols[0].text.strip(),
                    stock_code=cols[1].text.strip()
                )
            )

    return stock_market_list


def _market_type_to_int(market_type: MarketType) -> int:
    if market_type == MarketType.KOSPI:
        return 1
    elif market_type == MarketType.KOSDAQ:
        return 2
    elif market_type == MarketType.KONEX:
        return 6
    raise TypeError('cannot find market type')


def get_trading_halt_list(market_type: MarketType) -> dict:
    """ 
    return dictionary of halted corps, key: stock code, value: issue
    """
    url = 'https://kind.krx.co.kr/investwarn/tradinghaltissue.do'
    referer = 'https://kind.krx.co.kr/investwarn/' \
              'tradinghaltissue.do?method=searchTradingHaltIssueMain'

    payload = {
        'method': 'searchTradingHaltIssueSub',
        'currentPageSize': 3000,
        'pageIndex': 1,
        'searchMode': '',
        'searchCodeType': '',
        'searchCorpName': '',
        'forward': 'tradinghaltissue_down',
        'paxreq': '',
        'outsvcno': '',
        'marketType': _market_type_to_int(market_type),
        'repIsuSrtCd': '',
    }

    trading_halt_dict = {}

    resp = request.post(url=url, payload=payload, referer=referer)
    html = BeautifulSoup(resp.text, 'html.parser')
    rows = html.find_all('tr')

    for row in rows:
        cols = row.find_all('td')
        if len(cols) > 0:
            trading_halt_dict[cols[2].text.strip()] = cols[3].text.strip()

    return trading_halt_dict


def get_krx_all(exclude_halt=True) -> Dict[str, KrxCorp]:
    """
    return dictionary(key: stock_code, value: KrxInfo)
    """
    market_types = [MarketType.KOSPI, MarketType.KOSDAQ, MarketType.KONEX]
    halt_corps = {}
    corps: Dict[str, KrxCorp] = {}
    for market_type in market_types:
        halt_corps = {**get_trading_halt_list(market_type)}

    for market_type in market_types:
        market_list = get_stock_market_list(market_type)
        for corp in market_list:
            if corp.stock_code in halt_corps.keys():
                corp.is_halt = True
                corp.halt_reason = halt_corps[corp.stock_code]

            if not corp.is_halt or not exclude_halt:
                corps[corp.stock_code] = corp

    return corps