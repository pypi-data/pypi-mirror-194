import aiohttp
import pytz
from datetime import datetime
import os


# 10년치 데이터 종목당 180포인트 소모

cols1 = [
    'M111000',
    'M111100',
    'M111600',
    'M113000',
    'M113100',
    'M113800',
    'M113900',
    'M113500',
    'M115000',
    'M115020',
    'M115100',
    'M115500',
    'M115600',
    'M115850',
    'M121000',
    'M121100',
    'M121200',
    'M121300',
    'M121500',
    'M121540',
]

cols2 = [
    'M121550',
    'M121570',
    'M121580',
    'M122100',
    'M122500',
    'M122700',
    'M122710',
    'M122720',
    'M131000',
    'M132020',
    'M131025',
    'M132000',
    'M132010',
    'M133000',
    'M134000',
    'M134010',
    'M123500',
    'M123600',
    'M123900',
    'M123955',
]


async def get_performance(code, is_quarter: bool = True):
    """
    https://www.fnspace.com/Api/FinanceApi?key=sample&format=json&code=A005930&item='M111000',
    조회결과
    {
        key: string,
        format: string, (json / xml)
        success: string, (true / false),
        errcd: string, (성공일 경우""),
        errmsg: string,
        code: string,
        item: string,
        consolgb: string,
        annualgb: string,
        accdategb: string,
        fraccyear: string,
        toaccyear: string,
        dataset: object {
            CODE: string,
            NAME: string,
            DATA: object {
                DATE: string, # ex) 201509
                YYMM: string, # 결산 년월
                FS_YEAR: string, # 회계 년
                FS_MONTH: string, # 회계 월
                FS_QTR: string, # 회계 구분 ex) 3Q
                MAIN_TERM:string, # 주제무재표 구분 ex: 연결
                'M111000',
                'M111100',
                'M111600',
                ...
            }
        }
    }
    """
    print('fetch from fnguide', code)

    def validate(result):
        return (result is not None and
                'dataset' in result and
                len(result['dataset']) != 0 and
                'DATA' in result['dataset'][0])

    def merge(prev, row):
        data = prev['dataset'][0]['DATA']
        for prev_row in data:
            if (row['FS_YEAR'] == prev_row['FS_YEAR'] and
                    row['FS_MONTH'] == prev_row['FS_MONTH'] and
                    row['FS_QTR'] == prev_row['FS_QTR']):
                for key in row.keys():
                    if key.startswith('M') and key[1:].isnumeric():
                        prev_row[key] = row[key]

    url = 'https://www.fnspace.com/Api/FinanceApi'
    dt = datetime.now().astimezone(pytz.timezone("Asia/Seoul"))
    params = {
        'key': os.getenv('FN_GUIDE_KEY'), 
        'code': code.upper(),
        'format': 'json',
        # 회계기준. 주재무제표(M)/연결(C)/별도(I) - 연결은 자본적 결합회사까지 합산
        'consolgb': 'M',
        # 연간(A)/분기(QQ)/분기누적(QY)
        'annualgb': 'QQ' if is_quarter else 'A',
        # 컨센서스 결산년월 선택 기준. Calendar(C)/Fiscal(F)
        'accdategb': 'C',
        'item': cols1,
        # 조회 시작 결산년월, toaccyear 에서 10년까지만 지원, 현재 년에서 -9
        'fraccyear': dt.year - 9,
        # 조회 종료 결산년월
        'toaccyear': dt.year
    }

    async with aiohttp.ClientSession() as session:
        d = None
        async with session.get(url, params=params) as response:
            # 존재하는 코드이나 값이 없으면, success: 'true' 이나 dataset: []
            if response.status == 200:
                d = await response.json()
        
        if validate(d):
            params['item'] = cols2
            async with session.get(url, params=params) as response:
                # 존재하는 코드이나 값이 없으면, success: 'true' 이나 dataset: []
                if response.status == 200:
                    result = await response.json()
                    if validate(result):
                        data = result['dataset'][0]['DATA']
                        for row in data:
                            merge(d, row)
        else:
            print(code, 'validate failed')
            return None
                            
        if d is not None:
            return d['dataset'][0]['DATA']
        return None
