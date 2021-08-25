# Streamlined Data Ingestion with pandas

### Importing data from flat files
- Flat file
  - csv같은 가장 쉽게 볼 수 있는 file
- modifying flat file import
  - limiting columns
    - `usecols` : 불러올때 특정 column을 불러온다
  - limiting rows
    - `nrows` : 원하는 row수 만큼 불러온다
    - `skiprows` : 원하는 row수 만큼 skip하고 불러온다
  - assigning column names
    - `names` : 원하는 이름으로 column지정해서 불러온다
- handling error and missing data
  - specifying data types
    - pandas가 자동으로 알아서 하지만 직접 지정가능
    - `dtype` : dictionary형태로 지정하면 된다
  - customizing missing data values
    - `na_values` : sigle value, list, dictionary 를 통해서 특정 column의 특정 값을 `NA`로 읽게 만들 수 있다
  -  line with error
    - `error_bad_lines=False` : skip unparseable records
    - `warn_bad_line=True` : skip한 records가 무엇인지 알려줌

### Importing data from excel files
- Introduction to spreadsheets
  - spreadsheet : excel file을 의미
  - flat file 과 다른게 formatting, formulas 존재
  - `read_excel()`로 읽기 가능
- getting data from multiple worksheet
  - select sheet to load
    - `read_excel`을 default로 맨 처음 sheet만 불러온다
    - `sheet_name` : 이름이나 index를 넣으면 여러 개의 shhet를 읽을 수 있다
    - `sheet_name=None`하면 한번에 전체 읽을 수 있다
- modifying imports: true/false data
  - `true_values=['Yes']` 이런식으로 하면 `Yes`를 `True`로 바꾼다
  - `false_valus`도 마찬가지
- modifying imports: parsing dates
  - pandas에서는 Datetime을 default로 object로 불러온다
  - `parse_dates`
    - datetime으로 불러오려면 list에 원하는 column들을 넣으면 된다
    - 또한 나누어져있는 column을 합칠 수도 있다
  - `parse_dates`가 잘 안되는 경우 `pd.to_datetime()`을 이용하자
    - datetime으로 만들고자 하는 column의 값들이 `08312021 21:12:10` 같이 일반적이지 않은 경우
    - `df['특정컬럼'] = pd.to_datetime(df['특정컬럼'], format='%m%d%Y %H:%M:%S')` 같은 방법으로 datetime으로 parse할 수 있다.

```python
# 나누어져있는 column을 합칠 수도 있다
datetime_cols = {"Part2Start": ['Part2StartDate','Part2StartTime']}
survey_data = pd.read_excel("fcc_survey_dts.xlsx",
                            parse_dates=datetime_cols)
```

### Importing data from databases
- Relational Database with pandas

```python
# db는 SQLite
# Import sqlalchemy's create_engine() function
import pandas as pd
from sqlalchemy import create_engine
# Create the database engine
engine = create_engine('sqlite:///data.db')
# View the tables in the database
print(engine.table_names())
# import df
df = pd.read_sql('df', engine)
```
- Refining imports with SQL queries

```python
# Create database engine for data.db
engine = create_engine('sqlite:///data.db')
# Write query to get date, tmax, and tmin from weather
query = """
SELECT date, 
       tmax, 
       tmin
  FROM weather;
"""
# Make a data frame by passing query and engine to read_sql()
temperatures = pd.read_sql(query, engine)
# View the resulting data frame
print(temperatures)
```

### Importing JSON data and working with APIs
- JSON
  - collections of objects
  - `read_json()`으로 읽을 수 있다
- API
  - `requests` 이용
- nested json
  - `pandas.io.json`을 이용
    - `json_normalize()`

```python
flat_cafes = json_normalize(data["businesses"],
                            sep="_",
                    		record_path="categories",
                    		meta=['name', 
                                  'alias',  
                                  'rating',
                          		  ['coordinates', 'latitude'], 
                          		  ['coordinates', 'longitude']],
                    		meta_prefix='biz_')
```
- Combining multiple dataset
  - `append`
  - `merge`