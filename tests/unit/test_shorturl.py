from shorty.shorturl import bitly, tinyURL
from multidict import MultiDict
from shorty.helper import getQueryParameters, getEnvVars


def test_getEnvVars():
    token, groupguid = getEnvVars(TOKEN='BITLY_TOKEN', GROUPGUID='GROUPGUID')

    assert groupguid is not None
    assert token is not None


def test_getQueryParameters():
    t = MultiDict([('provider', 'tinyurl'), ('url', 'https://validurl.com')])
    assert getQueryParameters(t) == ('https://validurl.com', 'tinyurl')


def test_bitly():
    correctURL = bitly('https://test.com')

    assert correctURL[0]['link'] == 'https://bit.ly/3nwhmWl'


def test_tinyURL():

    correctURL = tinyURL('https://test.com')

    assert correctURL[0]['link'] == 'https://tinyurl.com/2k6mt2'
