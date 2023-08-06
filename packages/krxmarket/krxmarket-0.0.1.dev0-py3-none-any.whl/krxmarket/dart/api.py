from typing import Literal
import copy
import tempfile

from .status import check_status
from .auth import get_api_key
from .request import api_request, download_xbrl
from ..common.xbrl.xbrl import Xbrl
from ..common.webrequest import request
from ..common.file import read_file_from_zip
from ..common.types import KrxCorp


class Report:
    _DART_URL_ = 'https://dart.fss.or.kr'
    _REPORT_URL_ = _DART_URL_ + '/dsaf001/main.do'
    _DOWNLOAD_URL_ = _DART_URL_ + '/pdf/download/main.do'

    def __init__(self, **kwargs):
        self.rcp_no = (kwargs['rcept_no'] if 'rcept_no' in kwargs
                       else kwargs.get('rcp_no'))
        if self.rcp_no is None:
            raise ValueError('no rcp number in report')
        self.dcm_no = kwargs.get('dcm_no')
        self.info = copy.deepcopy(kwargs)
        """
        info example
        {
            'corp_code': '00126380',
            'corp_name': '삼성전자',
            'stock_code': '005930',
            'corp_cls': 'Y',
            'report_nm': '기타경영사항(자율공시)',
            'rcept_no': '20230214801207',
            'flr_nm': '삼성전자',
            'rcept_dt': '20230214',
            'rm': '유'
        }
        """
        self.xbrl = None

    def load_xbrl(self):
        with tempfile.TemporaryDirectory() as path:
            try:
                file_uri = download_xbrl(path=path, rcept_no=self.rcp_no)
                if len(file_uri) > 0:
                    self.xbrl = Xbrl(file_uri)
            except Exception:
                pass


class SearchResult:
    """ DART 검색결과 정보를 저장하는 클래스"""

    def __init__(self, resp):
        self._page_no = resp['page_no']
        self._page_count = resp['page_count']
        self._total_count = resp['total_count']
        self._total_page = resp['total_page']
        self._report_list = [Report(**x) for x in resp['list']]

    @property
    def page_no(self):
        """ 표시된 페이지 번호 """
        return self._page_no

    @property
    def page_count(self):
        """페이지당 표시할 리포트수"""
        return self._page_count

    @property
    def total_count(self):
        """int: 총 건수"""
        return self._total_count

    @property
    def total_page(self):
        """int: 총 페이지수"""
        return self._total_page

    @property
    def report_list(self):
        """list of Report: 검색된 리포트 리스트"""
        return self._report_list

    def pop(self, index=-1):
        """ 주어진 index 의 리포트를 반환하며, 리스트에서 삭제하는 함수"""
        return self._report_list.pop(index)

    def __len__(self):
        return len(self._report_list)


def get_corp_code() -> list:
    """ DART에 등록되어있는 공시대상회사의 고유번호,회사명,대표자명,종목코드, 최근변경일자 다운로드

    Returns
    -------
    OrderedDict
        고유번호 및 회사 정보
    """
    url = 'https://opendart.fss.or.kr/api/corpCode.xml'
    # Set API KEY
    api_key = get_api_key()
    payload = {'crtfc_key': api_key}

    # Request Download
    file_url = request.download(url=url, payload=payload)
    
    data = read_file_from_zip(file_url, 'CORPCODE.xml')
    if len(data) == 0:
        raise FileNotFoundError('CORPCODE.xml Not Found')
    return data['result']['list']


def get_corp_info(corp_code: str):
    """ 기업 개황 조회

    Parameters
    ----------
    corp_code: str
        공시대상회사의 고유번호(8자리)

    Returns
    -------
    dict
        기업 개황
    """
    path = '/api/company.json'

    return api_request(path=path, corp_code=corp_code)


def get_executive_holders(corp_code: str) -> dict:
    """ 
    임원ㆍ주요주주특정증권등 소유상황보고서 내에 임원ㆍ주요주주 소유보고 
    정보를 제공합니다.

    Parameters
    ----------
    corp_code: str
        공시대상회사의 고유번호(8자리)※ 개발가이드 > 공시정보 > 고유번호 참고
    api_key: str, optional
        DART_API_KEY, 만약 환경설정 DART_API_KEY를 설정한 경우 제공하지 않아도 됨
    Returns
    -------
    dict
        임원ㆍ주요주주 소유보고
    """

    path = '/api/elestock.json'

    return api_request(
        path=path,
        corp_code=corp_code,
    )


def get_major_holder_changes(
    corp_code: str,
) -> dict:
    """ 주식등의 대량보유상황보고서 내에 대량보유 상황보고 정보를 제공합니다.

    Parameters
    ----------
    corp_code: str
        공시대상회사의 고유번호(8자리)※ 개발가이드 > 공시정보 > 고유번호 참고
    api_key: str, optional
        DART_API_KEY, 만약 환경설정 DART_API_KEY를 설정한 경우 제공하지 않아도 됨
    Returns
    -------
    dict
        대량보유 상황보고
    """

    path = '/api/majorstock.json'

    return api_request(
        path=path,
        corp_code=corp_code,
    )


def disclosure_list(
    krx_corp: KrxCorp,
    start_time: str = None,
    end_time: str = None,
    last_reprt_at: Literal['N', 'Y'] = 'N',
    pblntf_ty: str = None,
    pblntf_detail_ty: str = None,
    sort: Literal['date', 'rpt', 'crp'] = 'date',
    sort_mth: Literal['desc', 'asc'] = 'desc',
    page_no: int = 1,
    page_count: int = 10
) -> SearchResult:
    """ 
    개발가이드 -> 공시정보 -> 공시 검색
    Parameters
    ----------
    start_time: str, optional
        검색시작 접수일자(YYYYMMDD), 없으면 종료일(end_de)
    end_time: str, optional
        검색종료 접수일자(YYYYMMDD), 없으면 당일
    last_reprt_at: str, optional
        최종보고서만 검색여부(Y or N), default : N
    pblntf_ty: see report_type.py
    pblntf_detail_ty: see report_type.py
    sort: str, optional
        정렬, {접수일자: date, 회사명: crp, 고서명: rpt}
    sort_mth: str, optional
        오름차순(asc), 내림차순(desc), default : desc
    page_no: int, optional
        페이지 번호(1~n) default : 1
    page_count: int, optional
        페이지당 건수(1~100) 기본값 : 10, default : 100

    Returns
    -------
    dict
        Response data
    """
    url = 'https://opendart.fss.or.kr/api/list.json'

    api_key = get_api_key()

    payload = {
        'crtfc_key': api_key,
        'corp_code': krx_corp.corp_code,
        'bgn_de': start_time,
        'end_de': end_time,
        'last_reprt_at': last_reprt_at,
        'pblntf_ty': pblntf_ty,
        'pblntf_detail_ty': pblntf_detail_ty,
        'corp_cls': krx_corp.short_market_type,
        'sort': sort,
        'sort_mth': sort_mth,
        'page_no': page_no,
        'page_count': page_count
    }

    resp = request.get(url=url, payload=payload)
    dataset = resp.json()
    check_status(**dataset)
    return SearchResult(dataset)


def fnltt_singl_acnt(
    corp_code: str,
    bsns_year: str,
    reprt_code: str
) -> dict:
    """
    상장법인(금융업 제외)이 제출한 정기보고서 내에 XBRL재무제표의 주요계정과목(재무상태표, 손익계산서)을 제공합니다.
    Parameters
    ----------
    corp_code: str
        공시대상회사의 고유번호(8자리)※ 개발가이드 > 공시정보 > 고유번호 참고
    bsns_year: str
        사업연도(4자리) ※ 2015년 이후 부터 정보제공
    reprt_code: str
        1분기보고서:11013, 반기보고서:11012, 3분기보고서:11014, 사업보고서 : 11011
    api_key: str, optional
        DART_API_KEY, 만약 환경설정 DART_API_KEY를 설정한 경우 제공하지 않아도 됨
    Returns
    -------
    dict
        단일회사 주요계정
    """

    return api_request(
        path='/api/fnlttSinglAcnt.json',
        corp_code=corp_code,
        bsns_year=bsns_year,
        reprt_code=reprt_code,
    )


def fnltt_singl_acnt_all(
    corp_code: str,
    bsns_year: str,
    reprt_code: str,
    fs_div: Literal['CFS', 'OFS']
) -> dict:
    """ 
    상장법인(금융업 제외)이 제출한 정기보고서 내에 XBRL재무제표의 모든계정과목을 제공합니다.
    Parameters
    ----------
    corp_code: str
        공시대상회사의 고유번호(8자리)※ 개발가이드 > 공시정보 > 고유번호 참고
    bsns_year: str
        사업연도(4자리) ※ 2015년 이후 부터 정보제공
    reprt_code: str
        1분기보고서:11013, 반기보고서:11012, 3분기보고서:11014, 사업보고서 : 11011
    Returns
    -------
    dict
        단일회사 주요계정
    """
    return api_request(
        path='/api/fnlttSinglAcntAll.json',
        corp_code=corp_code,
        bsns_year=bsns_year,
        reprt_code=reprt_code,
        fs_div=fs_div
    )
