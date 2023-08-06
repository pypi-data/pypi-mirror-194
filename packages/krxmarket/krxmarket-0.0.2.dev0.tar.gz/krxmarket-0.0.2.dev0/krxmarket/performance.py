import logging
from datetime import datetime
from krxmarket import fnltt_singl_acnt_all


LOGGER = logging.getLogger(__name__)


def _fv(item: dict, key: str):
    value = item.get(key)
    return value


def get_performance(corp_code: str, start_year: int) -> list:
    """
    json structure
    [
        {
            'year': '2016',
            'quarter': 1,
            'apx_ms': xxxxxxxx
            data: {
                CF: [
                    {},
                    {}
                ],
                IS: {
                
                }
            }
        }
    ]
    """
    year = start_year
    current_year = datetime.now().year
    # 1분기보고서:11013, 반기보고서:11012, 3분기보고서:11014, 사업보고서 : 11011
    report_seq = ['11013', '11012', '11014', '11011']
    report_all = []

    while year <= current_year:
        for i, seq in enumerate(report_seq):
            result = {
                'year': str(year),
                'quarter': str(i + 1),
                'data': {}
            }
            try:
                report = fnltt_singl_acnt_all(corp_code, str(year), seq, 'CFS')
                if report['status'] == '000' and 'list' in report:
                    items = _fv(report, 'list')
                    for item in items:
                        sj_div = _fv(item, 'sj_div')
                        if sj_div not in result['data']:
                            result['data'][sj_div] = []
                        
                        result['data'][sj_div].append({
                            'account_nm': _fv(item, 'account_nm'),
                            'frmtrm_amount': _fv(item, 'frmtrm_amount'),
                            'thstrm_amount': _fv(item, 'thstrm_amount'),
                            'account_id': _fv(item, 'account_id'),
                            'rcept_no': _fv(item, 'rcept_no')
                        })
            except Exception as ex:
                LOGGER.warning('skip %d, quarter: %d, %s',
                               year, i + 1, str(ex))
                continue
                
            report_all.append(result)
        year += 1

    return report_all


if __name__ == '__main__':
    json_content = get_performance('00126380', 2022)
    import json
    with open('data.json', 'w') as f:
        json.dump(json_content, f)

