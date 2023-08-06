#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.gen
from tornado.ioloop import IOLoop
from lycium.asyncrequest import async_get

@tornado.gen.coroutine
def test_query_url(url):
    resp_code, resp = yield async_get(url)
    print('query:', url, 'response:', resp)

def test_http_query():
    urls = ['http://127.0.0.1:8081/debug?t=1',
            'http://127.0.0.1:8081/debug?t=2',
            'http://127.0.0.1:8081/debug?t=3',
            'http://127.0.0.1:8081/debug?t=4',
            'http://127.0.0.1:8081/debug?t=5',
            'http://127.0.0.1:8081/debug?t=6',
            'http://127.0.0.1:8081/debug?t=7',
            'http://127.0.0.1:8081/debug?t=8',
            'http://127.0.0.1:8081/debug?t=9',
            'http://127.0.0.1:8081/debug?t=10'
           ]
    reqs = [test_query_url(url) for url in urls]
    @tornado.gen.coroutine
    def test_queries():
        yield reqs
    IOLoop.instance().run_sync(test_queries)

if __name__ == '__main__':
    test_http_query()
