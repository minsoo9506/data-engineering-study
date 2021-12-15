# Pyspark SQL
## Creating and quering a SQL table in Spark
```python
df.createOrReplaceTempView('df_view')
result = spark.sql('SELECT * from df_view')
```
## Window function SQL
- row끼리 계산
- 예를 들어 `time`이라는 컬럼에 시간이 있고 각 다음 시간과의 차이를 구하고 싶을 떄

```python
query = """
SELECT train_id, station, time,
LEAD(time, 1) OVER (ORDER BY time) AS time_next
FROM sched
WHERE train_id=324
"""
```

## Dot notation and SQL
- 특정 컬럼을 불러오는 방법 3가지 있다
```python
df.select('train_id', 'station')
df.select(df.train_id, df.station)
df.select(col('train_id'), col('station'))
```
- window function
```python
from pyspark.sql import Window
from pyspark.sql.functions import row_number

df.withColumns('id', row_number()
    .over(
        Window.partitionBy('train_id')
              .orderBy('time')
    )
)

window = Window.partitionBy('train_id').orderBy('time')
dfx = df.withColumn('next', lead('time', 1).over(window))
```

# Using window function sql for natural language processing
## Loading natural language text
- Replacing text
  - `df.select(regexp_replace('value', 'don\'t', 'do not').alias('v'))`
- Repartitioning on a column
  - `df.repartition(4, 'part')`
- Reading pre-partitioned text
  - 예를 들어, `text`폴더에 `text_1, text_2, ...` 이런식으로 나누어져 있다면
  - `spark.read.text('text)` 이렇게 하면 된다.

## Moving window analysis
- `LAG, LEAD`

## Common word sequences
```python
# Find the top 10 sequences of five words
query = """
SELECT w1, w2, w3, w4, w5, COUNT(*) AS count FROM (
   SELECT word AS w1,
   LEAD(word,1) OVER(PARTITION BY part ORDER BY id ) AS w2,
   LEAD(word,2) OVER(PARTITION BY part ORDER BY id ) AS w3,
   LEAD(word,3) OVER(PARTITION BY part ORDER BY id ) AS w4,
   LEAD(word,4) OVER(PARTITION BY part ORDER BY id ) AS w5
   FROM text
)
GROUP BY w1, w2, w3, w4, w5
ORDER BY count DESC
LIMIT 10
""" 
df = spark.sql(query)
df.show()
```

# Caching, Logging, and the Spark UI
## Caching
- caching : keeping data in memory
- spark는 사용하지 않는 데이터틑 memory에서 내리려고 한다.
- `df.cache()` = `df.persist()`, `df.unpersist()`, `df.is_cached`
- table도 caching 할 수 있다.
  - `spark.catalog.isCached(tableName='df_view')`

## The Spark UI
- Spark Task : a unit of execution that runs on a single cpu
- Spark Stage : a group of tasks
- Spark Job : computation triggered by an action

## Logging
## Query plans
- `Explain`을 query 앞에 붙이면 plan을 볼 수 있다. query가 실행되는 것은 아니다.

```python
spark.sql('EXPLAIN SELECT * FROM df').first()

spark.sql('SELECT * FROM df').explain()
```

# Text classification
## Extract Transform Select
## Creating feature data for classification
## Text Classification
## Predicting and evaluating
## Recap