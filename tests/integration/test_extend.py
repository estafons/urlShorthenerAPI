
def test_extendability(testExtendability):
    assert testExtendability.status_code == 200
    assert "dummy" in testExtendability.text
