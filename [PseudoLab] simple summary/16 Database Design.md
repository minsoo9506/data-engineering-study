## Processing, Storing, and Organizing Data
### OLTP, OLAP
- OLTP
  - online transaction processing
  - focus on supporting day-to-day operation
- OLAP
  - online analytical processing
  - focus on business decision making

||OLTP|OLAP|
|------|---|---|
|Purpose|support daily transaction|report and analyze data|
|Design|application-oriented|subject-oriented|
|Data|up-to-date, operational|consolidated, historical|
|Size|snapshot, gigabyte|archive, terabyte|
|Queries|simple transaction, frequent update|complex, aggregate queries, limited updates|
|Users|thousands|hundreds|

- OLTP data는 주로 operational database에 저장되고 이 data들을 이용하여 OLAP data warehouse를 구성한다.

### Storing data
- Data lake
  - 최대한 적은 cost로 모든 type의 data를 저장하는 것
  - 요즘 hadoop같은 거로 이용
  - 딥러닝도 이용 (이미지, 텍스트 같이 다양한 data type과 대용량데이터 필요)
- ETL
  - more traditional aproach for warehousing and smaller-scale analytics
  - 여러가지 data source들로부터 Extract하고 transform한 뒤에서 Data warehouse로 Load 한다.
- ELT
  - 여러가지 data source들로부터 Extract하고 Data Lake에서 load과 transform을 하여서 사용한다.

### Database design
- Database design?
  - determines how data is logically stored
  - uses database models : high-level specifications for datbase structure
    - realtional model, NoSQL model, ...
  - uses schemas : blueprint of the database
    - tables, fields, relationships, indexes, views ...
- Data modeling : data가 저장될 data model을 만드는 과정
  - conceptual data model : describes entities, relationship, and attributes
    - tool : data structure diagrams
  - Logical data model : defines tables, columns, relationships
    - tool : database models and schemas
  - Physical data model : describes physical storage
    - tool : partition, cpu ...
- Dimensional modeling
  - adaptation of the relational model specifically for data warehouse
  - OLAP queries에 최적화
  - Built using the star schema
  - 구성 요소는 크게 두 가지
    - Fact table, Dimension table
    - star schema에서 중앙이 Fact

## Database Schemas and Normalization
### Star and Snowflake schema
- Start schema
  - dimension model이랑 같은 의미로 이해가능
- snowflake
  - star schema의 연장선
  - table이 더 많다.
- star는 one dimension이고 snowflake는 그 이상이다.
- normalization?
  - table을 작게 나누고 relationship으로 연결하는 과정
  - reduce redundancy
  - increase data integrity

### Normalized and denormalized database
- normalization을 하면 redundancy를 줄일 수 있다.
- data consistency
- data 수정이 쉽고 table의 확장이 용이하다.
- join을 많이 해야할 수 있으니 단점도 존재한다.
- OLTP가 OLAP보다 normalize를 더 많이한다.

### Normal form
- 1NF rule
  - Each record must be unique
  - Each cell must hold one value
- 2NF rule
  - 1NF를 만족해야하고 primary key가 하나의 column인 경우
  - primary key가 composite한 경우, non-key column은 모든 key에 dependent해야한다.
- 3NF rule
  - 2NF를 만족하고 non-key columns가 다른 non-key columns에 depend하지 않는 것을 의미한다.

## Database Views
- Database view
  - 저장장치에 물리적으로 존재하지 않는다.
  - 임시 테이블이라고 생각할 수 있다.
  - 하지만 기본 테이블과 거의 동일한 작업을 진행할 수 있다.
  - 원래 있던 테이블로 만든다. alias같은 느낌이다.

```sql
-- Get all non-systems views
SELECT * FROM information_schema.views
WHERE table_schema NOT IN ('pg_catalog', 'information_schema');

-- Create a view for reviews with a score above 9
CREATE VIEW high_scores AS
SELECT * FROM REVIEWS
WHERE score > 9;
```
### Managing Views
- 

## Database Management