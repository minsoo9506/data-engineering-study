import pytest
from mycode.calculate import sum

class TestSum:
    def test_return_int(self):
        expected = 10
        actual = sum(5,5)
        message = f'Expected {expected}! But got {actual}'  
        assert  actual == expected, message