- efficient code?
  - fast
  - small memory

## Foundations for efficiencies
- Building with built-in
  - built-in type : `list`, `tuple`, `set`, `dict` ...
  - built-in function , module
    - `range`, `enumerate`, `map`
  
```python
# Create a range object that goes from 0 to 5
nums = range(0,5)
print(type(nums))

# Convert nums to a list
nums_list = list(nums)
print(nums_list)

# Create a new list of odd numbers from 1 to 11 by unpacking a range object
nums_list2 = [*range(1,11,2)]
print(nums_list2)

# Rewrite the for loop to use enumerate
indexed_names = []
for i,name in enumerate(names):
    index_name = (i,name)
    indexed_names.append(index_name) 
print(indexed_names)

# Rewrite the above for loop using list comprehension
indexed_names_comp = [(i,name) for i,name in enumerate(names)]
print(indexed_names_comp)

# Unpack an enumerate object with a starting index of one
indexed_names_unpack = [*enumerate(names, 1)]
print(indexed_names_unpack)

# Use map to apply str.upper to each element in names
names_map  = map(str.upper, names)

# Print the type of the names_map
print(type(names_map))

# Unpack names_map into a list
names_uppercase = [*names_map]

# Print the list created above
print(names_uppercase)
```
- the power of numpy arrays
  - homogeneity : array에 모두 같은 type만 가능
  - broadcasting
  - indexing : 특히 차원이 높아지면 유용
  - boolean indexing

## Timing and profiling code
- examining runtime
  - IPython에서 사용하는 경우
    - `%timeit` : 한 줄 단위 측정
    - `%%timeit` : cell 단위 측정

- code profiling for runtime
  - `line_profiler` 패키지 이용

```python
# IPython
%load_ext line_profiler
%lprun -f 함수이름 함수실행
```

- code profiling for memory usage
  - `memory_profiler`

```python
# IPython
%load_ext memory_profiler
%mprun -f 함수이름 함수실행
```

## Gaining efficiencies
- combining, counting, iterating
  - `zip` 함수
  - `collections` 모듈
  - `itertools` 모듈
- Set
  - `intersection()`, `difference()`, `symmetric_difference()`, `union()`
  - `in`
  - 위의 연산들이 속도가 빠른편이니 필요할 때 잘 이용하자
- Eliminating loops
  - built-in, numpy 를 이용하여 loop 계산을 최대한 없애자

## Basic pandas optimizations
- `.iterrows()`

```python
# Print the row
for i, row in pit_df.iterrows():
    print(row)
```

- `.itertuples()`
  - 특이하게 `[]` 으로 indexing이 불가
```python
# Loop over the DataFrame and print each row's Index, Year and Wins (W)
for row in rangers_df.itertuples():
  i = row.Index
  year = row.Year
  wins = row.W
  print(i, year, wins)
```
- pandas alternative to looping
  - `.apply()`
  - 빠르다

```python
# Gather total runs scored in all games per year
total_runs_scored = rays_df[['RS', 'RA']].apply(lambda x : x.sum(), axis=1)
print(total_runs_scored)
```
- optimal pandas iterating
  - pandas는 numpy를 기반으로 만들어짐
  - 따라서 이를 이용하면 좋다
  - `.values` 이용