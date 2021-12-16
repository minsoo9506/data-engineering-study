# Starting with Cleaning Data
## Introduction to Cleaning Data
```sql
SELECT 
	-- Concat the strings
	CONCAT(
		carrier_code, 
		' - ', 
      	-- Replicate zeros
		REPLICATE('0', 9 - LEN(registration_code)), 
		registration_code, 
		', ', 
		airport_code)
	AS registration_code
FROM flight_statistics
-- Filter registers with more than 100 delays
WHERE delayed > 100
```
## Cleaning messy strings
- `TRIM` : 빈칸 없애기
- `REPLACE` : 특정 단어 원하는 단어로 바꾸기
- `UPPER`

```sql
SELECT airport_code, airport_name, 
	-- Use the CASE statement
	CASE
    	-- Unify the values
		WHEN airport_city <> 'Chicago' THEN REPLACE(airport_city, 'ch', 'Chicago')
		ELSE airport_city 
	END AS airport_city,
    airport_state
FROM airports
WHERE airport_code IN ('ORD', 'MDW')
```

## Comparing the similarity between strings
- `SOUNDEX` : return four-character code
  - 특정 rule-based 알고리즘으로 변환 -> similarity를 파악할 수 있음
  - 실제로 얼마나 쓰일지는 모르겠음

```sql
SELECT 
    -- First name and surname of the statisticians
	DISTINCT S1.statistician_name, S1.statistician_surname
-- Join flight_statistics with itself
FROM flight_statistics S1 INNER JOIN flight_statistics S2 
	-- The SOUNDEX result of the first name and surname have to be the same
	ON SOUNDEX(S1.statistician_name) = SOUNDEX(S2.statistician_name) 
	AND SOUNDEX(S1.statistician_surname) = SOUNDEX(S2.statistician_surname) 
-- The texts of the first name or the texts of the surname have to be different
WHERE S1.statistician_name <> S2.statistician_name
	OR S1.statistician_surname <> S2.statistician_surname
```

# Dealing with missing data, duplicate data, and different data formats
## Dealing with missing data
- `ISNULL(chech_expr, replacement)`
- `COALESCE(arg1, arg2, arg3 ...)`

```sql
SELECT
  airport_code,
  airport_name,
  -- Replace missing values for airport_city with 'Unknown'
  ISNULL(airport_city, 'Unknown') AS airport_city,
  -- Replace missing values for airport_state with 'Unknown'
  ISNULL(airport_state, 'Unknown') AS airport_state
FROM airports

SELECT
airport_code,
airport_name,
-- Replace the missing values
COALESCE(airport_city, airport_state, 'Unknown') AS location
FROM airports
```

## Avoiding duplicate data
- `ROW_NUMBER()`
  - 아래 예시 코드처럼 query를 날리면 중복 row의 경우는 2이상의 값을 가지게 되서 중복여부를 판단할 수 있다.

```sql
WITH cte AS (
    SELECT *, 
        ROW_NUMBER() OVER (
            PARTITION BY 
                airport_code, 
                carrier_code, 
                registration_date
			ORDER BY 
                airport_code, 
                carrier_code, 
                registration_date
        ) row_num
    FROM flight_statistics
)
SELECT * FROM cte
-- Exclude duplicates
WHERE row_num = 1;
```

## Dealing with different data formats
- `CONVERT(data_type[(length)], expr [, style])`
  - `style`은 이미 정해져 있음 필요할 때 찾아서 이용
- `FORMAT(value, format [, culture])`
  - `CONVERT` 보다 flexible
  - 근데 좀 더 느려서 high volume data에는 사용 비추

```sql
SELECT 
    airport_code,
    carrier_code,
    canceled,
    -- Convert the registration_date to a DATE and print it in mm/dd/yyyy format
    CONVERT(VARCHAR(10), CAST(registration_date AS DATE), 101) AS registration_date
FROM flight_statistics 
-- Convert the registration_date to mm/dd/yyyy format
WHERE CONVERT(VARCHAR(10), CAST(registration_date AS DATE), 101) 
	-- Filter the first six months of 2014 in mm/dd/yyyy format 
	BETWEEN '01/01/2014' AND '06/30/2014'
```
```sql
SELECT 
	pilot_code,
	pilot_name,
	pilot_surname,
	carrier_code,
    -- Convert the entry_date to a DATE and print it in dd/MM/yyyy format
	FORMAT(CAST(entry_date AS DATE), 'dd/MM/yyyy') AS entry_date
from pilots
```

# Dealing with out of range values, different data types, and pattern matching

## Out of range values and inaccurate data
- 원래 예상되는 값의 범위를 벗어나는 경우 존재

```sql
SELECT * FROM series
-- Detect the out of range values
WHERE num_ratings NOT BETWEEN 0 AND 5000

SELECT * FROM series
-- Detect the out of range values
WHERE num_ratings < 0 OR num_ratings > 5000
```

- 서로 상반되는 데이터 존재
  - 예를 들어 회원가입날짜보다 회원탈퇴날짜가 더 빠른 경우

```sql
SELECT * FROM series
-- Filter series for adults
WHERE is_adult = 1
-- Exclude series with the minimum age greater or equals to 18
AND min_age > 18
```

## Converting data with different types
- `CAST`, `CONVERT`

```sql
-- Use CAST() to convert the num_ratings column
SELECT AVG(CAST(num_ratings AS INT))
FROM series
-- Use CAST() to convert the num_ratings column
WHERE CAST(num_ratings AS INT) BETWEEN 0 AND 5000

-- Use CONVERT() to convert the num_ratings column
SELECT AVG(CONVERT(INT, num_ratings))
FROM series
-- Use CONVERT() to convert the num_ratings column
WHERE CONVERT(INT, num_ratings) BETWEEN 0 AND 5000
```

## Pattern matching
- `LIKE` 를 이용하여 원하는 패턴을 찾을 수 있다.

```sql
SELECT 
	name,
    -- URL of the official site
	official_site
FROM series
-- Get the URLs that don't match the pattern
WHERE official_site NOT LIKE
	-- Write the pattern
	'www.%'
```

# Combining, splitting, and transforming data
## Combining data of some columns into one column
- `CONCAT`, `+`
  - `CONCAT`의 경우는 NULL이 있으면 무시하고 합치는데 `+`는 NULL이 결과
  - `DATEFROMPARTS`

```sql
SELECT 
	client_name,
	client_surname,
    -- Consider the NULL values
	ISNULL(city, '') + ISNULL(', ' + state, '') AS city_state
FROM clients

SELECT 
	product_name,
	units,
 	-- Use the function to concatenate the different parts of the date
	DATEFROMPARTS(
      	year_of_sale, 
      	month_of_sale, 
      	day_of_sale) AS complete_date
FROM paper_shop_daily_sales
```

## Splitting data of one column into more columns
- `SUBSTRING(string, start, length)`
  - `CHARINDEX(substring, string [,start])`

```sql
SELECT 
	client_name,
	client_surname,
    -- Extract the name of the city
	SUBSTRING(city_state, 1, CHARINDEX(', ', city_state) - 1) AS city,
    -- Extract the name of the state
    SUBSTRING(city_state, CHARINDEX(', ', city_state) + 1, LEN(city_state)) AS state
FROM clients_split
```

## Transforming rows into columns and vice versa
- `PIVOT`, `UNPIVOT`

```sql
SELECT
	year_of_sale,
    -- Select the pivoted columns
	notebooks, 
	pencils, 
	crayons
FROM
   (SELECT 
		SUBSTRING(product_name_units, 1, charindex('-', product_name_units)-1) product_name, 
		CAST(SUBSTRING(product_name_units, charindex('-', product_name_units)+1, len(product_name_units)) AS INT) units,	
    	year_of_sale
	FROM paper_shop_monthly_sales) sales
-- Sum the units for column that contains the values that will be column headers
PIVOT (SUM(units) FOR product_name IN (notebooks, pencils, crayons))
-- Give the alias name
AS paper_shop_pivot

SELECT * FROM pivot_sales
-- Use the operator to convert columns into rows
UNPIVOT
	-- The resulting column that will contain the turned columns into rows
	(units FOR product_name IN (notebooks, pencils, crayons))
-- Give the alias name
AS unpivot_sales
```