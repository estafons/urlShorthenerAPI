import json
import functools
import os
import sys
import pytest
from flask import Flask
from mock import patch
from tests.dummy_funcs import thirdPartyDummyApi

# Set up the path to import from `shorty`.
root = os.path.join(os.path.dirname(__file__))
package = os.path.join(root, '..')
sys.path.insert(0, os.path.abspath(package))

from shorty.app import create_app  # noqa


class TestResponseClass(Flask.response_class):
    @property
    def json(self):
        return json.loads(self.data)


Flask.response_class = TestResponseClass


def humanize_werkzeug_client(client_method):
    """Wraps a `werkzeug` client method (the client provided by `Flask`) to make
    it easier to use in tests.
    """
    @functools.wraps(client_method)
    def wrapper(url, **kwargs):
        # Always set the content type to `application/json`.
        kwargs.setdefault('headers', {}).update({
            'content-type': 'application/json'
        })

        # If data is present then make sure it is json encoded.
        if 'data' in kwargs:
            data = kwargs['data']
            if isinstance(data, dict):
                kwargs['data'] = json.dumps(data)

        kwargs['buffered'] = True

        return client_method(url, **kwargs)

    return wrapper


@pytest.fixture(scope='session', autouse=True)
def app(request):
    app = create_app({
        'TESTING': True
    })

    # Establish an application context before running the tests.
    ctx = app.app_context()
    ctx.push()

    def teardown():
        ctx.pop()

    request.addfinalizer(teardown)
    return app


@pytest.fixture(scope='function')
def client(app, request):
    return app.test_client()


@pytest.fixture(scope='function')
def get(client):
    return humanize_werkzeug_client(client.get)


@pytest.fixture(scope='function')
def goodURLBitly(client):
    return client.post('/shortlinks?url=http://test.to&provider=bitly')


@pytest.fixture(scope='function')
def badURLBitly(client):
    return client.post('/shortlinks?url=test&provider=bitly')


@pytest.fixture(scope='function')
def goodURLTiny(client):
    return client.post('/shortlinks?url=http://test.to&provider=tinyurl')


@pytest.fixture(scope='function')
def badURLTiny(client):
    return client.post('/shortlinks?url=test&provider=tinyurl')


@pytest.fixture(scope='function')
def testGET(client):
    return client.get('/shortlinks?url=http://test.to&provider=bitly')


@pytest.fixture(scope='function')
def testDefaultProvider(client):
    return client.post('/shortlinks?url=http://test.to')


@pytest.fixture(scope='function')
def testNoUrl(client):
    return client.post('/shortlinks?provider=bitly')


@pytest.fixture(scope='function')
def testInvalidProvider(client):
    return client.post('/shortlinks?url=https://test.to&provider=asd')


@pytest.fixture(scope='function')
def testThirdPartyDown(client):
    with patch('shorty.shorturl.tinyURL',
               return_value=('Internal Server Error', 500)), \
            patch('shorty.shorturl.bitly',
                  return_value=('Internal Server Error', 500)):

        return client.post('/shortlinks?url=http://test.to&provider=bitly')


@pytest.fixture(scope='function')
def testBadRequestToThirdParty(client):
    with patch('shorty.shorturl.tinyURL',
               return_value=('Internal Server Error', 400)), \
            patch('shorty.shorturl.bitly',
                  return_value=('Internal Server Error', 500)):

        return client.post('/shortlinks?url=http://test.to&provider=bitly')


@pytest.fixture(scope='function')
def testExtendability(client):
    with patch('shorty.api.providersInterface',
               return_value=({'dummy': thirdPartyDummyApi})):

        return client.post('/shortlinks?url=https://test.to')
