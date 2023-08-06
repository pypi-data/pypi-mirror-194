import execjs
from urllib import request, parse


def query_encode(query: str) -> str:
    """
    :param query:
    :return:
    """
    if isinstance(query, str):
        return parse.quote(query)
    raise f"query is not string!"


def get_x96(token, search_api):
    with open('./KnowAlmost/static/x-zse-96.js', 'r', encoding='utf-8') as f:
        js = f.read()
    etx = execjs.compile(js)
    return etx.call('get_xzse96', token, search_api)
