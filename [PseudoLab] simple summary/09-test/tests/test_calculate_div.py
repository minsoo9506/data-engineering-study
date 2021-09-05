from mycode.calculate import div
import pytest

class TestSum:
    def test_return_int(self):
        expected = 2
        actual = div(10,5)
        message = f'Expected {expected}! But got {actual}'  
        assert  actual == expected, message

class TestSumXfail:
    @pytest.mark.xfail(reason="For xfail Test!")
    def test_return_int(self):
        expected = 3
        actual = div(10,5)
        message = f'Expected {expected}! But got {actual}'  
        assert  actual == expected, message