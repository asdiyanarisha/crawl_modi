import requests
from lib import log

logger = log.get_logger("http_request.core")

default_headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:94.0) Gecko/20100101 Firefox/94.0'
}


def html_post(url, payload=None, headers=None, proxy=None):
    # if set none, use default headers
    if headers is None:
        headers = default_headers
    try:
        if proxy:
            proxy = {"https": proxy}
            r = requests.post(url, data=payload, headers=headers, proxies=proxy, timeout=30)
        else:
            r = requests.post(url, data=payload,  headers=headers, timeout=30)
        return r.content

    except requests.exceptions.HTTPError:
        logger.error("Http error")
    except requests.exceptions.ConnectionError:
        logger.error("Connection error {}".format(url))
        return html_conn_err()
    except requests.exceptions.Timeout:
        logger.error("Request timeout {}".format(url))
        return html_timeout()
    except requests.exceptions.RequestException:
        logger.error("Something else error")


def html_get(url, payload=None, headers=None, proxy=None):
    # if set none, use default headers
    if headers is None:
        headers = default_headers
    try:
        if proxy:
            proxy = {"https": proxy}
            r = requests.get(url, data=payload, headers=headers, proxies=proxy, timeout=30)
        else:
            r = requests.get(url, data=payload,  headers=headers, timeout=30)
        return r.content

    except requests.exceptions.HTTPError:
        logger.error("Http error")
    except requests.exceptions.ConnectionError:
        logger.error("Connection error {}".format(url))
        return html_conn_err()
    except requests.exceptions.Timeout:
        logger.error("Request timeout {}".format(url))
        return html_timeout()
    except requests.exceptions.RequestException:
        logger.error("Something else error")


def html_conn_err():
    return """<html><head><title>Netray Tag</title></head><body><h1>Connection Error</h1></body></html>"""


def html_timeout():
    return """<html><head><title>Netray Tag</title></head><body><h1>Request Timeout</h1></body></html>"""
