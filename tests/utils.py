import _setup

import os

from email import message_from_file

import httplib2

from github2.request import charset_from_headers


HTTP_DATA_DIR = "tests/data/"

ORIG_HTTP_OBJECT = httplib2.Http


class HttpMock(object):
    """Simple Http mock that returns saved entries

    Implementation tests should never span network boundaries
    """

    def __init__(self, cache=None, timeout=None, proxy_info=None):
        pass

    def request(self, uri, method='GET', body=None, headers=None,
                redirections=5, connection_type=None):
        file = os.path.join(HTTP_DATA_DIR, httplib2.safename(uri))
        if os.path.exists(file):
            response = message_from_file(open(file))
            headers = httplib2.Response(response)
            body = response.get_payload().encode(charset_from_headers(headers))
            return (headers, body)
        else:
            return (httplib2.Response({"status": "404"}),
                    "Resource %r unavailable from test data store" % file)


def set_http_mock():
    httplib2.Http = HttpMock


def unset_http_mock():
    httplib2.Http = ORIG_HTTP_OBJECT
