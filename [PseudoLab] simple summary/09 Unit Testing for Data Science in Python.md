## Unit testing basics
### Why unit test?
- 당연히 필요한 과정~
- manually testing보다 훨씬 빠르다.

### pytest
- 함수이름을 `test_`로 해야한다.
- `assert` 사용
- `pytest test함수가있는파일.py` 하면 된다.

```python
import pytest
from process import convert_to_int

def test_on_string_with_one_comma():
  # Complete the assert statement
  assert convert_to_int("2,081") == 2081
```

## Intermediate unit testing
### assert
- 기본은 `assert boolean_expression`인데 `assert boolean_expression, message`처럼 원하는 message를 에러발생시 보이게 할 수 있다.
- float같은 경우 오차가 있으니 `==`보다는 `== pytest.approx(원하는float)` 을 사용하자.

### Testing for exceptions instead of return values
- exception 자체를 테스트한다.
- `with`문과 `pytest.raises()`를 이용

```python
import numpy as np
import pytest
from train import split_into_training_and_testing_sets

def test_on_one_row():
    test_argument = np.array([[1382.0, 390167.0]])
    # ValueError 메세지를 exc_info에 저장
    with pytest.raises(ValueError) as exc_info:
      split_into_training_and_testing_sets(test_argument)
    expected_error_msg = "Argument data_array must have at least 2 rows, it actually has just 1"
    # Check if the raised ValueError contains the correct message
    exc_info.match(expected_error_msg)
```

### well tested function
- test를 할 때, 얼마나 해야할까
  - Bad, Special, Normal argument!
- Bad argument
  - 함수가 exception을 만드는 값
- Special argument
  - Boundary value, Special logic
- Normal argument
  - 그냥 정상적인 argement

### Test Driven Development (TDD)
- 해당 코드를 완성하기 전에 unit test 작성해라!

## Test organization and Execution
### How to organize a growing set of tests?
- 개발하고 있는 python module과 매칭이 되도록 test module을 만든다.
  - `my_module.py` & `test_my_module.py`
- test module안데 여러 개의 test 함수를 만들면 된다.
- class를 만드는 방법도 있다. 
  - `class TestSomething` : camel, `Test`로 시작

```python
import pytest 
from data.preprocessing_helpers  import row_to_list, convert_to_int
class TestRowToList(object):# Always put the argument object
  def test_on_no_tab_no_missing_value(self):# Always put the argument self        
    ...
  deftest_on_two_tabs_no_missing_value(self):# Always put the argument self       
    ...
class TestConvertToInt(object):# Test class for convert_to_int()
  def test_with_no_comma(self):# A test for convert_to_int() 
    ...
```

### Mastering test execution
- 한번에 test할 수도 있다.
  - test module이 있는 폴더에 가서 `pytest`만 명령어로 치면 된다.
  - `test_`로 시작하는 file -> `Test`로 시작하는 class -> `test_`로 시작하는 함수
- `pytest -x` : 하나라고 실패하면 거기서 멈춤
- node ID를 이용하여 특정한 test만 실행하기
  - test class : `[path to test module]::[test class name]`
  - unit test : `[path to test module]::[test class name]::[unit test name]`
- `-k` option
  - `-k` 뒤에 적은 단어가 들어가는 경우 test
  - `pytest -k TestTrain` : class중에 `TestTrain`으로 시작하는 class들 test하겠구나!

### Expected failures and conditional skipping
- TDD에서 배웠듯이 아직 코드가 완성하기 전에 test코드를 작성하기로 한다. 그러면 당연히 fail이 발생할 것이다. 이를 CI/CD로 자동화했다면 문제가 발생할 수 있다. 즉, fail이 발생하는 것이 맞다는 것을 notice할 필요가 있는 것이다.
  - 이는 `@pytest.mark.xfail` 데코레이터를 이용한다.
- 특정 조건에서 test를 skip하고 싶은 경우
  - `@pytest.mark.skipif(boolean_expression)`을 이용한다. `boolean_expression`이 true이면 skip한다.
- 둘다 reason으로 이유도 적을 수 있다.
  - 그러면 `pytest -r[찾고 싶은 상황에 들어간 아무 글자]`를 통해 이유를 확인 할 수도 있다.
  - `pytest -rx` : xfail 이유를 보여준다.

### Continuous intergration and code coverage
- Travis
  - 1. create `.travis.yml`
  - 2. push the file to GitHub
  - 3. Install the Travis CI app
- Codecov
  - 1. `.travis.yml`를 추가수정

## Testing Models, Plots and Much More
### setup and teardown
- test를 진행하려고 할 때, 임시의 데이터를 만들고 (set up) 이를 함수 test에 이용한 뒤에 없애버리는 과정 (tear down)이 필요하다.
- setup -> test -> teardown
  - `@pytext.fixture` 이용

```python
# Add a decorator to make this function a fixture
@pytest.fixture
def clean_data_file():
    file_path = "clean_data_file.txt"
    with open(file_path, "w") as f:
        f.write("201\t305671\n7892\t298140\n501\t738293\n")
    yield file_path
    os.remove(file_path)
    
# Pass the correct argument so that the test can use the fixture
def test_on_clean_file(clean_data_file):
    expected = np.array([[201.0, 305671.0], [7892.0, 298140.0], [501.0, 738293.0]])
    # Pass the clean data file path yielded by the fixture as the first argument
    actual = get_data_as_numpy_array(clean_data_file, 2)
    assert actual == pytest.approx(expected), "Expected: {0}, Actual: {1}".format(expected, actual) 
```

### Mocking
- test할 때 함수끼리 dependency를 없애주는 것
- 강의 참고

### Testing models
- model에서 test하고 싶은 부분을 이전까지 해왔던것처럼 진행하면 된다.

### Testing plots
- `pytest-mpl`
  - 따로 설치해야함
  - baseline image와 비교해서 잘 나왔는지 test