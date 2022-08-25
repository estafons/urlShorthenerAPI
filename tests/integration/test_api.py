
def test_good_bitly(goodURLBitly):
    assert goodURLBitly.status_code == 200


def test_bad_bitly(badURLBitly):
    assert badURLBitly.status_code == 400


def test_good_tiny(goodURLTiny):
    assert goodURLTiny.status_code == 200


def test_bad_tiny(badURLTiny):
    assert badURLTiny.status_code == 400


def test_get(testGET):
    assert testGET.status_code == 405


def test_defaultprovider(testDefaultProvider):
    assert testDefaultProvider.status_code == 200
    assert 'bit.ly' in testDefaultProvider.text


def test_InvalidProvider(testInvalidProvider):
    assert testInvalidProvider.status_code == 400


def test_NoURL(testNoUrl):
    assert testNoUrl.status_code == 400


def test_thirdPartyFail(testThirdPartyDown):
    assert testThirdPartyDown.status_code == 502


def test_internalServerError(testBadRequestToThirdParty):
    assert testBadRequestToThirdParty.status_code == 500
