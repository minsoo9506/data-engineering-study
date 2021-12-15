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

# Combining, splitting, and transforming data