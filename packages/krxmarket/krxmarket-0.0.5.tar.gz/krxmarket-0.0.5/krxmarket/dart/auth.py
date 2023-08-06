import os


def get_api_key():
    api_key = os.getenv('DART_API_KEY')
    if api_key is None:
        raise ValueError('no dart api key')
    return api_key
