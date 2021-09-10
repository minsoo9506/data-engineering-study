## Database

### Tables
- table만들기
```sql
CREATE TABLE table_name (
    column_name data_type,
    column_name data_type,
    column_name data_type
);
```
- table 수정
```sql
ALTER TABLE table_name
ADD COLUMN column_name data_type;
```

### Update database
- `INSERT INTO`
```sql
-- 예시
INSERT INTO professors 
SELECT DISTINCT firstname, lastname, university_shortname 
FROM university_professors;
```
- `RENAME`
```sql
ALTER TABLE table_name
RENAME COLUMN old_name TO new_name;
```
- `DROP`
```sql
ALTER TABLE table_name
DROP COLUMN column_name;

-- table 삭제
DROP TABLE table_name;
```

## Enforce data consistency with attribute constraints

### Better data quality with constraints
- 왜 constraints?
  - 제약이 있어서 data quality가 좋다, 효율적, 관리하기 좋다
- `CAST`
```sql
-- fee를 integer로 CAST해야 계산이 가능하다
SELECT transaction_date, amount + CAST(fee AS integer) AS net_amount 
FROM transactions;
```

### Working with data types
- column의 data type을 지정
  - 저장되는 data type, 사용가능 연산자들이 제한됨
- table을 만들때 지정할 수 있다.
- 나중에 바꿀수도 있다.

```sql
-- type 바꾸기
ALTER TABLE table_name
ALTER COLUMN column_name
TYPE varchar(10)

-- type을 바꿀 때 원래 데이터 변환
-- USING + 특정 함수들 사용
ALTER TABLE table_name
ALTER COLUMN column_name
TYPE varchar(x)
USING SUBSTRING(column_name FROM 1 FOR x)
```

### not-null, unique constraints
- not-null constraint
  - 데이터가 null이 못 들어오게 제한

```sql
-- 아래예시처럼 NOT NULL 조건 추가 가능
ALTER TABLE professors 
ALTER COLUMN firstname SET NOT NULL;
```

- unique constraint
  - unique한 값만 들어오게 제한

```sql
-- some_name은 별로 의미는 없는 것 같다
-- 내부적으로 쓰이는 듯
ALTER TABLE table_name
ADD CONSTRAINT some_name UNIQUE(column_name);
```

## Uniquely identify records with key constraints
### Keys and superKeys
- superkey는 record를 unique하게 파악할 수 있는 attribute(column)의 조합들로 이해할 수 있다. 그 중에 가장 작은게 key라고 할 수 있다.
- Key
  - attributes that identify a record uniquely
  - minimal superkey

### Primary Keys
- key들 중에서 선택된 하나의 key!
- unique, not null이 동시에 적용된다.

```sql
-- 처음 만들 때
CREATE TABLE table_name (
  col_name1 integer PRIMARY KEY,
  col_name2 text
);

CREATE TABLE table_name (
  col_name1 integer,
  col_name2 text,
  col_name3 text,
  PRIMARY KEY (col_name1, col_name2)
);

-- 나중에 추가할 때
ALTER TABLE table_name
ADD CONSTRAINT some_name PRIMARY KEY (col_name1)
```

### Surrogate keys
- primary key로 설정하기 적절한 상황이 없을 때 사용할 수 있다.
- serial id를 만들 수도 있고 column들을 조합해서 새로운 column을 만들고 이를 primary key로 만들수도 있다.

```sql
-- serial id를 만들 수도 있고
-- Add the new column to the table
ALTER TABLE professors 
ADD COLUMN id serial;
-- Make id a primary key
ALTER TABLE professors 
ADD CONSTRAINT professors_pkey PRIMARY KEY (id);
```
```sql
-- 새로운 column을 만들고 이를 primary key로 만들수도 있다
-- Count the number of distinct rows with columns make, model
SELECT COUNT(DISTINCT(make, model)) 
FROM cars;

-- Add the id column
ALTER TABLE cars
ADD COLUMN id varchar(128);

-- Update id with make + model
UPDATE cars
SET id = CONCAT(make, model);

-- Make id a primary key
ALTER TABLE cars
ADD CONSTRAINT id_pk PRIMARY KEY(id);

-- Have a look at the table
SELECT * FROM cars;
```


## Glue together tables with foreign keys

### Model 1:N relationship with foreign keys
- foreign key는 다른 table의 primary key를 가르킨다.
- domain이 primary key와 같아야한다.
- foreign key는 실제 key가 아니다. 중복값도 있고 NULL도 가능하다.
- referential integrity를 확인하기 위해 사용된다.
- foreign key로 지정한 경우 해당 column의 값은 primary key로 지정한 column에 없는 값이 들어오지 못한다.

```sql
ALTER TABLE a 
ADD CONSTRAINT a_fkey FOREIGN KEY (b_id) REFERENCES b (id);
```
- table `a`가 `b_id`를 통해`b`를 참조한다.
- `b_id`가 table `a`의 foreign key이다.
- `id`가 table `b`의 primary key이다.
- 이름을 주로 위처럼 짓는다고 한다.

### Referential intergrity
- record referencing another table must refer to an existing record in that table
- 그래서 만약에 refer당하는 table에서 특정 값이 사라지면 violation!
  - 그러면 error 발생 `... ON DELETE NO ACTION`
  - 그에 해당하는 foreign key의 해당 row를 삭제 한다. `... ON DELETE CASCADE`
  - 그에 해당하는 foreign key의 해당값을 NULL로 바꾼다. `... ON DELETE SET NULL`
  - 그에 해당하는 foreign key의 해당값을 default value로 바꾼다. `... ON DELETE SET DEFAULT`

```sql
-- Add a new foreign key constraint from affiliations to organizations which cascades deletion
ALTER TABLE affiliations
ADD CONSTRAINT affiliations_organization_id_fkey FOREIGN KEY (organization_id) REFERENCES organizations (id) ON DELETE CASCADE;
```