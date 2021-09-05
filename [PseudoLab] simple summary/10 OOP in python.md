## OOP Fundamentals
### OOP?
- 단순히 순차적으로 사고를 하기에는 복잡한 상황이 많고 중복되는 패턴이 많다.
- 그래서 OOP가 필요하다!
  - object들끼리의 연관성
  - framework, tool 을 만들기에 좋다
  - maintainable, reusable code
- Object as data structure
  - Object = state + behavior
- Class as blueprint
- Object in python
  - python에서는 모든 것이 object!
  - state -> attribute
  - behavior -> method
  - `dir(object)`로 모든 attribute, method 볼 수 있다.
### Class anatomy: attributes and methods
- class 만들기

```python
class Introduce: # 이름은 CamelCase로 쓴다
    def get_name(self, name):
        self.name = name
    def identify(self):
        print(f'I am {self.name}')

me = Introduce()
me.identify('minsoo')
print(me.name)
```
- `self` : stand-in for a particular object used in class definition
  - class 정의하는 코드에서만 있고 object를 만들때는 안 보인다.
  - 위에서 `me.identify('minsoo')`는 `Introduce.identify(me, 'minsoo')`라고 이해할 수 있다.
  - method의 첫번째 argument이기도 하고 attribute를 만들때 앞에 붙여야 한다.
### Class anatomy: the `__init__` constructor
- Constructor `__init__()` method를 통해 object를 만들때, attribute들을 만들자.
- default 값을 지정할 수도 있다.

```python
class Introduce:
    def __init__(self, name='minsoo', age=27):
        self.name = name
        self.age = age
```

## Inheritance and Polymorphism
- core principle of oop
  - Inheritance : extending functionality of existing code
  - Polymorphism : creating a unified interface
  - Encapsulation : bundling of data and methods
### Instance, class data
- class data
  - instance마다 data가 아니라 'global variable' in class가 필요한 경우가 존재한다.
  - 이런 경우 `self`를 사용하지 않고 그냥 변수를 사용하면 된다.
  - instance에서도 불러올수 있다. 다만 이 경우 instance로 class data를 불러서 수정하면 해당 instance가 불러오는 class data만 값이 바뀐다. 즉, class data 사용 의미가 없다. 쓸 필요가 없다는 것!
  - 근데 class data를 수정하면 모든 instance의 class data가 수정된다.

```python
class Player:
    MAX_POSITION = 10
    
    def __init__(self):
        self.position = 0

    def move(self, steps):
        if self.position + steps < Player.MAX_POSITION:
            self.position += steps
        else:
            self.position = Player.MAX_POSITION
```

- class method
  - class를 통해 이용가능한 method (instance에서는 불가)
  - `@classmethod`를 해당 method에 붙이고 `cls`를 첫번째 argument로 사용
  - 그리고 return할 때 `cls()`를 사용하면 `__init__()`을 호출한 것과 동일한 기능을 한다.

```python
class BetterDate:    
    def __init__(self, year, month, day):
      self.year, self.month, self.day = year, month, day
    
    @classmethod
    def from_str(cls, datestr):
        parts = datestr.split("-")
        year, month, day = int(parts[0]), int(parts[1]), int(parts[2])
        return cls(year, month, day)

bd = BetterDate.from_str('2020-04-30') 
```

### class inheritance
- 코드를 재사용 할 때 유용하겠다.
- `isinstance(instance이름, class이름)`를 통해 해당 class로 만들어졌는지 확인이 가능하다. 상속받은 class(parent)_도 True로 나온다.
- 상속은 `class child(parent)` 처럼 하면 된다.
- parent의 변수, 함수 그대로 사용할 수 있고 수정해서 사용할 수도 있다.
- customizing constructor
  - `__init__()` 함수에 `Parent이름.__init__(self, args..)`으로 먼저 parent class의 constructor를 부르고 추가 내용을 작성하면 된다. (필수는 아님)
- customizing functionality
  - parent class의 method를 사용해서 덮어써도 되고 아예 새로 덮어써도 된다.

```python
class Employee:
    def __init__(self, name, salary=30000):
        self.name = name
        self.salary = salary

    def give_raise(self, amount):
        self.salary += amount
       
class Manager(Employee):
    def display(self):
        print("Manager ", self.name)

    def __init__(self, name, salary=50000, project=None):
        Employee.__init__(self, name, salary)
        self.project = project

    def give_raise(self, amount, bonus=1.05):
        Employee.give_raise(self, amount * bonus)
```

## Integrating with Standard Python
### Operator overloading : comparision
- `__eq__()`
  - `==`을 사용할때 불려진다.
  - 같은 class에서 만들어진 instance들의 변수들이 같은 값을 갖고 있어도 `==`으로 비교하면 무조건 `False`가 나온다.
  - 그런데 instance의 변수가 같은 경우에 둘이 같다고 하고 싶은 경우 (또는 원하는 조건 아무거나) `def __eq__(self, arg~)`로 overloading하면 된다.
### Operator overloading : string representation
- `__str__()` vs `__repr__()`
  - `__str__()` 
    - `print(obj)`, `str(obj)`
    - informal, for end user
    - string representation
  - `__repr__()`
    - `repr(obj)`
    - formal, for developer
    - reproducible representation
- 둘 다 `print(instance이름)` 했을 때, 나오는 결과를 정할 수 있다.
### Exception
- `try` - `except` - `finally`
  - `except`는 여러 개 쓸 수 있다.
  - `finally`는 optional
- `Exception`을 상속받아서 원하는 custom exception을 만들 수 ㅣ있다.
## Best Practices of Class Design
### Designing for inheritance and polymorphism
- *Base class should be interchangeable with any of its subclasses without altering any properties of the program*
### Managing data acsess
- python에서 모든 class data는 public이다.
- restricting access
  - Naming convention
  - use `@property` to customize access
  - overriding `__getattr__()` and `__setattr__()`
- Naming convention
  - `_`으로 시작하면 class 내부에서만 쓰이는 것으로 약속!
  - `__`으로 시작하면 private, not inherited
- Properties
  - attribute를 바꿀때 직접 바꾸는 것보다 함수를 통해 바꾸는 것이 안전하다. attribute를 read only만 가능하게 하는게 좋다.

```python
class Person:
  def __init__(self, name, salary):
    self._salary = salary

  @property
  def salary(self):
    return self._salary

  @salary.setter
  def salary(self, new_salary):
    if new_salary < 0:
      raise ValueError("Salary is too small!")
    self._salary = new_salary
```
- 일단 보호할 attribute를 `_`을 붙인다.
- attribute와 동일한 이름의 method를 만들고 `@property`를 붙인다. 해당 attribute를 instance가 read할 때 사용된다.
-  attribute와 동일한 이름의 method를 만들고 `@attr.setter`를 붙인다. 해당 attribute를 수정할 때 사용되는 것이다. 예시처럼 조건을 걸어 안전하게 수정할 수 있다.
`@property`부분은 만들고 setter함수를 안만들면 read only만 가능하다.