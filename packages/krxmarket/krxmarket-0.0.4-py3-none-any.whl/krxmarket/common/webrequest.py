# -*- coding: utf-8 -*-
import re
import requests
from time import sleep
from fake_useragent import UserAgent
import datetime
import functools
import tempfile
from urllib.parse import unquote
import os


# Default Time-To-Live
CACHE_DEFAULT_TTL = datetime.timedelta(hours=1)


def cache(ttl=CACHE_DEFAULT_TTL):
    """ TTL Cache Decorator

    Parameters
    ----------
    ttl: datetime.timedelta
        Time-To-Live

    Returns
    -------
    function
        Wrapped Function
    """
    def wrap(func):
        cached = {}

        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            now = datetime.datetime.now()
            # see lru_cache for fancier alternatives
            key = tuple(args), frozenset(kwargs.items())
            if key not in cached or now - cached[key][0] > ttl:
                value = func(*args, **kwargs)
                cached[key] = (now, value)
            return cached[key][1]
        return wrapped
    return wrap


@cache()
def get_user_agent():
    """ Return user-agent
    Returns
    -------
    str
        user-agent
    """
    ua = UserAgent()
    agent = ua.chrome
    return str(agent)


def query_to_regex(query):
    """ query to regular expression

    Parameters
    ----------
    query: str or list of str
        query

    Returns
    -------
    Pattern object
        regular expression
    """
    if isinstance(query, str):
        regex = re.compile(query, re.IGNORECASE)
    elif isinstance(query, list):
        pattern = '(' + '|'.join(query) + ')'
        regex = re.compile(pattern, re.IGNORECASE)
    else:
        raise TypeError('Invalid query type')
    return regex


class Request(object):
    """HTTP 요청을 보내는 클래스

    HTTP 요청을 위해 사용되는 클래스입니다.
    User-Agent 및 Cookies 관련 정보를 저장하고 있습니다.

    Attributes
    ---------
    s: Session
        Requests Session
    delay: float
        Delay for repeat delay, Default: 1s

    """
    def __init__(self):
        self.s = requests.Session()
        self.update_user_agent()
        # 분당 1000회 이상 자체적으로 24시간 IP차단
        # IP 차단 방지 위해 delay 0.1s -> 0.2s
        self.delay = 0.2

    def update_user_agent(self, force: bool = False):
        """ Update User-Agent

        Parameters
        ----------
        force: bool
            Force update
        """
        if force:
            ua = UserAgent()
            agent = ua.chrome
            user_agent = str(agent)
        else:
            user_agent = get_user_agent()
        self.s.headers.update({'user-agent': user_agent})

    def set_proxies(self, proxies: dict = None):
        """ Set proxies

        Parameters
        ----------
        proxies: dict
            proxies
        """
        if proxies is not None:
            import copy
            self.s.proxies = copy.deepcopy(proxies)

    def set_delay(self, second: float = None):
        """ Set delay

        Parameters
        ----------
        second: float
            delay for repeat
        """
        self.delay = second

    def request(self,
                url: str,
                method: str = 'GET',
                payload: dict = None,
                referer: str = None,
                stream: bool = False,
                timeout: int = 120):
        """ send http requests

        Parameters
        ----------
        url: str
            URL
        method: str, optional
            GET, OPTIONS, POST, PUT, PATCH or DELETE
        payload: dict, optional
            Request parameters
        referer: str, optional
            Temporary referer
        stream: bool, optional
            Stream optional, default False
        timeout: int, optional
            default 120s

        Returns
        -------
        requests.Response
            Response
        """
        headers = self.s.headers
        if referer is not None:
            headers['referer'] = referer

        """
        noqa: E501
        Session-level state such as cookies will not get 
        applied to your request.
        To get a PreparedRequest with that state applied,
        replace the call to Request.prepare() with
          a call to Session.prepare_request()
        """
        req = requests.Request(
            method,
            url=url,
            params=payload,
            headers=headers
        )
        prepped = self.s.prepare_request(req)
        resp = self.s.send(prepped, stream=stream, timeout=timeout)
        if self.delay is not None:
            sleep(self.delay)
        return resp

    def get(self, url: str,
            payload: dict = None,
            referer: str = None,
            stream: bool = False,
            timeout: int = 120):
        """
        request get method
        """
        return self.request(
            url=url,
            method='GET',
            payload=payload,
            referer=referer,
            stream=stream,
            timeout=timeout
        )

    def post(self, url: str,
             payload: dict = None,
             referer: str = None,
             stream: bool = False,
             timeout: int = 120):
        """ 
        request post method
        """
        return self.request(
            url=url,
            method='POST',
            payload=payload,
            referer=referer,
            stream=stream,
            timeout=timeout
        )

    def download(self,
                 url: str,
                 method: str = 'GET',
                 payload: dict = None,
                 referer: str = None,
                 timeout: int = 120) -> dict:
        """
        Download file from url and return file uri
        """
        r = self.request(
            url=url, method=method, payload=payload,
            referer=referer, stream=True, timeout=timeout)

        # Check validity
        headers = r.headers.get('Content-Disposition')
        if headers is None or not re.search('attachment', headers):
            raise FileNotFoundError('target does not exist')

        block_size = 8192

        # Extract filename
        extracted_filename = unquote(
            re.findall(r'filename="?([^"]*)"?', headers)[0]
        )
        temp_dir = tempfile.mkdtemp()
        file_path = os.path.join(temp_dir, extracted_filename)
        
        with open(file_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=block_size):
                if chunk is not None:
                    f.write(chunk)
        r.close()
        return file_path


# Request object
request = Request()
