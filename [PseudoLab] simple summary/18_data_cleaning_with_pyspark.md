# DataFrame Details
- spark
  - immutability and lazy processing
## Understanding parquet
- parquet
  - columnar data format
  - supports predicate pushdown
  - automatically stores schema information
## working with parquet
- `spark.read.parquet(~)`
- `df.write.parquet(~)`

# Manipulating DataFrames in the real world
## DataFrame column operation
- dataframe transformation
  - `filter`, `where`
  - `select`
  - `withColumn` : 새로운 컬럼 만듬
  - `drop`
- filtering data
  - negate with `~` : `df.where(~ df["colname"].isNull())`
## Conditional DataFrame column operations
- `.when(<if condition>, <then x>)`
- `otherwise`
```python
df.select(df.Name, df.Age,
          .when(df.Age > 18, "Adult")
          .when(df.Age = 18, "Minor")
          .otherwise("Else"))
```

## User defined functions
1. Python method
2. Wrapped via the `pyspark.sql.functions.udf` method
3. Stored as a variable
4. Called like a normal Spark function

```python
def reverseString(mystr):
  return mystr[::-1]

# wrap the function and store as a variable
udfReverseString = udf(reverseString, StringType())

user_df = user_df.withColumn('ReverseName', udfReverseString(user_df.Name))
```

## Partitioning and lazy processing
- data들이 나누어서 저장되어 있다.
  - `df.rdd.getNumPartitions()` : partition 갯수를 알 수 있다.
- 그리고 예를 들어, row id를 의미하는 컬럼을 만들고 싶을 때 수동으로 하면 너무 느리다. data가 partition되어있으므로!
  - `df = df.withColumn('ROW_ID', F.monotonically_increasing_id())`
- 이전까지 봤던 transformation은 action전까지는 일어나지 않는다.
- action이 일어나면 최적화된 transformation이 행해진다.

# Improving Performance

## Caching
- 장점
  - DataFrame을 memory or disk 에 저장
  - transformation, action 속도 향상
  - Resource 사용 줄임
- 단점
  - 너무 큰 데이터는 cache 노노
  - local disk 기반의 caching은 성능이 별로 일 수 있다
- `.cache()` : cache되게 하기
  - ex) `df.cache().show()`
- `.is_cached` : cache되었는지 확인
  - ex) `df.is_cached`
- `.unpersist()` : 삭제
  - ex) `departures_df.unpersist()`

## Improve Import performance
- *Spark Clusters* are made of two types of processes
  - Driver process
  - Worker process
- file을 작고 여러개로 나누는게 더 빠르다.
- Schemas
  - well-defined schema를 import 성능을 높인다.
  - parquet 사용하자.

## Cluster configurations
- configuration
```python
# Name of the Spark application instance
app_name = spark.conf.get('spark.app.name')

# Driver TCP port
driver_tcp_port = spark.conf.get('spark.driver.port')

# Number of join partitions
num_partitions = spark.conf.get('spark.sql.shuffle.partitions')

# Show the results
print("Name: %s" % app_name)
print("Driver TCP port: %s" % driver_tcp_port)
print("Number of partitions: %s" % num_partitions)
```
- Cluster Types
  - Single node
  - Standalone
  - Managed
    - YARN
    - Mesos
    - Kubernetes
- Driver
  - Task assignment
  - Result consolidation
  - Shared data access
  - Tips
    - Driver node should have double the memory of the worker
    - Fast local storage helpful
- Woker
  - Runs actual tasks
  - Recommendations
    - More worker nodes are often better than larger workers
    - Test to find the balance
    - Fast local storage helpful

## Performance improvements
- shuffling : moving data around to various workers to complete a task
- how to limit shuffling?
  - Limit use of `.repartition(num_partitions)`
    - Use `.coalesce(num_partitions)` instead
  - Use care when calling `.join()`
  - Use `.broadcast()`
  - May not need to limit it
- Show the query plan : `df.explain()`
- Broadcasting
  - provides a copy of an object to each worker
  - prevents undue / excess communication between nodes
  - can drastically speed up `.join()` operations
  - join할 때, 그냥 하는 것과 비교해보니 더 빠름

```python
from pyspark.sql.functions import broadcast
combined_df = df1.join(broadcast(df2))
```

# Complex processing and data pipelines
## Introduction to data pipelines
- data pipeline
  - input -> transformation -> output -> validation -> analysis
  - formally 정해진 것은 없다.

## Data handling techniques
- spark's csv parser
  - 알아서 blank line은 없애준다
  - 아래처럼 comment를 없애는 것도 가능
    - `spark.read.csv('sample.csv', comment='#')`

## Data validation
- verifying that a dataset compiles with the expected format
  - number of row , col
  - data types
  - complex validation rules

## Final analysis and delivery
- calculations using UDF
  - `df.withColumn('avg', (df.total_sales / df.sales_count))`
  - `df.withColumn('avg', df.width * df.length)`